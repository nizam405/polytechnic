from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.decorators import controller_required
from applicants.models import Applicant
from .models import Student, StdLink
from .forms import (
    AdmitForm, 
    StudentRegisterForm, 
    StudentAcademicInfoUpdateForm, 
    StudentPersonalInfoUpdateForm,
)
from applicants.forms import PersonalInfoForm

@controller_required
def students_list(request):
    students  = Student.objects.all()
    template    = 'students/students_list.html'
    context     = {
                'title'         : 'Students',
                'students'      : students,
                'page_name'     : 'students_list',
                'menu'          : 'students_list',
                'menu_header'   : 'academic',
                }
    return render(request, template, context)

@controller_required
def show_student(request, student_id):
    student   = Student.objects.get(id=student_id)
    template    = 'students/show_student.html'
    context     = {
                'title'         : student.applicant.name,
                'student'       : student,
                'page_name'     : 'show_student',
                'menu'          : 'students_list',
                'menu_header'   : 'academic',
                }
    return render(request, template, context)

@controller_required
def admit_student(request, applicant_id):
    applicant   = Applicant.objects.get(id=applicant_id)
    students    = Student.objects.filter(applicant__batch=applicant.batch, applicant__course=applicant.course)
    if len(students) == 0:
        class_roll = '01'
    else:
        class_roll = int(students.last().class_roll) + 1
    # print(students)
    identity    = applicant.course.short_hand + "-" + applicant.batch.session[2:4] + applicant.batch.session[-2:]
    form        = AdmitForm(request.POST or None)
    form.fields['applicant'].initial= applicant
    form.fields['semester'].initial = applicant.semester_apply
    form.fields['class_roll'].initial = class_roll
    form.fields['identity'].initial = identity

    # template    = 'root/form.html'
    template    = 'account/students/admit_edit_student.html'
    context     = {
                'title'         : 'Admit Student',
                'applicant'     : applicant,
                'page_name'     : 'admit_student',
                'menu'          : 'applicant_list',
                'menu_header'   : 'admission',
                # Form properties
                'form'          : form,
                # 'extend_file'   : 'account/base.html',
                'header'        : 'Admit Student',
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
            applicant.admitted = True
            applicant.save()
            messages.success(request, 'The student has admitted successfully')
            return redirect('students_list')
    return render(request, template, context)

@controller_required
def edit_student_academic_info(request, student_id):
    student     = Student.objects.get(id=student_id)
    form        = StudentAcademicInfoUpdateForm(request.POST or None, instance=student)
    template    = 'students/admit_edit_student.html'
    # template    = 'root/form.html'
    context     = {
                'title'         : 'Edit Student Academic Information',
                'student'       : student,
                'page_name'     : 'edit_student_academic_info',
                'menu'          : 'students_list',
                'menu_header'   : 'academic',
                # Form properties
                'form'          : form,
                'extend_file'   : 'account/base.html',
                'header'        : 'Edit Student Academic Information',
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
            messages.success(request, f'Academic info of {student.applicant.name} has updated successfully')
    return render(request, template, context)

@controller_required
def confirm_expel_student(request, student_id):
    student   = Student.objects.get(id=student_id)
    template    = 'root/confirm_delete.html'
    context     = {
                'title'         : 'Confirm expel student',
                'student'       : student,
                'page_name'     : 'confirm_expel_student',
                'menu'          : 'students_list',
                'menu_header'   : 'academic',
                # template options
                'extends_file'  : 'account/base.html',
                'content'       : f'You are expelling {student.applicant.name}',
                'warning_list'  : [
                    f'{student.applicant.name} will no longer available',
                ],
                'delete_url'    : 'expel_student',
                'no_url'        : 'show_student',
                'id'            : student_id,
                'delete_text'   : 'Expel',
                }
    return render(request, template, context)

@controller_required
def expel_student(request, student_id):
    student             = Student.objects.get(id=student_id)
    student.delete()
    applicant           = Applicant.objects.get(id=student.applicant.id)
    applicant.admitted  = False
    applicant.save()
    messages.success(request, f'{student.applicant.name} has expelled successfully')
    return redirect('students_list')

# Student view
@login_required
def StudentPersonalInfoUpdateView(request):
    applicant = request.user.stdlink.student.applicant
    form = PersonalInfoForm(request.POST or None, instance=applicant)
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
