from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.ImageUploadView.as_view(), name='image-upload'),
     path('delete/', views.ImageDeleteView.as_view(), name='image-delete'),
]
