import bpy
import math
from mathutils import Euler

class AIPoseGenerator:
    """توليد الأوضاع بالذكاء الاصطناعي"""
    
    def __init__(self):
        self.pose_categories = {
            'action': ['running', 'jumping', 'fighting', 'dancing'],
            'emotion': ['happy', 'sad', 'angry', 'surprised', 'relaxed'],
            'professional': ['standing', 'sitting', 'presenting', 'working'],
            'creative': ['floating', 'flying', 'superhero', 'yoga']
        }
    
    def generate_standing_pose(self, armature, style='neutral'):
        """وضعية وقوف"""
        bpy.context.view_layer.objects.active = armature
        pose_bones = armature.pose.bones
        
        for bone in pose_bones:
            bone.rotation_euler = Euler((0, 0, 0))
        
        # تعديلات بناءً على الأسلوب
        if style == 'confident':
            if 'spine_02' in pose_bones:
                pose_bones['spine_02'].rotation_euler.x = -0.1
            if 'upper_arm_L' in pose_bones:
                pose_bones['upper_arm_L'].rotation_euler.z = 0.2
            if 'upper_arm_R' in pose_bones:
                pose_bones['upper_arm_R'].rotation_euler.z = -0.2
        
        elif style == 'relaxed':
            if 'spine_02' in pose_bones:
                pose_bones['spine_02'].rotation_euler.x = 0.05
            if 'upper_arm_L' in pose_bones:
                pose_bones['upper_arm_L'].rotation_euler.z = 0.1
            if 'upper_arm_R' in pose_bones:
                pose_bones['upper_arm_R'].rotation_euler.z = -0.1
        
        return f"وضعية وقوف: {style}"
    
    def generate_action_pose(self, armature, action='fighting'):
        """وضعية حركة"""
        bpy.context.view_layer.objects.active = armature
        pose_bones = armature.pose.bones
        
        if action == 'fighting':
            # وضعية قتال
            if 'upper_arm_L' in pose_bones:
                pose_bones['upper_arm_L'].rotation_euler.z = 2.0
                pose_bones['upper_arm_L'].rotation_euler.x = -0.5
            if 'forearm_L' in pose_bones:
                pose_bones['forearm_L'].rotation_euler.z = 2.0
            if 'upper_arm_R' in pose_bones:
                pose_bones['upper_arm_R'].rotation_euler.z = -0.5
            if 'thigh_L' in pose_bones:
                pose_bones['thigh_L'].rotation_euler.x = -0.5
            if 'thigh_R' in pose_bones:
                pose_bones['thigh_R'].rotation_euler.x = 0.5
        
        elif action == 'superhero':
            # وضعية الطيران
            if 'root' in pose_bones:
                pose_bones['root'].rotation_euler.x = 1.0
            if 'upper_arm_L' in pose_bones:
                pose_bones['upper_arm_L'].rotation_euler.z = 2.5
            if 'upper_arm_R' in pose_bones:
                pose_bones['upper_arm_R'].rotation_euler.z = -2.5
        
        return f"وضعية: {action}"
    
    def save_pose(self, armature, name):
        """حفظ الوضعية"""
        pose_library = armature.pose_library
        if not pose_library:
            bpy.ops.poselib.new()
        
        bpy.ops.poselib.pose_add(name=name, frame=1)
        return name
    
    def blend_poses(self, armature, pose1, pose2, factor=0.5):
        """خلط وضعيتين"""
        # محاكاة الخلط
        return f"خلط {pose1} و {pose2} بنسبة {factor}"
