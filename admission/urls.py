from django.urls import path
from . import views

urlpatterns = [
    path('', views.admission, name='admission'),
    path('admission-form1/', views.admissionForm1, name='admission-form1'),
    path('admission-form2/', views.admissionForm2, name='admission-form2'),
    path('admission-form3/', views.admissionForm3, name='admission-form3'),
    path('admission-form/', views.admissionForm, name='admission-form'),
    path('admission-form-min/', views.admissionFormMin, name='admission-form-min'),
    path('application-done/', views.applicationDone, name='application-done'),
]
