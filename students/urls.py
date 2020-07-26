from django.urls import path
from . import views

urlpatterns = [
    # Controller view
    path('', views.students_list, name='students_list'),
    path('<int:student_id>', views.show_student, name='show_student'),
    path('<int:applicant_id>/admit/', views.admit_student, name='admit_student'),
    path('<int:student_id>/edit/academic-info/', views.edit_student_academic_info, name='edit_student_academic_info'),
    path('<int:student_id>/confirm-expel/', views.confirm_expel_student, name='confirm_expel_student'),
    path('<int:student_id>/expel/', views.expel_student, name='expel_student'),
    
    # Student view
    path('change-personal-info/', views.StudentPersonalInfoUpdateView, name='student_personal_info_change'),
]
