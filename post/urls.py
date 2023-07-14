from django.urls import path, include
# from .views import PostListCreateView, PostDetailView
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register('', PostViewSet)


urlpatterns = [
    # path('', PostListCreateView.as_view()),
    # path('<int:pk>/', PostDetailView.as_view())
    path('', include(router.urls))
]
