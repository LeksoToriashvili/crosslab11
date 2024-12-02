from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Question, Answer, Tag, Like
from core.serializers import TagSerializer, QuestionSerializer, AnswerSerializer, LikeSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().prefetch_related('tags')
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def tags(self, request):
        tag_name=request.query_params.get('tag_name')
        if not tag_name:
            return Response({"error": "Tag parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        questions = Question.objects.filter(tags__name__contains=tag_name)
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)