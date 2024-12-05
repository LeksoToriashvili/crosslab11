from django.db.models import Count
from rest_framework import serializers
from core.models import Question, Answer, Tag, Like


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


###############################  answerserializer with likes count #############################
# class AnswerSerializer(serializers.ModelSerializer):
#     likes_count = serializers.IntegerField(read_only=True)
#
#     class Meta:
#         model = Answer
#         fields = '__all__'
#
#     def to_representation(self, instance):
#         # Use annotate to add the like count to the queryset
#         instance = Answer.objects.annotate(likes_count=Count('likes')).get(id=instance.id)
#         representation = super().to_representation(instance)
#         return representation


class QuestionAnswerSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = '__all__'

    def get_likes_count(self, obj):
        """
        Returns the count of likes for the given answer.
        """
        return Like.objects.filter(answer=obj).count()
#################################     ---end---        ##############################################


class QuestionsSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class QuestionWithAnswerSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    answers = QuestionAnswerSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

    def get_answers(self, obj):
        return Answer.objects.all()
        #Answer.objects.filter(question=obj).order_by('created_at')


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
