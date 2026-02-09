import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from myapp.models import Profile

# Create or get admin user
try:
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@university.edu',
        password='Admin123!@#'
    )
    
    # Create admin profile
    Profile.objects.create(
        user=admin_user,
        role='admin',
        phone='07123456789',
        department='IT Department',
        is_active=True
    )
    
    print("Admin user created successfully!")
    print("Username: admin")
    print("Password: Admin123!@#")
    
except Exception as e:
    print(f"Error: {e}")
    print("Admin user might already exist.")
