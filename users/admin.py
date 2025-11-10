from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, MemberProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """커스텀 유저 관리자"""
    
    list_display = ('email', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('권한', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('날짜', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'tier', 'is_premium', 'created_at', 'last_active')
    list_filter = ('tier', 'is_premium')
    search_fields = ('user__email', 'nickname', 'full_name')
    readonly_fields = ('created_at', 'last_active')
