from django.db import models
from accounts.models import CustomUser


class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Tag(models.Model):
    name = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question, related_name='tags')

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = (('user', 'answer'),)
