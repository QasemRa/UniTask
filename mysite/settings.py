import os
from pathlib import Path
import dj_database_url # ضروري لربط قاعدة بيانات Render

# المسار الرئيسي للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# الأمان: المفتاح السري يُقرأ من البيئة في Render أو يستخدم الافتراضي محلياً
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-m37%()gywdj11$6g-$svw%+&s5mx(hxgvkk9$blw%j5qo02u^&')

# الرفع يتطلب DEBUG = False
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# السماح لجميع الروابط بالوصول (أو حدد رابط Render الخاص بك)
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp', # تأكد من اسم الـ App الخاص بك
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # يجب أن يكون هنا لتقديم ملفات الـ Static
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls' # تأكد من اسم مجلد المشروع الأساسي

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# قاعدة البيانات: سحب إعدادات PostgreSQL من Render تلقائياً أو استخدام SQLite محلياً
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==========================================================
# إعدادات الملفات الثابتة والميديا (Static & Media)
# ==========================================================

STATIC_URL = 'static/'
# المجلد الذي سيجمع Render فيه الملفات عند تنفيذ collectstatic
STATIC_ROOT = BASE_DIR / 'staticfiles'

# تفعيل WhiteNoise لضغط وتقديم الملفات الثابتة
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# مجلد الـ Static الرئيسي في مشروعك
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# إعدادات صور الميديا
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# كود إنشاء حساب المدير تلقائياً عند التشغيل
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username='1').exists():
        User.objects.create_superuser(
            username='1',
            email='admin@example.com',
            password='1'
        )
        print("Done! Superuser '1' with password '1' created successfully.")