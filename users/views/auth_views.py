from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
from django.contrib.auth import get_user_model
from users.serializers import (
    RegisterSerializer, 
    ChangePasswordSerializer, 
    LoginSerializer,
    UserSerializer
)

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from drf_spectacular.utils import extend_schema


User = get_user_model()
@extend_schema(tags=['Auth Management']) 
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            # Sirf actual auth failure yahan aana chahiye
            return Response(
                {'status': 401, 'message': 'Invalid credentials.', 'results': None},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {'status': 500, 'message': f'Server error: {str(e)}', 'results': None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Desired Response Format
        return Response({
            "status": 200,
            "message": "Login successful.",
            "results": serializer.validated_data
        }, status=status.HTTP_200_OK)
@extend_schema(tags=['Auth Management']) 
class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint (public)
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

@extend_schema(tags=['Auth Management']) 
class UserProfileView(generics.RetrieveAPIView):
    """
    Get current user's profile
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

@extend_schema(tags=['Auth Management']) 
class ChangePasswordView(APIView):
    """
    Change current user's password
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Password changed successfully."}, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@extend_schema(tags=['Auth Management']) 
class LogoutView(APIView):
    """
    Logout a specific session by blacklisting the refresh token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Auth Management']) 
class LogoutAllView(APIView):
    """
    Logout from all sessions by blacklisting all outstanding tokens for the user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        return Response({"message": "Logged out from all sessions successfully."}, status=status.HTTP_200_OK)