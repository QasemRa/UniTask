from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Subject, Enrollment, Submission

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role')
        }),
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'doctor', 'get_enrolled_count', 'created_at')
    list_filter = ('doctor', 'created_at')
    search_fields = ('name', 'description', 'doctor__username')
    
    fieldsets = (
        ('Subject Information', {
            'fields': ('name', 'description')
        }),
        ('Assignment', {
            'fields': ('doctor',),
            'description': 'Assign a doctor to this subject'
        }),
    )
    
    def get_enrolled_count(self, obj):
        return obj.enrollments.count()
    get_enrolled_count.short_description = 'Enrolled Students'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'get_doctor', 'enrolled_date')
    list_filter = ('subject', 'enrolled_date')
    search_fields = ('student__username', 'subject__name')
    autocomplete_fields = []
    
    fieldsets = (
        ('Enrollment Details', {
            'fields': ('student', 'subject'),
            'description': 'Assign a student to a subject. The student will see this subject and can submit assignments to the assigned doctor.'
        }),
    )
    
    def get_doctor(self, obj):
        return obj.subject.doctor.username if obj.subject.doctor else "No Doctor"
    get_doctor.short_description = 'Assigned Doctor'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = User.objects.filter(profile__role='student')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'get_doctor', 'file', 'upload_date')
    list_filter = ('subject', 'upload_date', 'subject__doctor')
    search_fields = ('student__username', 'subject__name')
    readonly_fields = ('upload_date', 'text')
    
    fieldsets = (
        ('Submission Information', {
            'fields': ('student', 'subject', 'file')
        }),
        ('Metadata', {
            'fields': ('upload_date', 'text'),
            'classes': ('collapse',)
        }),
    )
    
    def get_doctor(self, obj):
        return obj.subject.doctor.username if obj.subject.doctor else "No Doctor"
    get_doctor.short_description = 'Assigned Doctor'
    
    def has_add_permission(self, request):
        return False


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
