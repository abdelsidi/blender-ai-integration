import bpy
from bpy.types import Panel, Operator

class AIDenoiserPanel(Panel):
    """لوحة إزالة الضوضاء"""
    bl_label = "✨ AI Denoiser"
    bl_idname = "RENDER_PT_ai_denoiser"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        box = layout.box()
        box.label(text="إعدادات إزالة الضوضاء", icon='SHADERFX')
        
        row = box.row()
        row.prop(scene, "ai_denoiser_type", text="النوع")
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("ai_denoiser.setup", text="إعداد تلقائي", icon='CHECKMARK')
        
        row = box.row()
        row.operator("ai_denoiser.analyze", text="تحليل الضوضاء")

class SetupDenoiserOperator(Operator):
    """إعداد إزالة الضوضاء"""
    bl_idname = "ai_denoiser.setup"
    bl_label = "Setup Denoiser"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            from ..ai_denoiser import AIDenoiser
            denoiser = AIDenoiser()
            result = denoiser.auto_setup(context.scene)
            self.report({'INFO'}, f"✅ تم الإعداد: {result['denoiser']}")
        except Exception as e:
            self.report({'ERROR'}, f"❌ خطأ: {e}")
        return {'FINISHED'}

class AnalyzeNoiseOperator(Operator):
    """تحليل الضوضاء"""
    bl_idname = "ai_denoiser.analyze"
    bl_label = "Analyze Noise"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            from ..ai_denoiser import AIDenoiser
            denoiser = AIDenoiser()
            level = denoiser.estimate_noise_level(context.scene)
            self.report({'INFO'}, f"📊 مستوى الضوضاء: {level}")
        except Exception as e:
            self.report({'ERROR'}, f"❌ خطأ: {e}")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AIDenoiserPanel)
    bpy.utils.register_class(SetupDenoiserOperator)
    bpy.utils.register_class(AnalyzeNoiseOperator)
    
    bpy.types.Scene.ai_denoiser_type = bpy.props.EnumProperty(
        items=[('optix', 'OptiX', 'NVIDIA OptiX'), ('oidn', 'OIDN', 'Intel Open Image Denoise')],
        default='optix'
    )

def unregister():
    bpy.utils.unregister_class(AIDenoiserPanel)
    bpy.utils.unregister_class(SetupDenoiserOperator)
    bpy.utils.unregister_class(AnalyzeNoiseOperator)
    del bpy.types.Scene.ai_denoiser_type
