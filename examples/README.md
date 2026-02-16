# أمثلة الاستخدام

## مثال 1: توليد مادة باستخدام AI
```python
import bpy

# التأكد من تفعيل الإضافة
bpy.ops.preferences.addon_enable(module="ai_material_generator")

# توليد مادة جديدة
scene = bpy.context.scene
scene.ai_material_prompt = "rusty metal surface"
scene.ai_material_style = 'realistic'

# تطبيق على الكائن المحدد
bpy.ops.ai_material.generate()
bpy.ops.ai_material.apply()
```

## مثال 2: تحسين إضاءة المشهد
```python
import bpy

bpy.ops.preferences.addon_enable(module="ai_lighting")

scene = bpy.context.scene
scene.ai_lighting_style = 'dramatic'

bpy.ops.ai_lighting.analyze()
bpy.ops.ai_lighting.optimize()
```
