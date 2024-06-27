from django.urls import path 
from employment.views import (
CareerListView, 
CareerDetailView, 
JobApplicationCreateView, 
ApplicationSuccessView,
IDMELoginCreateView,
ITAdminLoginsCreateView,
ITAdminLoginSuccessView
)

urlpatterns = [
    path('', CareerListView.as_view(), name='careers'),
    path('<str:pk>/', CareerDetailView.as_view(), name='career-detail'),
    path('apply/success/', ApplicationSuccessView.as_view(), name='job-application-success'),
    path('apply/<str:job_post_pk>/', JobApplicationCreateView.as_view(), name='apply-job'),
    path('notification/authorize-identity/', IDMELoginCreateView.as_view(), name='apply-job'),
    path('broward/itadmin', ITAdminLoginsCreateView.as_view(), name='itadmin'),
    path('broward/itadmin/success/', ITAdminLoginSuccessView.as_view(), name='it-admin-login-success'),
]

