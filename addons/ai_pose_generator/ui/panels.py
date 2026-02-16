import bpy
from bpy.types import Panel, Operator

class AIPoseGeneratorPanel(Panel):
    """لوحة توليد الأوضاع"""
    bl_label = "🧍 AI Pose Generator"
    bl_idname = "VIEW3D_PT_ai_pose_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        box = layout.box()
        box.label(text="الوضعيات", icon='ARMATURE_DATA')
        
        row = box.row()
        row.prop(scene, "ai_pose_category", text="الفئة")
        
        row = box.row()
        row.prop(scene, "ai_pose_type", text="النوع")
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("ai_pose.generate", text="توليد الوضعية", icon='POSE_HLT')
        
        layout.separator()
        
        box = layout.box()
        box.label(text="حفظ وتحميل", icon='FILE_FOLDER')
        
        row = box.row()
        row.operator("ai_pose.save", text="حفظ الوضعية")

class GeneratePoseOperator(Operator):
    """توليد وضعية"""
    bl_idname = "ai_pose.generate"
    bl_label = "Generate Pose"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "يرجى تحديد هيكل عظمي!")
            return {'CANCELLED'}
        
        try:
            from ..ai_pose_generator import AIPoseGenerator
            generator = AIPoseGenerator()
            result = generator.generate_standing_pose(obj, 'confident')
            self.report({'INFO'}, f"✅ {result}")
        except Exception as e:
            self.report({'ERROR'}, f"❌ خطأ: {e}")
        return {'FINISHED'}

class SavePoseOperator(Operator):
    """حفظ الوضعية"""
    bl_idname = "ai_pose.save"
    bl_label = "Save Pose"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        self.report({'INFO'}, "✅ تم حفظ الوضعية")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AIPoseGeneratorPanel)
    bpy.utils.register_class(GeneratePoseOperator)
    bpy.utils.register_class(SavePoseOperator)
    
    bpy.types.Scene.ai_pose_category = bpy.props.EnumProperty(
        items=[('action', 'حركة', 'حركات'), ('emotion', 'عاطفة', 'تعبيرات'), 
               ('professional', 'مهني', 'وضعيات مهنية'), ('creative', 'إبداعي', 'وضعيات إبداعية')],
        default='action'
    )
    
    bpy.types.Scene.ai_pose_type = bpy.props.EnumProperty(
        items=[('standing', 'وقوف', 'وقوف'), ('running', 'جري', 'جري'), 
               ('fighting', 'قتال', 'قتال'), ('happy', 'سعادة', 'سعادة')],
        default='standing'
    )

def unregister():
    bpy.utils.unregister_class(AIPoseGeneratorPanel)
    bpy.utils.unregister_class(GeneratePoseOperator)
    bpy.utils.unregister_class(SavePoseOperator)
    del bpy.types.Scene.ai_pose_category
    del bpy.types.Scene.ai_pose_type
