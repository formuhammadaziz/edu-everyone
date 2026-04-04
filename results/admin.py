from django.contrib import admin
from .models import ExamResult


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'overall_band', 'listening_score', 'reading_score',
                    'writing_score', 'speaking_score', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
