import bpy
from bpy.types import Panel, Operator

class AIAnimationPanel(Panel):
    """لوحة التحريك بالذكاء الاصطناعي"""
    bl_label = "🎬 AI Animation"
    bl_idname = "VIEW3D_PT_ai_animation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # قسم نوع الحركة
        box = layout.box()
        box.label(text="🎭 نوع الحركة", icon='ARMATURE_DATA')
        
        row = box.row()
        row.prop(scene, "ai_animation_type", text="")
        
        row = box.row()
        row.prop(scene, "ai_animation_frames", text="الإطارات")
        
        layout.separator()
        
        # قسم التوليد
        box = layout.box()
        box.label(text="⚡ توليد الحركة", icon='PLAY')
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("ai_animation.generate", 
                     text="Generate Animation", 
                     icon='RENDER_ANIMATION')
        
        layout.separator()
        
        # قسم التحسينات
        box = layout.box()
        box.label(text="🔧 تحسينات", icon='MODIFIER')
        
        row = box.row()
        row.operator("ai_animation.smooth", text="تنعيم", icon='SMOOTHCURVE')
        
        row = box.row()
        row.operator("ai_animation.mirror", text="عكس الحركة", icon='MOD_MIRROR')
        
        row = box.row()
        row.prop(scene, "ai_animation_mirror_side", text="الجانب")
        
        layout.separator()
        
        # قسم الاختصارات
        box = layout.box()
        box.label(text="⚡ اختصارات", icon='TIME')
        
        row = box.row(align=True)
        row.operator("ai_animation.quick_walk", text="مشي", icon='ANIM')
        row.operator("ai_animation.quick_run", text="جري", icon='ANIM')
        
        row = box.row(align=True)
        row.operator("ai_animation.quick_idle", text="خمول", icon='PAUSE')
        row.operator("ai_animation.quick_wave", text="تحية", icon='VIEW_HAND')

class GenerateAnimationOperator(Operator):
    """توليد حركة"""
    bl_idname = "ai_animation.generate"
    bl_label = "Generate Animation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "يرجى تحديد هيكل عظمي!")
            return {'CANCELLED'}
        
        anim_type = context.scene.ai_animation_type
        frames = context.scene.ai_animation_frames
        
        try:
            from ..ai_animation import AIAnimation
            animation = AIAnimation()
            
            if anim_type == 'walk':
                result = animation.create_walk_cycle(obj, frames)
            elif anim_type == 'run':
                result = animation.create_run_cycle(obj, frames)
            elif anim_type == 'idle':
                result = animation.create_idle_animation(obj, frames)
            elif anim_type == 'wave':
                result = animation.create_wave_animation(obj, frames)
            else:
                result = animation.create_walk_cycle(obj, frames)
            
            self.report({'INFO'}, f"✅ {result}")
        except Exception as e:
            self.report({'ERROR'}, f"❌ خطأ: {e}")
        
        return {'FINISHED'}

class SmoothAnimationOperator(Operator):
    """تنعيم الحركة"""
    bl_idname = "ai_animation.smooth"
    bl_label = "Smooth Animation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "يرجى تحديد هيكل عظمي!")
            return {'CANCELLED'}
        
        try:
            from ..ai_animation import AIAnimation
            animation = AIAnimation()
            animation.smooth_animation(obj)
            
            self.report({'INFO'}, "✅ تم تنعيم الحركة")
        except Exception as e:
            self.report({'ERROR'}, f"❌ خطأ: {e}")
        
        return {'FINISHED'}

class MirrorAnimationOperator(Operator):
    """عكس الحركة"""
    bl_idname = "ai_animation.mirror"
    bl_label = "Mirror Animation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "يرجى تحديد هيكل عظمي!")
            return {'CANCELLED'}
        
        side = context.scene.ai_animation_mirror_side
        
        try:
            from ..ai_animation import AIAnimation
            animation = AIAnimation()
            result = animation.mirror_animation(obj, side)
            
            self.report({'INFO'}, f"✅ {result}")
        except Exception as e:
            self.report({'ERROR'}, f"❌ خطأ: {e}")
        
        return {'FINISHED'}

class QuickWalkOperator(Operator):
    """حركة مشي سريعة"""
    bl_idname = "ai_animation.quick_walk"
    bl_label = "Quick Walk"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "يرجى تحديد هيكل عظمي!")
            return {'CANCELLED'}
        
        try:
            from ..ai_animation import AIAnimation
            animation = AIAnimation()
            animation.create_walk_cycle(obj, 24)
            self.report({'INFO'}, "✅ تم إنشاء حركة المشي")
        except Exception as e:
            self.report({'ERROR'}, f"❌ خطأ: {e}")
        
        return {'FINISHED'}

class QuickRunOperator(Operator):
    """حركة جري سريعة"""
    bl_idname = "ai_animation.quick_run"
    bl_label = "Quick Run"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "يرجى تحديد هيكل عظمي!")
            return {'CANCELLED'}
        
        try:
            from ..ai_animation import AIAnimation
            animation = AIAnimation()
            animation.create_run_cycle(obj, 16)
            self.report({'INFO'}, "✅ تم إنشاء حركة الجري")
        except Exception as e:
            self.report({'ERROR'}, f"❌ خطأ: {e}")
        
        return {'FINISHED'}

class QuickIdleOperator(Operator):
    """حركة خمول سريعة"""
    bl_idname = "ai_animation.quick_idle"
    bl_label = "Quick Idle"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "يرجى تحديد هيكل عظمي!")
            return {'CANCELLED'}
        
        try:
            from ..ai_animation import AIAnimation
            animation = AIAnimation()
            animation.create_idle_animation(obj, 120)
            self.report({'INFO'}, "✅ تم إنشاء حركة الخمول")
        except Exception as e:
            self.report({'ERROR'}, f"❌ خطأ: {e}")
        
        return {'FINISHED'}

class QuickWaveOperator(Operator):
    """حركة تحية سريعة"""
    bl_idname = "ai_animation.quick_wave"
    bl_label = "Quick Wave"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "يرجى تحديد هيكل عظمي!")
            return {'CANCELLED'}
        
        try:
            from ..ai_animation import AIAnimation
            animation = AIAnimation()
            animation.create_wave_animation(obj, 48)
            self.report({'INFO'}, "✅ تم إنشاء حركة التحية")
        except Exception as e:
            self.report({'ERROR'}, f"❌ خطأ: {e}")
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AIAnimationPanel)
    bpy.utils.register_class(GenerateAnimationOperator)
    bpy.utils.register_class(SmoothAnimationOperator)
    bpy.utils.register_class(MirrorAnimationOperator)
    bpy.utils.register_class(QuickWalkOperator)
    bpy.utils.register_class(QuickRunOperator)
    bpy.utils.register_class(QuickIdleOperator)
    bpy.utils.register_class(QuickWaveOperator)
    
    bpy.types.Scene.ai_animation_type = bpy.props.EnumProperty(
        name="نوع الحركة",
        items=[
            ('walk', 'مشي', 'دورة مشي'),
            ('run', 'جري', 'دورة جري'),
            ('idle', 'خمول', 'حركة تنفس/انتظار'),
            ('wave', 'تحية', 'حركة التلويح باليد'),
            ('jump', 'قفز', 'قفزة (قيد التطوير)'),
            ('dance', 'رقص', 'حركة رقص (قيد التطوير)'),
        ],
        default='walk'
    )
    
    bpy.types.Scene.ai_animation_frames = bpy.props.IntProperty(
        name="عدد الإطارات",
        default=24,
        min=1,
        max=500
    )
    
    bpy.types.Scene.ai_animation_mirror_side = bpy.props.EnumProperty(
        name="الجانب المصدر",
        items=[
            ('L', 'يسار', 'نسخ من اليسار إلى اليمين'),
            ('R', 'يمين', 'نسخ من اليمين إلى اليسار'),
        ],
        default='L'
    )

def unregister():
    bpy.utils.unregister_class(AIAnimationPanel)
    bpy.utils.unregister_class(GenerateAnimationOperator)
    bpy.utils.unregister_class(SmoothAnimationOperator)
    bpy.utils.unregister_class(MirrorAnimationOperator)
    bpy.utils.unregister_class(QuickWalkOperator)
    bpy.utils.unregister_class(QuickRunOperator)
    bpy.utils.unregister_class(QuickIdleOperator)
    bpy.utils.unregister_class(QuickWaveOperator)
    
    del bpy.types.Scene.ai_animation_type
    del bpy.types.Scene.ai_animation_frames
    del bpy.types.Scene.ai_animation_mirror_side
