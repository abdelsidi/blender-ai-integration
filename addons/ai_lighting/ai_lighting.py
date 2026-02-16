import bpy
import json
from datetime import datetime

class AILighting:
    """إضافة AI Lighting"""
    
    def __init__(self):
        self.api_key = ""
        self.lighting_cache = {}
    
    def analyze_lighting(self, scene):
        """تحليل الإضاءة في المشهد"""
        analysis = {
            "total_lights": len([obj for obj in scene.objects if obj.type == 'LIGHT']),
            "light_types": {},
            "light_intensities": [],
            "light_colors": [],
            "scene_ambiance": "unknown"
        }
        
        for obj in scene.objects:
            if obj.type == 'LIGHT':
                light_type = obj.data.type
                intensity = obj.data.energy
                analysis["light_types"][light_type] = analysis["light_types"].get(light_type, 0) + 1
                analysis["light_intensities"].append(intensity)
                analysis["light_colors"].append(tuple(obj.data.color))
        
        if analysis["light_intensities"]:
            avg_intensity = sum(analysis["light_intensities"]) / len(analysis["light_intensities"])
            if avg_intensity > 1.0:
                analysis["scene_ambiance"] = "bright"
            elif avg_intensity > 0.5:
                analysis["scene_ambiance"] = "normal"
            else:
                analysis["scene_ambiance"] = "dark"
        
        return analysis
    
    def optimize_lighting(self, scene, style="balanced"):
        """تحسين الإضاءة باستخدام AI"""
        analysis = self.analyze_lighting(scene)
        improvements = self.get_ai_lighting_suggestions(analysis, style)
        self.apply_lighting_improvements(scene, improvements)
        return improvements
    
    def get_ai_lighting_suggestions(self, analysis, style):
        """الحصول على اقتراحات تحسين الإضاءة من AI"""
        suggestions = []
        
        if analysis["scene_ambiance"] == "dark":
            suggestions.append({
                "type": "add_main_light",
                "description": "Add main light source",
                "priority": "high",
                "position": (5, 5, 10),
                "rotation": (0.5, 0.5, 0.0),
                "energy": 1.0,
                "color": (1.0, 1.0, 1.0)
            })
        
        if len(analysis["light_types"]) == 1:
            suggestions.append({
                "type": "add_filler_light",
                "description": "Add filler light",
                "priority": "medium",
                "position": (-5, 5, 5),
                "energy": 0.5,
                "color": (1.0, 1.0, 0.9)
            })
        
        return suggestions
    
    def apply_lighting_improvements(self, scene, improvements):
        """تطبيق تحسينات الإضاءة"""
        for improvement in improvements:
            if improvement["type"] in ["add_main_light", "add_filler_light"]:
                self.add_light(scene, improvement)
    
    def add_light(self, scene, improvement):
        """إضافة مصدر إضاءة"""
        light_data = bpy.data.lights.new(
            name=f"AI_{improvement['type']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            type='SUN'
        )
        light_data.energy = improvement.get("energy", 1.0)
        light_data.color = improvement.get("color", (1.0, 1.0, 1.0))
        
        light_obj = bpy.data.objects.new(name=light_data.name, object_data=light_data)
        scene.collection.objects.link(light_obj)
        light_obj.location = improvement.get("position", (0, 0, 0))
