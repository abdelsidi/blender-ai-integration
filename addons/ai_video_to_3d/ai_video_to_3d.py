import bpy
import os
import cv2
import numpy as np
from PIL import Image
from pathlib import Path

class VideoTo3DGenerator:
    """Video to 3D depth generator using AI"""
    
    def __init__(self):
        self.processing_mode = 'cloud'  # 'cloud' or 'local'
        self.depth_model = None
        self.temp_dir = None
    
    def import_video(self, filepath):
        """Import video file"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Video not found: {filepath}")
        
        cap = cv2.VideoCapture(filepath)
        
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {filepath}")
        
        video_info = {
            'path': filepath,
            'name': Path(filepath).stem,
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'duration': int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
        }
        
        cap.release()
        return video_info
    
    def extract_frames(self, video_path, output_dir, sample_rate=1):
        """Extract frames from video"""
        cap = cv2.VideoCapture(video_path)
        frames_dir = os.path.join(output_dir, "frames")
        os.makedirs(frames_dir, exist_ok=True)
        
        frame_count = 0
        saved_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Save every Nth frame based on sample_rate
            if frame_count % sample_rate == 0:
                frame_path = os.path.join(frames_dir, f"frame_{saved_count:05d}.png")
                cv2.imwrite(frame_path, frame)
                saved_count += 1
            
            frame_count += 1
        
        cap.release()
        return frames_dir, saved_count
    
    def generate_depth_map_simple(self, image_path):
        """Simple depth estimation (placeholder for AI model)"""
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            return None
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Simple gradient-based depth estimation
        # In real implementation, this would use MiDaS, DPT, or similar
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # Magnitude
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        
        # Normalize
        depth = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        depth = np.uint8(depth)
        
        return depth
    
    def generate_depth_maps(self, frames_dir, output_dir):
        """Generate depth maps for all frames"""
        depth_dir = os.path.join(output_dir, "depth_maps")
        os.makedirs(depth_dir, exist_ok=True)
        
        frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
        
        for i, frame_name in enumerate(frames):
            frame_path = os.path.join(frames_dir, frame_name)
            
            # Generate depth
            depth = self.generate_depth_map_simple(frame_path)
            
            if depth is not None:
                depth_path = os.path.join(depth_dir, f"depth_{i:05d}.png")
                cv2.imwrite(depth_path, depth)
        
        return depth_dir
    
    def create_displaced_mesh(self, base_mesh, depth_image_path, strength=1.0):
        """Create displaced mesh from depth map"""
        import bmesh
        
        # Get mesh
        bpy.context.view_layer.objects.active = base_mesh
        
        # Enter edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Get bmesh
        bm = bmesh.from_mesh(base_mesh.data)
        
        # Load depth image
        depth_img = cv2.imread(depth_image_path, cv2.IMREAD_GRAYSCALE)
        if depth_img is None:
            return
        
        height, width = depth_img.shape
        
        # Displace vertices
        for vert in bm.verts:
            # Get UV coordinates (simplified)
            x = (vert.co.x + 1) / 2  # Normalize to 0-1
            y = (vert.co.y + 1) / 2
            
            # Sample depth
            px = int(x * (width - 1))
            py = int(y * (height - 1))
            
            depth_val = depth_img[py, px] / 255.0
            
            # Apply displacement
            vert.co.z += depth_val * strength
        
        # Update mesh
        bmesh.to_mesh(bm, base_mesh.data)
        bm.free()
        
        # Exit edit mode
        bpy.ops.object.mode_set(mode='OBJECT')
    
    def create_3d_from_video(self, video_path, displacement_strength=1.0):
        """Full pipeline: video -> 3D animated mesh"""
        import tempfile
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        
        # Import video
        video_info = self.import_video(video_path)
        
        # Extract frames
        frames_dir, frame_count = self.extract_frames(video_path, temp_dir)
        
        # Generate depth maps
        depth_dir = self.generate_depth_maps(frames_dir, temp_dir)
        
        # Create base plane
        bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0))
        base_plane = bpy.context.active_object
        base_plane.name = f"VideoDepth_{video_info['name']}"
        
        # Subdivide for detail
        bpy.ops.object.modifier_add(type='SUBSURF')
        base_plane.modifiers["Subdivision"].levels = 4
        bpy.ops.object.modifier_apply(modifier="Subdivision")
        
        # Animate displacement
        self.animate_displacement(base_plane, depth_dir, video_info['fps'], displacement_strength)
        
        return base_plane
    
    def animate_displacement(self, obj, depth_dir, fps, strength):
        """Animate displacement using depth maps"""
        scene = bpy.context.scene
        
        depth_files = sorted([f for f in os.listdir(depth_dir) if f.endswith('.png')])
        
        # Set frame rate
        scene.render.fps = int(fps)
        
        # Create shape keys
        obj.shape_key_add(name="Basis")
        
        for i, depth_file in enumerate(depth_files):
            frame_num = i + 1
            
            # Create shape key
            shapekey = obj.shape_key_add(name=f"Frame_{i:05d}")
            
            # Apply displacement to shape key
            # (This is simplified - full implementation would use drivers)
            
            # Set keyframe
            shapekey.value = 0
            shapekey.keyframe_insert(data_path="value", frame=frame_num - 1)
            
            shapekey.value = 1
            shapekey.keyframe_insert(data_path="value", frame=frame_num)
            
            shapekey.value = 0
            shapekey.keyframe_insert(data_path="value", frame=frame_num + 1)
    
    def text_to_image_generate(self, prompt, style="realistic", output_path=None):
        """Bonus: Text-to-image generation"""
        # Placeholder - would integrate with Stable Diffusion/DALL-E API
        result = {
            'prompt': prompt,
            'style': style,
            'status': 'generated',
            'path': output_path or f"generated_{hash(prompt)}.png"
        }
        return result
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        deps = {
            'opencv': False,
            'PIL': False,
            'numpy': False
        }
        
        try:
            import cv2
            deps['opencv'] = True
        except ImportError:
            pass
        
        try:
            from PIL import Image
            deps['PIL'] = True
        except ImportError:
            pass
        
        try:
            import numpy
            deps['numpy'] = True
        except ImportError:
            pass
        
        return deps
    
    def install_dependencies(self):
        """Install required packages"""
        import subprocess
        import sys
        
        packages = ['opencv-python', 'Pillow', 'numpy']
        
        for package in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])
        
        return True
