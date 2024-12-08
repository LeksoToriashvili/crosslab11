from django.contrib import admin
from core.models import Question, Answer, Tag, Like


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ['id', 'title', 'author']
    list_filter = ['author']
    search_fields = ['title']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    model = Answer
    list_display = ['id', 'text', 'question', 'author', 'accepted']
    list_filter = ['question', 'author', 'accepted']
    search_fields = ['question__title', 'author__username']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ['id', 'name']
    list_filter = ['name']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    model = Like
    list_display = ['id', 'user', 'answer']
    list_filter = ['user', 'answer']
