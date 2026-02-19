from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer

User = get_user_model()


class RegisterView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    # GET for browser testing
    def get(self, request):
        return Response({
            "message": "Send a POST request with username, email and password to register."
        })

    # POST to register user
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response({
            "user": serializer.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    # GET for browser testing
    def get(self, request):
        return Response({
            "message": "Send a POST request with username and password to login."
        })

    # POST to login
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key
        })


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
