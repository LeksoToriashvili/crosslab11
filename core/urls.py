from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet, LikeViewSet, QuestionListingViewSet, QuestionByUsernameViewSet

router = DefaultRouter()
router.register('questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answers')
router.register(r'likes', LikeViewSet, basename='likes')
router.register(r'all-questions', QuestionListingViewSet, basename='all-questions')
router.register(r'questions-by-user', QuestionByUsernameViewSet, basename='questions-by-user')


urlpatterns = [
    path('', include(router.urls)),
]