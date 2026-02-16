import bpy
import bmesh
import json
import os
from datetime import datetime
from mathutils import Vector

class AIModelGenerator:
    """مولد النماذج ثلاثية الأبعاد بالذكاء الاصطناعي"""
    
    def __init__(self):
        self.api_key = ""
        self.available_models = [
            "pointe",           # OpenAI Point-E
            "shap_e",           # OpenAI Shap-E
            "dreamfusion",      # DreamFusion
            "magic3d"           # Magic3D
        ]
        self.current_model = "shap_e"
        self.models_cache = {}
    
    def generate_model_from_text(self, prompt, style="detailed", resolution="medium"):
        """توليد نموذج 3D من نص"""
        cache_key = f"text_{prompt}_{style}_{resolution}"
        if cache_key in self.models_cache:
            return self.models_cache[cache_key]
        
        # استدعاء AI لتوليد النموذج
        model_data = self.call_ai_model(prompt, style, resolution, input_type="text")
        self.models_cache[cache_key] = model_data
        return model_data
    
    def generate_model_from_image(self, image_path, style="detailed", resolution="medium"):
        """توليد نموذج 3D من صورة"""
        cache_key = f"img_{image_path}_{style}_{resolution}"
        if cache_key in self.models_cache:
            return self.models_cache[cache_key]
        
        # معالجة الصورة واستدعاء AI
        model_data = self.call_ai_model(image_path, style, resolution, input_type="image")
        self.models_cache[cache_key] = model_data
        return model_data
    
    def call_ai_model(self, input_data, style, resolution, input_type="text"):
        """استدعاء نموذج AI"""
        # محاكاة استجابة AI (في الواقع، سيتم استدعاء API)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        model_data = {
            "name": f"AI_Model_{timestamp}",
            "input_type": input_type,
            "prompt": input_data if input_type == "text" else os.path.basename(input_data),
            "style": style,
            "resolution": resolution,
            "model_type": self.current_model,
            "timestamp": timestamp,
            "vertices_count": self.get_resolution_vertices(resolution),
            "file_format": ".obj",
            "download_url": f"https://example.com/models/{timestamp}.obj"
        }
        
        return model_data
    
    def get_resolution_vertices(self, resolution):
        """عدد الرؤوس حسب الدقة"""
        resolutions = {
            "low": 1000,
            "medium": 5000,
            "high": 20000,
            "ultra": 100000
        }
        return resolutions.get(resolution, 5000)
    
    def create_primitive_model(self, model_type="cube", name="AI_Model"):
        """إنشاء نموذج بدائي كمثال"""
        if model_type == "cube":
            bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
        elif model_type == "sphere":
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
        elif model_type == "cylinder":
            bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=(0, 0, 0))
        elif model_type == "torus":
            bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=0.25, location=(0, 0, 0))
        elif model_type == "monkey":
            bpy.ops.mesh.primitive_monkey_add(size=2, location=(0, 0, 0))
        
        obj = bpy.context.active_object
        obj.name = name
        return obj
    
    def apply_subdivision(self, obj, levels=2):
        """تطبيق تقسيم الأسطح لزيادة التفاصيل"""
        # إضافة معدل subdivision
        subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf.levels = levels
        subsurf.render_levels = levels
        
        # تطبيق المعدل
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier="Subdivision")
        
        return obj
    
    def optimize_mesh(self, obj, target_vertices=5000):
        """تحسين شبكة النموذج"""
        # الانتقال إلى وضع التحرير
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        
        # تحديد كل الرؤوس
        bpy.ops.mesh.select_all(action='SELECT')
        
        # تقليل الرؤوس إذا لزم الأمر
        current_vertices = len(obj.data.vertices)
        if current_vertices > target_vertices:
            ratio = target_vertices / current_vertices
            bpy.ops.mesh.decimate(ratio=ratio)
        
        # العودة إلى وضع الكائن
        bpy.ops.object.mode_set(mode='OBJECT')
        
        return obj
    
    def add_material(self, obj, material_type="clay"):
        """إضافة مادة للنموذج"""
        material = bpy.data.materials.new(name=f"{obj.name}_Material")
        material.use_nodes = True
        
        nodes = material.node_tree.nodes
        principled = nodes.get("Principled BSDF")
        
        if material_type == "clay":
            principled.inputs['Base Color'].default_value = (0.8, 0.6, 0.5, 1.0)
            principled.inputs['Roughness'].default_value = 0.8
        elif material_type == "metal":
            principled.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)
            principled.inputs['Metallic'].default_value = 1.0
            principled.inputs['Roughness'].default_value = 0.3
        elif material_type == "plastic":
            principled.inputs['Base Color'].default_value = (0.2, 0.5, 0.8, 1.0)
            principled.inputs['Roughness'].default_value = 0.1
        
        obj.data.materials.append(material)
        return material
