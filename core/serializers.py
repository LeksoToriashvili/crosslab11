from rest_framework import serializers
from .models import Question, Answer, Tag, Like

#Serializer for tag model
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

#Serializer for Question model
#allows many-to-many Tag relation and makes it optional
class QuestionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False) #make tags optional

    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'author', 'tags', 'created_at']
        read_only_fields = ['created_at', 'author'] #makes these fields non-editable by API users

        def create(self, validated_data):
            """
            Handling of creation of a question
            extracts tags data if provided in the request, or default to an empty list.
            """
            tags_data = validated_data.pop('tags', [])
            question = Question.objects.create(**validated_data)
            #process each tag in the 'tags' data
            for tag_data in tags_data:
                # Get or create Tag object for each tag in the request
                tag, _ = Tag.objects.get_or_create(**tag_data)
                # associate the tag with the question
                question.tags.add(tag)
            return question

#Serializer for Answer model
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'author', 'question', 'accepted', 'created_at']
        read_only_fields = ['created_at', 'author', 'accepted']

#Serializer for Like model
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'answer']
        read_only_fields = ['user']
