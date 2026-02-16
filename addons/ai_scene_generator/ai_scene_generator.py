import bpy
import random
from mathutils import Vector

class AISceneGenerator:
    """توليد المشاهد بالذكاء الاصطناعي"""
    
    def __init__(self):
        self.scene_types = {
            'nature': ['forest', 'desert', 'mountain', 'ocean', 'garden'],
            'urban': ['city', 'street', 'interior', 'office', 'room'],
            'fantasy': ['castle', 'dungeon', 'space', 'alien', 'magical'],
            'studio': ['photo_studio', 'stage', 'gallery', 'showroom']
        }
    
    def generate_nature_scene(self, scene_type='forest', complexity='medium'):
        """توليد مشهد طبيعة"""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        # إضافة أرضية
        bpy.ops.mesh.primitive_plane_add(size=50, location=(0, 0, 0))
        ground = bpy.context.active_object
        ground.name = "Ground"
        
        # إضافة أشجار
        tree_count = 10 if complexity == 'low' else 30 if complexity == 'medium' else 60
        
        for i in range(tree_count):
            x = random.uniform(-20, 20)
            y = random.uniform(-20, 20)
            
            # جذع
            bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=3, location=(x, y, 1.5))
            trunk = bpy.context.active_object
            trunk.name = f"Tree_Trunk_{i}"
            
            # أوراق
            bpy.ops.mesh.primitive_ico_sphere_add(radius=1.5, location=(x, y, 3.5))
            leaves = bpy.context.active_object
            leaves.name = f"Tree_Leaves_{i}"
        
        # إضافة إضاءة
        bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
        sun = bpy.context.active_object
        sun.data.energy = 5
        
        return f"مشهد {scene_type} مع {tree_count} شجرة"
    
    def generate_studio_scene(self, style='photo_studio'):
        """توليد استوديو"""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        # خلفية لانهائية
        bpy.ops.mesh.primitive_plane_add(size=50, location=(0, 0, 0))
        backdrop = bpy.context.active_object
        backdrop.name = "Backdrop"
        
        # منحنى الخلفية
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        
        # إضاءات الاستوديو
        # Key Light
        bpy.ops.object.light_add(type='AREA', location=(5, -5, 8))
        key_light = bpy.context.active_object
        key_light.data.energy = 1000
        key_light.data.size = 3
        
        # Fill Light
        bpy.ops.object.light_add(type='AREA', location=(-5, -3, 5))
        fill_light = bpy.context.active_object
        fill_light.data.energy = 500
        fill_light.data.size = 2
        
        # Rim Light
        bpy.ops.object.light_add(type='SPOT', location=(0, 10, 8))
        rim_light = bpy.context.active_object
        rim_light.data.energy = 800
        rim_light.data.spot_size = 1.0
        
        return f"استوديو {style} مع إضاءة احترافية"
    
    def setup_camera(self, target=None, angle='three_quarter'):
        """إعداد الكاميرا"""
        bpy.ops.object.camera_add(location=(7, -7, 5))
        camera = bpy.context.active_object
        camera.name = "AI_Camera"
        
        # توجيه الكاميرا
        if target:
            direction = target.location - camera.location
            camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        else:
            camera.rotation_euler = (1.1, 0, 0.785)
        
        bpy.context.scene.camera = camera
        return camera
    
    def add_preset_composition(self, composition='rule_of_thirds'):
        """إضافة قواعد التكوين"""
        # إضافة خطوط الإرشاد
        bpy.context.scene.render.use_border = False
        
        if composition == 'rule_of_thirds':
            # تفعيل خطوط الثلث
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.overlay.show_gizmo = True
        
        return composition
