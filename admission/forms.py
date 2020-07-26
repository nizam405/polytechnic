from django import forms
from django.conf import settings

# from batches.models import Batch
from applicants.models import Applicant

# Admission Form part-1
class AdmissionForm1(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['ssc_year', 'ssc_board', 'ssc_roll', 'ssc_reg']

# Admission Form (Full)
class AdmissionForm(forms.ModelForm):
    image = forms.FileField(required=True)
    class Meta:
        model   = Applicant
        fields  = '__all__'
        widgets = {
            'date_of_birth'     : forms.DateInput(format=('%Y-%m-%d'), attrs={'type' : 'date'}),
            'present_address'   : forms.Textarea(attrs={'rows':2}),
            'permanent_address' : forms.Textarea(attrs={'rows':2}),
            # 'batch'             : forms.HiddenInput()
        }
    def __init__(self, *args, **kwargs):
        super(AdmissionForm, self).__init__(*args, **kwargs)
        self.fields['batch'].disabled = True

# Admission Form (minimalist)
class AdmissionFormMin(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['ssc_board', 'ssc_year', 'ssc_roll', 'ssc_reg', 'course', 'phone']

class ApplicantLoginForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['ssc_year', 'ssc_roll', 'ssc_reg', 'phone']
