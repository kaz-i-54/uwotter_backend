from django.urls import path
from . import views

app_name = "aptv1_tag"

urlpatterns = [
    path('tags/', views.TagListAPIView.as_view()),
=======
    path('tags', views.TagListAPIView.as_view()),
>>>>>>> c598ee35d91a30f687eefcb485c23ac84568ec28
]
