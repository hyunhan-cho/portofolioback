from django.urls import path
from .views import RegisterView, LoginView, UserInfoView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserInfoView.as_view(), name='user-info'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]

