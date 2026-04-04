from django.contrib import admin
from .models import ExamSet, Section, ReadingPassage, Question, ExamAttempt, StudentResponse


class SectionInline(admin.StackedInline):
    model = Section
    extra = 0


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    fields = ('question_number', 'question_type', 'question_text', 'option_a', 'option_b',
              'option_c', 'option_d', 'correct_answer', 'explanation', 'image', 'speaking_part')


class ReadingPassageInline(admin.StackedInline):
    model = ReadingPassage
    extra = 0


@admin.register(ExamSet)
class ExamSetAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)
    inlines = [SectionInline]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('exam_set', 'section_type', 'title', 'duration_minutes', 'order')
    list_filter = ('section_type', 'exam_set')
    inlines = [ReadingPassageInline, QuestionInline]


@admin.register(ReadingPassage)
class ReadingPassageAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order')
    list_filter = ('section__exam_set',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_type', 'section', 'question_text_short')
    list_filter = ('question_type', 'section__section_type', 'section__exam_set')
    search_fields = ('question_text',)

    def question_text_short(self, obj):
        return obj.question_text[:80]
    question_text_short.short_description = 'Question'


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam_set', 'status', 'started_at', 'completed_at')
    list_filter = ('status', 'exam_set')
    search_fields = ('user__username',)
    readonly_fields = ('started_at',)


@admin.register(StudentResponse)
class StudentResponseAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'is_correct', 'score', 'answered_at')
    list_filter = ('is_correct', 'question__section__section_type')
