from django.urls import path
from . import views

urlpatterns = [
    # Controller url
    path('', views.applicant_list, name='applicant_list'),
    path('<int:applicant_id>', views.show_applicant, name='show_applicant'),
    path('<int:applicant_id>/edit/', views.edit_applicant, name='edit_applicant'),
    path('<int:applicant_id>/verify/', views.verifyApplication, name='verify_applicant'),
    path('<int:applicant_id>/confirm-reject/', views.confirm_reject_applicant, name='confirm_reject_applicant'),
    path('<int:applicant_id>/reject/', views.reject_applicant, name='reject_applicant'),
    path('<int:applicant_id>/change-image/', views.change_applicant_image, name='change_applicant_image'),

    # Applicant url
    path('view-form/', views.viewApplication, name='applicant_view_application'),
    path('edit-form/', views.editApplication, name='applicant_edit_form'),
    path('verify-form/<int:applicant_id>/', views.verifyApplication, name='verify-form'),
    path('update-image/', views.updateProfilePicture, name='applicant-image'),
    path('confirm-delete-form/', views.confirmDeleteApplication, name='confirm-delete-form'),
    path('delete-form/', views.deleteApplication, name='delete-form'),
    path('profile/', views.applicantProfile, name='applicant-profile'),
    path('logout/', views.logout, name='applicant-logout'),
    
]
