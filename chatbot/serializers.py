from rest_framework import serializers


class ChatbotSerializer(serializers.Serializer):
    """챗봇 메시지 시리얼라이저"""
    
    message = serializers.CharField(
        required=True,
        max_length=1000,
        help_text="챗봇에게 보낼 메시지"
    )

