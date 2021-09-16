from django.urls import path
from . import views

app_name = "aptv1_user"

urlpatterns = [
    path('register/', views.UserAuthenticationView.as_view()),
]
