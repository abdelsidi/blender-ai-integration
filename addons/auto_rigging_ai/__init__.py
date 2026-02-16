bl_info = {
    "name": "Auto Rigging AI",
    "author": "Blender AI Team",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > AI Tools > Auto Rigging",
    "description": "Automatic character rigging using AI",
    "category": "AI",
    "doc_url": "https://github.com/abdelsidi/blender-ai-integration/blob/main/docs/AUTO_RIGGING_AI.md",
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
