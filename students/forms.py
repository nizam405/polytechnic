from django import forms
from .models import Student
from applicants.models import Applicant

class StudentRegisterForm(forms.Form):
    ssc_roll    = forms.CharField(max_length=20)
    ssc_reg     = forms.CharField(max_length=20)

class AdmitForm(forms.ModelForm):
    class Meta:
        model   = Student
        fields  = '__all__'

class StudentAcademicInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('applicant',)
        
class StudentPersonalInfoUpdateForm(forms.ModelForm):
    class Meta:
        model   = Applicant
        fields  = [
                'gender', 'nationality', 'religion', 'phone', 'blood_group', 
                'present_address', 'permanent_address'
                ]