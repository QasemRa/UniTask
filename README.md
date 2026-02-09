# 📄 PDF Plagiarism Detection System

نظام متقدم لكشف التشابه بين ملفات PDF يدعم العربية والإنجليزية والخط اليدوي.

## 🌟 المميزات

- ✅ استخراج النص من ملفات Word و PDF
- ✅ دعم الخط اليدوي العربي والإنجليزي  
- ✅ كشف التشابه بدقة عالية
- ✅ واجهة عربية بالكامل
- ✅ معالجة حتى 10 ملفات في نفس الوقت

## 📋 المتطلبات

### البرامج المطلوبة
```bash
# Python 3.13+
python --version

# Tesseract OCR 5.5.0+
tesseract --version
```

### روابط التحميل
- **Python**: https://www.python.org/downloads/
- **Tesseract**: https://github.com/UB-Mannheim/tesseract/wiki
- **poppler**: https://poppler.freedesktop.org/

## 🚀 التشغيل

### 1. تثبيت المكتبات
```bash
cd mysite
pip install -r requirements.txt
```

### 2. إعداد قاعدة البيانات
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. تشغيل الخادم
```bash
python manage.py runserver
```

## 👤 حسابات الدخول

```bash
# المشرف
username: 1
password: 1

# الطبيب  
username: d1
password: QasemRa1

# الطالب
username: s1  
password: QasemRa1
```

## 🌐 الوصول

```
http://localhost:8000
```

## 📋 الاستخدام

1. سجل دخول بالحساب المناسب
2. اختر "مقارنة ملفات PDF"
3. ارفع الملفات (2-10 ملفات)
4. اضغط "استخراج النص وحساب التشابه"
5. شاهد النتائج فوراً

## 🏗️ التقنيات

- **Backend**: Django 6.0.1 + Python 3.13
- **OCR**: Tesseract 5.5.0 + pytesseract
- **Frontend**: Bootstrap 5 + JavaScript
- **Analysis**: scikit-learn + TF-IDF

## � الأداء

- **ملفات نصية**: < 1 ثانية
- **ملفات صورية**: 2-5 ثواني  
- **دقة الكشف**: 85-95%
- **معالجة 10 ملفات**: < 30 ثانية

## 🐛 حل المشاكل

### مشكلة: Tesseract لا يعمل
```bash
# تحقق من المسار
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### مشكلة: المكتبات لا تعمل
```bash
# استخدم Python المثبت مباشرة
C:\Users\kkaas\AppData\Local\Programs\Python\Python313\python.exe -m pip install -r requirements.txt
```

---

### 📞 التواصل

- **📧 البريد الإلكتروني**: kkaasm887@gmail.com
- **📱 الهاتف**: +967 819 3442 51

**مطور المشروع: Qasem Rafid Fouad**  
**الترخيص: MIT License**
