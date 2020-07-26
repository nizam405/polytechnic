from functools import wraps
# from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from applicants.models import Applicant
from students.models import Student
from django.contrib import messages

def show_profile_if_logged_in(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.session.has_key('applicant_id'):
            return redirect('applicant-profile')
            # return HttpResponseRedirect('/')
        else:
            return function(request, *args, **kwargs)
    return wrap

def applicant_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.session.has_key('applicant_id'):
            try:
                applicant = Applicant.objects.get(id=request.session['applicant_id'])
                try:
                    student = Student.objects.get(applicant=applicant)
                    messages.warning(request, "You have already admitted. Please Signup or Login to your account")
                    return redirect('applicant-logout')
                    # del request.session['applicant_id']
                    # return redirect('admission')
                except:
                    return function(request, *args, **kwargs)
            except:
                return redirect('admission')
        elif request.user.is_staff:
            return function(request, *args, **kwargs)
    return wrap