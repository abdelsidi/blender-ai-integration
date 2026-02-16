import bpy
from bpy.types import Panel, Operator

class AIAnimationPanel(Panel):
    """لوحة تحكم AI Animation"""
    bl_label = "AI Animation"
    bl_idname = "VIEW3D_PT_ai_animation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text="نوع الحركة:")
        row = layout.row()
        row.prop(context.scene, "ai_animation_type")
        
        layout.separator()
        
        layout.label(text="المدة:")
        row = layout.row()
        row.prop(context.scene, "ai_animation_duration")
        
        layout.separator()
        
        row = layout.row()
        row.scale_y = 1.5
        row.operator("ai_animation.generate", text="Generate Animation", icon='ANIM')

class GenerateAnimationOperator(Operator):
    """توليد الحركة"""
    bl_idname = "ai_animation.generate"
    bl_label = "Generate Animation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selected = context.selected_objects
        if not selected:
            self.report({'ERROR'}, "Please select a rigged object!")
            return {'CANCELLED'}
        
        anim_type = context.scene.ai_animation_type
        duration = context.scene.ai_animation_duration
        
        self.report({'INFO'}, f"Generating {anim_type} animation ({duration} frames)...")
        
        # هنا سيكون منطق توليد الحركة
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AIAnimationPanel)
    bpy.utils.register_class(GenerateAnimationOperator)
    
    bpy.types.Scene.ai_animation_type = bpy.props.EnumProperty(
        name="Animation Type",
        items=[
            ('walk', 'Walk', 'Walking animation'),
            ('run', 'Run', 'Running animation'),
            ('idle', 'Idle', 'Idle animation'),
            ('jump', 'Jump', 'Jumping animation'),
            ('dance', 'Dance', 'Dancing animation')
        ],
        default='walk'
    )
    
    bpy.types.Scene.ai_animation_duration = bpy.props.IntProperty(
        name="Duration (frames)",
        default=120,
        min=1,
        max=10000
    )

def unregister():
    bpy.utils.unregister_class(AIAnimationPanel)
    bpy.utils.unregister_class(GenerateAnimationOperator)
    del bpy.types.Scene.ai_animation_type
    del bpy.types.Scene.ai_animation_duration
