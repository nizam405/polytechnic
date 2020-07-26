from django.db import models

from .choices import CURRENT_DATE, LATER30D
# Create your models here.
class Batch(models.Model):
    batch_no        = models.CharField(verbose_name="Batch No", max_length=3, 
                    unique=True, help_text="Example: 1st, 2nd, 3rd etc.")
    session         = models.CharField(max_length=9, help_text="Example: 2019-2020", unique=True)
    regulation      = models.CharField(max_length=4, default="2016")
    admission_start = models.DateField(default=CURRENT_DATE)
    admission_end   = models.DateField(default=LATER30D)
    maintain_date   = models.BooleanField(default=True)

    def __str__(self):
        return self.batch_no + " (" + self.session + ")"
    
    class Meta:
        verbose_name_plural = "Batches"