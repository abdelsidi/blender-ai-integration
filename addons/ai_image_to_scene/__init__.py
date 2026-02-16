bl_info = {
    "name": "AI Image to 3D Scene",
    "author": "Blender AI Team",
    "version": (2, 0, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > AI Image to Scene",
    "description": "Transform any photo into a complete 3D scene with AI-powered depth, mesh generation, and automatic lighting/materials",
    "category": "AI",
    "doc_url": "https://github.com/abdelsidi/blender-ai-integration",
    "tracker_url": "https://github.com/abdelsidi/blender-ai-integration/issues",
}

import bpy
from . import ui, utils, core

def register():
    ui.register()
    utils.register()
    core.register()

def unregister():
    ui.unregister()
    utils.unregister()
    core.unregister()

if __name__ == "__main__":
    register()
