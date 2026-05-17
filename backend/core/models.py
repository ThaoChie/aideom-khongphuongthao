from django.db import models

class LessonRun(models.Model):
    lesson_id = models.CharField(max_length=32)
    params = models.JSONField(default=dict)
    result = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
