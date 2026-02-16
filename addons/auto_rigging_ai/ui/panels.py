import bpy
from bpy.types import Panel, Operator

class AutoRiggingPanel(Panel):
    """Auto Rigging Panel"""
    bl_label = "Auto Rigging AI"
    bl_idname = "VIEW3D_PT_auto_rigging_ai"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Analysis section
        box = layout.box()
        box.label(text="Character Analysis", icon='VIEWZOOM')
        
        row = box.row()
        row.operator("auto_rigging.analyze", text="Analyze Mesh", icon='MESH_DATA')
        
        if scene.auto_rigging_analysis:
            col = box.column()
            col.label(text=scene.auto_rigging_analysis, icon='INFO')
        
        layout.separator()
        
        # Character type section
        box = layout.box()
        box.label(text="Character Type", icon='ARMATURE_DATA')
        
        row = box.row()
        row.prop(scene, "auto_rigging_type", text="")
        
        layout.separator()
        
        # Rig creation section
        box = layout.box()
        box.label(text="Create Rig", icon='BONE_DATA')
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("auto_rigging.generate", 
                     text="Generate Rig", 
                     icon='OUTLINER_OB_ARMATURE')
        
        layout.separator()
        
        # Options section
        box = layout.box()
        box.label(text="Options", icon='PREFERENCES')
        
        row = box.row()
        row.prop(scene, "auto_rigging_add_ik", text="Add IK")
        
        row = box.row()
        row.prop(scene, "auto_rigging_auto_bind", text="Auto Bind")

class AnalyzeMeshOperator(Operator):
    """Analyze Character Mesh"""
    bl_idname = "auto_rigging.analyze"
    bl_label = "Analyze Character Mesh"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Please select a mesh object!")
            return {'CANCELLED'}
        
        try:
            from ..auto_rigging_ai import AutoRiggingAI
            rigging = AutoRiggingAI()
            joints = rigging.analyze_mesh(obj)
            
            analysis = f"Vertices: {len(obj.data.vertices)} | Joints: {len(joints)}"
            context.scene.auto_rigging_analysis = analysis
            
            self.report({'INFO'}, f"Found {len(joints)} potential joints")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        
        return {'FINISHED'}

class GenerateRigOperator(Operator):
    """Generate Rig"""
    bl_idname = "auto_rigging.generate"
    bl_label = "Generate Rig"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Please select a mesh object!")
            return {'CANCELLED'}
        
        rig_type = context.scene.auto_rigging_type
        
        try:
            from ..auto_rigging_ai import AutoRiggingAI
            rigging = AutoRiggingAI()
            
            if rig_type == 'human':
                armature = rigging.create_human_rig(obj)
            elif rig_type == 'quadruped':
                armature = rigging.create_quadruped_rig(obj)
            else:
                self.report({'WARNING'}, "Type in development, using human")
                armature = rigging.create_human_rig(obj)
            
            # Add IK if enabled
            if context.scene.auto_rigging_add_ik:
                rigging.add_ik_constraints(armature)
            
            self.report({'INFO'}, f"Rig created: {armature.name}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed: {e}")
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AutoRiggingPanel)
    bpy.utils.register_class(AnalyzeMeshOperator)
    bpy.utils.register_class(GenerateRigOperator)
    
    bpy.types.Scene.auto_rigging_type = bpy.props.EnumProperty(
        name="Character Type",
        items=[
            ('human', 'Human', 'Human character'),
            ('quadruped', 'Quadruped', 'Four-legged animal'),
            ('bird', 'Bird', 'Bird (coming soon)'),
            ('spider', 'Spider', 'Spider (coming soon)'),
            ('custom', 'Custom', 'Custom (coming soon)'),
        ],
        default='human'
    )
    
    bpy.types.Scene.auto_rigging_add_ik = bpy.props.BoolProperty(
        name="Add IK",
        description="Add inverse kinematics constraints",
        default=True
    )
    
    bpy.types.Scene.auto_rigging_auto_bind = bpy.props.BoolProperty(
        name="Auto Bind",
        description="Automatically bind mesh to armature",
        default=True
    )
    
    bpy.types.Scene.auto_rigging_analysis = bpy.props.StringProperty(
        name="Analysis Results",
        default=""
    )

def unregister():
    bpy.utils.unregister_class(AutoRiggingPanel)
    bpy.utils.unregister_class(AnalyzeMeshOperator)
    bpy.utils.unregister_class(GenerateRigOperator)
    
    del bpy.types.Scene.auto_rigging_type
    del bpy.types.Scene.auto_rigging_add_ik
    del bpy.types.Scene.auto_rigging_auto_bind
    del bpy.types.Scene.auto_rigging_analysis
