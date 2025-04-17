from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser, Group, Permission

from .enums import InstitutionType


class Plan(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in days", default=30)
    max_users = models.IntegerField(default=1)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Plans"
        ordering = ["created_at"]


class Subscription(models.Model):
    start_plan_date = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    ## POLYMORPHIC RELATIONSHIP WITH INSTITUTION OR USER
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"Subscription for {self.content_object} - ID: {self.object_id}"

    class Meta:
        verbose_name_plural = "Subscriptions"
        ordering = ["-start_plan_date"]


class Institution(models.Model):

    name = models.CharField(max_length=255)
    institution_type = models.SmallIntegerField(
        choices=InstitutionType.choices, default=InstitutionType.OTHER
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Institutions"
        ordering = ["created_at"]


class User(AbstractUser):
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, blank=True, null=True
    )
    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_permissions_set", blank=True
    )
