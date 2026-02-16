"""
Image Processing Utilities for Material Generation
"""
import bpy
from PIL import Image
import numpy as np
import tempfile
import os
from typing import Tuple, Optional

class ImageProcessor:
    """معالج الصور للمواد"""
    
    @staticmethod
    def make_seamless(image_path: str, method: str = "mirror") -> str:
        """
        جعل الصورة متجانسة Seamless
        
        Args:
            image_path: مسار الصورة
            method: طريقة المعالجة (mirror, fade, wrap)
            
        Returns:
            مسار الصورة المعالجة
        """
        try:
            img = Image.open(image_path)
            width, height = img.size
            
            if method == "mirror":
                # طريقة المرآة
                left = img.crop((0, 0, width // 2, height))
                right = img.crop((width // 2, 0, width, height))
                new_img = Image.new(img.mode, (width, height))
                new_img.paste(left, (0, 0))
                new_img.paste(right.transpose(Image.FLIP_LEFT_RIGHT), (width // 2, 0))
            
            elif method == "fade":
                # طريقة التلاشي
                arr = np.array(img)
                fade_width = width // 10
                
                # إنشاء mask للتلاشي
                mask = np.ones((height, width))
                for i in range(fade_width):
                    alpha = i / fade_width
                    mask[:, i] = alpha
                    mask[:, width - 1 - i] = alpha
                
                # تطبيق mask
                for c in range(3):
                    arr[:, :, c] = (arr[:, :, c] * mask).astype(np.uint8)
                
                new_img = Image.fromarray(arr)
            
            else:  # wrap
                return image_path
            
            # حفظ الصورة
            output_path = tempfile.mktemp(suffix=".png")
            new_img.save(output_path)
            return output_path
            
        except Exception as e:
            print(f"Error making seamless: {e}")
            return image_path
    
    @staticmethod
    def generate_normal_map(image_path: str, strength: float = 1.0) -> str:
        """
        توليد خريطة Normal من النسيج
        
        Args:
            image_path: مسار النسيج
            strength: شدة الـ Normal
            
        Returns:
            مسار خريطة Normal
        """
        try:
            img = Image.open(image_path).convert('L')
            arr = np.array(img, dtype=np.float32)
            
            # حساب الـ gradients
            grad_x = np.gradient(arr, axis=1) * strength
            grad_y = np.gradient(arr, axis=0) * strength
            
            # إنشاء خريطة Normal
            normal_map = np.zeros((*arr.shape, 3), dtype=np.float32)
            normal_map[..., 0] = ((-grad_x / 255.0) + 1) * 127.5  # R
            normal_map[..., 1] = ((-grad_y / 255.0) + 1) * 127.5  # G
            normal_map[..., 2] = 255  # B
            
            # تحويل إلى uint8
            normal_map = normal_map.astype(np.uint8)
            
            # حفظ
            output_img = Image.fromarray(normal_map)
            output_path = tempfile.mktemp(suffix="_normal.png")
            output_img.save(output_path)
            
            return output_path
            
        except Exception as e:
            print(f"Error generating normal map: {e}")
            return image_path
    
    @staticmethod
    def generate_roughness_map(image_path: str) -> str:
        """
        توليد خريطة Roughness من النسيج
        
        Args:
            image_path: مسار النسيج
            
        Returns:
            مسار خريطة Roughness
        """
        try:
            img = Image.open(image_path).convert('L')
            
            # Roughness غالباً يعتمد على التباين
            arr = np.array(img, dtype=np.float32)
            
            # حساب التباين المحلي
            from scipy.ndimage import generic_filter
            
            def local_variance(patch):
                return np.var(patch)
            
            variance = generic_filter(arr, local_variance, size=5)
            
            # تطبيع
            variance = (varariance / variance.max() * 255).astype(np.uint8)
            
            output_img = Image.fromarray(variance)
            output_path = tempfile.mktemp(suffix="_roughness.png")
            output_img.save(output_path)
            
            return output_path
            
        except ImportError:
            # إذا لم يكن scipy متاحاً
            img = Image.open(image_path).convert('L')
            output_path = tempfile.mktemp(suffix="_roughness.png")
            img.save(output_path)
            return output_path
            
        except Exception as e:
            print(f"Error generating roughness map: {e}")
            return image_path
    
    @staticmethod
    def resize_for_blender(image_path: str, target_size: Tuple[int, int] = (1024, 1024)) -> str:
        """
        تغيير حجم الصورة لتناسب Blender
        
        Args:
            image_path: مسار الصورة
            target_size: الحجم المستهدف
            
        Returns:
            مسار الصورة المُعاد تحجيمها
        """
        try:
            img = Image.open(image_path)
            
            # التأكد من أن الحجم قوة 2
            width, height = target_size
            width = 2 ** int(np.log2(width))
            height = 2 ** int(np.log2(height))
            
            # تغيير الحجم
            img = img.resize((width, height), Image.LANCZOS)
            
            output_path = tempfile.mktemp(suffix=".png")
            img.save(output_path)
            return output_path
            
        except Exception as e:
            print(f"Error resizing image: {e}")
            return image_path
    
    @staticmethod
    def detect_seamless(image_path: str) -> bool:
        """
        التحقق مما إذا كانت الصورة متجانسة
        
        Args:
            image_path: مسار الصورة
            
        Returns:
            True إذا كانت الصورة متجانسة
        """
        try:
            img = Image.open(image_path)
            arr = np.array(img)
            
            width, height = img.size
            
            # مقارنة الحواف
            left_edge = arr[:, 0]
            right_edge = arr[:, -1]
            top_edge = arr[0, :]
            bottom_edge = arr[-1, :]
            
            # حساب الفرق
            h_diff = np.mean(np.abs(left_edge - right_edge))
            v_diff = np.mean(np.abs(top_edge - bottom_edge))
            
            return h_diff < 30 and v_diff < 30
            
        except Exception as e:
            print(f"Error checking seamless: {e}")
            return False

def register():
    bpy.utils.register_class(ImageProcessor)

def unregister():
    bpy.utils.unregister_class(ImageProcessor)
