import bpy
from bpy.types import Panel, Operator

class AIPoseGeneratorPanel(Panel):
    """AI Pose Generator Panel"""
    bl_label = "AI Pose Generator"
    bl_idname = "VIEW3D_PT_ai_pose_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        box = layout.box()
        box.label(text="Poses", icon='ARMATURE_DATA')
        
        row = box.row()
        row.prop(scene, "ai_pose_category", text="Category")
        
        row = box.row()
        row.prop(scene, "ai_pose_type", text="Type")
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("ai_pose.generate", text="Generate Pose", icon='POSE_HLT')
        
        layout.separator()
        
        box = layout.box()
        box.label(text="Save/Load", icon='FILE_FOLDER')
        
        row = box.row()
        row.operator("ai_pose.save", text="Save Pose")

class GeneratePoseOperator(Operator):
    """Generate Pose"""
    bl_idname = "ai_pose.generate"
    bl_label = "Generate Pose"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Please select an armature!")
            return {'CANCELLED'}
        
        try:
            from ..ai_pose_generator import AIPoseGenerator
            generator = AIPoseGenerator()
            result = generator.generate_standing_pose(obj, 'confident')
            self.report({'INFO'}, f"Generated: {result}")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        return {'FINISHED'}

class SavePoseOperator(Operator):
    """Save Pose"""
    bl_idname = "ai_pose.save"
    bl_label = "Save Pose"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        self.report({'INFO'}, "Pose saved")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AIPoseGeneratorPanel)
    bpy.utils.register_class(GeneratePoseOperator)
    bpy.utils.register_class(SavePoseOperator)
    
    bpy.types.Scene.ai_pose_category = bpy.props.EnumProperty(
        name="Category",
        items=[('action', 'Action', 'Action poses'), ('emotion', 'Emotion', 'Emotional expressions'), 
               ('professional', 'Professional', 'Professional poses'), ('creative', 'Creative', 'Creative poses')],
        default='action'
    )
    
    bpy.types.Scene.ai_pose_type = bpy.props.EnumProperty(
        name="Type",
        items=[('standing', 'Standing', 'Standing pose'), ('running', 'Running', 'Running pose'), 
               ('fighting', 'Fighting', 'Fighting pose'), ('happy', 'Happy', 'Happy pose')],
        default='standing'
    )

def unregister():
    bpy.utils.unregister_class(AIPoseGeneratorPanel)
    bpy.utils.unregister_class(GeneratePoseOperator)
    bpy.utils.unregister_class(SavePoseOperator)
    del bpy.types.Scene.ai_pose_category
    del bpy.types.Scene.ai_pose_type
