from django.contrib import admin

from .apps import QuestionsConfig
from .models import Question
from .models import Answer, Exam, Area, Subject, ExamDraft

# Register your models here.
admin.site.register(Area)
admin.site.register(Subject)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(ExamDraft)
