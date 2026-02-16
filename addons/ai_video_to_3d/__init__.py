bl_info = {
    "name": "AI Video to 3D",
    "author": "Blender AI Team",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > AI Tools > Video to 3D",
    "description": "Convert videos to 3D depth maps and animated displacement",
    "category": "AI",
    "doc_url": "https://github.com/abdelsidi/blender-ai-integration",
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
