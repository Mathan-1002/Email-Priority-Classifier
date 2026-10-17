from django.db import models


class Email(models.Model):
    PRIORITIES = [("High", "High"), ("Medium", "Medium"), ("Low", "Low")]

    sender = models.CharField(max_length=254, blank=True)
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    priority = models.CharField(max_length=6, choices=PRIORITIES)
    confidence = models.FloatField(default=0)
    corrected = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"[{self.priority}] {self.subject}"
