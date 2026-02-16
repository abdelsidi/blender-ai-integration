import bpy
import bmesh
import random
from mathutils import Vector, Euler
from datetime import datetime

class AIModelGenerator:
    """AI 3D Model Generator with procedural shapes"""
    
    def __init__(self):
        self.api_key = ""
        self.models_cache = {}
    
    def generate_model_from_prompt(self, prompt, style="detailed", material="clay"):
        """Generate 3D model from text prompt"""
        prompt_lower = prompt.lower()
        
        # Detect model type from prompt
        if any(word in prompt_lower for word in ['cube', 'box', 'square']):
            obj = self.create_cube()
        elif any(word in prompt_lower for word in ['sphere', 'ball', 'circle', 'round']):
            obj = self.create_sphere()
        elif any(word in prompt_lower for word in ['cylinder', 'tube', 'pipe']):
            obj = self.create_cylinder()
        elif any(word in prompt_lower for word in ['torus', 'donut', 'ring']):
            obj = self.create_torus()
        elif any(word in prompt_lower for word in ['cone', 'pyramid']):
            obj = self.create_cone()
        elif any(word in prompt_lower for word in ['monkey', 'suzanne', 'head']):
            obj = self.create_monkey()
        elif any(word in prompt_lower for word in ['tree', 'plant', 'nature']):
            obj = self.create_tree()
        elif any(word in prompt_lower for word in ['chair', 'furniture']):
            obj = self.create_chair()
        elif any(word in prompt_lower for word in ['apple', 'fruit', 'food']):
            obj = self.create_apple()
        elif any(word in prompt_lower for word in ['car', 'vehicle']):
            obj = self.create_car()
        else:
            # Default to a modified sphere
            obj = self.create_procedural_shape(prompt)
        
        # Apply material
        self.add_material(obj, material)
        
        return obj
    
    def create_cube(self, size=2):
        """Create a cube"""
        bpy.ops.mesh.primitive_cube_add(size=size, location=(0, 0, 0))
        obj = bpy.context.active_object
        obj.name = f"AI_Cube_{datetime.now().strftime('%H%M%S')}"
        return obj
    
    def create_sphere(self, radius=1):
        """Create a sphere"""
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(0, 0, 0))
        obj = bpy.context.active_object
        obj.name = f"AI_Sphere_{datetime.now().strftime('%H%M%S')}"
        return obj
    
    def create_cylinder(self, radius=1, depth=2):
        """Create a cylinder"""
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=(0, 0, 0))
        obj = bpy.context.active_object
        obj.name = f"AI_Cylinder_{datetime.now().strftime('%H%M%S')}"
        return obj
    
    def create_torus(self, major=1, minor=0.25):
        """Create a torus"""
        bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, location=(0, 0, 0))
        obj = bpy.context.active_object
        obj.name = f"AI_Torus_{datetime.now().strftime('%H%M%S')}"
        return obj
    
    def create_cone(self, radius=1, depth=2):
        """Create a cone"""
        bpy.ops.mesh.primitive_cone_add(radius1=radius, depth=depth, location=(0, 0, 0))
        obj = bpy.context.active_object
        obj.name = f"AI_Cone_{datetime.now().strftime('%H%M%S')}"
        return obj
    
    def create_monkey(self, size=2):
        """Create Suzanne (monkey head)"""
        bpy.ops.mesh.primitive_monkey_add(size=size, location=(0, 0, 0))
        obj = bpy.context.active_object
        obj.name = f"AI_Monkey_{datetime.now().strftime('%H%M%S')}"
        return obj
    
    def create_tree(self):
        """Create a simple tree"""
        # Trunk
        bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=2, location=(0, 0, 1))
        trunk = bpy.context.active_object
        trunk.name = "Tree_Trunk"
        
        # Leaves (icosphere)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.8, location=(0, 0, 2.5))
        leaves = bpy.context.active_object
        leaves.name = "Tree_Leaves"
        
        # Join them
        bpy.ops.object.select_all(action='DESELECT')
        trunk.select_set(True)
        leaves.select_set(True)
        bpy.context.view_layer.objects.active = trunk
        bpy.ops.object.join()
        
        trunk.name = f"AI_Tree_{datetime.now().strftime('%H%M%S')}"
        return trunk
    
    def create_chair(self):
        """Create a simple chair"""
        # Seat
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.5))
        seat = bpy.context.active_object
        seat.scale = (1, 1, 0.1)
        
        # Back
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.45, 1))
        back = bpy.context.active_object
        back.scale = (1, 0.1, 0.5)
        
        # Legs
        leg_positions = [(-0.4, -0.4, 0.25), (0.4, -0.4, 0.25), (-0.4, 0.4, 0.25), (0.4, 0.4, 0.25)]
        legs = []
        for pos in leg_positions:
            bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
            leg = bpy.context.active_object
            leg.scale = (0.1, 0.1, 0.5)
            legs.append(leg)
        
        # Join all
        bpy.ops.object.select_all(action='DESELECT')
        seat.select_set(True)
        back.select_set(True)
        for leg in legs:
            leg.select_set(True)
        bpy.context.view_layer.objects.active = seat
        bpy.ops.object.join()
        
        seat.name = f"AI_Chair_{datetime.now().strftime('%H%M%S')}"
        return seat
    
    def create_apple(self):
        """Create an apple-like shape"""
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0, 0, 0))
        obj = bpy.context.active_object
        
        # Deform to look like apple
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Add top dent
        bpy.ops.transform.translate(value=(0, 0, 0.2))
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Add stem
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.5, location=(0, 0, 0.9))
        stem = bpy.context.active_object
        
        # Join
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        stem.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.join()
        
        obj.name = f"AI_Apple_{datetime.now().strftime('%H%M%S')}"
        return obj
    
    def create_car(self):
        """Create a simple car shape"""
        # Body
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.5))
        body = bpy.context.active_object
        body.scale = (2, 1, 0.5)
        
        # Top
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1))
        top = bpy.context.active_object
        top.scale = (1.2, 0.8, 0.4)
        
        # Wheels
        wheel_positions = [(-1.2, -0.8, 0.3), (1.2, -0.8, 0.3), (-1.2, 0.8, 0.3), (1.2, 0.8, 0.3)]
        wheels = []
        for pos in wheel_positions:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.2, location=pos)
            wheel = bpy.context.active_object
            wheel.rotation_euler = (1.5708, 0, 0)
            wheels.append(wheel)
        
        # Join
        bpy.ops.object.select_all(action='DESELECT')
        body.select_set(True)
        top.select_set(True)
        for wheel in wheels:
            wheel.select_set(True)
        bpy.context.view_layer.objects.active = body
        bpy.ops.object.join()
        
        body.name = f"AI_Car_{datetime.now().strftime('%H%M%S')}"
        return body
    
    def create_procedural_shape(self, prompt):
        """Create a unique shape based on prompt hash"""
        # Use prompt to seed random variations
        random.seed(hash(prompt) % 10000)
        
        # Create a sphere and deform it
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
        obj = bpy.context.active_object
        
        # Random deformation
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        
        bm = bmesh.from_mesh(obj.data)
        
        for vert in bm.verts:
            # Random displacement
            noise = random.uniform(-0.3, 0.3)
            vert.co += vert.normal * noise
        
        bmesh.to_mesh(bm, obj.data)
        bm.free()
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        obj.name = f"AI_Procedural_{datetime.now().strftime('%H%M%S')}"
        return obj
    
    def apply_subdivision(self, obj, levels=2):
        """Apply subdivision surface modifier"""
        subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf.levels = levels
        subsurf.render_levels = levels
        
        # Apply modifier
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier="Subdivision")
        
        return obj
    
    def add_material(self, obj, material_type="clay"):
        """Add material to object"""
        material = bpy.data.materials.new(name=f"{obj.name}_Mat")
        material.use_nodes = True
        
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        
        # Clear default nodes
        nodes.clear()
        
        # Create output node
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        # Create principled BSDF
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.location = (0, 0)
        
        # Link
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Configure based on material type
        if material_type == "clay":
            principled.inputs['Base Color'].default_value = (0.8, 0.6, 0.5, 1.0)
            principled.inputs['Roughness'].default_value = 0.9
        elif material_type == "metal":
            principled.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)
            principled.inputs['Metallic'].default_value = 1.0
            principled.inputs['Roughness'].default_value = 0.2
        elif material_type == "plastic":
            principled.inputs['Base Color'].default_value = (0.2, 0.5, 0.8, 1.0)
            principled.inputs['Roughness'].default_value = 0.1
            principled.inputs['Specular'].default_value = 0.5
        elif material_type == "gold":
            principled.inputs['Base Color'].default_value = (1.0, 0.8, 0.2, 1.0)
            principled.inputs['Metallic'].default_value = 1.0
            principled.inputs['Roughness'].default_value = 0.1
        elif material_type == "wood":
            principled.inputs['Base Color'].default_value = (0.4, 0.2, 0.1, 1.0)
            principled.inputs['Roughness'].default_value = 0.8
        elif material_type == "glass":
            principled.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
            principled.inputs['Roughness'].default_value = 0.0
            principled.inputs['Transmission'].default_value = 0.9
            principled.inputs['IOR'].default_value = 1.45
        
        # Assign material
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)
        
        return material
