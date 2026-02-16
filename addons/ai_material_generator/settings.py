import bpy

class AIMaterialGeneratorSettings(bpy.types.PropertyGroup):
    """إعدادات AI Material Generator"""
    
    prompt: bpy.props.StringProperty(
        name="Prompt",
        description="Describe the material you want to generate",
        default="metal surface with scratches"
    )
    
    model: bpy.props.EnumProperty(
        name="AI Model",
        description="Select AI model for material generation",
        items=[
            ('dalle', 'DALL-E', 'Generate materials with DALL-E'),
            ('stable_diffusion', 'Stable Diffusion', 'Generate materials with Stable Diffusion'),
            ('midjourney', 'Midjourney', 'Generate materials with Midjourney')
        ],
        default='stable_diffusion'
    )
    
    style: bpy.props.EnumProperty(
        name="Material Style",
        description="Select material style",
        items=[
            ('realistic', 'Realistic', 'Realistic materials'),
            ('stylized', 'Stylized', 'Stylized materials'),
            ('cartoon', 'Cartoon', 'Cartoon materials'),
            ('abstract', 'Abstract', 'Abstract materials')
        ],
        default='realistic'
    )
    
    api_key: bpy.props.StringProperty(
        name="API Key",
        description="AI service API key",
        default="",
        subtype='PASSWORD'
    )

def register():
    bpy.utils.register_class(AIMaterialGeneratorSettings)
    bpy.types.Scene.ai_material_prompt = bpy.props.PointerProperty(type=AIMaterialGeneratorSettings)
    bpy.types.Scene.ai_material_model = bpy.props.PointerProperty(type=AIMaterialGeneratorSettings)
    bpy.types.Scene.ai_material_style = bpy.props.PointerProperty(type=AIMaterialGeneratorSettings)
    bpy.types.Scene.ai_material_api_key = bpy.props.PointerProperty(type=AIMaterialGeneratorSettings)
    bpy.types.Scene.ai_material_last_prompt = bpy.props.StringProperty(default="")
    bpy.types.Scene.ai_material_last_style = bpy.props.StringProperty(default="")

def unregister():
    bpy.utils.unregister_class(AIMaterialGeneratorSettings)
    del bpy.types.Scene.ai_material_prompt
    del bpy.types.Scene.ai_material_model
    del bpy.types.Scene.ai_material_style
    del bpy.types.Scene.ai_material_api_key
    del bpy.types.Scene.ai_material_last_prompt
    del bpy.types.Scene.ai_material_last_style
