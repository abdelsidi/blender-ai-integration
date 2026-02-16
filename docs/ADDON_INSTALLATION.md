# دليل تثبيت الإضافات

## المتطلبات

- Blender 3.0 أو أحدث
- Python 3.8 أو أحدث
- اتصال بالإنترنت (للخدمات السحابية)

## طرق التثبيت

### الطريقة الأولى: التثبيت اليدوي

1. قم بتنزيل الإضافات من GitHub:
```bash
git clone https://github.com/abdelsidi/blender-ai-integration.git
```

2. انسخ المجلدات إلى مجلد إضافات Blender:
```bash
cd blender-ai-integration/addons
cp -r ai_material_generator ~/.config/blender/3.0/scripts/addons/
cp -r ai_lighting ~/.config/blender/3.0/scripts/addons/
cp -r auto_rigging_ai ~/.config/blender/3.0/scripts/addons/
cp -r ai_animation ~/.config/blender/3.0/scripts/addons/
```

3. فعّل الإضافات في Blender:
   - Edit > Preferences > Add-ons
   - ابحث عن "AI"
   - فعّل الإضافات المطلوبة

### الطريقة الثانية: التثبيت من ملف ZIP

1. قم بضغط مجلد الإضافة المطلوبة
2. في Blender: Edit > Preferences > Add-ons > Install
3. اختر ملف ZIP
4. فعّل الإضافة

## التحقق من التثبيت

بعد التثبيت، يجب أن ترى:
- لوحة "AI Material Generator" في الشريط الجانبي
- لوحة "AI Lighting" في الشريط الجانبي
- قائمة "AI Tools" في View3D

## استكشاف الأخطاء

### الإضافة لا تظهر
- تأكد من تشغيل Blender كمسؤول (على Windows)
- تحقق من وجود ملف `__init__.py`
- تأكد من عدم وجود أخطاء في System Console

### مشاكل في الاستيراد
- تأكد من تثبيت Python dependencies إن وجدت
- تحقق من إصدار Blender (3.0+ مطلوب)

## دعم

للمزيد من المساعدة، تواصل معنا عبر GitHub Issues.
