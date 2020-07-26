# from io import StringIO
# from PIL import Image, ImageOps
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from applicants.models import Applicant
from .choices import USER_CATEGORY_CHOICES

class SignUpForm(forms.Form):
    user_category = forms.ChoiceField(
        choices = USER_CATEGORY_CHOICES,
        widget  = forms.RadioSelect
    )
    identity    = forms.CharField(max_length=254, help_text='Enter ID which our institite provided')

class UserRegisterForm(UserCreationForm):
    class Meta:
        model   = User
        fields  = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model   = User
        fields  = ['first_name', 'last_name', 'email']

