from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import QuestionViewSet, AnswerViewSet, LikeViewSet, UserRatingAPIView, UserAnswerCountView, \
    accept_answer, reject_answer, TagViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answers')
router.register(r'likes', LikeViewSet, basename='likes')
router.register(r'tags', TagViewSet, basename='tags')

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
    path('acceptorreject/<int:answer_id>/accept/', accept_answer, name='accept_answer'),
    path('acceptorreject/<int:answer_id>/reject/', reject_answer, name='deselect_answer'),
]
