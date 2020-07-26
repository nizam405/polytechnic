from django import forms
from .models import Applicant

class ApplicantEditForm(forms.ModelForm):
    class Meta:
        model   = Applicant
        exclude = ('image',)
        widgets = {
            'present_address': forms.Textarea(attrs={'rows':2}),
            'permanent_address': forms.Textarea(attrs={'rows':2})
        }

class ApplicantFilterForm(forms.ModelForm):
    class Meta:
        model   = Applicant
        fields  = ['course']

# Admission Form part-2
class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = [
            'gender', 'nationality', 'religion', 'blood_group', 'phone', 
            'gurdian_phone', 'present_address', 'permanent_address', 'course'
            ]
        widgets = {
            'present_address': forms.Textarea(attrs={'rows':2}),
            'permanent_address': forms.Textarea(attrs={'rows':2})
        }
# Admission Form part-3
class ImageUploadForm(forms.ModelForm):
    image = forms.FileField(required=True)
    class Meta:
        model   = Applicant
        fields  = ['image']