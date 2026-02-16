import bpy
import bmesh
from mathutils import Vector

class AIRenderOptimizer:
    """محسن الرندر بالذكاء الاصطناعي"""
    
    def __init__(self):
        self.render_presets = {
            'draft': {'samples': 32, 'resolution': 50, 'denoise': False},
            'preview': {'samples': 128, 'resolution': 75, 'denoise': True},
            'production': {'samples': 512, 'resolution': 100, 'denoise': True},
            'cinematic': {'samples': 2048, 'resolution': 100, 'denoise': True, 'motion_blur': True},
        }
    
    def analyze_scene_complexity(self, scene):
        """تحليل تعقيد المشهد"""
        stats = {
            'objects': len(scene.objects),
            'meshes': len([obj for obj in scene.objects if obj.type == 'MESH']),
            'lights': len([obj for obj in scene.objects if obj.type == 'LIGHT']),
            'vertices': 0,
            'materials': len(bpy.data.materials),
            'complexity_score': 0
        }
        
        # حساب عدد الرؤوس
        for obj in scene.objects:
            if obj.type == 'MESH' and obj.data:
                stats['vertices'] += len(obj.data.vertices)
        
        # حساب درجة التعقيد
        stats['complexity_score'] = (
            stats['objects'] * 1 +
            stats['meshes'] * 2 +
            stats['lights'] * 3 +
            stats['vertices'] / 1000 +
            stats['materials'] * 2
        )
        
        return stats
    
    def optimize_settings(self, scene, quality_level='production'):
        """تحسين إعدادات الرندر"""
        render = scene.render
        cycles = scene.cycles if scene.render.engine == 'CYCLES' else None
        
        preset = self.render_presets.get(quality_level, self.render_presets['production'])
        
        # إعدادات الدقة
        render.resolution_percentage = preset['resolution']
        
        # إعدادات Cycles
        if cycles:
            cycles.samples = preset['samples']
            cycles.use_denoising = preset['denoise']
            
            # تحسينات إضافية للجودة العالية
            if quality_level in ['production', 'cinematic']:
                cycles.max_bounces = 12
                cycles.diffuse_bounces = 4
                cycles.glossy_bounces = 4
                cycles.transmission_bounces = 8
                cycles.volume_bounces = 2
                cycles.caustics_reflective = True
                cycles.caustics_refractive = True
            else:
                cycles.max_bounces = 4
                cycles.caustics_reflective = False
                cycles.caustics_refractive = False
        
        # Motion Blur للسينمائي
        if preset.get('motion_blur'):
            render.use_motion_blur = True
            render.motion_blur_shutter = 0.5
        
        return preset
    
    def auto_optimize(self, scene):
        """تحسين تلقائي بناءً على تعقيد المشهد"""
        stats = self.analyze_scene_complexity(scene)
        
        # اختيار الإعدادات المناسبة
        if stats['complexity_score'] < 50:
            quality = 'preview'
        elif stats['complexity_score'] < 150:
            quality = 'production'
        else:
            quality = 'cinematic'
        
        settings = self.optimize_settings(scene, quality)
        
        return {
            'quality_level': quality,
            'settings': settings,
            'stats': stats
        }
    
    def optimize_lighting_for_render(self, scene):
        """تحسين الإضاءة للرندر"""
        lights = [obj for obj in scene.objects if obj.type == 'LIGHT']
        
        optimizations = []
        
        for light in lights:
            # تحويل الأضواء النقاطية إلى مساحية للجودة
            if light.data.type == 'POINT' and light.data.energy > 100:
                light.data.size = 0.1  # حجم صغير لظلال ناعمة
                optimizations.append(f"{light.name}: تحسين حجم الضوء النقطي")
            
            # تفعيل Shadow Caustics للأضواء القوية
            if light.data.energy > 50:
                light.data.cycles.use_shadow_caustics = True
                optimizations.append(f"{light.name}: تفعيل Shadow Caustics")
        
        return optimizations
    
    def estimate_render_time(self, scene):
        """تقدير وقت الرندر"""
        stats = self.analyze_scene_complexity(scene)
        
        # عوامل التأثير
        vertices_factor = stats['vertices'] / 10000
        lights_factor = stats['lights'] * 2
        materials_factor = stats['materials'] * 1.5
        
        # وقت أساسي (بالدقائق)
        base_time = 5
        estimated_time = base_time + vertices_factor + lights_factor + materials_factor
        
        # تعديل حسب جودة الرندر
        if scene.render.engine == 'CYCLES':
            samples = scene.cycles.samples
            estimated_time *= (samples / 128)
        
        return {
            'estimated_minutes': round(estimated_time, 1),
            'estimated_seconds': round(estimated_time * 60),
            'complexity_score': round(stats['complexity_score'], 1)
        }
    
    def batch_render_settings(self, scenes, quality='preview'):
        """تطبيق إعدادات على عدة مشاهد"""
        results = []
        for scene in scenes:
            settings = self.optimize_settings(scene, quality)
            results.append({
                'scene': scene.name,
                'settings': settings
            })
        return results
