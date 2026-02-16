from . import stable_diffusion
from . import dalle

def register():
    stable_diffusion.register()
    dalle.register()

def unregister():
    dalle.unregister()
    stable_diffusion.unregister()
