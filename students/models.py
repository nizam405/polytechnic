from django.db import models
from django.contrib.auth.models import User

from applicants.models import Applicant
from accounts.validators import valid_alpha, validate_image
from .choices import SEMESTERS

# Create your models here.

class Student(models.Model):
    # Academic info
    applicant       = models.OneToOneField(Applicant, on_delete=models.CASCADE)
    # batch           = models.ForeignKey(to=Batch, on_delete=models.SET_NULL, blank=True, null=True)
    semester        = models.CharField(default='1st', choices=SEMESTERS, max_length=3)
    class_roll      = models.CharField(default='00', max_length=5)
    identity        = models.CharField(max_length=50, unique=True)
    roll            = models.CharField(max_length=10, unique=True, blank=True, null=True)
    registration    = models.CharField(max_length=10, unique=True, blank=True, null=True)

    def __str__(self):
        return self.identity + " - " + self.applicant.name

class StdLink(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    student         = models.OneToOneField(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.applicant.name
    
