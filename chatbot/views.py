from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ChatbotSerializer
from .models import ChatMessage
from django.conf import settings
import os


_PROFILE_CACHE = {"content": None, "mtime": None, "path": None}


def _get_profile_md_path():
    base_dir = getattr(settings, "BASE_DIR", None)
    if not base_dir:
        # settings에 BASE_DIR이 없다면 앱 기준 루트 추정
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "hyunhan.md")


def _load_profile_context() -> str:
    """루트 경로의 hyunhan.md를 읽어 캐시 후 반환. 실패 시 빈 문자열."""
    try:
        path = _get_profile_md_path()
        mtime = os.path.getmtime(path)
        if (
            _PROFILE_CACHE.get("content") is None
            or _PROFILE_CACHE.get("mtime") != mtime
            or _PROFILE_CACHE.get("path") != path
        ):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # 과도한 토큰 사용 방지를 위해 길이 제한
            max_chars = 15000
            if len(content) > max_chars:
                content = content[:max_chars] + "\n\n[...생략됨: 파일이 매우 깁니다 ...]"
            _PROFILE_CACHE["content"] = content
            _PROFILE_CACHE["mtime"] = mtime
            _PROFILE_CACHE["path"] = path
        return str(_PROFILE_CACHE.get("content") or "")
    except Exception:
        return ""


class ChatbotView(APIView):
    """챗봇 API - 로그인한 사용자만 접근 가능"""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """챗봇 메시지 전송"""
        serializer = ChatbotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_message = serializer.validated_data['message']
        profile_context = _load_profile_context()

        # OpenAI API 통합 (환경변수 설정 시)
        api_key = getattr(settings, 'OPENAI_API_KEY', None)
        if api_key:
            # SDK 미설치 시 사용자에게 안내
            try:
                from openai import OpenAI  # type: ignore[reportMissingImports]
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
                    },
                ]
                if profile_context:
                    messages.append({
                        "role": "system",
                        "content": (
                            "다음은 조현한님의 공개 프로필/기술/수상/수료증 등 참고 자료(markdown/HTML)야. "
                            "질문과 직접 관련 있을 때만 인용하고, 사실만 사용해. "
                            "개인정보나 민감정보는 유출하지 말고 링크·이미지 URL은 설명으로만 다뤄.\n\n"
                            f"{profile_context}"
                        )
                    })
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
