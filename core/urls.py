from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet, LikeViewSet

router = DefaultRouter()
router.register('questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answers')
router.register(r'likes', LikeViewSet, basename='likes')


urlpatterns = [
    path('', include(router.urls)),
]