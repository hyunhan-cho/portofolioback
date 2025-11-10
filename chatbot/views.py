from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ChatbotSerializer
from .models import ChatMessage
from django.conf import settings


class ChatbotView(APIView):
    """챗봇 API - 로그인한 사용자만 접근 가능"""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """챗봇 메시지 전송"""
        serializer = ChatbotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_message = serializer.validated_data['message']

        # OpenAI API 통합 (환경변수 설정 시)
        api_key = getattr(settings, 'OPENAI_API_KEY', None)
        if api_key:
            # SDK 미설치 시 사용자에게 안내
            try:
                from openai import OpenAI
            except Exception:
                return Response({
                    "error": "AI 기능이 비활성화되어 있습니다. 서버에 openai 패키지를 설치해야 합니다.",
                    "instruction": "pip install openai"
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            try:
                client = OpenAI(api_key=api_key)

                # 최근 대화 이력을 함께 전달하여 문맥 유지
                history_qs = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:10]
                messages = [
                    {
                        "role": "system",
                        "content": (
                            "너는 조현한님의 포트폴리오 웹사이트에 내장된 한국어 비서야. "
                            "정확하고 간결하게 답하고, 공격적 표현은 중립적으로 재해석해. "
                            "사이트/기능/사용법/계정/보안/기술스택 질문에 친절히 답변해."
                        )
                    }
                ]
                for m in reversed(list(history_qs)):
                    messages.append({"role": "user", "content": m.user_message})
                    if m.bot_response:
                        messages.append({"role": "assistant", "content": m.bot_response})
                messages.append({"role": "user", "content": user_message})

                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.3,
                )
                bot_response = (completion.choices[0].message.content or "").strip()
                if not bot_response:
                    bot_response = "죄송해요, 방금 응답을 생성하지 못했어요. 다시 한 번 시도해 주세요."
            except Exception as e:
                return Response({
                    "error": "AI 응답 생성 중 오류가 발생했습니다.",
                    "detail": str(e)
                }, status=status.HTTP_502_BAD_GATEWAY)
        else:
            # API 키 미설정: 기존의 간단한 에코 응답 유지
            bot_response = f"안녕하세요 {request.user.email}님! 당신의 메시지: '{user_message}'를 받았습니다."

        # 메시지 저장
        chat_obj = ChatMessage.objects.create(
            user=request.user,
            user_message=user_message,
            bot_response=bot_response,
        )
        
        return Response({
            'id': chat_obj.id,
            'user_message': user_message,
            'bot_response': bot_response,
            'user': request.user.email,
            'created_at': chat_obj.created_at,
        }, status=status.HTTP_200_OK)
