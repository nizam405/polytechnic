from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/users/login_signup.html', 
        extra_context={
            'title'         : 'Change Password',
            'page_name'     : 'login',
            # Form properties
            'submit_content': 'Login',
            }
        ), 
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='accounts/users/logout.html'), 
        name='logout'),
    path('signup/step-1/', views.signupFormView, name='signup'),
    path('signup/step-2/', views.userCreationFormView, name='user_creation_form'),
    path('account/', views.account, name='user_account'),
    path('account-setting/', views.userUpdateView, name='change_user_account'),
    path('profile/', views.profile, name='user_profile'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='root/form.html', 
        extra_context={
            'title'         : 'Change Password',
            'menu'          : 'account',
            'menu_header'   : 'account',
            # Form properties
            'extend_file'   : 'account/base.html',
            'header'        : 'Change Password',
            'column'        : '1',
            'form_layout'   : 'horizontal',
            'form_size'     : 'small',
            'submit_content': 'Save',
            'reset_content' : 'Reset',
            # 'skip_content'  : 'Skip',
            # 'skip_href'     : "/applicant/profile/",
            'button_size'   : 'sm',
            }
        ), name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/users/password_change_done.html'), 
        name='password_change_done'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('confirm_delete-account/', views.confirm_delete_account, name='confirm_delete_account'),
    
]
