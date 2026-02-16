import bpy
from bpy.types import Panel, Operator

class AIAnimationPanel(Panel):
    """AI Animation Panel"""
    bl_label = "AI Animation"
    bl_idname = "VIEW3D_PT_ai_animation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Animation type section
        box = layout.box()
        box.label(text="Animation Type", icon='ARMATURE_DATA')
        
        row = box.row()
        row.prop(scene, "ai_animation_type", text="")
        
        row = box.row()
        row.prop(scene, "ai_animation_frames", text="Frames")
        
        layout.separator()
        
        # Generate section
        box = layout.box()
        box.label(text="Generate Animation", icon='PLAY')
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("ai_animation.generate", 
                     text="Generate Animation", 
                     icon='RENDER_ANIMATION')
        
        layout.separator()
        
        # Enhancements section
        box = layout.box()
        box.label(text="Enhancements", icon='MODIFIER')
        
        row = box.row()
        row.operator("ai_animation.smooth", text="Smooth", icon='SMOOTHCURVE')
        
        row = box.row()
        row.operator("ai_animation.mirror", text="Mirror", icon='MOD_MIRROR')
        
        row = box.row()
        row.prop(scene, "ai_animation_mirror_side", text="Side")
        
        layout.separator()
        
        # Quick actions section
        box = layout.box()
        box.label(text="Quick Actions", icon='TIME')
        
        row = box.row(align=True)
        row.operator("ai_animation.quick_walk", text="Walk", icon='ANIM')
        row.operator("ai_animation.quick_run", text="Run", icon='ANIM')
        
        row = box.row(align=True)
        row.operator("ai_animation.quick_idle", text="Idle", icon='PAUSE')
        row.operator("ai_animation.quick_wave", text="Wave", icon='VIEW_HAND')

class GenerateAnimationOperator(Operator):
    """Generate Animation"""
    bl_idname = "ai_animation.generate"
    bl_label = "Generate Animation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Please select an armature!")
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
            
            self.report({'INFO'}, f"Generated: {result}")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        
        return {'FINISHED'}

class SmoothAnimationOperator(Operator):
    """Smooth Animation"""
    bl_idname = "ai_animation.smooth"
    bl_label = "Smooth Animation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Please select an armature!")
            return {'CANCELLED'}
        
        try:
            from ..ai_animation import AIAnimation
            animation = AIAnimation()
            animation.smooth_animation(obj)
            
            self.report({'INFO'}, "Animation smoothed")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        
        return {'FINISHED'}

class MirrorAnimationOperator(Operator):
    """Mirror Animation"""
    bl_idname = "ai_animation.mirror"
    bl_label = "Mirror Animation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Please select an armature!")
            return {'CANCELLED'}
        
        side = context.scene.ai_animation_mirror_side
        
        try:
            from ..ai_animation import AIAnimation
            animation = AIAnimation()
            result = animation.mirror_animation(obj, side)
            
            self.report({'INFO'}, f"{result}")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        
        return {'FINISHED'}

class QuickWalkOperator(Operator):
    """Quick Walk"""
    bl_idname = "ai_animation.quick_walk"
    bl_label = "Quick Walk"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Please select an armature!")
            return {'CANCELLED'}
        
        try:
            from ..ai_animation import AIAnimation
            animation = AIAnimation()
            animation.create_walk_cycle(obj, 24)
            self.report({'INFO'}, "Walk animation created")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        
        return {'FINISHED'}

class QuickRunOperator(Operator):
    """Quick Run"""
    bl_idname = "ai_animation.quick_run"
    bl_label = "Quick Run"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Please select an armature!")
            return {'CANCELLED'}
        
        try:
            from ..ai_animation import AIAnimation
            animation = AIAnimation()
            animation.create_run_cycle(obj, 16)
            self.report({'INFO'}, "Run animation created")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        
        return {'FINISHED'}

class QuickIdleOperator(Operator):
    """Quick Idle"""
    bl_idname = "ai_animation.quick_idle"
    bl_label = "Quick Idle"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Please select an armature!")
            return {'CANCELLED'}
        
        try:
            from ..ai_animation import AIAnimation
            animation = AIAnimation()
            animation.create_idle_animation(obj, 120)
            self.report({'INFO'}, "Idle animation created")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        
        return {'FINISHED'}

class QuickWaveOperator(Operator):
    """Quick Wave"""
    bl_idname = "ai_animation.quick_wave"
    bl_label = "Quick Wave"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Please select an armature!")
            return {'CANCELLED'}
        
        try:
            from ..ai_animation import AIAnimation
            animation = AIAnimation()
            animation.create_wave_animation(obj, 48)
            self.report({'INFO'}, "Wave animation created")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        
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
        name="Animation Type",
        items=[
            ('walk', 'Walk', 'Walk cycle'),
            ('run', 'Run', 'Run cycle'),
            ('idle', 'Idle', 'Breathing/idle'),
            ('wave', 'Wave', 'Hand wave'),
            ('jump', 'Jump', 'Jump (coming soon)'),
            ('dance', 'Dance', 'Dance (coming soon)'),
        ],
        default='walk'
    )
    
    bpy.types.Scene.ai_animation_frames = bpy.props.IntProperty(
        name="Frames",
        default=24,
        min=1,
        max=500
    )
    
    bpy.types.Scene.ai_animation_mirror_side = bpy.props.EnumProperty(
        name="Source Side",
        items=[
            ('L', 'Left', 'Mirror from left to right'),
            ('R', 'Right', 'Mirror from right to left'),
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
