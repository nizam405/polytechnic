from django.db import models
from PIL import Image, ImageOps

from .choices import COURSE_TYPE, COURSE_DURATIONS, SEMESTER_DURATIONS, SEMESTER_CHOICES
from .validators import validate_image
# Create your models here.
class Course(models.Model):
    name            = models.CharField(max_length=255)
    short_hand      = models.CharField(default="-T", max_length=5)
    code            = models.CharField(max_length=3)
    course_type     = models.CharField(max_length=100, choices=COURSE_TYPE, default="Diploma in Engineering")
    admission_fee   = models.IntegerField(verbose_name="Admission Fee", default=5000)
    readmission_fee = models.IntegerField(verbose_name="Re-admission Fee", default=0)
    semeseters      = models.IntegerField(verbose_name="No. of semesters", default=8)
    duration        = models.CharField(max_length=100, choices=COURSE_DURATIONS, default="4 Years")
    image           = models.ImageField(
                        upload_to='courses', 
                        default='1280x640.png', 
                        validators=[validate_image],
                        help_text = 'Image size: 1280x640')
    description     = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.code + " " + self.name
    
    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        if img.mode not in ("L","RGB"):
            img = img.convert("RGB")
        w, h = img.size
        # Make image ratio 2:1
        if w != h*2:
            height  = h if h*2 <= w else w/2
            width   = height * 2
            img     = ImageOps.fit(img, (width, height), Image.ANTIALIAS)
        # Resize image
        if w > 1280 or h > 640:
            output_size = (1280,640)
            img.thumbnail(output_size, Image.ANTIALIAS)
        img.save(self.image.path)

# Unused
# class Semester(models.Model):
#     course          = models.ForeignKey(to=Course, on_delete=models.CASCADE)
#     duration        = models.CharField(max_length=100, choices=SEMESTER_DURATIONS, default="6 Months")
#     name            = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
#     semester_fee    = models.IntegerField(verbose_name="Semester Fee", default=3000)
#     monthly_fee     = models.IntegerField(verbose_name="Monthly Fee", default=2000)

#     def __str__(self):
#         return self.name + " (" + self.course.code + ") " + self.course.name
    
