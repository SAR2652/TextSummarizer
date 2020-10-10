from django.db import models

# Create your models here.
class TextSummary(models.Model):
    text_id = models.BigIntegerField(primary_key=True)
    text = models.TextField()
    summary = models.TextField()
    created_at = models.DateTimeField()