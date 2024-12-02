from rest_framework import serializers
from .models import Question, Answer, Tag, Like

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class QuestionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'author', 'tags', 'created_at']
        read_only_fields = ['created_at', 'author']

        def create(self, validated_data):
            tags_data = validated_data.pop('tags')
            question = Question(**validated_data)
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(**tag_data)
            return question

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'author', 'question', 'accepted', 'created_at']
        read_only_fields = ['created_at', 'author', 'accepted']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'answer']
        read_only_fields = ['user']
