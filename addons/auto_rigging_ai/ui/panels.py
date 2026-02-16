import bpy
from bpy.types import Panel, Operator

class AutoRiggingPanel(Panel):
    """لوحة الرقمنة التلقائية"""
    bl_label = "🦴 Auto Rigging AI"
    bl_idname = "VIEW3D_PT_auto_rigging_ai"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # قسم التحليل
        box = layout.box()
        box.label(text="🔍 تحليل الشخصية", icon='VIEWZOOM')
        
        row = box.row()
        row.operator("auto_rigging.analyze", text="تحليل الشبكة", icon='MESH_DATA')
        
        if scene.auto_rigging_analysis:
            col = box.column()
            col.label(text=scene.auto_rigging_analysis, icon='INFO')
        
        layout.separator()
        
        # قسم نوع الشخصية
        box = layout.box()
        box.label(text="🎯 نوع الشخصية", icon='ARMATURE_DATA')
        
        row = box.row()
        row.prop(scene, "auto_rigging_type", text="")
        
        layout.separator()
        
        # قسم إنشاء الهيكل
        box = layout.box()
        box.label(text="⚡ إنشاء الهيكل العظمي", icon='BONE_DATA')
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("auto_rigging.generate", 
                     text="Generate Rig", 
                     icon='OUTLINER_OB_ARMATURE')
        
        layout.separator()
        
        # خيارات إضافية
        box = layout.box()
        box.label(text="⚙️ خيارات", icon='PREFERENCES')
        
        row = box.row()
        row.prop(scene, "auto_rigging_add_ik", text="إضافة IK")
        
        row = box.row()
        row.prop(scene, "auto_rigging_auto_bind", text="ربط تلقائي")

class AnalyzeMeshOperator(Operator):
    """تحليل شبكة الشخصية"""
    bl_idname = "auto_rigging.analyze"
    bl_label = "Analyze Character Mesh"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "يرجى تحديد كائن شبكة!")
            return {'CANCELLED'}
        
        try:
            from ..auto_rigging_ai import AutoRiggingAI
            rigging = AutoRiggingAI()
            joints = rigging.analyze_mesh(obj)
            
            analysis = f"الرؤوس: {len(obj.data.vertices)} | المفاصل المحتملة: {len(joints)}"
            context.scene.auto_rigging_analysis = analysis
            
            self.report({'INFO'}, f"✅ تم العثور على {len(joints)} منطقة محتملة")
        except Exception as e:
            self.report({'ERROR'}, f"❌ خطأ: {e}")
        
        return {'FINISHED'}

class GenerateRigOperator(Operator):
    """إنشاء الهيكل العظمي"""
    bl_idname = "auto_rigging.generate"
    bl_label = "Generate Rig"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "يرجى تحديد كائن شبكة!")
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
                self.report({'WARNING'}, "هذا النوع قيد التطوير، سيتم استخدام النوع البشري")
                armature = rigging.create_human_rig(obj)
            
            # إضافة IK إذا كان مفعلاً
            if context.scene.auto_rigging_add_ik:
                rigging.add_ik_constraints(armature)
            
            self.report({'INFO'}, f"✅ تم إنشاء الهيكل: {armature.name}")
        except Exception as e:
            self.report({'ERROR'}, f"❌ فشل الإنشاء: {e}")
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AutoRiggingPanel)
    bpy.utils.register_class(AnalyzeMeshOperator)
    bpy.utils.register_class(GenerateRigOperator)
    
    bpy.types.Scene.auto_rigging_type = bpy.props.EnumProperty(
        name="نوع الشخصية",
        items=[
            ('human', 'بشري', 'شخصية بشرية'),
            ('quadruped', 'رباعي', 'حيوان رباعي الأرجل'),
            ('bird', 'طائر', 'طائر (قيد التطوير)'),
            ('spider', 'عنكبوت', 'عنكبوت (قيد التطوير)'),
            ('custom', 'مخصص', 'مخصص (قيد التطوير)'),
        ],
        default='human'
    )
    
    bpy.types.Scene.auto_rigging_add_ik = bpy.props.BoolProperty(
        name="إضافة IK",
        description="إضافة قيود العكسية الحركية",
        default=True
    )
    
    bpy.types.Scene.auto_rigging_auto_bind = bpy.props.BoolProperty(
        name="ربط تلقائي",
        description="ربط الشبكة بالهيكل تلقائياً",
        default=True
    )
    
    bpy.types.Scene.auto_rigging_analysis = bpy.props.StringProperty(
        name="نتائج التحليل",
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
