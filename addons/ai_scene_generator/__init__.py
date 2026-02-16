bl_info = {
    "name": "AI Scene Generator",
    "author": "Blender AI Team",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > AI Tools > Scene Generator",
    "description": "Generate complete 3D scenes using AI",
    "category": "AI",
    "doc_url": "https://github.com/abdelsidi/blender-ai-integration/blob/main/docs/AI_SCENE_GENERATOR.md",
}

import bpy
from . import ui

def register():
    ui.register()

def unregister():
    ui.unregister()

if __name__ == "__main__":
    register()
