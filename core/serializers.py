from django.db.models import Count
from rest_framework import serializers
from core.models import Question, Answer, Tag, Like


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class QuestionAnswerSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = '__all__'

    def get_likes_count(self, obj):
        """
        Returns the count of likes for the given answer.
        """
        return Like.objects.filter(answer=obj).count()

    def get_author_username(self, obj):
        return obj.author.username

    def get_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(answer=obj, user=request.user).exists()
        return False


class QuestionsSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    number_of_answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = '__all__'

    def get_number_of_answers(self, obj):
        return obj.answers.count()


class QuestionWithAnswerSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    answers = QuestionAnswerSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'description']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'author', 'question', 'accepted', 'created_at']
        read_only_fields = ['created_at', 'author']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'answer']
        read_only_fields = ['user']
