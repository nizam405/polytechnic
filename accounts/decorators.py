from functools import wraps
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect
from django.shortcuts import redirect
# from .models import Applicant
# from accounts.models import Student
# from django.contrib import messages

def controller_required(function):
    @wraps(function)
    @login_required
    def wrap(request, *args, **kwargs):
        if request.user.is_staff and request.user.staffprofile.staff.role == 'Controller':
            return function(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrap