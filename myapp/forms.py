from django import forms
from .models import Submission, Enrollment

class UploadForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['subject', 'file']
        widgets = {
            'subject': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
                'required': True
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Get only subjects the student is enrolled in
            enrolled_subjects = Enrollment.objects.filter(
                student=user
            ).select_related('subject').values_list('subject', 'subject__name')
            
            self.fields['subject'].queryset = Submission._meta.get_field('subject').related_model.objects.filter(
                id__in=[subj[0] for subj in enrolled_subjects]
            )
            
            # Update the widget choices
            self.fields['subject'].widget.choices = [('', '--- اختر المادة ---')] + [
                (subj[0], subj[1]) for subj in enrolled_subjects
            ]
        else:
            # If no user, show empty queryset
            self.fields['subject'].queryset = Submission._meta.get_field('subject').related_model.objects.none()

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.lower().endswith('.pdf'):
                raise forms.ValidationError('يُسمح فقط بملفات PDF.')
            # Check file size (max 10MB)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('حجم الملف يجب أن يكون أقل من 10 ميجابايت.')
        return file
