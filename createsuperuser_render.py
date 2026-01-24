import os
import django
from django.contrib.auth import get_user_model

# تأكد إن 'mysite' هو اسم الفولدر اللي بيه ملف settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

User = get_user_model()
username = '1'
password = '1' # هذا الرمز مالتك، تكدر تغيره

user, created = User.objects.get_or_create(username=username)
user.set_password(password) # هاي الخطوة تضمن إن الرمز يصير YourPassword123 حتى لو الحساب قديم
user.is_superuser = True
user.is_staff = True
user.save()

if created:
    print("Superuser created successfully!")
else:
    print("Superuser password updated successfully!")