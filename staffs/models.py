from django.db import models
# from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image, ImageOps
from .choices import ROLE_CHOICES, DESIGNATION_CHOICES
from accounts.choices import RELIGIONS, GENDERS
from accounts.validators import validate_image, valid_alpha

# Create your models here.
class Staff(models.Model):
    identity        = models.CharField(max_length=10, unique=True)
    name            = models.CharField(max_length=254, null=True)
    role            = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Teacher')
    designation     = models.CharField(max_length=20, choices=DESIGNATION_CHOICES, default='Junior Instructor')

    def __str__(self):
        return self.name + " (" + self.role + ")"
    
class StaffProfile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    staff           = models.OneToOneField(Staff, on_delete=models.CASCADE)
    phone           = models.CharField(max_length=14, blank=True, null=True)
    date_of_birth   = models.DateField(verbose_name="Date of Birth", blank=True, null=True)
    nationality     = models.CharField(max_length=50, default="Bangladeshi", validators=[valid_alpha])
    religion        = models.CharField(max_length=50, default="Islam", choices=RELIGIONS, blank=True, null=True)
    gender          = models.CharField(choices=GENDERS, default="Male", max_length=10)
    blood_group     = models.CharField(max_length=3, blank=True, null=True)
    present_address = models.TextField(verbose_name="Present Address", blank=True, null=True)
    permanent_address = models.TextField(verbose_name="Permanent Address", blank=True, null=True)
    image           = models.ImageField(max_length=120, upload_to='staffs/',
                    validators=[validate_image], default="default-user.jpg",
                    help_text="Upload your recent photo. Image must be 200px or more both in height and width",
                    )
    def __str__(self):
        return self.user.username
    
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
        if w > 600 or h > 600:
            output_size = (600,600)
            img.thumbnail(output_size, Image.ANTIALIAS)
        img.save(self.image.path)
