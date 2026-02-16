"""
Material Utility Functions
"""
import bpy
import os
from typing import List, Dict, Optional

class MaterialUtils:
    """أدوات مساعدة للمواد"""
    
    PRESETS = {
        "metal": {
            "base_color": (0.8, 0.8, 0.8, 1.0),
            "metallic": 1.0,
            "roughness": 0.3,
            "specular": 0.5,
        },
        "wood": {
            "base_color": (0.4, 0.25, 0.1, 1.0),
            "metallic": 0.0,
            "roughness": 0.6,
            "specular": 0.1,
        },
        "plastic": {
            "base_color": (0.8, 0.2, 0.2, 1.0),
            "metallic": 0.0,
            "roughness": 0.1,
            "specular": 0.5,
        },
        "glass": {
            "base_color": (1.0, 1.0, 1.0, 1.0),
            "metallic": 0.0,
            "roughness": 0.0,
            "specular": 0.5,
            "transmission": 1.0,
            "ior": 1.45,
        },
        "fabric": {
            "base_color": (0.6, 0.3, 0.3, 1.0),
            "metallic": 0.0,
            "roughness": 0.9,
            "specular": 0.1,
        },
        "stone": {
            "base_color": (0.5, 0.5, 0.5, 1.0),
            "metallic": 0.0,
            "roughness": 0.8,
            "specular": 0.2,
        },
    }
    
    @classmethod
    def create_material(cls, name: str, preset: str = "plastic") -> bpy.types.Material:
        """
        إنشاء مادة جديدة باستخدام preset
        
        Args:
            name: اسم المادة
            preset: نوع المادة المسبقة
            
        Returns:
            المادة المنشأة
        """
        material = bpy.data.materials.new(name=name)
        material.use_nodes = True
        
        # الحصول على المعلومات المسبقة
        preset_data = cls.PRESETS.get(preset, cls.PRESETS["plastic"])
        
        # تعيين الخصائص
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            for key, value in preset_data.items():
                if hasattr(bsdf.inputs, key):
                    bsdf.inputs[key].default_value = value
        
        return material
    
    @classmethod
    def apply_texture_maps(cls, material: bpy.types.Material, 
                          maps: Dict[str, str]) -> None:
        """
        تطبيق خرائط النسيج على المادة
        
        Args:
            material: المادة المستهدفة
            maps: قاموس الخرائط (base_color, normal, roughness, metallic)
        """
        if not material.use_nodes:
            material.use_nodes = True
        
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        
        # الحصول على Principled BSDF
        bsdf = nodes.get("Principled BSDF")
        if not bsdf:
            return
        
        # تطبيق Base Color
        if "base_color" in maps and os.path.exists(maps["base_color"]):
            tex_image = nodes.new(type='ShaderNodeTexImage')
            tex_image.image = bpy.data.images.load(maps["base_color"])
            tex_image.location = (-400, 300)
            
            links.new(tex_image.outputs['Color'], bsdf.inputs['Base Color'])
        
        # تطبيق Normal Map
        if "normal" in maps and os.path.exists(maps["normal"]):
            normal_node = nodes.new(type='ShaderNodeNormalMap')
            normal_node.location = (-200, -200)
            
            tex_normal = nodes.new(type='ShaderNodeTexImage')
            tex_normal.image = bpy.data.images.load(maps["normal"])
            tex_normal.image.colorspace_settings.name = 'Non-Color'
            tex_normal.location = (-400, -200)
            
            links.new(tex_normal.outputs['Color'], normal_node.inputs['Color'])
            links.new(normal_node.outputs['Normal'], bsdf.inputs['Normal'])
        
        # تطبيق Roughness Map
        if "roughness" in maps and os.path.exists(maps["roughness"]):
            tex_roughness = nodes.new(type='ShaderNodeTexImage')
            tex_roughness.image = bpy.data.images.load(maps["roughness"])
            tex_roughness.image.colorspace_settings.name = 'Non-Color'
            tex_roughness.location = (-400, 0)
            
            links.new(tex_roughness.outputs['Color'], bsdf.inputs['Roughness'])
        
        # تطبيق Metallic Map
        if "metallic" in maps and os.path.exists(maps["metallic"]):
            tex_metallic = nodes.new(type='ShaderNodeTexImage')
            tex_metallic.image = bpy.data.images.load(maps["metallic"])
            tex_metallic.image.colorspace_settings.name = 'Non-Color'
            tex_metallic.location = (-400, -400)
            
            links.new(tex_metallic.outputs['Color'], bsdf.inputs['Metallic'])
    
    @classmethod
    def get_material_info(cls, material: bpy.types.Material) -> Dict:
        """
        الحصول على معلومات المادة
        
        Args:
            material: المادة
            
        Returns:
            قاموس بالمعلومات
        """
        info = {
            "name": material.name,
            "use_nodes": material.use_nodes,
            "nodes_count": len(material.node_tree.nodes) if material.use_nodes else 0,
        }
        
        if material.use_nodes:
            bsdf = material.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                info["base_color"] = tuple(bsdf.inputs["Base Color"].default_value)
                info["metallic"] = bsdf.inputs["Metallic"].default_value
                info["roughness"] = bsdf.inputs["Roughness"].default_value
        
        return info
    
    @classmethod
    def export_material_gltf(cls, material: bpy.types.Material, filepath: str) -> bool:
        """
        تصدير المادة بتنسيق glTF
        
        Args:
            material: المادة للتصدير
            filepath: مسار الملف
            
        Returns:
            True إذا نجح التصدير
        """
        try:
            # إنشاء كائن مؤقت
            temp_mesh = bpy.data.meshes.new("TempMesh")
            temp_obj = bpy.data.objects.new("TempObj", temp_mesh)
            temp_obj.data.materials.append(material)
            
            # التصدير
            bpy.context.collection.objects.link(temp_obj)
            
            bpy.ops.export_scene.gltf(
                filepath=filepath,
                use_selection=True,
                export_materials='EXPORT'
            )
            
            # التنظيف
            bpy.context.collection.objects.unlink(temp_obj)
            bpy.data.objects.remove(temp_obj)
            bpy.data.meshes.remove(temp_mesh)
            
            return True
            
        except Exception as e:
            print(f"Error exporting material: {e}")
            return False
    
    @staticmethod
    def set_uv_projection(obj: bpy.types.Object, projection_type: str = "CUBE"):
        """
        تعيين نوع الإسقاط UV
        
        Args:
            obj: الكائن
            projection_type: نوع الإسقاط (CUBE, SPHERE, CYLINDER)
        """
        if obj.type != 'MESH':
            return
        
        # التأكد من وجود UV Map
        if not obj.data.uv_layers:
            obj.data.uv_layers.new()
        
        # تعيين الإسقاط
        for mat_slot in obj.material_slots:
            if mat_slot.material and mat_slot.material.use_nodes:
                nodes = mat_slot.material.node_tree.nodes
                for node in nodes:
                    if node.type == 'TEX_IMAGE':
                        # يمكن إضافة Mapping node هنا
                        pass

def register():
    pass

def unregister():
    pass
