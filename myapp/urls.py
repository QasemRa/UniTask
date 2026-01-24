from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login'),
    path('student/', views.StudentView.as_view(), name='student'),
    path('doctor/', views.DoctorView.as_view(), name='doctor'),
    path('logout/', LogoutView.as_view(http_method_names=['get', 'post'], template_name='registration/logged_out.html'), name='logout'),
]
