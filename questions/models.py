from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from authorization.models import User, Institution
from .enums import AnswerStatus


class Area(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Exam(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    year = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    published = models.BooleanField(default=False)
    source_url = models.CharField(max_length=255, null=True, blank=True)

    # Polymorphic relationship with Institution or User
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    owner = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.name} - {self.year} - {self.area.name if self.area else 'No Area'}"
        )


class Question(models.Model):
    order = models.IntegerField(blank=True, null=True)
    body = models.TextField()
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)
    tags = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.body} - {self.exam.name if self.exam else 'No Exam'}"


class Answer(models.Model):
    order = models.IntegerField(blank=True, null=True)
    body = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.body} - {'Correct' if self.is_correct else 'Incorrect'}"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    status = models.SmallIntegerField(
        choices=AnswerStatus.choices, default=AnswerStatus.UNUSED
    )
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.body} - {self.answer.body}"

class ExamDraft(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)
    draft_data = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Draft for {self.exam.name} by {self.user.username if self.user else 'Anonymous'}"