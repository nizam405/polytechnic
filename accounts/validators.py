from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.validators import RegexValidator

def validate_image(imageField):
    filesize = imageField.file.size
    w, h = get_image_dimensions(imageField)
    if w < 200:
        raise ValidationError("The image is %i pixel wide. It should be greater than or equal to 200px" %w)
    if h < 200:
        raise ValidationError("The image is %i pixel high. It should be greater than or equal to 200px" %h)

valid_alpha = RegexValidator(r"^[a-zA-Z\s.\-]*$", "Only characters are allowed. Don\'t use number")
valid_phone = RegexValidator(r"^[+0-9]{6,11}$", "Enter a valid phone number")
valid_number = RegexValidator(r"^[0-9]{6,10}$", "Only numbers are allowed")

