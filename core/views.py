from http.client import HTTPResponse

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.models import Question, Tag, Answer, Like
from core.serializers import QuestionSerializer, QuestionsSerializer, QuestionWithAnswerSerializer, AnswerSerializer, \
    LikeSerializer
from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.author == request.user


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.prefetch_related('author').all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            list_type = self.request.query_params.get('list', None)
            if list_type == 'answers':
                return QuestionWithAnswerSerializer
            else:
                return QuestionsSerializer
        else:
            return QuestionSerializer

    def perform_create(self, serializer):
        # serializer.save(author=self.request.user)

        tag_names = self.request.data.get('tags', [])
        # Ensure tag_names is a list
        if not isinstance(tag_names, list):
            raise ValueError("Tags must be provided as a list of strings.")

        # Create or get existing tags
        tags = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            tags.append(tag)

        # Save the question with the author
        question = serializer.save(author=self.request.user)

        # Associate tags with the question
        question.tags.set(tags)

        # After saving, return the full serialized data for the question
        question_serializer = QuestionsSerializer(question)
        print(question_serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(question_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        list_type = self.request.query_params.get('list', None)
        print(self.request.user)

        if list_type == 'private':
            queryset = queryset.filter(author=self.request.user)
        elif list_type == 'public':
            queryset = queryset.exclude(author=self.request.user)

        return queryset


class AnswerViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for answers.
    fatching all answers and only authenticated users can access
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        #only logged-in user saves this answer as the answers author
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_accepted(self, request, pk=None):
        """
        Custom action to mark an answer as accepted
        Only the questions author is allowed to mark an answer
        """
        answer = self.get_object()
        #following checks if the request user questions author, if not returns a 403 error
        if answer.question.author == self.request.user:
            answer.accepted = True
            answer.save()
            return Response({"success":"Answer marked as accepted"}, status=status.HTTP_200_OK)
        return Response({"error":"you are not the author!"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, url_path='by_question/(?P<question_id>[^/.]+)', methods=['get'], permission_classes=[AllowAny])
    def by_question(self, request, question_id=None):
        # question_id = request.query_params.get('question_id')
        if not question_id:
            return Response({"error":"question_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        answers = Answer.objects.filter(question_id=question_id)
        if not answers.exists():
            return Response({"error":"no answer"}, status=status.HTTP_404_NOT_FOUND)
        serializer=self.get_serializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for likes.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """
        allows to change object creation behavior. it calls automatically when you use POST method
        """
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_like(self, request, pk=None):
        """
        allows to add a like to a question
        """
        answer = Answer.objects.get(pk=pk)
        Like.objects.create(author=self.request.user, answer=answer, like=True)
        return Response({"success":"like added"}, status=status.HTTP_200_OK)
