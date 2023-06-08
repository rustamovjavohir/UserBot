from django.urls import path
from api.authorization.views.views import LoginPage, LoginView, GetRefreshTokenView, LogoutView, CustomUserProfile, \
    VerifyTokenView, ChangePasswordView

monolith_urls = [
    path('', LoginPage, name='login'),
]
urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='token'),
    path('auth/refresh/', GetRefreshTokenView.as_view(), name='refresh_token'),
    path('auth/log-out/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', CustomUserProfile.as_view(), name='user-profile'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('auth/verify/', VerifyTokenView.as_view(), name='verify-token'),
]
