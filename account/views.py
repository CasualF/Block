from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, UserDetailSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import generics, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action


class UserRegistration(APIView):
    def get(self, request):
        permission_classes = [IsAuthenticated]
        queryset = User.objects.all()
        serializer = RegisterSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('User created', status=201)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdminUser]


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        response_data = {
            'token' : token.key,
            'username': user.username,
            'id': user.id
        }
        return Response(response_data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('You logged out')


class CustomViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    GenericViewSet):
    pass


class UserViewSet(CustomViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return RegisterSerializer

    def get_permissions(self):
        if self.request.method == 'retrieve':
            return [IsAdminUser()]
        return [IsAuthenticated()]

