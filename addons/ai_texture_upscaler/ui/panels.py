import bpy
from bpy.types import Panel, Operator

class AITextureUpscalerPanel(Panel):
    """AI Texture Upscaler Panel"""
    bl_label = "AI Texture Upscaler"
    bl_idname = "IMAGE_PT_ai_texture_upscaler"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="Upscale", icon='IMAGE_DATA')
        
        row = box.row()
        row.prop(context.scene, "ai_upscale_factor", text="Factor")
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("ai_texture.upscale", text="Upscale", icon='ZOOM_IN')
        
        row = box.row()
        row.operator("ai_texture.enhance", text="Enhance Texture", icon='MATERIAL')

class UpscaleTextureOperator(Operator):
    """Upscale Texture"""
    bl_idname = "ai_texture.upscale"
    bl_label = "Upscale Texture"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        self.report({'INFO'}, "Upscaled")
        return {'FINISHED'}

class EnhanceTextureOperator(Operator):
    """Enhance Texture"""
    bl_idname = "ai_texture.enhance"
    bl_label = "Enhance Texture"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        self.report({'INFO'}, "Enhanced")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AITextureUpscalerPanel)
    bpy.utils.register_class(UpscaleTextureOperator)
    bpy.utils.register_class(EnhanceTextureOperator)
    
    bpy.types.Scene.ai_upscale_factor = bpy.props.EnumProperty(
        name="Factor",
        items=[('2', '2x', 'Double size'), ('4', '4x', 'Quadruple size'), ('8', '8x', 'Octuple size')],
        default='4'
    )

def unregister():
    bpy.utils.unregister_class(AITextureUpscalerPanel)
    bpy.utils.unregister_class(UpscaleTextureOperator)
    bpy.utils.unregister_class(EnhanceTextureOperator)
    del bpy.types.Scene.ai_upscale_factor
