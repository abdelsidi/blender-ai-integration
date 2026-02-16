# ملفات المساعدة

## install_all_addons.py
```python
import bpy
import os
import sys

def install_addons():
    """تثبيت جميع الإضافات"""
    addons_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(addons_dir)
    
    addons = [
        "ai_material_generator",
        "ai_lighting",
        "auto_rigging_ai",
        "ai_animation"
    ]
    
    for addon in addons:
        addon_path = os.path.join(parent_dir, "addons", addon)
        if os.path.exists(addon_path):
            bpy.ops.preferences.addon_install(filepath=addon_path)
            bpy.ops.preferences.addon_enable(module=addon)
            print(f"✅ Installed: {addon}")
        else:
            print(f"❌ Not found: {addon}")
    
    bpy.ops.wm.save_userpref()
    print("🎉 All addons installed!")

if __name__ == "__main__":
    install_addons()
```
