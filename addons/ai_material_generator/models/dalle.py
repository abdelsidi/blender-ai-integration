"""
DALL-E Integration for Material Generation
"""
import bpy
import requests
import base64
import tempfile
from typing import Optional, Dict

class DALLEAPI:
    """واجهة برمجة التطبيقات لـ DALL-E"""
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/images/generations"
        self.model = "dall-e-3"
    
    def set_api_key(self, api_key: str):
        """تعيين مفتاح API"""
        self.api_key = api_key
    
    def generate_texture(self, prompt: str, size: str = "1024x1024", 
                        quality: str = "standard") -> Optional[str]:
        """
        توليد نسيج باستخدام DALL-E
        
        Args:
            prompt: وصف النسيج
            size: حجم الصورة (1024x1024, 1024x1792, 1792x1024)
            quality: جودة الصورة (standard, hd)
            
        Returns:
            مسار الصورة المولدة أو None
        """
        if not self.api_key:
            print("Error: DALL-E API key not set")
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # تحسين الـ prompt للحصول على نسيج أفضل
            enhanced_prompt = f"Seamless texture tile, {prompt}, material texture, high detail, photorealistic, tileable pattern"
            
            payload = {
                "model": self.model,
                "prompt": enhanced_prompt,
                "n": 1,
                "size": size,
                "quality": quality,
                "response_format": "b64_json"
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                # تحويل base64 إلى ملف
                image_data = base64.b64decode(data["data"][0]["b64_json"])
                
                temp_path = tempfile.mktemp(suffix=".png")
                with open(temp_path, "wb") as f:
                    f.write(image_data)
                
                return temp_path
            
            return None
            
        except Exception as e:
            print(f"Error generating texture with DALL-E: {e}")
            return None
    
    def generate_material_from_reference(self, reference_path: str, 
                                        prompt: str = "") -> Optional[str]:
        """
        توليد مادة مشابهة لصورة مرجعية
        
        Args:
            reference_path: مسار الصورة المرجعية
            prompt: وصف إضافي
            
        Returns:
            مسار الصورة المولدة أو None
        """
        try:
            # تحويل الصورة إلى base64
            with open(reference_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            enhanced_prompt = f"Create a seamless tileable texture similar to this reference image. {prompt}"
            
            payload = {
                "model": self.model,
                "prompt": enhanced_prompt,
                "n": 1,
                "size": "1024x1024",
            }
            
            response = requests.post(
                "https://api.openai.com/v1/images/edits",
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            return self._save_response_image(response.json())
            
        except Exception as e:
            print(f"Error generating from reference: {e}")
            return None
    
    def _save_response_image(self, data: Dict) -> Optional[str]:
        """حفظ صورة من استجابة API"""
        try:
            if "data" in data and len(data["data"]) > 0:
                image_data = base64.b64decode(data["data"][0]["b64_json"])
                temp_path = tempfile.mktemp(suffix=".png")
                with open(temp_path, "wb") as f:
                    f.write(image_data)
                return temp_path
            return None
        except Exception as e:
            print(f"Error saving image: {e}")
            return None
    
    def is_available(self) -> bool:
        """التحقق من صلاحية مفتاح API"""
        if not self.api_key:
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers=headers,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

class DALLESettings(bpy.types.PropertyGroup):
    """إعدادات DALL-E"""
    
    api_key: bpy.props.StringProperty(
        name="API Key",
        description="OpenAI API Key",
        default="",
        subtype='PASSWORD'
    )
    
    image_size: bpy.props.EnumProperty(
        name="Image Size",
        description="Output image size",
        items=[
            ('1024x1024', '1024x1024 (Square)', 'Square format'),
            ('1024x1792', '1024x1792 (Portrait)', 'Portrait format'),
            ('1792x1024', '1792x1024 (Landscape)', 'Landscape format'),
        ],
        default='1024x1024'
    )
    
    quality: bpy.props.EnumProperty(
        name="Quality",
        description="Image quality",
        items=[
            ('standard', 'Standard', 'Faster generation'),
            ('hd', 'HD', 'Higher quality, slower'),
        ],
        default='standard'
    )
    
    style: bpy.props.EnumProperty(
        name="Style",
        description="Image style",
        items=[
            ('vivid', 'Vivid', 'More dramatic and hyper-real'),
            ('natural', 'Natural', 'More natural and realistic'),
        ],
        default='natural'
    )

def register():
    bpy.utils.register_class(DALLESettings)
    bpy.types.Scene.dalle_settings = bpy.props.PointerProperty(type=DALLESettings)

def unregister():
    del bpy.types.Scene.dalle_settings
    bpy.utils.unregister_class(DALLESettings)
