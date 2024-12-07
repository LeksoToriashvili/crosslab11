from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import QuestionViewSet, AnswerViewSet, LikeViewSet, UserRatingAPIView, UserAnswerCountView

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answers')
router.register(r'likes', LikeViewSet, basename='likes')

urlpatterns = [
    path(
        '',
        include(
            router.urls)),
    path(
        'rating/',
        UserRatingAPIView.as_view(),
        name='rating'),
    path(
        'answers-count/',
        UserAnswerCountView.as_view(),
        name='answers-count'),
]
