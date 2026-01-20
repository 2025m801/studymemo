from django.conf import settings
from django.db import models


class Subject(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subjects"
    )
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ("user", "name")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Memo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memos"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="memos"
    )

    title = models.CharField(max_length=120)
    content = models.TextField()

    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text="例: #試験 #要復習（スペース区切り）"
    )
    importance = models.PositiveSmallIntegerField(default=3)
    understanding = models.PositiveSmallIntegerField(default=3)
    next_action = models.CharField(max_length=200, blank=True)

    is_favorite = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title
