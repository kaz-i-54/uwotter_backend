from django.urls import path
from . import views

app_name = "apiv1_voice"

urlpatterns = [
    path("get_voices", views.VoiceListAPIView.as_view()),
    path("put_voice", views.VoiceCreateAPIView.as_view()),
]
