import bpy
from bpy.types import Panel, Operator

class AutoRiggingPanel(Panel):
    """لوحة تحكم Auto Rigging AI"""
    bl_label = "Auto Rigging AI"
    bl_idname = "VIEW3D_PT_auto_rigging_ai"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text="اختيار الشخصية:")
        row = layout.row()
        row.prop(context.scene, "auto_rigging_target")
        
        layout.separator()
        
        layout.label(text="نوع الرقمنة:")
        row = layout.row()
        row.prop(context.scene, "auto_rigging_type")
        
        layout.separator()
        
        row = layout.row()
        row.scale_y = 1.5
        row.operator("auto_rigging.generate", text="Generate Rig", icon='ARMATURE_DATA')

class GenerateRigOperator(Operator):
    """توليد الهيكل العظمي"""
    bl_idname = "auto_rigging.generate"
    bl_label = "Generate Rig"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selected = context.selected_objects
        if not selected:
            self.report({'ERROR'}, "Please select a mesh object!")
            return {'CANCELLED'}
        
        rig_type = context.scene.auto_rigging_type
        self.report({'INFO'}, f"Generating {rig_type} rig...")
        
        # هنا سيكون منطق توليد الهيكل العظمي
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AutoRiggingPanel)
    bpy.utils.register_class(GenerateRigOperator)
    
    bpy.types.Scene.auto_rigging_target = bpy.props.StringProperty(
        name="Target",
        default="Selected Object"
    )
    
    bpy.types.Scene.auto_rigging_type = bpy.props.EnumProperty(
        name="Rig Type",
        items=[
            ('humanoid', 'Humanoid', 'Human character rig'),
            ('quadruped', 'Quadruped', '4-legged animal rig'),
            ('bird', 'Bird', 'Bird/winged rig'),
            ('custom', 'Custom', 'Custom rig')
        ],
        default='humanoid'
    )

def unregister():
    bpy.utils.unregister_class(AutoRiggingPanel)
    bpy.utils.unregister_class(GenerateRigOperator)
    del bpy.types.Scene.auto_rigging_target
    del bpy.types.Scene.auto_rigging_type
