from django.urls import path
from . import views

urlpatterns = [
    path('', views.allCourses, name='courses'),
    path('<course_code>/', views.viewCourse, name='view_course'),
]
