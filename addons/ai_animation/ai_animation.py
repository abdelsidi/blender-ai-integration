import bpy
import math
from mathutils import Vector, Quaternion, Euler
from datetime import datetime

class AIAnimation:
    """نظام التحريك التلقائي بالذكاء الاصطناعي"""
    
    def __init__(self):
        self.animations = {
            'walk': 'Walking',
            'run': 'Running',
            'idle': 'Idle',
            'jump': 'Jumping',
            'dance': 'Dancing',
            'wave': 'Waving',
            'sit': 'Sitting',
            'attack': 'Attack'
        }
    
    def create_walk_cycle(self, armature, frames=24):
        """إنشاء دورة مشي"""
        bpy.context.view_layer.objects.active = armature
        
        # إعداد الإطارات
        start_frame = bpy.context.scene.frame_current
        end_frame = start_frame + frames
        
        # الحصول على عظام Pose
        pose_bones = armature.pose.bones
        
        # دورة مشي بسيطة
        for frame in range(start_frame, end_frame + 1):
            bpy.context.scene.frame_set(frame)
            
            progress = (frame - start_frame) / frames
            angle = progress * 2 * math.pi
            
            # تحريك الأرجل
            if 'thigh_L' in pose_bones:
                pose_bones['thigh_L'].rotation_euler.x = math.sin(angle) * 0.5
            if 'thigh_R' in pose_bones:
                pose_bones['thigh_R'].rotation_euler.x = math.sin(angle + math.pi) * 0.5
            
            if 'shin_L' in pose_bones:
                pose_bones['shin_L'].rotation_euler.x = max(0, math.sin(angle + math.pi/2) * 0.8)
            if 'shin_R' in pose_bones:
                pose_bones['shin_R'].rotation_euler.x = max(0, math.sin(angle + math.pi * 1.5) * 0.8)
            
            # تحريك الذراعين (عكس الأرجل)
            if 'upper_arm_L' in pose_bones:
                pose_bones['upper_arm_L'].rotation_euler.x = math.sin(angle + math.pi) * 0.3
            if 'upper_arm_R' in pose_bones:
                pose_bones['upper_arm_R'].rotation_euler.x = math.sin(angle) * 0.3
            
            # ارتداد الجذع
            if 'root' in pose_bones:
                pose_bones['root'].location.z = abs(math.sin(angle * 2)) * 0.05
            
            # إضافة keyframes
            for bone in pose_bones:
                bone.keyframe_insert(data_path="rotation_euler", frame=frame)
                bone.keyframe_insert(data_path="location", frame=frame)
        
        # إعادة تعيين الإطار
        bpy.context.scene.frame_set(start_frame)
        
        return f"تم إنشاء دورة مشي من {start_frame} إلى {end_frame}"
    
    def create_run_cycle(self, armature, frames=16):
        """إنشاء دورة جري"""
        bpy.context.view_layer.objects.active = armature
        
        start_frame = bpy.context.scene.frame_current
        end_frame = start_frame + frames
        
        pose_bones = armature.pose.bones
        
        for frame in range(start_frame, end_frame + 1):
            bpy.context.scene.frame_set(frame)
            
            progress = (frame - start_frame) / frames
            angle = progress * 2 * math.pi
            
            # تحريك الأرجل (أكثر حدة من المشي)
            if 'thigh_L' in pose_bones:
                pose_bones['thigh_L'].rotation_euler.x = math.sin(angle) * 0.8
            if 'thigh_R' in pose_bones:
                pose_bones['thigh_R'].rotation_euler.x = math.sin(angle + math.pi) * 0.8
            
            if 'shin_L' in pose_bones:
                pose_bones['shin_L'].rotation_euler.x = max(0, math.sin(angle + math.pi/2) * 1.2)
            if 'shin_R' in pose_bones:
                pose_bones['shin_R'].rotation_euler.x = max(0, math.sin(angle + math.pi * 1.5) * 1.2)
            
            # تحريك الذراعين
            if 'upper_arm_L' in pose_bones:
                pose_bones['upper_arm_L'].rotation_euler.x = math.sin(angle + math.pi) * 0.6
            if 'upper_arm_R' in pose_bones:
                pose_bones['upper_arm_R'].rotation_euler.x = math.sin(angle) * 0.6
            
            # ارتداد أعلى
            if 'root' in pose_bones:
                pose_bones['root'].location.z = abs(math.sin(angle * 2)) * 0.1
            
            for bone in pose_bones:
                bone.keyframe_insert(data_path="rotation_euler", frame=frame)
                bone.keyframe_insert(data_path="location", frame=frame)
        
        bpy.context.scene.frame_set(start_frame)
        
        return f"تم إنشاء دورة جري من {start_frame} إلى {end_frame}"
    
    def create_idle_animation(self, armature, frames=120):
        """إنشاء حركة خاملة (تنفس)"""
        bpy.context.view_layer.objects.active = armature
        
        start_frame = bpy.context.scene.frame_current
        end_frame = start_frame + frames
        
        pose_bones = armature.pose.bones
        
        for frame in range(start_frame, end_frame + 1):
            bpy.context.scene.frame_set(frame)
            
            progress = (frame - start_frame) / frames
            angle = progress * 2 * math.pi
            
            # حركة تنفس خفيفة
            if 'spine_02' in pose_bones:
                pose_bones['spine_02'].rotation_euler.x = math.sin(angle * 2) * 0.05
            
            if 'spine_03' in pose_bones:
                pose_bones['spine_03'].rotation_euler.x = math.sin(angle * 2) * 0.03
            
            if 'root' in pose_bones:
                # ارتفاع الجذع مع التنفس
                pose_bones['root'].location.z = math.sin(angle * 2) * 0.02
            
            # حركة خفيفة للذراعين
            if 'upper_arm_L' in pose_bones:
                pose_bones['upper_arm_L'].rotation_euler.z = math.sin(angle + math.pi/4) * 0.02
            if 'upper_arm_R' in pose_bones:
                pose_bones['upper_arm_R'].rotation_euler.z = -math.sin(angle + math.pi/4) * 0.02
            
            for bone in pose_bones:
                bone.keyframe_insert(data_path="rotation_euler", frame=frame)
                bone.keyframe_insert(data_path="location", frame=frame)
        
        bpy.context.scene.frame_set(start_frame)
        
        return f"تم إنشاء حركة الخمول من {start_frame} إلى {end_frame}"
    
    def create_wave_animation(self, armature, frames=48):
        """إنشاء حركة التحية"""
        bpy.context.view_layer.objects.active = armature
        
        start_frame = bpy.context.scene.frame_current
        end_frame = start_frame + frames
        
        pose_bones = armature.pose.bones
        
        for frame in range(start_frame, end_frame + 1):
            bpy.context.scene.frame_set(frame)
            
            progress = (frame - start_frame) / frames
            
            # رفع الذراع
            if 'upper_arm_R' in pose_bones:
                if progress < 0.2:
                    # رفع
                    pose_bones['upper_arm_R'].rotation_euler.z = progress * 5 * (math.pi / 2)
                elif progress < 0.8:
                    # التلويح
                    wave_progress = (progress - 0.2) / 0.6
                    pose_bones['upper_arm_R'].rotation_euler.z = (math.pi / 2) + math.sin(wave_progress * math.pi * 4) * 0.3
                    if 'forearm_R' in pose_bones:
                        pose_bones['forearm_R'].rotation_euler.z = math.sin(wave_progress * math.pi * 4) * 0.5
                else:
                    # إنزال
                    lower_progress = (progress - 0.8) / 0.2
                    pose_bones['upper_arm_R'].rotation_euler.z = (math.pi / 2) * (1 - lower_progress)
            
            for bone in pose_bones:
                bone.keyframe_insert(data_path="rotation_euler", frame=frame)
        
        bpy.context.scene.frame_set(start_frame)
        
        return f"تم إنشاء حركة التحية من {start_frame} إلى {end_frame}"
    
    def smooth_animation(self, armature):
        """تنعيم الحركة باستخدام F-Curves"""
        if not armature.animation_data:
            return
        
        action = armature.animation_data.action
        if not action:
            return
        
        for fcurve in action.fcurves:
            # تنعيم المنحنيات
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = 'BEZIER'
                keyframe.easing = 'AUTO'
    
    def mirror_animation(self, armature, side='L'):
 """عكس الحركة من جانب إلى آخر"""
        bpy.context.view_layer.objects.active = armature
        
        if not armature.animation_data or not armature.animation_data.action:
            return "لا توجد حركة لعكسها"
        
        action = armature.animation_data.action
        
        source_side = side
        target_side = 'R' if side == 'L' else 'L'
        
        # نسخ keyframes من جانب إلى آخر
        for fcurve in action.fcurves:
            if source_side in fcurve.data_path:
                new_path = fcurve.data_path.replace(f'_{source_side}_', f'_{target_side}_')
                
                # العثور على أو إنشاء F-curve للجانب المستهدف
                target_fcurve = None
                for fc in action.fcurves:
                    if fc.data_path == new_path and fc.array_index == fcurve.array_index:
                        target_fcurve = fc
                        break
                
                if not target_fcurve:
                    target_fcurve = action.fcurves.new(data_path=new_path, index=fcurve.array_index)
                
                # نسخ النقاط
                for keyframe in fcurve.keyframe_points:
                    target_fcurve.keyframe_points.insert(
                        frame=keyframe.co.x,
                        value=keyframe.co.y
                    )
        
        return f"تم عكس الحركة من {source_side} إلى {target_side}"
