from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Question, Answer, Tag, Like
from core.serializers import TagSerializer, QuestionSerializer, AnswerSerializer, LikeSerializer

#question managing view
class QuestionViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for questions.
    Includes additional actions for filtering by tags, or adding tags to questions
    """
    queryset = Question.objects.all().prefetch_related('tags')
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)
    def perform_create(self, serializer):
        """
        associates the question with a logged_in user
        """
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['GET'])
    def tags(self, request):
        """
        Filter questions by tags and expects a "tag_name" query parameter in the request
        """
        tag_name=request.query_params.get('tag_name')
        if not tag_name:
            return Response({"error": "Tag parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        #Filter questions by the given tag_name
        questions = Question.objects.filter(tags__name__icontains=tag_name)
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def add_tag(self, request, pk=None):
        """
        Add a new tag
        to the specific question using serializer logic
        """
        question = self.get_object()
        tag_name = request.data.get('tag_name')
        if not tag_name:
            return Response({"error": "Tag parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        #Retrieve or create the tag, ignores the second boolean value of get_or_create method.
        tag, created = Tag.objects.get_or_create(name=tag_name)
        question.tags.add(tag)

        serializer = self.get_serializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

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


    @action(detail=True, methods=['delete'], permission_classes = [IsAuthenticated])
    def remove_like(self, request, pk=None):
        like = self.Like.objects.get(user=self.request.user, answer_id=pk)
        if like.author == self.request.user:
            like.delete()
            return Response({"success":"Like removed"}, status=status.HTTP_200_OK)
