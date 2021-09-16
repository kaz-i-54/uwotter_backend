from django.urls import path
from . import views

app_name = "apiv1_like"

urlpatterns = [
    path("increment/", views.Like_historyListAPIView.as_view())
]
