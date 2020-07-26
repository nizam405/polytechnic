from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

def validate_image(imageField):
    filesize = imageField.file.size
    w, h = get_image_dimensions(imageField)
    if w < 1280:
        raise ValidationError(f"The image is {w} pixel wide. It should be greater than or equal to 1280px")
    if h < 640:
        raise ValidationError(f"The image is {h} pixel high. It should be greater than or equal to 640px")
