from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import CustomUserViewSet

router = DefaultRouter()
router.register(r'account', CustomUserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
