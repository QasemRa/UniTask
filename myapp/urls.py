from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login'),
    path('student/', views.StudentDashboardView.as_view(), name='student'),
    path('student/upload/', views.StudentUploadView.as_view(), name='student_upload'),
    path('student/subjects/', views.StudentSubjectsView.as_view(), name='student_subjects'),
    path('student/submissions/', views.StudentSubmissionsView.as_view(), name='student_submissions'),
    path('doctor/', views.DoctorView.as_view(), name='doctor'),
    path('doctor/dashboard/', views.DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('doctor/subjects/', views.DoctorSubjectsView.as_view(), name='doctor_subjects'),
    path('doctor/submissions/', views.DoctorSubmissionsView.as_view(), name='doctor_submissions'),
    path('doctor/plagiarism/', views.DoctorPlagiarismView.as_view(), name='doctor_plagiarism'),
    path('doctor/pdf-compare/', views.PDFCompareView.as_view(), name='pdf_compare'),
    path('doctor/select-subject/', views.DoctorSubjectSelectView.as_view(), name='doctor_subject_select'),
    path('doctor/subject/<int:subject_id>/', views.DoctorSubjectDetailView.as_view(), name='doctor_subject_detail'),
    path('doctor/subject/<int:subject_id>/students/', views.DoctorSubjectStudentsView.as_view(), name='doctor_subject_students'),
    path('doctor/subject/<int:subject_id>/submissions/', views.DoctorSubjectSubmissionsView.as_view(), name='doctor_subject_submissions'),
    path('doctor/subject/<int:subject_id>/plagiarism/', views.DoctorSubjectPlagiarismView.as_view(), name='doctor_subject_plagiarism'),
    path('admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/add-doctor/', views.AdminAddDoctorView.as_view(), name='admin_add_doctor'),
    path('admin/add-student/', views.AdminAddStudentView.as_view(), name='admin_add_student'),
    path('admin/assign-subjects/', views.AdminAssignSubjectsView.as_view(), name='admin_assign_subjects'),
    path('admin/enroll-students/', views.AdminEnrollStudentsView.as_view(), name='admin_enroll_students'),
    path('admin/subject/<int:subject_id>/students/', views.AdminSubjectStudentsView.as_view(), name='admin_subject_students'),
    path('admin/manage-users/', views.AdminManageUsersView.as_view(), name='admin_manage_users'),
    path('logout/', LogoutView.as_view(http_method_names=['get', 'post'], template_name='registration/logged_out.html'), name='logout'),
]
