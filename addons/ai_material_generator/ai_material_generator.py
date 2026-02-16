import bpy
import json
import os
from datetime import datetime

ADDON_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
PRESETS_DIR = os.path.join(ADDON_DIR, "..", "..", "assets", "presets")

class AIMaterialGenerator:
    """AI Material Generator with JSON presets"""
    
    def __init__(self):
        self.materials_cache = {}
    
    def load_material_from_json(self, material_id):
        """Load material data from JSON preset"""
        json_path = os.path.join(PRESETS_DIR, "materials.json")
        
        if not os.path.exists(json_path):
            return None
        
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        for mat in data.get('materials', []):
            if mat['id'] == material_id or mat['name'].lower() == material_id.lower():
                return mat
        
        return None
    
    def create_material_from_preset(self, preset_id, name=None):
        """Create Blender material from JSON preset"""
        preset = self.load_material_from_json(preset_id)
        
        if not preset:
            # Create default material
            return self.create_default_material(name or "AI_Material")
        
        # Create material
        mat_name = name or f"AI_{preset['name']}"
        material = bpy.data.materials.new(name=mat_name)
        material.use_nodes = True
        
        # Clear nodes
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        nodes.clear()
        
        # Create principled BSDF
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.location = (0, 0)
        
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Apply preset values
        color = preset.get('color', [0.5, 0.5, 0.5, 1.0])
        principled.inputs['Base Color'].default_value = color
        
        if 'roughness' in preset:
            principled.inputs['Roughness'].default_value = preset['roughness']
        
        if 'metallic' in preset:
            principled.inputs['Metallic'].default_value = preset['metallic']
        
        # Add texture if available
        if 'texture_url' in preset:
            self.add_texture_node(material, preset['texture_url'])
        
        return material
    
    def create_default_material(self, name="AI_Material"):
        """Create a default material"""
        material = bpy.data.materials.new(name=name)
        material.use_nodes = True
        
        nodes = material.node_tree.nodes
        principled = nodes.get("Principled BSDF")
        
        if principled:
            principled.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)
            principled.inputs['Roughness'].default_value = 0.5
        
        return material
    
    def create_material_from_prompt(self, prompt, material_type="standard"):
        """Create material based on text prompt"""
        prompt_lower = prompt.lower()
        
        # Detect material type from prompt
        if any(word in prompt_lower for word in ['metal', 'steel', 'iron', 'gold', 'silver', 'copper']):
            return self.create_metal_material(prompt)
        elif any(word in prompt_lower for word in ['wood', 'wooden', 'oak', 'pine']):
            return self.create_wood_material(prompt)
        elif any(word in prompt_lower for word in ['glass', 'crystal', 'transparent']):
            return self.create_glass_material(prompt)
        elif any(word in prompt_lower for word in ['plastic', 'rubber', 'silicone']):
            return self.create_plastic_material(prompt)
        elif any(word in prompt_lower for word in ['fabric', 'cloth', 'cotton', 'silk']):
            return self.create_fabric_material(prompt)
        else:
            return self.create_default_material(f"AI_{prompt[:15]}")
    
    def create_metal_material(self, prompt):
        """Create metal material"""
        material = bpy.data.materials.new(name=f"AI_Metal_{prompt[:10]}")
        material.use_nodes = True
        
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        nodes.clear()
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.location = (0, 0)
        
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Detect color
        prompt_lower = prompt.lower()
        if 'gold' in prompt_lower or 'golden' in prompt_lower:
            principled.inputs['Base Color'].default_value = (1.0, 0.84, 0.0, 1.0)
        elif 'silver' in prompt_lower:
            principled.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)
        elif 'copper' in prompt_lower or 'bronze' in prompt_lower:
            principled.inputs['Base Color'].default_value = (0.8, 0.5, 0.2, 1.0)
        elif 'red' in prompt_lower:
            principled.inputs['Base Color'].default_value = (0.8, 0.1, 0.1, 1.0)
        elif 'blue' in prompt_lower:
            principled.inputs['Base Color'].default_value = (0.1, 0.3, 0.8, 1.0)
        else:
            principled.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1.0)
        
        principled.inputs['Metallic'].default_value = 1.0
        principled.inputs['Roughness'].default_value = 0.2
        
        return material
    
    def create_wood_material(self, prompt):
        """Create wood material"""
        material = bpy.data.materials.new(name=f"AI_Wood_{prompt[:10]}")
        material.use_nodes = True
        
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        nodes.clear()
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (400, 0)
        
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.location = (0, 0)
        
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Wood color
        prompt_lower = prompt.lower()
        if 'dark' in prompt_lower or 'walnut' in prompt_lower:
            principled.inputs['Base Color'].default_value = (0.2, 0.1, 0.05, 1.0)
        elif 'light' in prompt_lower or 'pine' in prompt_lower:
            principled.inputs['Base Color'].default_value = (0.8, 0.7, 0.5, 1.0)
        else:
            principled.inputs['Base Color'].default_value = (0.4, 0.25, 0.1, 1.0)
        
        principled.inputs['Roughness'].default_value = 0.7
        
        # Add noise texture for wood grain
        noise = nodes.new(type='ShaderNodeTexNoise')
        noise.location = (-300, 200)
        noise.inputs['Scale'].default_value = 50.0
        
        colorramp = nodes.new(type='ShaderNodeValToRGB')
        colorramp.location = (-100, 200)
        
        links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
        
        # Mix with base color
        mix = nodes.new(type='ShaderNodeMixRGB')
        mix.location = (200, 100)
        mix.blend_type = 'MULTIPLY'
        mix.inputs['Fac'].default_value = 0.3
        
        links.new(colorramp.outputs['Color'], mix.inputs['Color1'])
        # Connect to base color would require rerouting
        
        return material
    
    def create_plastic_material(self, prompt):
        """Create plastic material"""
        material = bpy.data.materials.new(name=f"AI_Plastic_{prompt[:10]}")
        material.use_nodes = True
        
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        nodes.clear()
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.location = (0, 0)
        
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Detect color
        prompt_lower = prompt.lower()
        if 'red' in prompt_lower:
            principled.inputs['Base Color'].default_value = (0.8, 0.1, 0.1, 1.0)
        elif 'blue' in prompt_lower:
            principled.inputs['Base Color'].default_value = (0.1, 0.4, 0.8, 1.0)
        elif 'green' in prompt_lower:
            principled.inputs['Base Color'].default_value = (0.1, 0.7, 0.2, 1.0)
        elif 'yellow' in prompt_lower:
            principled.inputs['Base Color'].default_value = (0.9, 0.8, 0.1, 1.0)
        elif 'black' in prompt_lower:
            principled.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0)
        elif 'white' in prompt_lower:
            principled.inputs['Base Color'].default_value = (0.95, 0.95, 0.95, 1.0)
        else:
            principled.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)
        
        principled.inputs['Roughness'].default_value = 0.1
        principled.inputs['Specular'].default_value = 0.5
        
        return material
    
    def create_glass_material(self, prompt):
        """Create glass material"""
        material = bpy.data.materials.new(name=f"AI_Glass_{prompt[:10]}")
        material.use_nodes = True
        
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        nodes.clear()
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.location = (0, 0)
        
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Glass settings
        principled.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
        principled.inputs['Roughness'].default_value = 0.0
        principled.inputs['Transmission'].default_value = 0.95
        principled.inputs['IOR'].default_value = 1.45
        
        return material
    
    def create_fabric_material(self, prompt):
        """Create fabric material"""
        material = bpy.data.materials.new(name=f"AI_Fabric_{prompt[:10]}")
        material.use_nodes = True
        
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        nodes.clear()
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.location = (0, 0)
        
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        principled.inputs['Base Color'].default_value = (0.5, 0.5, 0.5, 1.0)
        principled.inputs['Roughness'].default_value = 0.9
        
        return material
    
    def add_texture_node(self, material, image_path):
        """Add texture node to material"""
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        
        # Load image
        try:
            img = bpy.data.images.load(image_path)
            
            tex_image = nodes.new(type='ShaderNodeTexImage')
            tex_image.image = img
            tex_image.location = (-300, 0)
            
            principled = nodes.get("Principled BSDF")
            if principled:
                links.new(tex_image.outputs['Color'], principled.inputs['Base Color'])
        except:
            pass
    
    def apply_material_to_object(self, obj, material):
        """Apply material to object"""
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)
        
        return material
