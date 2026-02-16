bl_info = {
    "name": "AI Material Generator",
    "author": "Blender AI Team",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > AI Tools > Material Generator",
    "description": "Generate materials using AI",
    "category": "AI",
    "doc_url": "https://github.com/abdelsidi/blender-ai-integration/blob/main/docs/ADDON_INSTALLATION.md",
    "tracker_url": "https://github.com/abdelsidi/blender-ai-integration/issues",
}

import bpy
import os
import sys

from . import ui
from . import utils
from . import models

def register():
    """تسجيل الإضافة"""
    ui.register()
    models.register()
    utils.register()
    from . import settings
    settings.register()

def unregister():
    """إلغاء تسجيل الإضافة"""
    ui.unregister()
    models.unregister()
    utils.unregister()
    from . import settings
    settings.unregister()

if __name__ == "__main__":
    register()
