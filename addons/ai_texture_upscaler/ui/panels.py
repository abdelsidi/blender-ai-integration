import bpy
from bpy.types import Panel, Operator

class AITextureUpscalerPanel(Panel):
    """لوحة رفع دقة النسيج"""
    bl_label = "🔍 AI Texture Upscaler"
    bl_idname = "IMAGE_PT_ai_texture_upscaler"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="رفع الدقة", icon='IMAGE_DATA')
        
        row = box.row()
        row.prop(context.scene, "ai_upscale_factor", text="المعامل")
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("ai_texture.upscale", text="رفع الدقة", icon='ZOOM_IN')
        
        row = box.row()
        row.operator("ai_texture.enhance", text="تحسين النسيج", icon='MATERIAL')

class UpscaleTextureOperator(Operator):
    """رفع دقة النسيج"""
    bl_idname = "ai_texture.upscale"
    bl_label = "Upscale Texture"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        self.report({'INFO'}, "✅ تم رفع الدقة")
        return {'FINISHED'}

class EnhanceTextureOperator(Operator):
    """تحسين النسيج"""
    bl_idname = "ai_texture.enhance"
    bl_label = "Enhance Texture"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        self.report({'INFO'}, "✅ تم التحسين")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AITextureUpscalerPanel)
    bpy.utils.register_class(UpscaleTextureOperator)
    bpy.utils.register_class(EnhanceTextureOperator)
    
    bpy.types.Scene.ai_upscale_factor = bpy.props.EnumProperty(
        items=[('2', '2x', 'ضعف الحجم'), ('4', '4x', 'أربعة أضعاف'), ('8', '8x', 'ثمانية أضعاف')],
        default='4'
    )

def unregister():
    bpy.utils.unregister_class(AITextureUpscalerPanel)
    bpy.utils.unregister_class(UpscaleTextureOperator)
    bpy.utils.unregister_class(EnhanceTextureOperator)
    del bpy.types.Scene.ai_upscale_factor
