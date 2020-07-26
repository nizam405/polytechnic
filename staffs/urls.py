from django.urls import path
from . import views

urlpatterns = [
    # Controller view
    path('', views.staff_list, name='staff_list'),
    path('add/', views.add_staff, name='add_staff'),
    path('<int:staff_id>/view/', views.view_staff, name='view_staff'),
    path('<int:staff_id>/edit/', views.edit_staff, name='edit_staff'),
    path('<int:staff_id>/confirm-remove/', views.confirm_remove_staff, name='confirm_remove_staff'),
    path('<int:staff_id>/remove/', views.remove_staff, name='remove_staff'),
    path('<int:staff_id>/change-image/', views.change_staff_image, name='change_staff_image'),
    path('<int:staff_id>/change-personal-info/', views.change_staff_personal_info, name='change_staff_personal_info'),

    # Staff view
    path('profile/update-staff/', views.updateStaffProfile, name='update_staff'),
    path('profile-picture/', views.changeProfilePicture, name='profile_picture'),
]
