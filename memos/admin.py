from django.contrib import admin
from .models import Subject, Memo

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")

@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "subject", "importance", "is_favorite", "updated_at")
    list_filter = ("importance", "is_favorite")
    search_fields = ("title", "content", "tags")
