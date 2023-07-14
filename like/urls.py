from django.urls import path
from .views import LikeCreateView, LikeDeleteView


urlpatterns = [
    path('create/', LikeCreateView.as_view()),
    path('delete/', LikeDeleteView.as_view()),
]