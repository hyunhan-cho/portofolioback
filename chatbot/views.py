from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ChatbotSerializer
from .models import ChatMessage


class ChatbotView(APIView):
    """챗봇 API - 로그인한 사용자만 접근 가능"""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """챗봇 메시지 전송"""
        serializer = ChatbotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_message = serializer.validated_data['message']
        
        # 여기에 실제 챗봇 로직을 구현할 수 있습니다
        # 현재는 간단한 응답을 반환합니다
        # TODO: 추후 OpenAI API 연결 시 여기서 실제 응답 생성
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
