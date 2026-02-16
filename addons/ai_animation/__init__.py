bl_info = {
    "name": "AI Animation",
    "author": "Blender AI Team",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > AI Tools > Animation",
    "description": "AI-powered animation tools for automatic character animation",
    "category": "AI",
    "doc_url": "https://github.com/abdelsidi/blender-ai-integration/blob/main/docs/AI_ANIMATION.md",
    "tracker_url": "https://github.com/abdelsidi/blender-ai-integration/issues",
}

import bpy
from . import ui, utils

def register():
    ui.register()
    utils.register()

def unregister():
    ui.unregister()
    utils.unregister()

if __name__ == "__main__":
    register()
