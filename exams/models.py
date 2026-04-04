from django.db import models
from django.conf import settings


class ExamSet(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Section(models.Model):
    SECTION_TYPES = [
        ('listening', 'Listening'),
        ('reading', 'Reading'),
        ('writing', 'Writing'),
        ('speaking', 'Speaking'),
    ]
    exam_set = models.ForeignKey(ExamSet, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    title = models.CharField(max_length=200)
    instructions = models.TextField(blank=True)
    duration_minutes = models.IntegerField()
    order = models.IntegerField(default=0)
    audio_file = models.FileField(upload_to='listening/', blank=True, null=True)

    def __str__(self):
        return f"{self.exam_set.title} - {self.get_section_type_display()}"

    class Meta:
        ordering = ['order']


class ReadingPassage(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='passages')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('fill_blank', 'Fill in the Blank'),
        ('true_false_ng', 'True/False/Not Given'),
        ('yes_no_ng', 'Yes/No/Not Given'),
        ('matching', 'Matching Headings'),
        ('sentence_completion', 'Sentence Completion'),
        ('map_labelling', 'Map Labelling'),
        ('essay_task1', 'Writing Task 1'),
        ('essay_task2', 'Writing Task 2'),
        ('speaking', 'Speaking'),
    ]
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='questions')
    passage = models.ForeignKey(ReadingPassage, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    question_type = models.CharField(max_length=30, choices=QUESTION_TYPES)
    question_text = models.TextField()
    question_number = models.IntegerField()
    image = models.ImageField(upload_to='writing/', blank=True, null=True)
    option_a = models.CharField(max_length=500, blank=True)
    option_b = models.CharField(max_length=500, blank=True)
    option_c = models.CharField(max_length=500, blank=True)
    option_d = models.CharField(max_length=500, blank=True)
    correct_answer = models.TextField(blank=True)
    explanation = models.TextField(blank=True)
    speaking_part = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['question_number']

    def __str__(self):
        return f"Q{self.question_number}: {self.question_text[:50]}"


class ExamAttempt(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attempts')
    exam_set = models.ForeignKey(ExamSet, on_delete=models.CASCADE, related_name='attempts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    current_section = models.CharField(max_length=20, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    listening_start = models.DateTimeField(null=True, blank=True)
    reading_start = models.DateTimeField(null=True, blank=True)
    writing_start = models.DateTimeField(null=True, blank=True)
    speaking_start = models.DateTimeField(null=True, blank=True)
    listening_end = models.DateTimeField(null=True, blank=True)
    reading_end = models.DateTimeField(null=True, blank=True)
    writing_end = models.DateTimeField(null=True, blank=True)
    speaking_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.exam_set.title} ({self.status})"

    class Meta:
        ordering = ['-started_at']


class StudentResponse(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    answer_text = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='speaking/', blank=True, null=True)
    is_correct = models.BooleanField(null=True)
    score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['attempt', 'question']

    def __str__(self):
        return f"Response to Q{self.question.question_number}"
