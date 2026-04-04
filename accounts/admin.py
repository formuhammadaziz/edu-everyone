from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'target_band_score', 'exam_date')
    list_filter = ('role', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('IELTS Info', {'fields': ('role', 'target_band_score', 'exam_date')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('IELTS Info', {'fields': ('role', 'target_band_score', 'exam_date')}),
    )
