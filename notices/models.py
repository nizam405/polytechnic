from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

# Create your models here.
class Notice(models.Model):
    title           = models.CharField(max_length=255)
    content         = models.TextField()
    date_created    = models.DateTimeField(default=timezone.now)
    date_modified   = models.DateTimeField(auto_now=True)
    author          = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('title', 'date_created', 'date_modified',)

    def __str__(self):
        return self.title

class Attachment(models.Model):
    notice          = models.ForeignKey(to=Notice, on_delete=models.CASCADE)
    subject         = models.CharField(max_length=255)
    attachment      = models.FileField(upload_to='notices/attachments')

    def __str__(self):
        return self.subject
    