from django import forms
from .models import Staff, StaffProfile

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model   = StaffProfile
        fields  = [
                'phone', 'date_of_birth', 'nationality', 'religion', 'gender', 
                'blood_group', 'present_address', 'permanent_address'
                ]
        widgets = {
            'date_of_birth'     : forms.DateInput(format=('%Y-%m-%d'), attrs={'type' : 'date'}),
            'present_address'   : forms.Textarea(attrs={'rows':2}),
            'permanent_address' : forms.Textarea(attrs={'rows':2})
        }

class StaffProfilePicture(forms.ModelForm):
    class Meta:
        model   = StaffProfile
        fields  = ['image']

class StaffForm(forms.ModelForm):
    class Meta:
        model   = Staff
        fields  = '__all__'