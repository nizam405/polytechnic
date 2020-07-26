from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import EmptyResultSet
from requests.exceptions import ConnectionError

from .forms import ApplicantEditForm, ApplicantFilterForm, ImageUploadForm
from .models import Applicant
from accounts.decorators import controller_required
from .decorators import show_profile_if_logged_in, applicant_required
from .ScrapResult import EduInfo
from admission.settings import MIN_GPA

# Controller view
@controller_required
def applicant_list(request):
    applicants  = Applicant.objects.filter(admitted=False)
    form        = ApplicantFilterForm(request.POST or None)
    if request.method == 'POST':
        filter_course = request.POST['course']
        if filter_course != None:
            applicants.filter(course=filter_course)

    template    = 'applicants/applicant_list.html'
    context     = {
                'title'         : 'Applicants',
                'applicants'    : applicants,
                'page_name'     : 'applicant_list',
                'menu'          : 'applicant_list',
                'menu_header'   : 'admission',
                # Form properties
                'form'          : form,
                # 'form_layout'   : 'inline',
                # 'submit_content': 'Filter',
                # 'form_size'     : 'small',
                # 'button_size'   : 'sm',
                }
    return render(request, template, context)

@controller_required
def show_applicant(request, applicant_id):
    applicant   = Applicant.objects.get(id=applicant_id)
    try:
        student = Student.objects.get(applicant=applicant)
        return redirect('show_student', student.id)
    except: pass
    template    = 'applicants/show_applicant.html'
    context     = {
                'title'         : 'Application',
                'applicant'     : applicant,
                'page_name'     : 'show_applicant',
                'menu'          : 'applicant_list',
                'menu_header'   : 'admission',
                }
    return render(request, template, context)

@controller_required
def edit_applicant(request, applicant_id):
    applicant   = Applicant.objects.get(id=applicant_id)
    form        = ApplicantEditForm(request.POST or None, instance=applicant)
    template    = 'applicants/edit_applicant.html'
    # template    = 'root/form.html'
    context     = {
                'title'         : 'Edit Application',
                'applicant'     : applicant,
                'page_name'     : 'edit_applicant',
                'menu'          : 'applicant_list',
                'menu_header'   : 'admission',
                # Form properties
                'form'          : form,
                # 'extend_file'   : 'account/base.html',
                # 'header'        : 'Change Applicant Information',
                'submit_content': 'Save',
                'reset_content' : 'Reset',
                'column'        : '1',
                'form_layout'   : 'horizontal',
                'form_size'     : 'small',
                'button_size'   : 'sm',
                }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Applicant updated successfully')
            return redirect('show_applicant', applicant_id)
    return render(request, template, context)

@controller_required
def verifyApplication(request, applicant_id): 
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
    return redirect('show_applicant', applicant_id)

@controller_required
def confirm_reject_applicant(request, applicant_id):
    applicant   = Applicant.objects.get(id=applicant_id)
    # template    = 'account/applicants/confirm_delete_application.html'
    template    = 'root/confirm_delete.html'
    context     = {
                'title'         : 'Application',
                'applicant'     : applicant,
                'page_name'     : 'confirm_reject_applicant',
                'menu'          : 'applicant_list',
                'menu_header'   : 'admission',
                # template options
                'extends_file'  : 'account/base.html',
                'content'       : f'You are rejecting {applicant.name}',
                'warning_list'  : [
                    f'{applicant.name} will no longer available in applicants list',
                ],
                'delete_url'    : 'reject_applicant',
                'no_url'        : 'show_applicant',
                'id'            : applicant_id,
                'delete_text'   : 'Reject',
                }
    return render(request, template, context)

@controller_required
def reject_applicant(request, applicant_id):
    applicant   = Applicant.objects.get(id=applicant_id)
    applicant.delete()
    messages.success(request, f'Application of {applicant.name} has rejected successfully')
    return redirect('applicant_list')

@controller_required
def change_applicant_image(request, applicant_id):
    # applicant_id    = request.session['applicant_id']    
    applicant       = get_object_or_404(Applicant, id=applicant_id)
    form            = ImageUploadForm(request.POST, request.FILES, instance=applicant)
    # template        = 'applicant/update-profile-picture.html'
    template        = 'root/image_upload_form.html'
    context         = {
                    'title'         : 'Change Form Information',
                    'applicant'     : applicant,
                    'page'          : 'profile_pic',
                    # Form properties
                    'form'          : form,
                    'src'           : applicant.image.url,
                    'heading'       : 'Upload image',
                    'extends_file'  : 'account/base.html',
                    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Image uploaded successfully")
            return redirect('show_applicant', applicant_id) 
    return render(request, template, context)

# Applicant view
@applicant_required
def applicantProfile(request):
    applicant_id    = request.session['applicant_id']    
    applicant       = get_object_or_404(Applicant, id=applicant_id)
    template        = 'applicant/profile.html'
    context         = {
                    'title' : 'Applicant Profile',
                    'page': 'profile',
                    'applicant' : applicant,
                    }
    return render(request, template, context)

@applicant_required
def viewApplication(request):
    applicant_id    = request.session['applicant_id']    
    applicant       = get_object_or_404(Applicant, id=applicant_id)  
    template        = 'applicants/view_application.html'
    context         = {
                    'title'     : 'View Amission Form',
                    'page'      : 'view_form',
                    'applicant' : applicant,
                    }
    return render(request, template, context)

@applicant_required
def editApplication(request):
    applicant_id    = request.session['applicant_id']    
    applicant       = get_object_or_404(Applicant, id=applicant_id)
    form            = PersonalInfoForm(request.POST or None, instance=applicant)
    template        = 'root/form.html'
    context         = {
                    'title'         : 'Change Personal Information',
                    'form'          : form,
                    'applicant'     : applicant,
                    'page'          : 'edit_info',
                    # Form properties
                    'extend_file'   : 'applicant/base.html',
                    'header'        : 'Change Personal Information',
                    'column'        : '2',
                    # 'form_layout'   : 'horizontal',
                    'form_size'     : 'small',
                    'submit_content': 'Save',
                    'reset_content' : 'Reset',
                    # 'skip_content'  : 'Skip',
                    'skip_href'     : "/applicant/profile/",
                    'button_size'   : 'sm',
                    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('applicant_view_application')
    return render(request, template, context)

@applicant_required
def updateProfilePicture(request):
    applicant_id    = request.session['applicant_id']    
    applicant       = get_object_or_404(Applicant, id=applicant_id)
    form            = ImageUploadForm(request.POST, request.FILES, instance=applicant)
    # template        = 'applicant/update-profile-picture.html'
    template        = 'root/image_upload_form.html'
    context         = {
                    'title'         : 'Change Form Information',
                    'applicant'     : applicant,
                    'page'          : 'profile_pic',
                    # Form properties
                    'form'          : form,
                    'src'           : applicant.image.url,
                    'heading'       : 'Upload your image',
                    'extends_file'  : 'applicant/base.html',
                    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('applicant_view_application') 
    return render(request, template, context)

@applicant_required
def confirmDeleteApplication(request):
    applicant_id    = request.session['applicant_id']    
    applicant       = get_object_or_404(Applicant, id=applicant_id)
    # template        = 'applicants/delete_application.html'
    template        = 'root/confirm_delete.html'
    context         = {
                    'title'         : 'Cancle Application',
                    'applicant'     : applicant,
                    'page_name'     : 'delete_application',
                    # 'menu'          : 'staff_list',
                    # 'menu_header'   : 'academic',
                    # template options
                    'extends_file'  : 'applicants/base.html',
                    'content'       : 'You want to delete your application form',
                    'warning_list'  : [
                        'You can apply again in future',
                    ],
                    'delete_url'    : 'delete-form',
                    'no_url'        : 'applicant_view_application',
                    # 'id'            : applicant_id,
                    'delete_text'   : 'Remove',
                    }
    return render(request, template, context)

@applicant_required
def deleteApplication(request):
    applicant_id    = request.session['applicant_id']    
    applicant       = get_object_or_404(Applicant, id=applicant_id)
    applicant.delete()
    return redirect('applicant-logout')

@applicant_required
def logout(request):
    del request.session['applicant_id']
    return redirect('admission')