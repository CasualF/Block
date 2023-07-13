from django.urls import path, include
from .views import PostListCreateView, PostDetailView

urlpatterns = [
    path('', PostListCreateView.as_view()),
    path('<int:pk>/', PostDetailView.as_view())
]
