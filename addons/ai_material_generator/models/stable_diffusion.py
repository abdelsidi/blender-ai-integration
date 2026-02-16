"""
Stable Diffusion Integration for Material Generation
"""
import bpy
import requests
import tempfile
import os
from typing import Dict, Optional

class StableDiffusionAPI:
    """واجهة برمجة التطبيقات لـ Stable Diffusion"""
    
    def __init__(self, api_url: str = "http://localhost:7860", api_key: str = ""):
        self.api_url = api_url
        self.api_key = api_key
        self.model = "sdxl"
    
    def generate_texture(self, prompt: str, negative_prompt: str = "", 
                        width: int = 512, height: int = 512,
                        steps: int = 30, cfg_scale: float = 7.0) -> Optional[str]:
        """
        توليد نسيج باستخدام Stable Diffusion
        
        Args:
            prompt: وصف النسيج المطلوب
            negative_prompt: ما يجب تجنبه في النسيج
            width: عرض الصورة
            height: ارتفاع الصورة
            steps: عدد خطوات التوليد
            cfg_scale: مقياس CFG
            
        Returns:
            مسار الصورة المولدة أو None في حالةFailure
        """
        try:
            # بناء الطلب
            payload = {
                "prompt": f"texture, seamless, {prompt}",
                "negative_prompt": f"blur, low quality, {negative_prompt}",
                "width": width,
                "height": height,
                "steps": steps,
                "cfg_scale": cfg_scale,
                "sampler_name": "DPM++ 2M Karras",
                "batch_size": 1,
                "n_iter": 1,
            }
            
            # إرسال الطلب إلى API
            response = requests.post(
                f"{self.api_url}/sdapi/v1/txt2img",
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            data = response.json()
            if "images" in data and len(data["images"]) > 0:
                # حفظ الصورة
                import base64
                img_data = base64.b64decode(data["images"][0])
                
                temp_path = tempfile.mktemp(suffix=".png")
                with open(temp_path, "wb") as f:
                    f.write(img_data)
                
                return temp_path
            
            return None
            
        except Exception as e:
            print(f"Error generating texture with Stable Diffusion: {e}")
            return None
    
    def generate_material_maps(self, prompt: str, style: str = "realistic") -> Dict:
        """
        توليد خرائط المواد المختلفة
        
        Args:
            prompt: وصف المادة
            style: أسلوب المادة
            
        Returns:
            قاموس يحتوي على مسارات خرائط المواد
        """
        maps = {}
        
        # توليد النسيج الأساسي
        base_texture = self.generate_texture(
            prompt=f"{prompt}, {style} material, tileable texture"
        )
        if base_texture:
            maps["base_color"] = base_texture
        
        # توليد خريطة الـ Normal
        normal_map = self.generate_texture(
            prompt=f"{prompt}, normal map, bump map, height map",
            negative_prompt="color, saturation"
        )
        if normal_map:
            maps["normal"] = normal_map
        
        # توليد خريطة الـ Roughness
        roughness_map = self.generate_texture(
            prompt=f"{prompt}, roughness map, grayscale",
            negative_prompt="color, saturation, hue"
        )
        if roughness_map:
            maps["roughness"] = roughness_map
        
        # توليد خريطة الـ Metallic
        metallic_map = self.generate_texture(
            prompt=f"{prompt}, metallic map, metalness map, grayscale",
            negative_prompt="color, saturation, hue"
        )
        if metallic_map:
            maps["metallic"] = metallic_map
        
        return maps
    
    def is_available(self) -> bool:
        """التحقق من توفر خدمة Stable Diffusion"""
        try:
            response = requests.get(f"{self.api_url}/sdapi/v1/samplers", timeout=5)
            return response.status_code == 200
        except:
            return False

class StableDiffusionSettings(bpy.types.PropertyGroup):
    """إعدادات Stable Diffusion"""
    
    api_url: bpy.props.StringProperty(
        name="API URL",
        description="Stable Diffusion API URL",
        default="http://localhost:7860"
    )
    
    use_local: bpy.props.BoolProperty(
        name="Use Local Server",
        description="Use local Automatic1111 installation",
        default=True
    )
    
    steps: bpy.props.IntProperty(
        name="Steps",
        description="Number of sampling steps",
        default=30,
        min=10,
        max=150
    )
    
    cfg_scale: bpy.props.FloatProperty(
        name="CFG Scale",
        description="Classifier Free Guidance Scale",
        default=7.0,
        min=1.0,
        max=30.0
    )
    
    resolution: bpy.props.EnumProperty(
        name="Resolution",
        description="Output resolution",
        items=[
            ('512', '512x512', 'Standard quality'),
            ('1024', '1024x1024', 'High quality (SDXL)'),
        ],
        default='512'
    )

def register():
    bpy.utils.register_class(StableDiffusionSettings)
    bpy.types.Scene.sd_settings = bpy.props.PointerProperty(type=StableDiffusionSettings)

def unregister():
    del bpy.types.Scene.sd_settings
    bpy.utils.unregister_class(StableDiffusionSettings)
