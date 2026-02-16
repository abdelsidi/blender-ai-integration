import bpy

class AIDenoiser:
    """إزالة الضوضاء بالذكاء الاصطناعي"""
    
    def __init__(self):
        self.strength = 1.0
        self.preserve_details = True
    
    def setup_oidn(self, scene):
        """إعداد Intel Open Image Denoise"""
        if scene.render.engine == 'CYCLES':
            scene.cycles.use_denoising = True
            scene.cycles.denoiser = 'OPENIMAGEDENOISE'
            return True
        return False
    
    def setup_optix(self, scene):
        """إعداد NVIDIA OptiX Denoiser"""
        if scene.render.engine == 'CYCLES':
            scene.cycles.use_denoising = True
            scene.cycles.denoiser = 'OPTIX'
            return True
        return False
    
    def denoise_render_layers(self, scene):
        """تفعيل إزالة الضوضاء لطبقات الرندر"""
        view_layer = scene.view_layers[0] if scene.view_layers else None
        if view_layer:
            view_layer.cycles.use_denoising = True
            return True
        return False
    
    def estimate_noise_level(self, scene):
        """تقدير مستوى الضوضاء"""
        # محاكاة التحليل
        samples = scene.cycles.samples if scene.render.engine == 'CYCLES' else 128
        
        if samples < 64:
            return 'high'
        elif samples < 256:
            return 'medium'
        else:
            return 'low'
    
    def auto_setup(self, scene):
        """إعداد تلقائي"""
        noise_level = self.estimate_noise_level(scene)
        
        # محاولة OptiX أولاً، ثم OIDN
        if not self.setup_optix(scene):
            self.setup_oidn(scene)
        
        self.denoise_render_layers(scene)
        
        return {
            'noise_level': noise_level,
            'denoiser': scene.cycles.denoiser if scene.render.engine == 'CYCLES' else 'None'
        }
