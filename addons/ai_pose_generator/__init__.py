bl_info = {
    "name": "AI Pose Generator",
    "author": "Blender AI Team",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > AI Tools > Pose Generator",
    "description": "Generate character poses using AI",
    "category": "AI",
    "doc_url": "https://github.com/abdelsidi/blender-ai-integration/blob/main/docs/AI_POSE_GENERATOR.md",
}

import bpy
from . import ui

def register():
    ui.register()

def unregister():
    ui.unregister()

if __name__ == "__main__":
    register()
