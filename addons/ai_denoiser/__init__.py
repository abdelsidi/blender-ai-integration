bl_info = {
    "name": "AI Denoiser",
    "author": "Blender AI Team",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Properties > Render > AI Denoiser",
    "description": "AI-powered denoising for renders",
    "category": "AI",
    "doc_url": "https://github.com/abdelsidi/blender-ai-integration/blob/main/docs/AI_DENOISER.md",
}

import bpy
from . import ui

def register():
    ui.register()

def unregister():
    ui.unregister()

if __name__ == "__main__":
    register()
