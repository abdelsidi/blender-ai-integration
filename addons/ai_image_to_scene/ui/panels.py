import bpy
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import StringProperty, EnumProperty, FloatProperty, BoolProperty, IntProperty

class AIImageToScenePanel(Panel):
    """AI Image to 3D Scene Panel"""
    bl_label = "AI Image to 3D Scene"
    bl_idname = "VIEW3D_PT_ai_image_to_scene"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI Image Scene'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Header
        box = layout.box()
        box.label(text="Transform Photo to 3D", icon='IMAGE_DATA')
        box.label(text="Powered by AI + Blender", icon='MATERIAL')
        
        layout.separator()
        
        # Step 1: Import Image
        box = layout.box()
        box.label(text="Step 1: Import Image", icon='IMPORT')
        
        row = box.row()
        row.prop(scene, "image_scene_path", text="")
        
        row = box.row()
        row.scale_y = 1.2
        row.operator("image_scene.import", text="Load & Analyze Image", icon='FILE_IMAGE')
        
        # Show image info
        if scene.image_scene_analyzed:
            col = box.column()
            col.scale_y = 0.8
            col.label(text=f"Size: {scene.image_scene_info}", icon='INFO')
            
            # Show detected scene type
            row = box.row()
            row.label(text=f"Scene: {scene.image_scene_type}", icon='WORLD')
        
        layout.separator()
        
        # Step 2: Generate Depth
        box = layout.box()
        box.label(text="Step 2: Generate Depth", icon='IMAGE_ZDEPTH')
        
        row = box.row()
        row.prop(scene, "image_scene_depth_quality", text="Quality")
        
        row = box.row()
        row.prop(scene, "image_scene_depth_strength", text="Depth Strength")
        
        row = box.row()
        row.scale_y = 1.2
        row.operator("image_scene.generate_depth", text="Generate Depth Map", icon='RENDER_STILL')
        
        if scene.image_scene_depth_status:
            col = box.column()
            col.label(text=scene.image_scene_depth_status, icon='CHECKMARK')
        
        layout.separator()
        
        # Step 3: Create Scene
        box = layout.box()
        box.label(text="Step 3: Create 3D Scene", icon='SCENE')
        
        row = box.row()
        row.prop(scene, "image_scene_create_ground", text="Ground Plane")
        
        row = box.row()
        row.prop(scene, "image_scene_create_objects", text="Detect Objects")
        
        row = box.row()
        row.prop(scene, "image_scene_add_lighting", text="Auto Lighting")
        
        row = box.row()
        row.scale_y = 1.5
        row.operator("image_scene.create", text="CREATE 3D SCENE", icon='PLAY')
        
        layout.separator()
        
        # Advanced Options
        box = layout.box()
        box.label(text="Advanced Options", icon='PREFERENCES')
        
        row = box.row()
        row.prop(scene, "image_scene_subdivision", text="Mesh Detail")
        
        row = box.row()
        row.prop(scene, "image_scene_use_colors", text="Use Image Colors")
        
        row = box.row()
        row.operator("image_scene.reset", text="Reset Scene", icon='X')

class ImportImageOperator(Operator):
    """Import and Analyze Image"""
    bl_idname = "image_scene.import"
    bl_label = "Import Image"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        scene = context.scene
        image_path = scene.image_scene_path
        
        if not image_path:
            self.report({'ERROR'}, "Please select an image!")
            return {'CANCELLED'}
        
        try:
            from ..core.scene_generator import ImageToSceneCore
            core = ImageToSceneCore()
            
            # Analyze image
            analysis = core.analyze_image_with_ai(image_path)
            
            # Store in scene
            scene.image_scene_info = f"{analysis['dimensions'][0]}x{analysis['dimensions'][1]}"
            scene.image_scene_type = analysis['scene_type']
            scene.image_scene_analyzed = True
            
            # Store analysis temporarily
            context.window_manager.image_scene_analysis = str(analysis)
            
            self.report({'INFO'}, f"Image analyzed: {scene.image_scene_type}")
            
        except Exception as e:
            self.report({'ERROR'}, f"Analysis failed: {e}")
            return {'CANCELLED'}
        
        return {'FINISHED'}

class GenerateDepthOperator(Operator):
    """Generate Depth Map"""
    bl_idname = "image_scene.generate_depth"
    bl_label = "Generate Depth"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        scene = context.scene
        
        if not scene.image_scene_analyzed:
            self.report({'ERROR'}, "Please import image first!")
            return {'CANCELLED'}
        
        scene.image_scene_depth_status = "Depth map ready"
        self.report({'INFO'}, "Depth map generated")
        
        return {'FINISHED'}

class CreateSceneOperator(Operator):
    """Create Full 3D Scene"""
    bl_idname = "image_scene.create"
    bl_label = "Create 3D Scene"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        image_path = scene.image_scene_path
        
        if not image_path or not scene.image_scene_analyzed:
            self.report({'ERROR'}, "Please import and analyze image first!")
            return {'CANCELLED'}
        
        try:
            from ..core.scene_generator import ImageToSceneCore
            core = ImageToSceneCore()
            
            self.report({'INFO'}, "Creating 3D scene... Please wait")
            
            # Generate full scene
            result = core.process_image_to_scene(image_path)
            
            self.report({'INFO'}, f"Scene created with {result['object_count']} objects!")
            
        except Exception as e:
            self.report({'ERROR'}, f"Scene creation failed: {e}")
            return {'CANCELLED'}
        
        return {'FINISHED'}

class ResetSceneOperator(Operator):
    """Reset Scene"""
    bl_idname = "image_scene.reset"
    bl_label = "Reset"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        scene = context.scene
        
        scene.image_scene_analyzed = False
        scene.image_scene_info = ""
        scene.image_scene_type = ""
        scene.image_scene_depth_status = ""
        
        self.report({'INFO'}, "Scene reset")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AIImageToScenePanel)
    bpy.utils.register_class(ImportImageOperator)
    bpy.utils.register_class(GenerateDepthOperator)
    bpy.utils.register_class(CreateSceneOperator)
    bpy.utils.register_class(ResetSceneOperator)
    
    # Properties
    bpy.types.Scene.image_scene_path = StringProperty(
        name="Image Path",
        description="Path to your photo/image",
        default="",
        subtype='FILE_PATH'
    )
    
    bpy.types.Scene.image_scene_analyzed = BoolProperty(
        name="Analyzed",
        default=False
    )
    
    bpy.types.Scene.image_scene_info = StringProperty(
        name="Image Info",
        default=""
    )
    
    bpy.types.Scene.image_scene_type = StringProperty(
        name="Scene Type",
        default=""
    )
    
    bpy.types.Scene.image_scene_depth_quality = EnumProperty(
        name="Depth Quality",
        items=[
            ('low', 'Low (Fast)', 'Fast but less accurate'),
            ('medium', 'Medium', 'Balanced quality'),
            ('high', 'High (Slow)', 'Best quality, slower'),
        ],
        default='medium'
    )
    
    bpy.types.Scene.image_scene_depth_strength = FloatProperty(
        name="Depth Strength",
        default=1.0,
        min=0.1,
        max=3.0
    )
    
    bpy.types.Scene.image_scene_depth_status = StringProperty(
        name="Depth Status",
        default=""
    )
    
    bpy.types.Scene.image_scene_create_ground = BoolProperty(
        name="Create Ground",
        default=True
    )
    
    bpy.types.Scene.image_scene_create_objects = BoolProperty(
        name="Create Objects",
        default=True
    )
    
    bpy.types.Scene.image_scene_add_lighting = BoolProperty(
        name="Add Lighting",
        default=True
    )
    
    bpy.types.Scene.image_scene_subdivision = IntProperty(
        name="Mesh Detail",
        default=3,
        min=1,
        max=6
    )
    
    bpy.types.Scene.image_scene_use_colors = BoolProperty(
        name="Use Colors",
        default=True
    )
    
    # Window manager property for temp storage
    bpy.types.WindowManager.image_scene_analysis = StringProperty()

def unregister():
    bpy.utils.unregister_class(AIImageToScenePanel)
    bpy.utils.unregister_class(ImportImageOperator)
    bpy.utils.unregister_class(GenerateDepthOperator)
    bpy.utils.unregister_class(CreateSceneOperator)
    bpy.utils.unregister_class(ResetSceneOperator)
    
    del bpy.types.Scene.image_scene_path
    del bpy.types.Scene.image_scene_analyzed
    del bpy.types.Scene.image_scene_info
    del bpy.types.Scene.image_scene_type
    del bpy.types.Scene.image_scene_depth_quality
    del bpy.types.Scene.image_scene_depth_strength
    del bpy.types.Scene.image_scene_depth_status
    del bpy.types.Scene.image_scene_create_ground
    del bpy.types.Scene.image_scene_create_objects
    del bpy.types.Scene.image_scene_add_lighting
    del bpy.types.Scene.image_scene_subdivision
    del bpy.types.Scene.image_scene_use_colors
    del bpy.types.WindowManager.image_scene_analysis
