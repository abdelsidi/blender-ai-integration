bl_info = {
    "name": "AI Model Generator",
    "author": "Blender AI Team",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > AI Tools > Model Generator",
    "description": "Generate 3D models using AI from text or images",
    "category": "AI",
    "doc_url": "https://github.com/abdelsidi/blender-ai-integration/blob/main/docs/AI_MODEL_GENERATOR.md",
    "tracker_url": "https://github.com/abdelsidi/blender-ai-integration/issues",
}

import bpy
from . import ui, utils, models

def register():
    ui.register()
    utils.register()
    models.register()

def unregister():
    ui.unregister()
    utils.unregister()
    models.unregister()

if __name__ == "__main__":
    register()
