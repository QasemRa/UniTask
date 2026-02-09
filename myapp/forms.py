from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Submission, Enrollment

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

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
            enrolled_subjects = Enrollment.objects.filter(
                student=user
            ).select_related('subject').values_list('subject', 'subject__name')
            
            self.fields['subject'].queryset = Submission._meta.get_field('subject').related_model.objects.filter(
                id__in=[subj[0] for subj in enrolled_subjects]
            )
            
            self.fields['subject'].widget.choices = [('', '--- اختر المادة ---')] + [
                (subj[0], subj[1]) for subj in enrolled_subjects
            ]
        else:
            self.fields['subject'].queryset = Submission._meta.get_field('subject').related_model.objects.none()

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.lower().endswith('.pdf'):
                raise forms.ValidationError('يُسمح فقط بملفات PDF.')
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('حجم الملف يجب أن يكون أقل من 10 ميجابايت.')
        return file


class PDFCompareForm(forms.Form):
    pdf_files = forms.FileField(
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf',
            'multiple': True,
            'required': True
        }),
        label="اختر ملفات PDF للمقارنة"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pdf_files'].required = True
    
    def clean_pdf_files(self):
        files = self.files.getlist('pdf_files')
        if len(files) < 2:
            raise forms.ValidationError('يجب اختيار ملفين PDF على الأقل للمقارنة.')
        
        for file in files:
            if not file.name.lower().endswith('.pdf'):
                raise forms.ValidationError(f'الملف {file.name} ليس ملف PDF صالح.')
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError(f'حجم الملف {file.name} يجب أن يكون أقل من 10 ميجابايت.')
        
        return files
