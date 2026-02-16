bl_info = {
    "name": "AI Render Optimizer",
    "author": "Blender AI Team",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Properties > Render > AI Render Optimizer",
    "description": "AI-powered render quality optimization and automated settings",
    "category": "AI",
    "doc_url": "https://github.com/abdelsidi/blender-ai-integration/blob/main/docs/AI_RENDER_OPTIMIZER.md",
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
