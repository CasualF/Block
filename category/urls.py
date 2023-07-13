from django.urls import path, include
from .views import CategoryCreateListView, CategoryDetailView


urlpatterns = [
    path('', CategoryCreateListView.as_view()),
    path('<int:pk>', CategoryDetailView.as_view())
]
