import bpy
from bpy.types import Panel, Operator
import json
import os

ADDON_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
PRESETS_DIR = os.path.join(ADDON_DIR, "..", "..", "assets", "presets")

def load_material_presets():
    """Load materials from JSON"""
    json_path = os.path.join(PRESETS_DIR, "materials.json")
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
            return [(mat['id'], mat['name'], f"{mat['type']} material") for mat in data.get('materials', [])]
    return []

class AIMaterialGeneratorPanel(Panel):
    """AI Material Generator Panel"""
    bl_label = "AI Material Generator"
    bl_idname = "VIEW3D_PT_ai_material_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        
        # Prompt section
        box = layout.box()
        box.label(text="Generate Material", icon='MATERIAL')
        
        row = box.row()
        row.prop(context.scene, "ai_material_prompt", text="Prompt")
        
        # Type detection hint
        prompt = context.scene.ai_material_prompt.lower()
        detected = ""
        if any(w in prompt for w in ['metal', 'gold', 'silver']):
            detected = "Detecting: Metal"
        elif any(w in prompt for w in ['wood', 'oak']):
            detected = "Detecting: Wood"
        elif any(w in prompt for w in ['glass']):
            detected = "Detecting: Glass"
        elif any(w in prompt for w in ['plastic']):
            detected = "Detecting: Plastic"
        
        if detected:
            row = box.row()
            row.label(text=detected, icon='INFO')
        
        row = box.row()
        row.scale_y = 1.5
        row.operator("ai_material.generate", text="Generate Material", icon='MATERIAL')
        
        layout.separator()
        
        # JSON Presets section
        presets = load_material_presets()
        if presets:
            box = layout.box()
            box.label(text="Quick Presets", icon='PRESET')
            
            row = box.row()
            row.prop(context.scene, "ai_material_preset", text="")
            
            row = box.row()
            row.operator("ai_material.apply_preset", text="Apply Preset")
        
        layout.separator()
        
        # Apply to selected
        box = layout.box()
        box.label(text="Apply Material", icon='CHECKMARK')
        
        row = box.row()
        row.scale_y = 1.5
        row.operator("ai_material.apply", text="Apply to Selected", icon='CHECKMARK')

class GenerateMaterialOperator(Operator):
    """Generate Material from Prompt"""
    bl_idname = "ai_material.generate"
    bl_label = "Generate Material"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        prompt = scene.ai_material_prompt
        
        if not prompt:
            self.report({'ERROR'}, "Please enter a prompt!")
            return {'CANCELLED'}
        
        try:
            from ..ai_material_generator import AIMaterialGenerator
            generator = AIMaterialGenerator()
            
            # Create material based on prompt
            material = generator.create_material_from_prompt(prompt)
            
            # Store in scene for later application
            scene.ai_material_last_generated = material.name
            
            # Apply to selected object if available
            obj = context.active_object
            if obj and obj.type == 'MESH':
                generator.apply_material_to_object(obj, material)
                self.report({'INFO'}, f"Generated and applied: {material.name}")
            else:
                self.report({'INFO'}, f"Generated: {material.name} - Select an object to apply")
            
            # Save to recent prompts
            self.save_to_recent(prompt)
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed: {e}")
        
        return {'FINISHED'}
    
    def save_to_recent(self, prompt):
        """Save to recent prompts JSON"""
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

class ApplyPresetOperator(Operator):
    """Apply Material from JSON Preset"""
    bl_idname = "ai_material.apply_preset"
    bl_label = "Apply Preset"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        preset_id = context.scene.ai_material_preset
        
        try:
            from ..ai_material_generator import AIMaterialGenerator
            generator = AIMaterialGenerator()
            
            material = generator.create_material_from_preset(preset_id)
            
            # Apply to selected
            obj = context.active_object
            if obj and obj.type == 'MESH':
                generator.apply_material_to_object(obj, material)
                self.report({'INFO'}, f"Applied preset: {material.name}")
            else:
                self.report({'ERROR'}, "Please select a mesh object!")
                return {'CANCELLED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed: {e}")
        
        return {'FINISHED'}

class ApplyMaterialOperator(Operator):
    """Apply Last Generated Material"""
    bl_idname = "ai_material.apply"
    bl_label = "Apply Material"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Please select a mesh object!")
            return {'CANCELLED'}
        
        # Try to find last generated material
        last_mat_name = context.scene.ai_material_last_generated
        
        if last_mat_name and last_mat_name in bpy.data.materials:
            material = bpy.data.materials[last_mat_name]
            
            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)
            
            self.report({'INFO'}, f"Applied: {material.name}")
        else:
            self.report({'ERROR'}, "No material generated yet!")
            return {'CANCELLED'}
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AIMaterialGeneratorPanel)
    bpy.utils.register_class(GenerateMaterialOperator)
    bpy.utils.register_class(ApplyPresetOperator)
    bpy.utils.register_class(ApplyMaterialOperator)
    
    # Load presets
    presets = load_material_presets()
    preset_items = presets if presets else [('none', 'No Presets', 'No presets available')]
    
    bpy.types.Scene.ai_material_prompt = bpy.props.StringProperty(
        name="Prompt",
        description="Describe the material you want",
        default="red metal"
    )
    
    bpy.types.Scene.ai_material_preset = bpy.props.EnumProperty(
        name="Preset",
        items=preset_items
    )
    
    bpy.types.Scene.ai_material_last_generated = bpy.props.StringProperty(
        name="Last Material",
        default=""
    )

def unregister():
    bpy.utils.unregister_class(AIMaterialGeneratorPanel)
    bpy.utils.unregister_class(GenerateMaterialOperator)
    bpy.utils.unregister_class(ApplyPresetOperator)
    bpy.utils.unregister_class(ApplyMaterialOperator)
    
    del bpy.types.Scene.ai_material_prompt
    del bpy.types.Scene.ai_material_preset
    del bpy.types.Scene.ai_material_last_generated
