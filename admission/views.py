from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import EmptyResultSet
from requests.exceptions import ConnectionError

from .forms import ApplicantLoginForm, AdmissionForm, AdmissionForm1, AdmissionFormMin
from applicants.forms import PersonalInfoForm, ImageUploadForm
from batches.models import Batch
from applicants.models import Applicant
from courses.models import Course
from applicants.ScrapResult import EduInfo
from students.models import Student
from applicants.decorators import show_profile_if_logged_in, applicant_required
from .settings import MIN_GPA, FORM_URL
    
# Create your views here.
def admission(request):
    form = ApplicantLoginForm(request.POST or None)
    template = 'admission/admission.html'
    context = {
        'title'         : 'Admission Information',
        'page_name'     : 'admission',
        'form_url'      : FORM_URL,
        # Form properties
        'form'          : form,
        'submit_content': 'Login',
        'column'        : '2',
        }
    if request.method == 'POST':
        if form.is_valid():
            applicants = Applicant.objects.filter(
                    ssc_year    = form.cleaned_data.get('ssc_year'),
                    ssc_roll    = form.cleaned_data.get('ssc_roll'),
                    ssc_reg     = form.cleaned_data.get('ssc_reg'),
                    )
            if len(applicants) != 0:
                applicant = applicants[0]
                phone = form.cleaned_data.get('phone')
                if phone != applicant.phone:
                    messages.warning(request, "Invalid phone number")
                else:
                    request.session['applicant_id'] = applicant.id
                    return redirect('applicant-profile')
            else:
                messages.info(request, "No application found. Click on Apply now to place an application")
                return render(request, template, context)
            return redirect('applicant-profile')
    else:
        return render(request, template, context)

@show_profile_if_logged_in
def admissionForm1(request):
    template = 'admission/admission_form_1.html'
    admission_form = AdmissionForm1(request.POST or None)
    context = {
        'title' : 'Admission Form',
        'form' : admission_form,
        }
    if request.method == 'POST':
        if admission_form.is_valid():
            try:
                old_application = Applicant.objects.get(
                    ssc_year = admission_form.cleaned_data['ssc_year'],
                    ssc_roll = admission_form.cleaned_data['ssc_roll'],
                )
                messages.warning(request, "You have applied before. Please login to your profile.")
                return redirect('admission')
            except Applicant.DoesNotExist: pass
            # exam    = 'ssc'
            year    = admission_form.cleaned_data['ssc_year']
            board   = admission_form.cleaned_data['ssc_board']
            roll    = admission_form.cleaned_data['ssc_roll']
            reg     = admission_form.cleaned_data['ssc_reg']

            try:
                edu_info = EduInfo(year, board, roll, reg)
                data = edu_info.getSSCInfo()
                gpa = float(data['ssc_gpa'])
                if gpa < MIN_GPA:
                    messages.warning(request, f"required GPA {MIN_GPA} or more to apply.")
                    return redirect('admission')
                request.session['form_data'] = data
                # print(request.session['form_data'])
                return redirect('admission-form2')
            except ConnectionError:
                messages.warning(request, "Education Board server is not responding. Fill-up manually.")
                return redirect('admission-form')
            except EmptyResultSet:
                messages.warning(request, "Please input correct informaion!")
        else:
            print('not valid')
            
    return render(request, template, context)

@show_profile_if_logged_in
def admissionForm2(request):
    template = 'admission/admission_form_2.html'
    admission_form = PersonalInfoForm(request.POST or None)
    # print(admission_form)
    context = {
        'title' : 'Admission Form',
        'form'  : admission_form,
        'data'  : request.session['form_data'],
        }
    if request.method == 'POST':
        if admission_form.is_valid():
            data = {
                # Personal info
                'gender'            : request.POST['gender'],
                'nationality'       : request.POST['nationality'],
                'religion'          : request.POST['religion'],
                'phone'             : request.POST['phone'],
                'gurdian_phone'     : request.POST['gurdian_phone'],
                'blood_group'       : request.POST['blood_group'],
                'course'            : request.POST['course'],
                'present_address'   : request.POST['present_address'],
                'permanent_address' : request.POST['permanent_address'],
            }
            data.update(request.session['form_data'])
            request.session['form_data'] = data
            return redirect('admission-form3')
            
    return render(request, template, context)

@show_profile_if_logged_in
def admissionForm3(request):
    template = 'admission/admission_form_3.html'
    admission_form = ImageUploadForm(request.POST or None, request.FILES or None)
    # print(admission_form)
    context = {
            'title' : 'Admission Form',
            'form'  : admission_form,
            }
    if request.method == 'POST':
        if admission_form.is_valid():
            dataDict            = request.session['form_data']
            dataDict['course']  = Course.objects.get(id=dataDict['course'])
            batch               = Batch.objects.all().last()
            applicant           = Applicant(batch=batch, **dataDict)
            applicant.save()
            form3 = ImageUploadForm(request.POST or None, request.FILES, instance=applicant)
            form3.save()
            del request.session['form_data']
            request.session['applicant_id'] = applicant.id
            return redirect('application-done')
        else:
            print('error')      
    return render(request, template, context)

@show_profile_if_logged_in
def admissionForm(request):
    template = 'admission/admission_form.html'
    admission_form = AdmissionForm(request.POST or None, request.FILES or None)
    current_batch = Batch.objects.all().last()
    admission_form.fields['batch'].initial = current_batch
    if request.method == 'POST':
        if admission_form.is_valid():
            try:
                old_application = Applicant.objects.get(
                    ssc_year = admission_form.cleaned_data['ssc_year'],
                    ssc_roll = admission_form.cleaned_data['ssc_roll'],
                )
                messages.warning(request, "You have applied before. Please login to your profile.")
                return redirect('admission')
            except Applicant.DoesNotExist: pass
            ssc_gpa = int(admission_form.cleaned_data.get('ssc_gpa'))
            if ssc_gpa < MIN_GPA:
                messages.warning(request, f"required GPA {MIN_GPA} or more to apply.")
                return redirect('admission')
            instance = admission_form.save()
            request.session['applicant_id'] = instance.id
            if request.session.has_key('form_data'):
                del request.session['form_data']
            return redirect('application-done')
    else:
        if request.session.has_key('form_data'):
            admission_form.initial = request.session['form_data']
        else:
            admission_form = AdmissionForm()
    context = {
            'title' : 'Admission Form',
            'form' : admission_form,
            }
    return render(request, template, context)

@show_profile_if_logged_in
def admissionFormMin(request):
    template = 'admission/admission_form_min.html'
    form = AdmissionFormMin(request.POST or None)
    context = {
        'title' : 'Admission Form',
        'form' : form,
        }
    if request.method == 'POST':
        if form.is_valid():
            try:
                old_application = Applicant.objects.get(
                    ssc_year = form.cleaned_data['ssc_year'],
                    ssc_roll = form.cleaned_data['ssc_roll'],
                )
                messages.warning(request, "You have applied before. Please login to your profile.")
                return redirect('admission')
            except Applicant.DoesNotExist: pass
            # exam    = 'ssc'
            year    = form.cleaned_data['ssc_year']
            board   = form.cleaned_data['ssc_board']
            roll    = form.cleaned_data['ssc_roll']
            reg     = form.cleaned_data['ssc_reg']

            try:
                edu_info = EduInfo(year, board, roll, reg)
                data = edu_info.getSSCInfo()
                gpa = float(data['ssc_gpa'])
                if gpa < MIN_GPA:
                    messages.warning(request, f"required GPA {MIN_GPA} or more to apply.")
                    return redirect('admission')
                data.update({
                    # Required fields
                    'batch'         : Batch.objects.all().last(),
                    'phone'         : form.cleaned_data.get('phone'),
                    'course'        : form.cleaned_data.get('course'),
                })
                applicant = Applicant(**data)
                applicant.save()
                request.session['applicant_id'] = applicant.id
                # print(request.session['form_data'])
                return redirect('applicant_edit_form')
            except ConnectionError:
                messages.warning(request, "Education Board server is not responding. Fill-up manually.")
                return redirect('admission-form')
            except EmptyResultSet:
                messages.warning(request, "Please input correct informaion!")
        else:
            print('not valid')
            
    return render(request, template, context)

@applicant_required
def applicationDone(request):
    applicant_id    = request.session['applicant_id']    
    applicant       = get_object_or_404(Applicant, id=applicant_id)
    template        = 'admission/application_done.html'
    context         = {
                    'title' : 'Admission Form Done',
                    'applicant' : applicant,
                    }
    return render(request, template, context)
    
@applicant_required
def verifyApplication(request):
    applicant_id    = request.session['applicant_id']    
    applicant       = get_object_or_404(Applicant, id=applicant_id)
    try:
        edu_info    = EduInfo(applicant.ssc_year, applicant.ssc_board, applicant.ssc_roll, applicant.ssc_reg)
        data        = edu_info.getSSCInfo()
        gpa         = float(data['ssc_gpa'])
        if gpa < MIN_GPA:
            messages.warning(request, f"required GPA {MIN_GPA} or more to apply.")
            applicant.delete()
            messages.warning(request, "Your application will be cancaled automatically.")
            return redirect('applicant-logout')
        else:
            for (key, value) in data.items():
                setattr(applicant, key, value)
            applicant.save()
            messages.success(request, "Your application has been varified successfully.")
    except ConnectionError:
        messages.warning(request, "Education Board server is not responding. Fill-up manually.")
        # return redirect('applicant-profile')
    except EmptyResultSet:
        messages.warning(request, "Please input correct informaion!")
    return redirect('applicant-profile')
