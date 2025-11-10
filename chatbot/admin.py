from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
	list_display = ('user', 'short_user_message', 'created_at')
	search_fields = ('user__email', 'user_message', 'bot_response')
	list_filter = ('created_at',)

	def short_user_message(self, obj):
		return (obj.user_message or '')[:50]
	short_user_message.short_description = '메시지'
