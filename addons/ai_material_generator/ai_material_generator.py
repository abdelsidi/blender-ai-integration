import bpy
import json
import os
from datetime import datetime

class AIMaterialGenerator:
    """إضافة AI Material Generator"""
    
    def __init__(self):
        self.api_key = ""
        self.available_models = ["dalle", "stable_diffusion", "midjourney"]
        self.current_model = "stable_diffusion"
        self.materials_cache = {}
    
    def get_material_from_ai(self, prompt, style="realistic"):
        """الحصول على مادة من AI"""
        cache_key = f"{prompt}_{style}"
        if cache_key in self.materials_cache:
            return self.materials_cache[cache_key]
        
        material_data = self.generate_material_with_ai(prompt, style)
        self.materials_cache[cache_key] = material_data
        return material_data
    
    def generate_material_with_ai(self, prompt, style):
        """توليد المادة باستخدام AI"""
        if self.current_model == "stable_diffusion":
            return self.generate_with_stable_diffusion(prompt, style)
        elif self.current_model == "dalle":
            return self.generate_with_dalle(prompt, style)
        elif self.current_model == "midjourney":
            return self.generate_with_midjourney(prompt, style)
        else:
            raise ValueError(f"Unknown model: {self.current_model}")
    
    def generate_with_stable_diffusion(self, prompt, style):
        """توليد باستخدام Stable Diffusion"""
        material_data = {
            "texture_url": f"https://example.com/generated_texture_{prompt.replace(' ', '_')}.png",
            "normal_url": f"https://example.com/generated_normal_{prompt.replace(' ', '_')}.png",
            "roughness_url": f"https://example.com/generated_roughness_{prompt.replace(' ', '_')}.png",
            "metadata": {
                "prompt": prompt,
                "style": style,
                "model": "stable_diffusion",
                "timestamp": datetime.now().isoformat()
            }
        }
        return material_data
    
    def generate_with_dalle(self, prompt, style):
        """توليد باستخدام DALL-E"""
        material_data = {
            "texture_url": f"https://example.com/dalle_texture_{prompt.replace(' ', '_')}.png",
            "metadata": {
                "prompt": prompt,
                "style": style,
                "model": "dalle",
                "timestamp": datetime.now().isoformat()
            }
        }
        return material_data
    
    def generate_with_midjourney(self, prompt, style):
        """توليد باستخدام Midjourney"""
        material_data = {
            "texture_url": f"https://example.com/mj_texture_{prompt.replace(' ', '_')}.png",
            "metadata": {
                "prompt": prompt,
                "style": style,
                "model": "midjourney",
                "timestamp": datetime.now().isoformat()
            }
        }
        return material_data
    
    def apply_material_to_object(self, object_name, material_data):
        """تطبيق المادة على الكائن"""
        obj = bpy.data.objects.get(object_name)
        if not obj:
            raise ValueError(f"Object '{object_name}' not found")
        
        material = bpy.data.materials.new(
            name=f"AI_Material_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        material.use_nodes = True
        
        nodes = material.node_tree.nodes
        texture_node = nodes.new('ShaderNodeTexImage')
        texture_data = material_data.get("texture_url")
        
        if texture_data:
            texture_node.image = bpy.data.images.load(texture_data)
        
        principled_bsdf = nodes.get('Principled BSDF')
        if principled_bsdf:
            links = material.node_tree.links
            links.new(
                texture_node.outputs['Color'],
                principled_bsdf.inputs['Base Color']
            )
        
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)
        
        return material
