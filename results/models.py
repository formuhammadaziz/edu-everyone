from django.db import models
from django.conf import settings
from exams.models import ExamAttempt


class ExamResult(models.Model):
    attempt = models.OneToOneField(ExamAttempt, on_delete=models.CASCADE, related_name='result')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='results')
    overall_band = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    listening_score = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    listening_correct = models.IntegerField(default=0)
    reading_score = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    reading_correct = models.IntegerField(default=0)
    writing_score = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    speaking_score = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    time_listening = models.IntegerField(default=0)
    time_reading = models.IntegerField(default=0)
    time_writing = models.IntegerField(default=0)
    time_speaking = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Band {self.overall_band}"

    def calculate_overall_band(self):
        scores = []
        for s in [self.listening_score, self.reading_score, self.writing_score, self.speaking_score]:
            if s is not None:
                scores.append(float(s))
        if scores:
            avg = sum(scores) / len(scores)
            self.overall_band = round(avg * 2) / 2
        self.save()

    class Meta:
        ordering = ['-created_at']


class WritingCheckResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='writing_checks')
    task_type = models.CharField(max_length=20)
    task_prompt = models.TextField(blank=True)
    essay = models.TextField()
    feedback = models.TextField()
    word_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.task_type} - {self.created_at.date()}"
