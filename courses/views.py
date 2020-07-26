from django.shortcuts import render
# UI
from .models import Course
courses = Course.objects.all()
# Create your views here.
def allCourses(request):
    template = 'courses/courses.html'
    context = {
        'title'     : 'Courses',
        'courses'   : courses,
        'page_name' : 'course',
    }
    return render(request, template, context)


def viewCourse(request, course_code):
    course = Course.objects.get(code = course_code)
    template = 'courses/view_course.html'
    context = {
        'title'     : course.name,
        'course'    : course,
        'page_name' : 'course',
    }
    return render(request, template, context)