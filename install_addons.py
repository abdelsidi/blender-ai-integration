#!/usr/bin/env python3
"""
سكربت تثبيت إضافات Blender AI Integration
Installs all AI addons to Blender
"""

import os
import sys
import shutil
import platform

def get_blender_addons_path():
    """الحصول على مسار إضافات Blender"""
    system = platform.system()
    
    if system == "Linux":
        return os.path.expanduser("~/.config/blender/3.0/scripts/addons")
    elif system == "Darwin":  # macOS
        return os.path.expanduser("~/Library/Application Support/Blender/3.0/scripts/addons")
    elif system == "Windows":
        return os.path.expanduser("~/AppData/Roaming/Blender Foundation/Blender/3.0/scripts/addons")
    else:
        return None

def get_all_blender_versions():
    """الحصول على جميع إصدارات Blender المثبتة"""
    system = platform.system()
    paths = []
    
    if system == "Linux":
        base = os.path.expanduser("~/.config/blender/")
    elif system == "Darwin":
        base = os.path.expanduser("~/Library/Application Support/Blender/")
    elif system == "Windows":
        base = os.path.expanduser("~/AppData/Roaming/Blender Foundation/Blender/")
    else:
        return paths
    
    if os.path.exists(base):
        for version in os.listdir(base):
            addon_path = os.path.join(base, version, "scripts", "addons")
            if os.path.exists(addon_path):
                paths.append(addon_path)
    
    return paths

def install_addon(addon_name, source_dir, target_dir):
    """تثبيت إضافة واحدة"""
    source = os.path.join(source_dir, addon_name)
    target = os.path.join(target_dir, addon_name)
    
    # حذف النسخة القديمة إن وجدت
    if os.path.exists(target):
        print(f"  حذف النسخة القديمة: {addon_name}")
        shutil.rmtree(target)
    
    # نسخ الإضافة
    shutil.copytree(source, target)
    print(f"  ✓ تم تثبيت: {addon_name}")
    return True

def main():
    print("=" * 60)
    print("🎨 Blender AI Integration - Installer")
    print("=" * 60)
    
    # مسار الإضافات المصدر
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_addons_dir = os.path.join(script_dir, "addons")
    
    if not os.path.exists(source_addons_dir):
        print("❌ خطأ: لم يتم العثور على مجلد addons!")
        print(f"   المسار المتوقع: {source_addons_dir}")
        return 1
    
    # الحصول على إصدارات Blender
    blender_paths = get_all_blender_versions()
    
    if not blender_paths:
        print("⚠️  لم يتم العثور على إصدارات Blender!")
        print("   جاري استخدام المسار الافتراضي...")
        default_path = get_blender_addons_path()
        if default_path:
            blender_paths = [default_path]
    
    if not blender_paths:
        print("❌ لا يمكن العثور على مسار إضافات Blender!")
        print("\nيرجى تثبيت الإضافات يدوياً:")
        print("1. افتح Blender")
        print("2. Edit > Preferences > Add-ons > Install")
        print("3. اختر مجلد الإضافة المطلوبة")
        return 1
    
    # عرض الإصدارات المتاحة
    print("\n📁 إصدارات Blender الم found:")
    for i, path in enumerate(blender_paths, 1):
        print(f"   {i}. {path}")
    
    # اختيار الإصدار
    if len(blender_paths) == 1:
        selected_path = blender_paths[0]
    else:
        try:
            choice = int(input("\nاختر رقم الإصدار (أو 0 للخروج): "))
            if choice == 0:
                return 0
            selected_path = blender_paths[choice - 1]
        except (ValueError, IndexError):
            print("❌ اختيار غير صالح!")
            return 1
    
    print(f"\n📂 مسار التثبيت: {selected_path}")
    
    # التأكد من وجود المجلد
    os.makedirs(selected_path, exist_ok=True)
    
    # تثبيت جميع الإضافات
    print("\n🚀 جاري تثبيت الإضافات...")
    print("-" * 60)
    
    addons = [
        "ai_material_generator",
        "ai_lighting",
        "ai_model_generator",
        "ai_animation",
        "auto_rigging_ai",
        "ai_render_optimizer",
        "ai_texture_upscaler",
        "ai_denoiser",
        "ai_pose_generator",
        "ai_scene_generator"
    ]
    
    installed = 0
    failed = 0
    
    for addon in addons:
        addon_path = os.path.join(source_addons_dir, addon)
        if os.path.exists(addon_path):
            try:
                if install_addon(addon, source_addons_dir, selected_path):
                    installed += 1
            except Exception as e:
                print(f"  ✗ فشل: {addon} - {e}")
                failed += 1
        else:
            print(f"  ⚠️  لم يتم العثور: {addon}")
            failed += 1
    
    print("-" * 60)
    print(f"\n✅ تم بنجاح: {installed} إضافة")
    if failed > 0:
        print(f"⚠️  فشل: {failed} إضافة")
    
    print("\n📝 الخطوات التالية:")
    print("   1. افتح Blender")
    print("   2. اذهب إلى Edit > Preferences > Add-ons")
    print("   3. ابحث عن 'AI' في قائمة الإضافات")
    print("   4. فعّل الإضافات المطلوبة")
    print("\n💡 ملاحظة: قد تحتاج إلى إعادة تشغيل Blender")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
