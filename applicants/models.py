from django.db import models
from django.utils import timezone
from datetime import datetime
from PIL import Image, ImageOps

from courses.models import Course
from batches.models import Batch
from accounts.validators import validate_image, valid_alpha, valid_number, valid_phone
from .validators import valid_result
from .choices import INITIAL_SEMESTERS, BOARDS, SSC_YEARS
from accounts.choices import RELIGIONS, GENDERS, BLOOD_GROUPS

# Create your models here.
class Applicant(models.Model):
    # Required
    sub_date        = models.DateTimeField(verbose_name="Submission Date", auto_now_add=True)
    verified        = models.BooleanField(default=False)
    admitted        = models.BooleanField(default=False)
    batch           = models.ForeignKey(to=Batch, on_delete=models.CASCADE)
    course          = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    semester_apply  = models.CharField(max_length=3, choices=INITIAL_SEMESTERS, default='1st', verbose_name="Semester to apply")
    phone           = models.CharField(max_length=11, validators=[valid_phone], blank=False, null=False)
    # Education Board info
    ssc_year        = models.IntegerField(verbose_name="SSC Passing Year", choices=SSC_YEARS, default=datetime.now().year)
    ssc_board       = models.CharField(verbose_name="Board", max_length=20, choices=BOARDS)
    ssc_roll        = models.CharField(verbose_name="SSC Roll", max_length=10, validators=[valid_number])
    ssc_reg         = models.CharField(verbose_name="SSC Registration", max_length=10, validators=[valid_number])
    ssc_group       = models.CharField(verbose_name="Group", max_length=20)
    ssc_gpa          = models.DecimalField(verbose_name="SSC GPA", max_digits=3, decimal_places=2, validators=[valid_result])
    name            = models.CharField(max_length=255, validators=[valid_alpha])
    date_of_birth   = models.DateField(verbose_name="Date of Birth")
    father_name     = models.CharField(verbose_name="Father's Name", max_length=100, validators=[valid_alpha])
    mother_name     = models.CharField(verbose_name="Mother's Name", max_length=100, validators=[valid_alpha])
    # Optional
    gender          = models.CharField(choices=GENDERS, default="Male", max_length=10)
    nationality     = models.CharField(max_length=50, default="Bangladeshi", validators=[valid_alpha])
    religion        = models.CharField(max_length=50, default="Islam", choices=RELIGIONS)
    blood_group     = models.CharField(max_length=3, blank=True, null=True, choices=BLOOD_GROUPS)
    gurdian_phone   = models.CharField(verbose_name="Gurdian's Phone", max_length=11, validators=[valid_phone], blank=True)
    present_address = models.TextField(verbose_name="Present Address", default="", blank=True)
    permanent_address = models.TextField(verbose_name="Permanent Address", default="", blank=True)
    image           = models.ImageField(max_length=120, upload_to='applicants/',
                    validators=[validate_image], default="default-user.jpg",
                    help_text="Upload your recent photo. Image must be 200px or more both in height and width",
                    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.id) + ". " + self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.mode not in ("L","RGB"):
            img = img.convert("RGB")
        w, h = img.size
        # Make image square
        if w != h:
            min_size = h if h < w else w
            img = ImageOps.fit(img, (min_size, min_size), Image.ANTIALIAS)
        # Resize image
        if w > 200 or h > 200:
            output_size = (200,200)
            img.thumbnail(output_size, Image.ANTIALIAS)
        img.save(self.image.path)
