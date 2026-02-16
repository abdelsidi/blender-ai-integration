import bpy
import cv2
import numpy as np
from PIL import Image
import os
import requests
import json
from pathlib import Path
from datetime import datetime

class ImageToSceneCore:
    """Core engine for converting images to 3D scenes"""
    
    def __init__(self):
        self.api_key = ""
        self.use_local_depth = True
        self.temp_dir = None
    
    def analyze_image_with_ai(self, image_path):
        """Analyze image using AI to extract scene information"""
        
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Cannot load image: {image_path}")
        
        height, width = img.shape[:2]
        
        # Use OpenCV for initial analysis
        analysis = {
            'dimensions': (width, height),
            'dominant_colors': self.extract_dominant_colors(img),
            'detected_objects': self.detect_objects_basic(img),
            'depth_map': self.generate_depth_map(img),
            'lighting_direction': self.estimate_lighting(img),
            'scene_type': self.classify_scene(img)
        }
        
        return analysis
    
    def extract_dominant_colors(self, img, k=5):
        """Extract dominant colors from image"""
        data = np.float32(img).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
        _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        colors = []
        for center in centers:
            colors.append([int(c) for c in center])
        
        return colors
    
    def detect_objects_basic(self, img):
        """Basic object detection using contours"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        objects = []
        for i, contour in enumerate(contours[:10]):  # Limit to 10 objects
            area = cv2.contourArea(contour)
            if area > 1000:  # Filter small contours
                x, y, w, h = cv2.boundingRect(contour)
                objects.append({
                    'id': i,
                    'bbox': (x, y, w, h),
                    'area': area,
                    'center': (x + w//2, y + h//2)
                })
        
        return objects
    
    def generate_depth_map(self, img):
        """Generate depth map from image"""
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Use gradient-based depth estimation
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # Gradient magnitude
        gradient = np.sqrt(sobelx**2 + sobely**2)
        
        # Invert and normalize (closer objects = brighter)
        depth = 255 - cv2.normalize(gradient, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        
        # Apply blur for smoothness
        depth = cv2.GaussianBlur(depth, (15, 15), 0)
        
        return depth
    
    def estimate_lighting(self, img):
        """Estimate lighting direction from image"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Find brightest area
        _, max_val, _, max_loc = cv2.minMaxLoc(gray)
        
        height, width = img.shape[:2]
        
        # Normalize to -1 to 1
        light_x = (max_loc[0] / width) * 2 - 1
        light_y = (max_loc[1] / height) * 2 - 1
        light_z = 0.5  # Assume light is above
        
        return (light_x, light_y, light_z)
    
    def classify_scene(self, img):
        """Classify scene type"""
        # Simple classification based on color distribution
        mean_color = np.mean(img, axis=(0, 1))
        
        if mean_color[0] > mean_color[1] and mean_color[0] > mean_color[2]:
            return "indoor_warm"
        elif mean_color[2] > 150:
            return "outdoor_sky"
        elif np.std(img) < 30:
            return "minimal"
        else:
            return "mixed"
    
    def create_scene_from_analysis(self, analysis, image_path):
        """Create complete 3D scene from analysis"""
        
        # Clear existing objects (optional)
        # bpy.ops.object.select_all(action='SELECT')
        # bpy.ops.object.delete()
        
        scene_objects = []
        
        # 1. Create ground plane
        ground = self.create_ground_plane(analysis)
        scene_objects.append(ground)
        
        # 2. Create objects from detection
        for obj_data in analysis['detected_objects']:
            obj = self.create_object_from_detection(obj_data, analysis)
            if obj:
                scene_objects.append(obj)
        
        # 3. Create depth-based displacement plane
        displacement_plane = self.create_displacement_plane(analysis, image_path)
        scene_objects.append(displacement_plane)
        
        # 4. Setup lighting based on analysis
        self.setup_scene_lighting(analysis)
        
        # 5. Create environment/world
        self.setup_world_environment(analysis)
        
        # 6. Setup camera
        camera = self.setup_camera(analysis)
        
        return {
            'objects': scene_objects,
            'camera': camera,
            'object_count': len(scene_objects)
        }
    
    def create_ground_plane(self, analysis):
        """Create ground plane"""
        bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
        ground = bpy.context.active_object
        ground.name = "AI_Ground"
        
        # Subdivide for detail
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.subdivide(number_cuts=10)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Add material based on scene type
        mat = self.create_ground_material(analysis)
        ground.data.materials.append(mat)
        
        return ground
    
    def create_object_from_detection(self, obj_data, analysis):
        """Create 3D object from detection data"""
        x, y, w, h = obj_data['bbox']
        center_x = (x / analysis['dimensions'][0] - 0.5) * 10
        center_y = (0.5 - y / analysis['dimensions'][1]) * 10 + 2
        
        # Estimate depth based on size (larger = closer)
        depth_estimate = 1.0 - (obj_data['area'] / (analysis['dimensions'][0] * analysis['dimensions'][1]))
        z_pos = depth_estimate * 2
        
        # Create object based on aspect ratio
        aspect = w / h if h > 0 else 1
        
        if aspect > 1.5:
            # Wide object - likely a table, sofa, etc.
            bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x, center_y, z_pos))
            obj = bpy.context.active_object
            obj.scale = (2, 1, 0.5)
        elif aspect < 0.7:
            # Tall object - likely a person, lamp, etc.
            bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=2, location=(center_x, center_y, z_pos + 1))
            obj = bpy.context.active_object
        else:
            # Square-ish object
            bpy.ops.mesh.primitive_cube_add(size=1.5, location=(center_x, center_y, z_pos + 0.75))
            obj = bpy.context.active_object
        
        obj.name = f"AI_Object_{obj_data['id']}"
        
        # Add material
        mat = self.create_object_material(analysis, obj_data)
        obj.data.materials.append(mat)
        
        return obj
    
    def create_displacement_plane(self, analysis, image_path):
        """Create plane with displacement based on depth map"""
        # Create high-res plane
        bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0.5))
        plane = bpy.context.active_object
        plane.name = "AI_Depth_Scene"
        
        # Subdivide
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.subdivide(number_cuts=50)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Add displacement modifier
        disp = plane.modifiers.new(name="Displacement", type='DISPLACE')
        
        # Create texture from depth map
        depth_map = analysis['depth_map']
        
        # Save depth map temporarily
        temp_path = os.path.join(bpy.app.tempdir, "depth_map.png")
        cv2.imwrite(temp_path, depth_map)
        
        # Load as texture
        tex = bpy.data.textures.new(name="DepthTexture", type='IMAGE')
        img = bpy.data.images.load(temp_path)
        tex.image = img
        
        disp.texture = tex
        disp.strength = 2.0
        
        # Add material with original image
        mat = self.create_scene_material(image_path)
        plane.data.materials.append(mat)
        
        return plane
    
    def create_ground_material(self, analysis):
        """Create ground material"""
        mat = bpy.data.materials.new(name="AI_Ground_Material")
        mat.use_nodes = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output = nodes.new('ShaderNodeOutputMaterial')
        principled = nodes.new('ShaderNodeBsdfPrincipled')
        
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Set color based on dominant color
        if analysis['dominant_colors']:
            color = analysis['dominant_colors'][0]
            principled.inputs['Base Color'].default_value = (
                color[2]/255, color[1]/255, color[0]/255, 1.0
            )
        
        principled.inputs['Roughness'].default_value = 0.9
        
        return mat
    
    def create_object_material(self, analysis, obj_data):
        """Create material for detected object"""
        mat = bpy.data.materials.new(name=f"AI_Object_{obj_data['id']}_Mat")
        mat.use_nodes = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output = nodes.new('ShaderNodeOutputMaterial')
        principled = nodes.new('ShaderNodeBsdfPrincipled')
        
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Random variation based on object ID
        import random
        random.seed(obj_data['id'])
        
        r, g, b = random.random(), random.random(), random.random()
        principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
        principled.inputs['Roughness'].default_value = 0.5
        
        return mat
    
    def create_scene_material(self, image_path):
        """Create material with original image texture"""
        mat = bpy.data.materials.new(name="AI_Scene_Material")
        mat.use_nodes = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        # Create nodes
        output = nodes.new('ShaderNodeOutputMaterial')
        principled = nodes.new('ShaderNodeBsdfPrincipled')
        tex_image = nodes.new('ShaderNodeTexImage')
        mapping = nodes.new('ShaderNodeMapping')
        tex_coord = nodes.new('ShaderNodeTexCoord')
        
        # Load image
        img = bpy.data.images.load(image_path)
        tex_image.image = img
        
        # Position nodes
        output.location = (400, 0)
        principled.location = (200, 0)
        tex_image.location = (0, 0)
        mapping.location = (-200, 0)
        tex_coord.location = (-400, 0)
        
        # Link nodes
        links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], tex_image.inputs['Vector'])
        links.new(tex_image.outputs['Color'], principled.inputs['Base Color'])
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        return mat
    
    def setup_scene_lighting(self, analysis):
        """Setup lighting based on image analysis"""
        light_dir = analysis['lighting_direction']
        
        # Main light (sun)
        bpy.ops.object.light_add(type='SUN', location=(light_dir[0]*10, light_dir[1]*10, 10))
        sun = bpy.context.active_object
        sun.data.energy = 5
        sun.rotation_euler = (0.5, 0, 0)
        
        # Fill light
        bpy.ops.object.light_add(type='AREA', location=(-5, -5, 5))
        fill = bpy.context.active_object
        fill.data.energy = 2
        
        # Rim light
        bpy.ops.object.light_add(type='SPOT', location=(5, -5, 8))
        rim = bpy.context.active_object
        rim.data.energy = 3
        rim.rotation_euler = (1.2, 0, 0.8)
        
        return [sun, fill, rim]
    
    def setup_world_environment(self, analysis):
        """Setup world environment"""
        world = bpy.context.scene.world
        world.use_nodes = True
        
        nodes = world.node_tree.nodes
        links = world.node_tree.links
        nodes.clear()
        
        # Background shader
        output = nodes.new('ShaderNodeOutputWorld')
        bg = nodes.new('ShaderNodeBackground')
        
        links.new(bg.outputs['Background'], output.inputs['Surface'])
        
        # Set color based on dominant color
        if analysis['dominant_colors']:
            color = analysis['dominant_colors'][0]
            bg.inputs['Color'].default_value = (
                color[2]/255 * 0.3,
                color[1]/255 * 0.3,
                color[0]/255 * 0.3,
                1.0
            )
        
        bg.inputs['Strength'].default_value = 0.5
    
    def setup_camera(self, analysis):
        """Setup camera"""
        bpy.ops.object.camera_add(location=(7, -7, 5))
        camera = bpy.context.active_object
        camera.rotation_euler = (1.1, 0, 0.785)
        
        # Set as active camera
        bpy.context.scene.camera = camera
        
        return camera
    
    def process_image_to_scene(self, image_path):
        """Full pipeline: image -> 3D scene"""
        # Step 1: Analyze image
        print(f"Analyzing image: {image_path}")
        analysis = self.analyze_image_with_ai(image_path)
        
        # Step 2: Create scene
        print("Creating 3D scene...")
        scene_data = self.create_scene_from_analysis(analysis, image_path)
        
        return scene_data

def register():
    pass

def unregister():
    pass
