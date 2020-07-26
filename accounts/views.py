from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.exceptions import EmptyResultSet
from requests.exceptions import ConnectionError

from .forms import SignUpForm, UserUpdateForm, UserRegisterForm
from applicants.models import Applicant
from applicants.ScrapResult import EduInfo
from admission.settings import MIN_GPA
from students.models import Student, StdLink
from .decorators import controller_required

def signupFormView(request):
    if request.user.is_authenticated:
        return redirect('user_profile')
    else:
        form = SignUpForm(request.POST or None)
        template = 'accounts/users/login_signup.html'
        context = {
            'title'         : 'Registraion Form',
            'page_name'     : 'signup',
            # Form properties
            'form'          : form,
            'submit_content': 'Next',
            }
        if request.method == 'POST':
            if form.is_valid():
                # If a student
                identity = form.cleaned_data.get('identity')
                user_category = request.POST['user_category']
                if user_category == 'Student':
                    student = Student.objects.filter(identity=identity)
                    if len(student) != 0:
                        stdlink = StdLink.objects.filter(student=student[0])
                        if len(stdlink) != 0:
                            messages.warning(request, 'You are already registered. Please login to your account')
                            return redirect('login')
                        request.session['student_id'] = student[0].id
                        return redirect('user_creation_form')
                    else:
                        messages.warning(request, 'You are not our student')
                # If a staff
                elif user_category == 'Staff':
                    staff = Staff.objects.filter(identity=identity)
                    if len(staff) != 0:
                        staffprofile = StaffProfile.objects.filter(staff=staff[0])
                        if len(staffprofile) != 0:
                            messages.warning(request, 'You are already registered. Please login to your account')
                            return redirect('login')
                        request.session['staff_id'] = staff[0].id
                        return redirect('user_creation_form')
                    else:
                        messages.warning(request, 'You are not our staff')
                else:
                    return HttpResponse('Group does not exist')

        return render(request, template, context)

def userCreationFormView(request):
    if request.session.has_key('student_id') or request.session.has_key('staff_id'):
        form = UserRegisterForm(request.POST or None)
        template = 'accounts/users/login_signup.html'
        context = {
            'title'         : 'Registraion Form',
            'page_name'     : 'signup',
            # Form properties
            'form'          : form,
            'submit_content': 'Signup',
            }
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                if request.session.has_key('student_id'):
                    student = Student.objects.get(id=request.session['student_id'])
                    stdlink = StdLink.objects.create(user=user, student=student)
                    stdlink.save()
                    del request.session['student_id']
                    return redirect('user_profile')
                elif request.session.has_key('staff_id'):
                    staff = Staff.objects.get(id=request.session['staff_id'])
                    staffprofile = StaffProfile.objects.create(user=user, staff=staff)
                    staffprofile.save()
                    del request.session['staff_id']
                    return redirect('update_staff')
        return render(request, template, context)
    else:
        return redirect('signup')

@login_required
def dashboard(request):
    template = 'accounts/dashboard.html'
    context = {
        'title'         : 'Dashboard',
        'page_name'     : 'dashboard',
        'menu'          : 'dashboard',
        'menu_header'   : 'account',
        }
    return render(request, template, context)

@login_required
def account(request):
    template = 'accounts/users/account.html'
    context = {
        'title'         : 'Account Settings',
        'page_name'     : 'account_settings',
        'menu'          : 'account',
        'menu_header'   : 'account',
        }
    return render(request, template, context)

@login_required
def profile(request):
    template = 'accounts/profile.html'
    context = {
        'title'         : 'Profile',
        'page_name'     : 'profile',
        'menu'          : 'profile',
        'menu_header'   : 'account',
        }
    return render(request, template, context)

@login_required
def userUpdateView(request):
    form = UserUpdateForm(request.POST or None, instance=request.user)
    template = 'root/form.html'
    context = {
        'title'         : 'Edit Profile',
        'form'          : form,
        'page_name'     : 'edit_profile',
        'menu'          : 'profile',
        'menu_header'   : 'account',
        # Form properties
        'extend_file'   : 'account/base.html',
        'header'        : 'Edit Account Information',
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
            return redirect('user_account')
    return render(request, template, context)

@login_required
def confirm_delete_account(request):
    # template    = 'accounts/users/delete_account.html'
    context     = {
                'title'         : 'Delete Account',
                'page_name'     : 'delete_account',
                'menu'          : 'account',
                'menu_header'   : 'account',
                }
    template        = 'root/confirm_delete.html'
    context         = {
                    'title'         : 'Delete Account',
                    'page_name'     : 'delete_account',
                    # template options
                    'extends_file'  : 'accounts/base.html',
                    'content'       : 'You are deleting your Account',
                    'warning_list'  : [
                        'Your saved progress will also be deleted',
                    ],
                    'delete_url'    : 'delete_account',
                    'no_url'        : 'user_account',
                    'delete_text'   : 'Remove',
                    }
    return render(request, template, context)

@login_required
def delete_account(request):
    user = request.user
    user.delete()
    messages.success(request, "Account deleted successfully!")
    return redirect('signup')


# Used default view in urls.py
# 1. LoginView
# 2. LogoutView
# 3. PasswordChangeView
# 4. PasswordChangeDoneView 
