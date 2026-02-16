import bpy
import subprocess
import sys
import os

class InstallDependenciesOperator(bpy.types.Operator):
    """Install required Python packages"""
    bl_idname = "image_scene.install_deps"
    bl_label = "Install Dependencies"
    bl_description = "Install OpenCV, NumPy, and PIL"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        python_exe = sys.executable
        
        packages = [
            'opencv-python',
            'Pillow',
            'numpy'
        ]
        
        for package in packages:
            try:
                subprocess.check_call([python_exe, "-m", "pip", "install", "--user", package])
                self.report({'INFO'}, f"Installed {package}")
            except Exception as e:
                self.report({'ERROR'}, f"Failed to install {package}: {e}")
                return {'CANCELLED'}
        
        self.report({'INFO'}, "All dependencies installed! Please restart Blender.")
        return {'FINISHED'}

class CheckDependenciesOperator(bpy.types.Operator):
    """Check if dependencies are installed"""
    bl_idname = "image_scene.check_deps"
    bl_label = "Check Dependencies"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        deps = {
            'cv2': False,
            'PIL': False,
            'numpy': False
        }
        
        try:
            import cv2
            deps['cv2'] = True
        except:
            pass
        
        try:
            from PIL import Image
            deps['PIL'] = True
        except:
            pass
        
        try:
            import numpy
            deps['numpy'] = True
        except:
            pass
        
        missing = [k for k, v in deps.items() if not v]
        
        if missing:
            self.report({'WARNING'}, f"Missing: {', '.join(missing)}. Click Install Dependencies.")
        else:
            self.report({'INFO'}, "All dependencies installed!")
        
        return {'FINISHED'}

# Register
def register():
    bpy.utils.register_class(InstallDependenciesOperator)
    bpy.utils.register_class(CheckDependenciesOperator)

def unregister():
    bpy.utils.unregister_class(InstallDependenciesOperator)
    bpy.utils.unregister_class(CheckDependenciesOperator)

if __name__ == "__main__":
    register()
