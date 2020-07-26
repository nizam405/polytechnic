from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import StaffForm, StaffProfilePicture, StaffProfileForm
from accounts.decorators import controller_required
from .models import Staff, StaffProfile

# Staff
@controller_required
def staff_list(request):
    staffs  = Staff.objects.all()
    template    = 'staffs/staff_list.html'
    context     = {
                'title'         : 'Staffs',
                'staffs'        : staffs,
                'page_name'     : 'staff_list',
                'menu'          : 'staff_list',
                'menu_header'   : 'academic',
                }
    return render(request, template, context)

@controller_required
def add_staff(request):
    form        = StaffForm(request.POST or None)
    template    = 'root/form.html'
    context     = {
                'title'         : 'Add Staff',
                'page_name'     : 'add_staff',
                'menu'          : 'staff_list',
                'menu_header'   : 'academic',
                # Form properties
                'form'          : form,
                'extend_file'   : 'account/base.html',
                'header'        : 'Add Staff',
                'submit_content': 'Add',
                'reset_content' : 'Reset',
                'column'        : '1',
                'form_layout'   : 'horizontal',
                'form_size'     : 'small',
                'button_size'   : 'sm',
                'enable_buttons': True,
                }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    return render(request, template, context)

@controller_required
def view_staff(request, staff_id):
    staff   = Staff.objects.get(id=staff_id)
    template    = 'staffs/view_staff.html'
    context     = {
                'title'         : staff.name,
                'staff'         : staff,
                'page_name'     : 'view_staff',
                'menu'          : 'staffs_list',
                'menu_header'   : 'academic',
                }
    return render(request, template, context)

@controller_required
def edit_staff(request, staff_id):
    staff       = get_object_or_404(Staff, id=staff_id)
    form        = StaffForm(request.POST or None, instance=staff)
    template    = 'root/form.html'
    context     = {
                'title'         : 'Edit Staff',
                'page_name'     : 'edit_staff',
                'menu'          : 'staff_list',
                'menu_header'   : 'academic',
                # Form properties
                'form'          : form,
                'extend_file'   : 'account/base.html',
                'header'        : 'Edit Staff',
                'submit_content': 'Save',
                'reset_content' : 'Reset',
                'column'        : '1',
                'form_layout'   : 'horizontal',
                'form_size'     : 'small',
                'button_size'   : 'sm',
                'enable_buttons': True,
                }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('view_staff', staff_id)
    return render(request, template, context)

@controller_required
def change_staff_personal_info(request, staff_id):
    staff           = get_object_or_404(Staff, id=staff_id)
    staff_profile   = get_object_or_404(StaffProfile, staff=staff)
    form            = StaffProfileForm(request.POST or None, instance=staff_profile)
    template        = 'root/form.html'
    context         = {
                    'title'         : 'Edit Staff Personal Info',
                    'page_name'     : 'edit_staff',
                    'menu'          : 'staff_list',
                    'menu_header'   : 'academic',
                    # Form properties
                    'form'          : form,
                    'extend_file'   : 'account/base.html',
                    'header'        : 'Edit Staff Personal Info',
                    'submit_content': 'Save',
                    'reset_content' : 'Reset',
                    'column'        : '1',
                    'form_layout'   : 'horizontal',
                    'form_size'     : 'small',
                    'button_size'   : 'sm',
                    'enable_buttons': True,
                    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('view_staff', staff_id)
    return render(request, template, context)

@controller_required
def confirm_remove_staff(request, staff_id):
    staff       = Staff.objects.get(id=staff_id)
    template    = 'root/confirm_delete.html'
    context     = {
                'title'         : 'Confirm remove staff',
                'staff'         : staff,
                'page_name'     : 'confirm_remove_staff',
                'menu'          : 'staff_list',
                'menu_header'   : 'academic',
                # template options
                'extends_file'  : 'account/base.html',
                'content'       : f'You are removing {staff.name}',
                'warning_list'  : [
                    f'{staff.name} will no longer available',
                ],
                'delete_url'    : 'remove_staff',
                'no_url'        : 'view_staff',
                'id'            : staff_id,
                'delete_text'   : 'Remove',
                }
    return render(request, template, context)

@controller_required
def remove_staff(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    staff.delete()
    messages.success(request, f'{staff.name} has removed successfully')
    return redirect('staff_list')

@controller_required
def change_staff_image(request, staff_id):
    # applicant_id    = request.session['applicant_id']    
    staff           = get_object_or_404(Staff, id=staff_id)
    form            = StaffProfilePicture(request.POST, request.FILES, instance=staff.staffprofile)
    template        = 'root/image_upload_form.html'
    context         = {
                    'title'         : 'Change Image',
                    'page'          : 'profile_pic',
                    # Form properties
                    'form'          : form,
                    'src'           : staff.staffprofile.image.url,
                    'heading'       : 'Upload image',
                    'extends_file'  : 'account/base.html',
                    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Image uploaded successfully")
            return redirect('view_staff', staff_id) 
    return render(request, template, context)

@login_required
def updateStaffProfile(request):
    staff = request.user.staffprofile
    form = StaffProfileForm(request.POST or None, instance=staff)
    template = 'root/form.html'
    context = {
        'title'         : 'Edit Personal Information',
        'form'          : form,
        'page_name'     : 'edit_personal_info',
        'menu'          : 'profile',
        'menu_header'   : 'account',
        # Form properties
        'extend_file'   : 'account/base.html',
        'header'        : 'Edit Personal Information',
        'column'        : '1',
        'form_layout'   : 'horizontal',
        'form_size'     : 'small',
        'submit_content': 'Save',
        'reset_content' : 'Reset',
        # 'skip_content'  : 'Skip',
        # 'skip_href'     : "/applicant/profile/",
        'button_size'   : 'sm',
        }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    return render(request, template, context)

@login_required
def changeProfilePicture(request):
    if request.user.staffprofile:
        staff = request.user.staffprofile
        form = StaffProfilePicture(request.POST, request.FILES, instance=staff)
        template = 'account/profile-picture.html'
        context = {
            'title'         : 'Change Profile Picture',
            'form'          : form,
            'page_name'     : 'change_profile_picture',
            'menu'          : 'profile',
            'menu_header'   : 'account',
            }
        if request.method == 'POST':
            context['form'] = form
            if form.is_valid():
                form.save()
                messages.success(request, "Image Updated successfully")
            else:
                messages.warning(request, "Somethin went wrong!")
                return redirect('profile-picture')
        return render(request, template, context)
    else:
        return redirect('user_profile')

