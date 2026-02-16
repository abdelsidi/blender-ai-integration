from . import image_processor
from . import material_utils

def register():
    image_processor.register()
    material_utils.register()

def unregister():
    material_utils.unregister()
    image_processor.unregister()
