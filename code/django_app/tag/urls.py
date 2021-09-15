from django.urls import include, path
from rest_framework import routers
from .views import TagListViewSet

router = routers.DefaultRouter()
router.register(r'tags', TagListViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
