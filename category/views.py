from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer
from rest_framework import permissions
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import  OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView


class CategoryCreateListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return (permissions.IsAdminUser,)
        return (permissions.AllowAny(),)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return (permissions.AllowAny(),)
        return (permissions.IsAdminUser(),)


# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter
#     # callback_url  =
#     client_class = OAuth2Client
#
# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter