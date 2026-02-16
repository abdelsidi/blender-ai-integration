import bpy
from bpy.types import Panel, Operator

class AILightingPanel(Panel):
    """AI Lighting Panel"""
    bl_label = "AI Lighting"
    bl_idname = "VIEW3D_PT_ai_lighting"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Lighting Analysis:")
        row = layout.row()
        row.operator("ai_lighting.analyze", text="Analyze Scene", icon='LIGHT')
        
        layout.separator()
        
        layout.label(text="Lighting Style:")
        row = layout.row()
        row.prop(context.scene, "ai_lighting_style")
        
        layout.separator()
        
        row = layout.row()
        row.scale_y = 1.5
        row.operator("ai_lighting.optimize", text="Optimize Lighting", icon='CHECKMARK')

class AnalyzeLightingOperator(Operator):
    """Analyze Lighting"""
    bl_idname = "ai_lighting.analyze"
    bl_label = "Analyze Lighting"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        scene = context.scene
        total_lights = len([obj for obj in scene.objects if obj.type == 'LIGHT'])
        self.report({'INFO'}, f"Scene has {total_lights} lights")
        return {'FINISHED'}

class OptimizeLightingOperator(Operator):
    """Optimize Lighting"""
    bl_idname = "ai_lighting.optimize"
    bl_label = "Optimize Lighting"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        style = context.scene.ai_lighting_style
        self.report({'INFO'}, f"Optimizing lighting with style: {style}")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AILightingPanel)
    bpy.utils.register_class(AnalyzeLightingOperator)
    bpy.utils.register_class(OptimizeLightingOperator)
    
    bpy.types.Scene.ai_lighting_style = bpy.props.EnumProperty(
        name="Lighting Style",
        items=[
            ('balanced', 'Balanced', 'Balanced lighting'),
            ('dramatic', 'Dramatic', 'Dramatic lighting'),
            ('bright', 'Bright', 'Bright lighting'),
            ('dark', 'Dark', 'Dark lighting')
        ],
        default='balanced'
    )

def unregister():
    bpy.utils.unregister_class(AILightingPanel)
    bpy.utils.unregister_class(AnalyzeLightingOperator)
    bpy.utils.unregister_class(OptimizeLightingOperator)
    del bpy.types.Scene.ai_lighting_style
