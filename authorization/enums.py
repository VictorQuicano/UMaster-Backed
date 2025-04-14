from django.db import models

class InstitutionType(models.IntegerChoices):
    UNIVERSITY = 1, 'University'
    ACADEMY = 2, 'Academy'
    SCHOOL = 3, 'School'
    OTHER = 4, 'Other'