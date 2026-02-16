import bpy
import bmesh
from mathutils import Vector, Matrix
from datetime import datetime

class AutoRiggingAI:
    """نظام الرقمنة التلقائية بالذكاء الاصطناعي"""
    
    def __init__(self):
        self.rig_types = {
            'human': 'Humanoid',
            'quadruped': 'Four-legged',
            'bird': 'Bird',
            'spider': 'Spider/Multi-legged',
            'custom': 'Custom'
        }
        self.current_type = 'human'
    
    def analyze_mesh(self, obj):
        """تحليل الشبكة لتحديد أماكن المفاصل"""
        mesh = obj.data
        
        # الحصول على حدود الكائن
        bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        min_z = min(v.z for v in bbox)
        max_z = max(v.z for v in bbox)
        height = max_z - min_z
        
        # تحديد المناطق المحتملة للمفاصل
        joints = {
            'root': Vector((0, 0, min_z)),
            'spine': [],
            'neck': Vector((0, 0, max_z - height * 0.1)),
            'head': Vector((0, 0, max_z)),
            'arms': [],
            'legs': []
        }
        
        # تحليل الرؤوس للعثور على أماكن المفاصل
        for vert in mesh.vertices:
            world_pos = obj.matrix_world @ vert.co
            
            # العمود الفقري
            if abs(world_pos.x) < 0.1 and abs(world_pos.y) < 0.1:
                if min_z + height * 0.3 < world_pos.z < max_z - height * 0.2:
                    joints['spine'].append(world_pos)
            
            # الذراعين
            if world_pos.z > min_z + height * 0.5:
                if abs(world_pos.x) > 0.3:
                    joints['arms'].append(world_pos)
            
            # الأرجل
            if world_pos.z < min_z + height * 0.5:
                if abs(world_pos.x) > 0.2:
                    joints['legs'].append(world_pos)
        
        return joints
    
    def create_human_rig(self, obj):
        """إنشاء هيكل عظمي بشري"""
        bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        min_z = min(v.z for v in bbox)
        max_z = max(v.z for v in bbox)
        center_x = (min(v.x for v in bbox) + max(v.x for v in bbox)) / 2
        center_y = (min(v.y for v in bbox) + max(v.y for v in bbox)) / 2
        height = max_z - min_z
        
        # إنشاء Armature
        bpy.ops.object.armature_add(enter_editmode=True, location=(center_x, center_y, min_z))
        armature = bpy.context.active_object
        armature.name = f"{obj.name}_Rig"
        
        # الحصول على البيانات
        edit_bones = armature.data.edit_bones
        
        # مسح العظم الافتراضي
        for bone in edit_bones:
            edit_bones.remove(bone)
        
        # إنشاء العمود الفقري
        spine_bones = []
        spine_positions = [
            ('root', Vector((center_x, center_y, min_z))),
            ('spine_01', Vector((center_x, center_y, min_z + height * 0.25))),
            ('spine_02', Vector((center_x, center_y, min_z + height * 0.45))),
            ('spine_03', Vector((center_x, center_y, min_z + height * 0.65))),
            ('neck', Vector((center_x, center_y, min_z + height * 0.8))),
            ('head', Vector((center_x, center_y, max_z))),
        ]
        
        prev_bone = None
        for name, pos in spine_positions:
            bone = edit_bones.new(name)
            bone.head = pos
            bone.tail = pos + Vector((0, 0, height * 0.05))
            if prev_bone:
                bone.parent = prev_bone
                bone.use_connect = True
            spine_bones.append(bone)
            prev_bone = bone
        
        # إنشاء الذراعين
        arm_bones = []
        for side in ['L', 'R']:
            sign = 1 if side == 'L' else -1
            shoulder_pos = Vector((center_x + sign * height * 0.15, center_y, min_z + height * 0.75))
            
            # الكتف
            shoulder = edit_bones.new(f'shoulder_{side}')
            shoulder.head = shoulder_pos
            shoulder.tail = shoulder_pos + Vector((sign * height * 0.1, 0, -height * 0.05))
            shoulder.parent = spine_bones[3]  # spine_03
            
            # العلوي
            upper_arm = edit_bones.new(f'upper_arm_{side}')
            upper_arm.head = shoulder.tail
            upper_arm.tail = shoulder.tail + Vector((sign * height * 0.15, 0, -height * 0.15))
            upper_arm.parent = shoulder
            upper_arm.use_connect = True
            
            # السفلي
            forearm = edit_bones.new(f'forearm_{side}')
            forearm.head = upper_arm.tail
            forearm.tail = upper_arm.tail + Vector((sign * height * 0.15, 0, -height * 0.15))
            forearm.parent = upper_arm
            forearm.use_connect = True
            
            # اليد
            hand = edit_bones.new(f'hand_{side}')
            hand.head = forearm.tail
            hand.tail = forearm.tail + Vector((sign * height * 0.08, 0, 0))
            hand.parent = forearm
            hand.use_connect = True
            
            arm_bones.extend([shoulder, upper_arm, forearm, hand])
        
        # إنشاء الأرجل
        leg_bones = []
        for side in ['L', 'R']:
            sign = 1 if side == 'L' else -1
            hip_pos = Vector((center_x + sign * height * 0.08, center_y, min_z + height * 0.45))
            
            # الورك
            hip = edit_bones.new(f'hip_{side}')
            hip.head = hip_pos
            hip.tail = hip_pos + Vector((0, 0, -height * 0.05))
            hip.parent = spine_bones[0]  # root
            
            # الفخذ
            thigh = edit_bones.new(f'thigh_{side}')
            thigh.head = hip.tail
            thigh.tail = hip.tail + Vector((sign * height * 0.05, 0, -height * 0.25))
            thigh.parent = hip
            thigh.use_connect = True
            
            # الساق
            shin = edit_bones.new(f'shin_{side}')
            shin.head = thigh.tail
            shin.tail = thigh.tail + Vector((0, 0, -height * 0.25))
            shin.parent = thigh
            shin.use_connect = True
            
            # القدم
            foot = edit_bones.new(f'foot_{side}')
            foot.head = shin.tail
            foot.tail = shin.tail + Vector((0, height * 0.15, 0))
            foot.parent = shin
            foot.use_connect = True
            
            leg_bones.extend([hip, thigh, shin, foot])
        
        # الخروج من وضع التحرير
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # ربط الشبكة بالهيكل العظمي
        self.bind_mesh_to_armature(obj, armature)
        
        return armature
    
    def create_quadruped_rig(self, obj):
        """إنشاء هيكل عظمي رباعي الأرجل"""
        bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        min_z = min(v.z for v in bbox)
        max_z = max(v.z for v in bbox)
        center_x = (min(v.x for v in bbox) + max(v.x for v in bbox)) / 2
        center_y = (min(v.y for v in bbox) + max(v.y for v in bbox)) / 2
        height = max_z - min_z
        length = max(v.y for v in bbox) - min(v.y for v in bbox)
        
        bpy.ops.object.armature_add(enter_editmode=True, location=(center_x, center_y, min_z))
        armature = bpy.context.active_object
        armature.name = f"{obj.name}_Rig"
        
        edit_bones = armature.data.edit_bones
        for bone in list(edit_bones):
            edit_bones.remove(bone)
        
        # العمود الفقري
        spine_positions = [
            ('root', Vector((center_x, center_y - length * 0.3, min_z + height * 0.4))),
            ('spine_01', Vector((center_x, center_y - length * 0.1, min_z + height * 0.5))),
            ('spine_02', Vector((center_x, center_y + length * 0.1, min_z + height * 0.5))),
            ('spine_03', Vector((center_x, center_y + length * 0.25, min_z + height * 0.55))),
            ('neck', Vector((center_x, center_y + length * 0.35, min_z + height * 0.7))),
            ('head', Vector((center_x, center_y + length * 0.4, min_z + height * 0.85))),
        ]
        
        prev_bone = None
        for name, pos in spine_positions:
            bone = edit_bones.new(name)
            bone.head = pos
            bone.tail = pos + Vector((0, length * 0.05, 0))
            if prev_bone:
                bone.parent = prev_bone
                bone.use_connect = True
            prev_bone = bone
        
        # الأرجل الأمامية والخلفية (4 أرجل)
        leg_positions = [
            ('front_left', Vector((center_x - height * 0.15, center_y + length * 0.25, min_z + height * 0.4))),
            ('front_right', Vector((center_x + height * 0.15, center_y + length * 0.25, min_z + height * 0.4))),
            ('back_left', Vector((center_x - height * 0.15, center_y - length * 0.25, min_z + height * 0.4))),
            ('back_right', Vector((center_x + height * 0.15, center_y - length * 0.25, min_z + height * 0.4))),
        ]
        
        for leg_name, start_pos in leg_positions:
            # الفخذ
            thigh = edit_bones.new(f'{leg_name}_thigh')
            thigh.head = start_pos
            thigh.tail = start_pos + Vector((0, 0, -height * 0.2))
            
            # الساق
            shin = edit_bones.new(f'{leg_name}_shin')
            shin.head = thigh.tail
            shin.tail = thigh.tail + Vector((0, 0, -height * 0.2))
            shin.parent = thigh
            shin.use_connect = True
            
            # القدم
            foot = edit_bones.new(f'{leg_name}_foot')
            foot.head = shin.tail
            foot.tail = shin.tail + Vector((0, height * 0.08, 0))
            foot.parent = shin
            foot.use_connect = True
        
        # الذيل
        tail = edit_bones.new('tail')
        tail.head = Vector((center_x, center_y - length * 0.35, min_z + height * 0.4))
        tail.tail = tail.head + Vector((0, -length * 0.15, height * 0.1))
        
        bpy.ops.object.mode_set(mode='OBJECT')
        self.bind_mesh_to_armature(obj, armature)
        
        return armature
    
    def bind_mesh_to_armature(self, mesh_obj, armature_obj):
        """ربط الشبكة بالهيكل العظمي"""
        # إضافة معدل Armature
        modifier = mesh_obj.modifiers.new(name="Armature", type='ARMATURE')
        modifier.object = armature_obj
        
        # تفعيل الأوزان التلقائية
        bpy.context.view_layer.objects.active = mesh_obj
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    
    def add_ik_constraints(self, armature):
        """إضافة قيود العكسية الحركية (IK)"""
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bones = armature.pose.bones
        
        # إضافة IK للأرجل
        for side in ['L', 'R']:
            foot_name = f'foot_{side}'
            if foot_name in pose_bones:
                foot = pose_bones[foot_name]
                ik_constraint = foot.constraints.new(type='IK')
                ik_constraint.target = armature
                ik_constraint.subtarget = f'shin_{side}'
                ik_constraint.chain_count = 2
        
        bpy.ops.object.mode_set(mode='OBJECT')
