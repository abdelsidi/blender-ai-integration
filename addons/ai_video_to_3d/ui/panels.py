import bpy
from bpy.types import Panel, Operator

class AIVideoTo3DPanel(Panel):
    """AI Video to 3D Panel"""
    bl_label = "Video to 3D"
    bl_idname = "VIEW3D_PT_ai_video_to_3d"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI Tools'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Processing Mode
        box = layout.box()
        box.label(text="Processing Mode", icon='PREFERENCES')
        row = box.row()
        row.prop(scene, "video_3d_mode", text="Mode")
        
        if scene.video_3d_mode == 'local':
            box.label(text="NVIDIA GPU Required", icon='ERROR')
        
        layout.separator()
        
        # Video Import
        box = layout.box()
        box.label(text="Step 1: Import Video", icon='FILE_MOVIE')
        
        row = box.row()
        row.prop(scene, "video_3d_path", text="")
        
        row = box.row()
        row.scale_y = 1.2
        row.operator("video_3d.import", text="Import Video", icon='IMPORT')
        
        if scene.video_3d_info:
            col = box.column()
            col.scale_y = 0.8
            col.label(text=scene.video_3d_info, icon='INFO')
        
        layout.separator()
        
        # Depth Generation
        box = layout.box()
        box.label(text="Step 2: Generate Depth", icon='IMAGE_ZDEPTH')
        
        row = box.row()
        row.prop(scene, "video_3d_sample_rate", text="Sample Every N Frames")
        
        row = box.row()
        row.scale_y = 1.2
        row.operator("video_3d.generate_depth", text="Generate Depth Maps", icon='RENDER_STILL')
        
        if scene.video_3d_depth_status:
            col = box.column()
            col.label(text=scene.video_3d_depth_status, icon='INFO')
        
        layout.separator()
        
        # Displacement
        box = layout.box()
        box.label(text="Step 3: Create 3D", icon='MESH_DATA')
        
        row = box.row()
        row.prop(scene, "video_3d_displacement", text="Displacement Strength")
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("video_3d.displace", text="DISPLACE & ANIMATE", icon='PLAY')
        
        layout.separator()
        
        # Bonus: Text to Image
        box = layout.box()
        box.label(text="Bonus: Text to Image", icon='IMAGE_DATA')
        
        row = box.row()
        row.prop(scene, "video_3d_prompt", text="Prompt")
        
        row = box.row()
        row.prop(scene, "video_3d_image_style", text="Style")
        
        row = box.row()
        row.operator("video_3d.generate_image", text="Generate Image", icon='IMAGE_RGB')

class ImportVideoOperator(Operator):
    """Import Video"""
    bl_idname = "video_3d.import"
    bl_label = "Import Video"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        video_path = context.scene.video_3d_path
        
        if not video_path:
            self.report({'ERROR'}, "Please select a video file!")
            return {'CANCELLED'}
        
        try:
            from ..ai_video_to_3d import VideoTo3DGenerator
            generator = VideoTo3DGenerator()
            info = generator.import_video(video_path)
            
            context.scene.video_3d_info = f"FPS: {info['fps']:.1f} | Frames: {info['frame_count']} | Duration: {info['duration']}s"
            self.report({'INFO'}, f"Video imported: {info['name']}")
        except Exception as e:
            self.report({'ERROR'}, f"Import failed: {e}")
        
        return {'FINISHED'}

class GenerateDepthOperator(Operator):
    """Generate Depth Maps"""
    bl_idname = "video_3d.generate_depth"
    bl_label = "Generate Depth Maps"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        video_path = context.scene.video_3d_path
        
        if not video_path:
            self.report({'ERROR'}, "Please import a video first!")
            return {'CANCELLED'}
        
        self.report({'INFO'}, "Generating depth maps... This may take a while.")
        
        try:
            from ..ai_video_to_3d import VideoTo3DGenerator
            import tempfile
            
            generator = VideoTo3DGenerator()
            temp_dir = tempfile.mkdtemp()
            
            sample_rate = context.scene.video_3d_sample_rate
            frames_dir, frame_count = generator.extract_frames(video_path, temp_dir, sample_rate)
            depth_dir = generator.generate_depth_maps(frames_dir, temp_dir)
            
            context.scene.video_3d_depth_status = f"Generated {frame_count} depth maps"
            self.report({'INFO'}, f"Depth generation complete: {frame_count} frames")
        except Exception as e:
            self.report({'ERROR'}, f"Depth generation failed: {e}")
        
        return {'FINISHED'}

class DisplaceOperator(Operator):
    """Displace & Animate"""
    bl_idname = "video_3d.displace"
    bl_label = "Displace & Animate"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        video_path = context.scene.video_3d_path
        
        if not video_path:
            self.report({'ERROR'}, "Please import a video first!")
            return {'CANCELLED'}
        
        try:
            from ..ai_video_to_3d import VideoTo3DGenerator
            generator = VideoTo3DGenerator()
            
            strength = context.scene.video_3d_displacement
            obj = generator.create_3d_from_video(video_path, strength)
            
            self.report({'INFO'}, f"Created 3D animation: {obj.name}")
        except Exception as e:
            self.report({'ERROR'}, f"3D creation failed: {e}")
        
        return {'FINISHED'}

class GenerateImageOperator(Operator):
    """Generate Image from Text"""
    bl_idname = "video_3d.generate_image"
    bl_label = "Generate Image"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        prompt = context.scene.video_3d_prompt
        
        if not prompt:
            self.report({'ERROR'}, "Please enter a prompt!")
            return {'CANCELLED'}
        
        try:
            from ..ai_video_to_3d import VideoTo3DGenerator
            generator = VideoTo3DGenerator()
            
            style = context.scene.video_3d_image_style
            result = generator.text_to_image_generate(prompt, style)
            
            self.report({'INFO'}, f"Image generated: {result['status']}")
        except Exception as e:
            self.report({'ERROR'}, f"Generation failed: {e}")
        
        return {'FINISHED'}

class CheckDependenciesOperator(Operator):
    """Check Dependencies"""
    bl_idname = "video_3d.check_deps"
    bl_label = "Check Dependencies"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            from ..ai_video_to_3d import VideoTo3DGenerator
            generator = VideoTo3DGenerator()
            deps = generator.check_dependencies()
            
            missing = [k for k, v in deps.items() if not v]
            if missing:
                self.report({'WARNING'}, f"Missing: {', '.join(missing)}")
            else:
                self.report({'INFO'}, "All dependencies installed!")
        except Exception as e:
            self.report({'ERROR'}, f"Check failed: {e}")
        
        return {'FINISHED'}

class InstallDependenciesOperator(Operator):
    """Install Dependencies"""
    bl_idname = "video_3d.install_deps"
    bl_label = "Install Dependencies"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            from ..ai_video_to_3d import VideoTo3DGenerator
            generator = VideoTo3DGenerator()
            generator.install_dependencies()
            
            self.report({'INFO'}, "Dependencies installed! Please restart Blender.")
        except Exception as e:
            self.report({'ERROR'}, f"Install failed: {e}")
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AIVideoTo3DPanel)
    bpy.utils.register_class(ImportVideoOperator)
    bpy.utils.register_class(GenerateDepthOperator)
    bpy.utils.register_class(DisplaceOperator)
    bpy.utils.register_class(GenerateImageOperator)
    bpy.utils.register_class(CheckDependenciesOperator)
    bpy.utils.register_class(InstallDependenciesOperator)
    
    bpy.types.Scene.video_3d_mode = bpy.props.EnumProperty(
        name="Mode",
        items=[
            ('cloud', 'Cloud (Recommended)', 'Cloud processing - no setup'),
            ('local', 'Local (NVIDIA)', 'Local GPU processing - requires NVIDIA'),
        ],
        default='cloud'
    )
    
    bpy.types.Scene.video_3d_path = bpy.props.StringProperty(
        name="Video Path",
        description="Path to video file",
        default="",
        subtype='FILE_PATH'
    )
    
    bpy.types.Scene.video_3d_info = bpy.props.StringProperty(
        name="Video Info",
        default=""
    )
    
    bpy.types.Scene.video_3d_sample_rate = bpy.props.IntProperty(
        name="Sample Rate",
        description="Extract every Nth frame",
        default=1,
        min=1,
        max=30
    )
    
    bpy.types.Scene.video_3d_depth_status = bpy.props.StringProperty(
        name="Depth Status",
        default=""
    )
    
    bpy.types.Scene.video_3d_displacement = bpy.props.FloatProperty(
        name="Displacement",
        description="Displacement strength",
        default=1.0,
        min=0.0,
        max=5.0
    )
    
    bpy.types.Scene.video_3d_prompt = bpy.props.StringProperty(
        name="Prompt",
        description="Text prompt for image generation",
        default="A beautiful landscape"
    )
    
    bpy.types.Scene.video_3d_image_style = bpy.props.EnumProperty(
        name="Style",
        items=[
            ('realistic', 'Realistic', 'Photorealistic'),
            ('artistic', 'Artistic', 'Artistic style'),
            ('abstract', 'Abstract', 'Abstract style'),
        ],
        default='realistic'
    )

def unregister():
    bpy.utils.unregister_class(AIVideoTo3DPanel)
    bpy.utils.unregister_class(ImportVideoOperator)
    bpy.utils.unregister_class(GenerateDepthOperator)
    bpy.utils.unregister_class(DisplaceOperator)
    bpy.utils.unregister_class(GenerateImageOperator)
    bpy.utils.unregister_class(CheckDependenciesOperator)
    bpy.utils.unregister_class(InstallDependenciesOperator)
    
    del bpy.types.Scene.video_3d_mode
    del bpy.types.Scene.video_3d_path
    del bpy.types.Scene.video_3d_info
    del bpy.types.Scene.video_3d_sample_rate
    del bpy.types.Scene.video_3d_depth_status
    del bpy.types.Scene.video_3d_displacement
    del bpy.types.Scene.video_3d_prompt
    del bpy.types.Scene.video_3d_image_style
