from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from .forms import UploadForm
from .models import Submission, Profile, Enrollment, Subject
from .utils import extract_text_from_pdf, compute_similarity
from django.conf import settings
import os

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        try:
            profile = user.profile
            if profile.role == 'student':
                return '/student/'
            elif profile.role == 'doctor':
                return '/doctor/'
        except Profile.DoesNotExist:
            messages.error(self.request, 'الملف الشخصي غير موجود. يرجى الاتصال بالإدارة.')
            return '/'
        return '/'


@method_decorator(login_required, name='dispatch')
class StudentView(View):
    def get(self, request):
        # Check if user is a student
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'student':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        # Get enrolled subjects for this student
        enrollments = Enrollment.objects.filter(
            student=request.user
        ).select_related('subject', 'subject__doctor')
        
        # Get submissions for this student
        submissions = Submission.objects.filter(
            student=request.user
        ).select_related('subject').order_by('-upload_date')
        
        # Create form with user context
        form = UploadForm(user=request.user)
        
        # Organize data by subject
        subjects_data = []
        for enrollment in enrollments:
            subject = enrollment.subject
            subject_submissions = submissions.filter(subject=subject)
            
            subjects_data.append({
                'subject': subject,
                'doctor': subject.doctor,
                'total_submissions': subject_submissions.count(),
                'submissions': subject_submissions
            })
        
        context = {
            'form': form,
            'subjects_data': subjects_data,
            'enrollments': enrollments,
            'submissions': submissions,
            'total_subjects': enrollments.count(),
            'total_submissions': submissions.count()
        }
        
        return render(request, 'myapp/student.html', context)

    def post(self, request):
        # Check if user is a student
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'student':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        form = UploadForm(request.POST, request.FILES, user=request.user)
        
        if form.is_valid():
            # Check if student is enrolled in the selected subject
            subject = form.cleaned_data['subject']
            is_enrolled = Enrollment.objects.filter(
                student=request.user,
                subject=subject
            ).exists()
            
            if not is_enrolled:
                messages.error(request, 'أنت غير مسجل في هذه المادة.')
                return redirect('/student/')
            
            # Create submission
            submission = form.save(commit=False)
            submission.student = request.user
            submission.save()
            
            # Extract text from PDF
            try:
                file_path = os.path.join(settings.MEDIA_ROOT, submission.file.name)
                submission.text = extract_text_from_pdf(file_path)
                submission.save()
            except Exception as e:
                messages.warning(request, f'تم رفع الملف بنجاح، لكن فشل استخراج النص: {str(e)}')
            
            messages.success(request, f'تم رفع الواجب بنجاح لمادة {subject.name}!')
            return redirect('/student/')
        
        # If form is invalid, re-render with errors
        enrollments = Enrollment.objects.filter(
            student=request.user
        ).select_related('subject', 'subject__doctor')
        
        submissions = Submission.objects.filter(
            student=request.user
        ).select_related('subject').order_by('-upload_date')
        
        subjects_data = []
        for enrollment in enrollments:
            subject = enrollment.subject
            subject_submissions = submissions.filter(subject=subject)
            
            subjects_data.append({
                'subject': subject,
                'doctor': subject.doctor,
                'total_submissions': subject_submissions.count(),
                'submissions': subject_submissions
            })
        
        context = {
            'form': form,
            'subjects_data': subjects_data,
            'enrollments': enrollments,
            'submissions': submissions,
            'total_subjects': enrollments.count(),
            'total_submissions': submissions.count()
        }
        
        return render(request, 'myapp/student.html', context)


@method_decorator(login_required, name='dispatch')
class DoctorView(View):
    def get(self, request):
        # Check if user is a doctor
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'doctor':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        # Get subjects assigned to this doctor
        assigned_subjects = Subject.objects.filter(
            doctor=request.user
        ).prefetch_related('enrollments', 'submissions')
        
        # Get all submissions for doctor's subjects
        submissions = Submission.objects.filter(
            subject__doctor=request.user
        ).select_related('student', 'subject').order_by('-upload_date')
        
        # Organize submissions by subject
        subjects_data = []
        all_texts = []
        all_submissions_list = []
        
        for subject in assigned_subjects:
            subject_submissions = submissions.filter(subject=subject)
            enrolled_count = subject.enrollments.count()
            
            subjects_data.append({
                'subject': subject,
                'submissions_count': subject_submissions.count(),
                'enrolled_count': enrolled_count,
                'submissions': subject_submissions
            })
            
            # Collect texts for plagiarism detection
            for sub in subject_submissions:
                if sub.text:
                    all_texts.append(sub.text)
                    all_submissions_list.append(sub)
        
        # Compute plagiarism similarities
        similarities = []
        if len(all_texts) >= 2:
            try:
                similarities = compute_similarity(all_texts)
                # Add student names to similarities
                for sim in similarities:
                    if sim['text1_index'] < len(all_submissions_list) and sim['text2_index'] < len(all_submissions_list):
                        sim['student_a'] = all_submissions_list[sim['text1_index']].student.username
                        sim['student_b'] = all_submissions_list[sim['text2_index']].student.username
                        sim['subject'] = all_submissions_list[sim['text1_index']].subject.name
            except Exception as e:
                messages.warning(request, f'فشل حساب التشابه: {str(e)}')
        
        # Count high similarity cases (>70%)
        high_similarity_count = sum(1 for sim in similarities if sim.get('similarity', 0) > 70)
        
        # Get unique students count
        unique_students = submissions.values('student').distinct().count()
        
        context = {
            'assigned_subjects': assigned_subjects,
            'subjects_data': subjects_data,
            'submissions': submissions,
            'similarities': similarities,
            'total_subjects': assigned_subjects.count(),
            'total_submissions': submissions.count(),
            'unique_students': unique_students,
            'high_similarity_count': high_similarity_count
        }
        
        return render(request, 'myapp/doctor.html', context)
