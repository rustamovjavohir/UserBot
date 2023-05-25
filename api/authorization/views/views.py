from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from api.authorization.serializers.serializers import CustomObtainPairSerializer, CustomTokenRefreshSerializer, \
    LogoutSerializer, UserProfilesSerializer, VerifyTokenSerializer


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('checking')
        else:
            return render(request, 'authorization/login.html')

    if request.method == 'GET' and request.user.is_authenticated:
        return redirect('checking')

    return render(request, 'authorization/login.html')


class LoginView(TokenObtainPairView):
    serializer_class = CustomObtainPairSerializer

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        if isinstance(exc, InvalidToken):
            response.data['success'] = False
            response.data['message'] = response.data['detail']
            response.data['result'] = None
            response.data.pop('detail')
            response.status_code = status.HTTP_200_OK
            return response

        response.data['success'] = False
        response.data['message'] = str(exc)
        response.data['result'] = None
        response.data["status_code"] = response.status_code
        response.status_code = status.HTTP_200_OK
        response.data.pop('detail')
        return response


class GetRefreshTokenView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        return super(GetRefreshTokenView, self).post(request, *args, **kwargs)


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                'success': True,
                "message": "You are logged out"
            }
            return Response(data=data, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            data = {"error": str(e)}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class CustomUserProfile(GenericAPIView):
    serializer_class = UserProfilesSerializer
    permission_classes = [IsAuthenticated, ]
    # authentication_classes = [JWTAuthentication, ]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)


class VerifyTokenView(TokenVerifyView):
    serializer_class = VerifyTokenSerializer

    def handle_exception(self, exc):
        response = super().handle_exception(exc)

        if isinstance(exc, InvalidToken):
            response.data['success'] = False
            response.data['message'] = response.data['detail']
            response.data['result'] = None
            response.data.pop('detail')
            response.status_code = status.HTTP_200_OK
        return response
