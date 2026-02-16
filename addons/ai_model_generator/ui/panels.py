import bpy
from bpy.types import Panel, Operator
import json
import os

# Get addon directory for JSON paths
ADDON_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
PRESETS_DIR = os.path.join(ADDON_DIR, "..", "..", "assets", "presets")

def load_material_presets():
    """Load materials from JSON"""
    json_path = os.path.join(PRESETS_DIR, "materials.json")
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
            return [(mat['id'], mat['name'], mat['type']) for mat in data.get('materials', [])]
    return []

def load_model_presets():
    """Load models from JSON"""
    json_path = os.path.join(PRESETS_DIR, "models.json")
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
            return data.get('models', [])
    return []

class AIModelGeneratorPanel(Panel):
    """AI Model Generator Panel"""
    bl_label = "AI Model Generator"
    bl_idname = "VIEW3D_PT_ai_model_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Text generation section
        box = layout.box()
        box.label(text="Generate from Text", icon='FONT_DATA')
        
        row = box.row()
        row.prop(scene, "ai_model_text_prompt", text="Description")
        
        # Quick presets from JSON
        materials = load_material_presets()
        if materials:
            row = box.row()
            row.prop(scene, "ai_model_preset_material", text="Material")
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("ai_model.generate_from_text", text="Generate from Text", icon='MESH_CUBE')
        
        layout.separator()
        
        # Settings
        box = layout.box()
        box.label(text="Settings", icon='PREFERENCES')
        
        row = box.row()
        row.prop(scene, "ai_model_style")
        
        row = box.row()
        row.prop(scene, "ai_model_resolution")
        
        row = box.row()
        row.prop(scene, "ai_model_material")
        
        layout.separator()
        
        # Quick primitives
        box = layout.box()
        box.label(text="Quick Primitives", icon='MODIFIER')
        
        row = box.row(align=True)
        row.operator("ai_model.create_primitive", text="Cube").primitive_type = 'cube'
        row.operator("ai_model.create_primitive", text="Sphere").primitive_type = 'sphere'
        
        row = box.row(align=True)
        row.operator("ai_model.create_primitive", text="Cylinder").primitive_type = 'cylinder'
        row.operator("ai_model.create_primitive", text="Torus").primitive_type = 'torus'

class GenerateFromTextOperator(Operator):
    """Generate Model from Text"""
    bl_idname = "ai_model.generate_from_text"
    bl_label = "Generate Model"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        prompt = scene.ai_model_text_prompt
        
        if not prompt:
            self.report({'ERROR'}, "Please enter a description!")
            return {'CANCELLED'}
        
        try:
            from ..ai_model_generator import AIModelGenerator
            generator = AIModelGenerator()
            
            # Get material from preset or dropdown
            material = scene.ai_model_material
            
            # Generate model
            obj = generator.generate_model_from_prompt(prompt, scene.ai_model_style, material)
            
            # Apply subdivision if set
            if scene.ai_model_subdivision > 0:
                generator.apply_subdivision(obj, scene.ai_model_subdivision)
            
            self.report({'INFO'}, f"Created: {obj.name}")
            
            # Save to recent prompts JSON
            self.save_to_recent(prompt)
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed: {e}")
        
        return {'FINISHED'}
    
    def save_to_recent(self, prompt):
        """Save prompt to recent in user_preferences.json"""
        import json
        import os
        
        addon_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        prefs_path = os.path.join(addon_dir, "config", "user_preferences.json")
        
        try:
            prefs = {}
            if os.path.exists(prefs_path):
                with open(prefs_path, 'r') as f:
                    prefs = json.load(f)
            
            recent = prefs.get("recent_prompts", [])
            if prompt in recent:
                recent.remove(prompt)
            recent.insert(0, prompt)
            recent = recent[:10]
            
            prefs["recent_prompts"] = recent
            
            with open(prefs_path, 'w') as f:
                json.dump(prefs, f, indent=2)
        except:
            pass

class CreatePrimitiveOperator(Operator):
    """Create Primitive"""
    bl_idname = "ai_model.create_primitive"
    bl_label = "Create Primitive"
    bl_options = {'REGISTER', 'UNDO'}
    
    primitive_type: bpy.props.StringProperty(default='cube')
    
    def execute(self, context):
        try:
            from ..ai_model_generator import AIModelGenerator
            generator = AIModelGenerator()
            
            # Map primitive types to generator methods
            method_map = {
                'cube': generator.create_cube,
                'sphere': generator.create_sphere,
                'cylinder': generator.create_cylinder,
                'torus': generator.create_torus,
            }
            
            method = method_map.get(self.primitive_type, generator.create_cube)
            obj = method()
            
            scene = context.scene
            if scene.ai_model_subdivision > 0:
                generator.apply_subdivision(obj, scene.ai_model_subdivision)
            
            # Add material
            generator.add_material(obj, scene.ai_model_material)
            
            self.report({'INFO'}, f"Created: {obj.name}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed: {e}")
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AIModelGeneratorPanel)
    bpy.utils.register_class(GenerateFromTextOperator)
    bpy.utils.register_class(CreatePrimitiveOperator)
    
    # Load material presets for enum
    materials = load_material_presets()
    material_items = [(m[0], m[1], m[2]) for m in materials] if materials else [
        ('clay', 'Clay', 'Clay material'),
        ('metal', 'Metal', 'Metal material'),
        ('plastic', 'Plastic', 'Plastic material'),
    ]
    
    bpy.types.Scene.ai_model_text_prompt = bpy.props.StringProperty(
        name="Prompt",
        description="Model description",
        default="red apple"
    )
    
    bpy.types.Scene.ai_model_style = bpy.props.EnumProperty(
        name="Style",
        items=[
            ('simple', 'Simple', 'Simple model'),
            ('detailed', 'Detailed', 'Detailed model'),
            ('realistic', 'Realistic', 'Realistic model'),
        ],
        default='detailed'
    )
    
    bpy.types.Scene.ai_model_material = bpy.props.EnumProperty(
        name="Material",
        items=material_items,
        default='clay' if not materials else materials[0][0]
    )
    
    bpy.types.Scene.ai_model_preset_material = bpy.props.EnumProperty(
        name="Preset Material",
        items=material_items if materials else [('none', 'None', 'No presets')]
    )
    
    bpy.types.Scene.ai_model_subdivision = bpy.props.IntProperty(
        name="Subdivision",
        description="Subdivision surface levels",
        default=2,
        min=0,
        max=6
    )

def unregister():
    bpy.utils.unregister_class(AIModelGeneratorPanel)
    bpy.utils.unregister_class(GenerateFromTextOperator)
    bpy.utils.unregister_class(CreatePrimitiveOperator)
    
    del bpy.types.Scene.ai_model_text_prompt
    del bpy.types.Scene.ai_model_style
    del bpy.types.Scene.ai_model_material
    del bpy.types.Scene.ai_model_preset_material
    del bpy.types.Scene.ai_model_subdivision
