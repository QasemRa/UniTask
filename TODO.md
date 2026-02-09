# Student Pages Separation - TODO

## Tasks:
- [x] 1. Update views.py - Split StudentView into 4 separate views
  - [x] StudentDashboardView
  - [x] StudentUploadView  
  - [x] StudentSubjectsView
  - [x] StudentSubmissionsView
- [x] 2. Update urls.py - Add new URL patterns for each page
- [x] 3. Create student_dashboard.html template
- [x] 4. Create student_upload.html template (upload only)
- [x] 5. Create student_subjects.html template (subjects only)
- [x] 6. Create student_submissions.html template (submissions only)
- [x] 7. Update navigation links in all templates
- [x] 8. Test all pages work correctly


## Summary:
✅ تم فصل صفحة الطالب إلى 4 صفحات منفصلة:

1. **لوحة التحكم** - `/student/` - إحصائيات ونظرة عامة
2. **رفع واجب** - `/student/upload/` - صفحة خاصة برفع الواجبات فقط
3. **المواد الدراسية** - `/student/subjects/` - صفحة خاصة بالمواد المسجلة فقط
4. **واجباتي** - `/student/submissions/` - صفحة خاصة بالواجبات المرفوعة فقط

## الروابط الجديدة:
- `/student/` - لوحة التحكم الرئيسية
- `/student/upload/` - رفع واجب جديد
- `/student/subjects/` - المواد المسجلة
- `/student/submissions/` - الواجبات المرفوعة
