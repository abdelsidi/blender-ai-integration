import bpy
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import StringProperty, EnumProperty, BoolProperty, FloatProperty, IntProperty

class AIImageToScenePanel(Panel):
    """AI Image to 3D Scene - Main Panel"""
    bl_label = "AI Image to 3D Scene"
    bl_idname = "VIEW3D_PT_ai_image_to_scene"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI Scene'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Header
        box = layout.box()
        box.label(text="Transform Photo to 3D", icon='IMAGE_DATA')
        box.scale_y = 1.2
        
        layout.separator()
        
        # Step 1: Import Image
        box = layout.box()
        box.label(text="STEP 1: Import Photo", icon='FILE_IMAGE')
        
        row = box.row()
        row.prop(scene, "ai_scene_image_path", text="")
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("ai_scene.import_image", text="Load & Analyze Image", icon='IMPORT')
        
        if scene.ai_scene_image_loaded:
            col = box.column()
            col.label(text=f"Image: {scene.ai_scene_image_name}", icon='CHECKMARK')
            col.label(text=f"Size: {scene.ai_scene_image_size}", icon='INFO')
        
        layout.separator()
        
        # Step 2: Analysis Results
        if scene.ai_scene_analysis_done:
            box = layout.box()
            box.label(text="STEP 2: AI Analysis", icon='VIEWZOOM')
            
            row = box.row()
            row.label(text=f"Scene Type: {scene.ai_scene_type}")
            
            row = box.row()
            row.label(text=f"Objects Detected: {scene.ai_scene_objects}")
            
            row = box.row()
            row.label(text=f"Dominant Colors: {scene.ai_scene_colors}")
            
            layout.separator()
        
        # Step 3: Generation Settings
        box = layout.box()
        box.label(text="STEP 3: Scene Settings", icon='PREFERENCES')
        
        row = box.row()
        row.prop(scene, "ai_scene_create_ground", text="Ground Plane")
        
        row = box.row()
        row.prop(scene, "ai_scene_create_objects", text="Detected Objects")
        
        row = box.row()
        row.prop(scene, "ai_scene_displacement", text="Depth Displacement")
        
        row = box.row()
        row.prop(scene, "ai_scene_auto_light", text="Auto Lighting")
        
        if scene.ai_scene_displacement:
            row = box.row()
            row.prop(scene, "ai_scene_displacement_strength", text="Strength")
        
        layout.separator()
        
        # Step 4: Generate
        box = layout.box()
        box.label(text="STEP 4: Generate 3D Scene", icon='SCENE')
        
        row = box.row()
        row.scale_y = 1.5
        row.operator("ai_scene.generate", text="GENERATE 3D SCENE", icon='PLAY')
        
        if scene.ai_scene_generating:
            row = box.row()
            row.label(text="Generating... Please wait", icon='TIME')
        
        layout.separator()
        
        # Advanced Options
        box = layout.box()
        box.label(text="Advanced Options", icon='MODIFIER')
        
        row = box.row()
        row.prop(scene, "ai_scene_quality", text="Quality")
        
        row = box.row()
        row.prop(scene, "ai_scene_clear_scene", text="Clear Existing Objects")
        
        layout.separator()
        
        # Quick Actions
        box = layout.box()
        box.label(text="Quick Actions", icon='TOOL_SETTINGS')
        
        row = box.row(align=True)
        row.operator("ai_scene.setup_camera", text="Camera", icon='CAMERA_DATA')
        row.operator("ai_scene.setup_lighting", text="Lighting", icon='LIGHT')
        
        row = box.row(align=True)
        row.operator("ai_scene.add_depth", text="Add Depth", icon='IMAGE_ZDEPTH')
        row.operator("ai_scene.reset", text="Reset", icon='CANCEL')

class ImportImageOperator(Operator):
    """Import and Analyze Image"""
    bl_idname = "ai_scene.import_image"
    bl_label = "Import & Analyze Image"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        image_path = context.scene.ai_scene_image_path
        
        if not image_path:
            self.report({'ERROR'}, "Please select an image!")
            return {'CANCELLED'}
        
        try:
            from ..core.scene_generator import ImageToSceneCore
            generator = ImageToSceneCore()
            
            # Analyze image
            analysis = generator.analyze_image_with_ai(image_path)
            
            # Store results
            context.scene.ai_scene_image_loaded = True
            context.scene.ai_scene_image_name = bpy.path.basename(image_path)
            context.scene.ai_scene_image_size = f"{analysis['dimensions'][0]}x{analysis['dimensions'][1]}"
            context.scene.ai_scene_analysis_done = True
            context.scene.ai_scene_type = analysis['scene_type'].replace('_', ' ').title()
            context.scene.ai_scene_objects = str(len(analysis['detected_objects']))
            context.scene.ai_scene_colors = str(len(analysis['dominant_colors']))
            
            self.report({'INFO'}, f"Analyzed: {context.scene.ai_scene_image_name}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed: {str(e)}")
        
        return {'FINISHED'}

class GenerateSceneOperator(Operator):
    """Generate Complete 3D Scene"""
    bl_idname = "ai_scene.generate"
    bl_label = "Generate 3D Scene"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        image_path = context.scene.ai_scene_image_path
        
        if not image_path or not context.scene.ai_scene_image_loaded:
            self.report({'ERROR'}, "Please import an image first!")
            return {'CANCELLED'}
        
        if context.scene.ai_scene_clear_scene:
            # Clear existing objects
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete(use_global=False)
        
        try:
            from ..core.scene_generator import ImageToSceneCore
            generator = ImageToSceneCore()
            
            context.scene.ai_scene_generating = True
            
            # Generate scene
            scene_data = generator.process_image_to_scene(image_path)
            
            context.scene.ai_scene_generating = False
            
            self.report({'INFO'}, f"Scene created with {scene_data['object_count']} objects!")
        except Exception as e:
            context.scene.ai_scene_generating = False
            self.report({'ERROR'}, f"Generation failed: {str(e)}")
        
        return {'FINISHED'}

class SetupCameraOperator(Operator):
    """Setup Camera"""
    bl_idname = "ai_scene.setup_camera"
    bl_label = "Setup Camera"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.object.camera_add(location=(7, -7, 5))
        camera = context.active_object
        camera.rotation_euler = (1.1, 0, 0.785)
        context.scene.camera = camera
        
        self.report({'INFO'}, "Camera setup complete")
        return {'FINISHED'}

class SetupLightingOperator(Operator):
    """Setup Lighting"""
    bl_idname = "ai_scene.setup_lighting"
    bl_label = "Setup Lighting"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Three-point lighting
        bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
        sun = context.active_object
        sun.data.energy = 5
        
        bpy.ops.object.light_add(type='AREA', location=(-5, -5, 5))
        fill = context.active_object
        fill.data.energy = 2
        
        bpy.ops.object.light_add(type='SPOT', location=(0, -5, 8))
        rim = context.active_object
        rim.data.energy = 3
        
        self.report({'INFO'}, "Lighting setup complete")
        return {'FINISHED'}

class AddDepthOperator(Operator):
    """Add Depth to Selected Object"""
    bl_idname = "ai_scene.add_depth"
    bl_label = "Add Depth"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Please select a mesh object!")
            return {'CANCELLED'}
        
        # Add subdivision
        subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf.levels = 3
        
        # Add displacement
        disp = obj.modifiers.new(name="Displacement", type='DISPLACE')
        disp.strength = 0.5
        
        self.report({'INFO'}, "Depth modifiers added")
        return {'FINISHED'}

class ResetOperator(Operator):
    """Reset Scene"""
    bl_idname = "ai_scene.reset"
    bl_label = "Reset"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        context.scene.ai_scene_image_loaded = False
        context.scene.ai_scene_analysis_done = False
        context.scene.ai_scene_image_path = ""
        
        self.report({'INFO'}, "Scene reset")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AIImageToScenePanel)
    bpy.utils.register_class(ImportImageOperator)
    bpy.utils.register_class(GenerateSceneOperator)
    bpy.utils.register_class(SetupCameraOperator)
    bpy.utils.register_class(SetupLightingOperator)
    bpy.utils.register_class(AddDepthOperator)
    bpy.utils.register_class(ResetOperator)
    
    # Properties
    bpy.types.Scene.ai_scene_image_path = StringProperty(
        name="Image Path",
        default="",
        subtype='FILE_PATH'
    )
    
    bpy.types.Scene.ai_scene_image_loaded = BoolProperty(default=False)
    bpy.types.Scene.ai_scene_analysis_done = BoolProperty(default=False)
    bpy.types.Scene.ai_scene_generating = BoolProperty(default=False)
    
    bpy.types.Scene.ai_scene_image_name = StringProperty(default="")
    bpy.types.Scene.ai_scene_image_size = StringProperty(default="")
    bpy.types.Scene.ai_scene_type = StringProperty(default="")
    bpy.types.Scene.ai_scene_objects = StringProperty(default="")
    bpy.types.Scene.ai_scene_colors = StringProperty(default="")
    
    bpy.types.Scene.ai_scene_create_ground = BoolProperty(
        name="Create Ground",
        default=True
    )
    
    bpy.types.Scene.ai_scene_create_objects = BoolProperty(
        name="Create Objects",
        default=True
    )
    
    bpy.types.Scene.ai_scene_displacement = BoolProperty(
        name="Use Displacement",
        default=True
    )
    
    bpy.types.Scene.ai_scene_displacement_strength = FloatProperty(
        name="Displacement Strength",
        default=1.0,
        min=0.0,
        max=5.0
    )
    
    bpy.types.Scene.ai_scene_auto_light = BoolProperty(
        name="Auto Lighting",
        default=True
    )
    
    bpy.types.Scene.ai_scene_quality = EnumProperty(
        name="Quality",
        items=[
            ('low', 'Low (Fast)', 'Fast generation'),
            ('medium', 'Medium', 'Balanced'),
            ('high', 'High (Slow)', 'Best quality'),
        ],
        default='medium'
    )
    
    bpy.types.Scene.ai_scene_clear_scene = BoolProperty(
        name="Clear Scene",
        default=False
    )

def unregister():
    bpy.utils.unregister_class(AIImageToScenePanel)
    bpy.utils.unregister_class(ImportImageOperator)
    bpy.utils.unregister_class(GenerateSceneOperator)
    bpy.utils.unregister_class(SetupCameraOperator)
    bpy.utils.unregister_class(SetupLightingOperator)
    bpy.utils.unregister_class(AddDepthOperator)
    bpy.utils.unregister_class(ResetOperator)
    
    del bpy.types.Scene.ai_scene_image_path
    del bpy.types.Scene.ai_scene_image_loaded
    del bpy.types.Scene.ai_scene_analysis_done
    del bpy.types.Scene.ai_scene_generating
    del bpy.types.Scene.ai_scene_image_name
    del bpy.types.Scene.ai_scene_image_size
    del bpy.types.Scene.ai_scene_type
    del bpy.types.Scene.ai_scene_objects
    del bpy.types.Scene.ai_scene_colors
    del bpy.types.Scene.ai_scene_create_ground
    del bpy.types.Scene.ai_scene_create_objects
    del bpy.types.Scene.ai_scene_displacement
    del bpy.types.Scene.ai_scene_displacement_strength
    del bpy.types.Scene.ai_scene_auto_light
    del bpy.types.Scene.ai_scene_quality
    del bpy.types.Scene.ai_scene_clear_scene
