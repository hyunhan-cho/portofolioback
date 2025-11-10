from django.db import models
from django.conf import settings


class ChatMessage(models.Model):
	"""사용자-챗봇 간 메시지 저장"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_messages')
	user_message = models.TextField()
	bot_response = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']
		verbose_name = '챗봇 메시지'
		verbose_name_plural = '챗봇 메시지들'

	def __str__(self):
		return f"{self.user.email}: {self.user_message[:30]}"
