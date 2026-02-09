from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.CharField(max_length=20, blank=True, null=True)
    study_level = models.CharField(max_length=20, blank=True, null=True, 
                                choices=[('first_year', 'السنة الأولى'), ('second_year', 'السنة الثانية'), 
                                        ('third_year', 'السنة الثالثة'), ('fourth_year', 'السنة الرابعة')])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class Subject(models.Model):
    """Subject/Course model managed by admin"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    doctor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        limit_choices_to={'profile__role': 'doctor'},
        related_name='teaching_subjects'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        doctor_name = self.doctor.username if self.doctor else "No Doctor Assigned"
        return f"{self.name} - Dr. {doctor_name}"

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = ['name']


class Enrollment(models.Model):
    """Links students to subjects - managed by admin"""
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'profile__role': 'student'},
        related_name='enrollments'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrolled_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
        unique_together = ('student', 'subject')  
        ordering = ['-enrolled_date']

    def __str__(self):
        return f"{self.student.username} enrolled in {self.subject.name}"


class Submission(models.Model):
    """Student assignment submissions"""
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    file = models.FileField(upload_to='submissions/%Y/%m/%d/')
    text = models.TextField(blank=True)  
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'
        ordering = ['-upload_date']

    def __str__(self):
        return f"{self.student.username} - {self.subject.name} - {self.upload_date.strftime('%Y-%m-%d')}"

    def get_doctor(self):
        """Get the doctor assigned to this submission's subject"""
        return self.subject.doctor

    def get_subject_name(self):
        """Get the subject name"""
        return self.subject.name


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Profile)
def enroll_student_in_all_subjects(sender, instance, created, **kwargs):
    """Automatically enroll new students in all existing subjects - DISABLED"""
    # This signal is disabled to allow manual enrollment control
    pass

@receiver(post_save, sender=Subject)
def enroll_all_students_in_new_subject(sender, instance, created, **kwargs):
    """Automatically enroll all existing students in new subjects - DISABLED"""
    # This signal is disabled to allow manual enrollment control
    pass
