import bpy
from bpy.types import Panel, Operator

class AISceneGeneratorPanel(Panel):
    """لوحة توليد المشاهد"""
    bl_label = "🌍 AI Scene Generator"
    bl_idname = "VIEW3D_PT_ai_scene_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        box = layout.box()
        box.label(text="نوع المشهد", icon='WORLD')
        
        row = box.row()
        row.prop(scene, "ai_scene_type", text="النوع")
        
        row = box.row()
        row.prop(scene, "ai_scene_complexity", text="التعقيد")
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("ai_scene.generate", text="توليد المشهد", icon='WORLD_DATA')
        
        layout.separator()
        
        box = layout.box()
        box.label(text="الكاميرا", icon='CAMERA_DATA')
        
        row = box.row()
        row.operator("ai_scene.setup_camera", text="إعداد الكاميرا")
        
        row = box.row()
        row.operator("ai_scene.composition", text="قواعد التكوين")

class GenerateSceneOperator(Operator):
    """توليد مشهد"""
    bl_idname = "ai_scene.generate"
    bl_label = "Generate Scene"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            from ..ai_scene_generator import AISceneGenerator
            generator = AISceneGenerator()
            result = generator.generate_nature_scene('forest', context.scene.ai_scene_complexity)
            self.report({'INFO'}, f"✅ {result}")
        except Exception as e:
            self.report({'ERROR'}, f"❌ خطأ: {e}")
        return {'FINISHED'}

class SetupCameraOperator(Operator):
    """إعداد الكاميرا"""
    bl_idname = "ai_scene.setup_camera"
    bl_label = "Setup Camera"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            from ..ai_scene_generator import AISceneGenerator
            generator = AISceneGenerator()
            camera = generator.setup_camera()
            self.report({'INFO'}, f"✅ تم إعداد الكاميرا: {camera.name}")
        except Exception as e:
            self.report({'ERROR'}, f"❌ خطأ: {e}")
        return {'FINISHED'}

class CompositionOperator(Operator):
    """قواعد التكوين"""
    bl_idname = "ai_scene.composition"
    bl_label = "Apply Composition"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        self.report({'INFO'}, "✅ تم تطبيق قواعد التكوين")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AISceneGeneratorPanel)
    bpy.utils.register_class(GenerateSceneOperator)
    bpy.utils.register_class(SetupCameraOperator)
    bpy.utils.register_class(CompositionOperator)
    
    bpy.types.Scene.ai_scene_type = bpy.props.EnumProperty(
        items=[('nature', 'طبيعة', 'مشهد طبيعي'), ('urban', 'مدني', 'بيئة مدنية'), 
               ('fantasy', 'خيالي', 'عالم خيالي'), ('studio', 'استوديو', 'استوديو تصوير')],
        default='nature'
    )
    
    bpy.types.Scene.ai_scene_complexity = bpy.props.EnumProperty(
        items=[('low', 'بسيط', 'بسيط'), ('medium', 'متوسط', 'متوسط'), ('high', 'معقد', 'معقد')],
        default='medium'
    )

def unregister():
    bpy.utils.unregister_class(AISceneGeneratorPanel)
    bpy.utils.unregister_class(GenerateSceneOperator)
    bpy.utils.unregister_class(SetupCameraOperator)
    bpy.utils.unregister_class(CompositionOperator)
    del bpy.types.Scene.ai_scene_type
    del bpy.types.Scene.ai_scene_complexity
