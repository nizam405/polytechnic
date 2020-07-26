from django.urls import path
from . import views

urlpatterns = [
    path('', views.allNotices, name='all-notices'),
    path('<int:notice_id>', views.view_notice, name='view-notice'),
]
