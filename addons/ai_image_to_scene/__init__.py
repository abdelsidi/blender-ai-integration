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

# Check dependencies on load
def check_dependencies():
    """Check if required packages are installed"""
    deps_installed = True
    
    try:
        import cv2
    except ImportError:
        deps_installed = False
        print("AI Image to 3D Scene: OpenCV not found. Please install dependencies.")
    
    try:
        from PIL import Image
    except ImportError:
        deps_installed = False
        print("AI Image to 3D Scene: PIL not found. Please install dependencies.")
    
    try:
        import numpy
    except ImportError:
        deps_installed = False
        print("AI Image to 3D Scene: NumPy not found. Please install dependencies.")
    
    return deps_installed

def register():
    # Check dependencies first
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("="*60)
        print("AI Image to 3D Scene: Missing Dependencies!")
        print("="*60)
        print("Please install required packages:")
        print("1. Open Blender as Administrator")
        print("2. Go to Scripting tab")
        print("3. Run: import subprocess; subprocess.check_call([bpy.app.binary_path_python, '-m', 'pip', 'install', 'opencv-python', 'Pillow', 'numpy'])")
        print("4. Restart Blender")
        print("="*60)
    
    ui.register()
    utils.register()
    core.register()

def unregister():
    ui.unregister()
    utils.unregister()
    core.unregister()

if __name__ == "__main__":
    register()
