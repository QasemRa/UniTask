# TODO List for Django University System Project

## 1. Modify mysite/settings.py
- Add 'myapp' to INSTALLED_APPS
- Configure MEDIA_URL and MEDIA_ROOT
- Set LOGIN_URL and LOGIN_REDIRECT_URL
- Add TEMPLATES DIRS for templates

## 2. Modify mysite/urls.py
- Include myapp.urls
- Add media serving for development

## 3. Create myapp/models.py
- Profile model (OneToOneField to User, role choices, subject)
- Submission model (ForeignKey to User, subject, file, text, upload_date)

## 4. Create myapp/forms.py
- UploadForm with subject dropdown and file field (PDF only validation)

## 5. Create myapp/utils.py
- extract_text_from_pdf function (using pypdf, pdf2image, pytesseract)
- compute_similarity function (TF-IDF + Cosine Similarity)

## 6. Create myapp/views.py
- CustomLoginView
- StudentView (dashboard with upload form and submissions list)
- DoctorView (submissions and similarities for their subject)

## 7. Create myapp/urls.py
- URL patterns for login, student/, doctor/

## 8. Modify myapp/admin.py
- Register Profile and Submission models

## 9. Create Templates
- registration/login.html
- myapp/student.html
- myapp/doctor.html

## 10. Create Static CSS
- static/css/style.css (modern design with gradients, glassmorphism, RTL support)

## 11. Install Required Packages
- pip install pypdf pdf2image pytesseract scikit-learn pillow

## 12. Run Migrations
- python manage.py makemigrations
- python manage.py migrate

## 13. Create Superuser
- python manage.py createsuperuser

## 14. Run Server
- python manage.py runserver
