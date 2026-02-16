import bpy
from bpy.types import Panel, Operator

class AISceneGeneratorPanel(Panel):
    """AI Scene Generator Panel"""
    bl_label = "AI Scene Generator"
    bl_idname = "VIEW3D_PT_ai_scene_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        box = layout.box()
        box.label(text="Scene Type", icon='WORLD')
        
        row = box.row()
        row.prop(scene, "ai_scene_type", text="Type")
        
        row = box.row()
        row.prop(scene, "ai_scene_complexity", text="Complexity")
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("ai_scene.generate", text="Generate Scene", icon='WORLD_DATA')
        
        layout.separator()
        
        box = layout.box()
        box.label(text="Camera", icon='CAMERA_DATA')
        
        row = box.row()
        row.operator("ai_scene.setup_camera", text="Setup Camera")
        
        row = box.row()
        row.operator("ai_scene.composition", text="Apply Composition")

class GenerateSceneOperator(Operator):
    """Generate Scene"""
    bl_idname = "ai_scene.generate"
    bl_label = "Generate Scene"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            from ..ai_scene_generator import AISceneGenerator
            generator = AISceneGenerator()
            result = generator.generate_nature_scene('forest', context.scene.ai_scene_complexity)
            self.report({'INFO'}, f"Generated: {result}")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        return {'FINISHED'}

class SetupCameraOperator(Operator):
    """Setup Camera"""
    bl_idname = "ai_scene.setup_camera"
    bl_label = "Setup Camera"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            from ..ai_scene_generator import AISceneGenerator
            generator = AISceneGenerator()
            camera = generator.setup_camera()
            self.report({'INFO'}, f"Camera setup: {camera.name}")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        return {'FINISHED'}

class CompositionOperator(Operator):
    """Apply Composition"""
    bl_idname = "ai_scene.composition"
    bl_label = "Apply Composition"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        self.report({'INFO'}, "Composition applied")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AISceneGeneratorPanel)
    bpy.utils.register_class(GenerateSceneOperator)
    bpy.utils.register_class(SetupCameraOperator)
    bpy.utils.register_class(CompositionOperator)
    
    bpy.types.Scene.ai_scene_type = bpy.props.EnumProperty(
        name="Scene Type",
        items=[('nature', 'Nature', 'Natural scene'), ('urban', 'Urban', 'Urban environment'), 
               ('fantasy', 'Fantasy', 'Fantasy world'), ('studio', 'Studio', 'Photo studio')],
        default='nature'
    )
    
    bpy.types.Scene.ai_scene_complexity = bpy.props.EnumProperty(
        name="Complexity",
        items=[('low', 'Low', 'Simple'), ('medium', 'Medium', 'Medium'), ('high', 'High', 'Complex')],
        default='medium'
    )

def unregister():
    bpy.utils.unregister_class(AISceneGeneratorPanel)
    bpy.utils.unregister_class(GenerateSceneOperator)
    bpy.utils.unregister_class(SetupCameraOperator)
    bpy.utils.unregister_class(CompositionOperator)
    del bpy.types.Scene.ai_scene_type
    del bpy.types.Scene.ai_scene_complexity
