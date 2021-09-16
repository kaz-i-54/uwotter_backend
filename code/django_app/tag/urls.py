from django.urls import path
from . import views

app_name = "aptv1_tag"

urlpatterns = [
    path('tags', views.TagListAPIView.as_view())
]
