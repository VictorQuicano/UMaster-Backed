from django.db import models


class AnswerStatus(models.IntegerChoices):
    UNUSED = 1, "Unused"
    INCORRECT = 2, "Incorrect"
    MARKED = 3, "Marked"
    OMITTED = 4, "Omitted"
    CORRECT = 5, "Correct"
