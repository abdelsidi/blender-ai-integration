import bpy
from bpy.types import Panel, Operator
from bpy.props import StringProperty, EnumProperty, BoolProperty

class AIModelGeneratorPanel(Panel):
    """AI Model Generator Panel"""
    bl_label = "AI Model Generator"
    bl_idname = "VIEW3D_PT_ai_model_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Text generation section
        box = layout.box()
        box.label(text="Generate from Text", icon='FONT_DATA')
        
        row = box.row()
        row.prop(scene, "ai_model_text_prompt", text="Description")
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("ai_model.generate_from_text", 
                     text="Generate from Text", 
                     icon='MESH_CUBE')
        
        layout.separator()
        
        # Image section
        box = layout.box()
        box.label(text="Generate from Image", icon='IMAGE_DATA')
        
        row = box.row()
        row.prop(scene, "ai_model_image_path", text="Image Path")
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("ai_model.generate_from_image", 
                     text="Generate from Image", 
                     icon='IMAGE_PLANE')
        
        layout.separator()
        
        # Settings
        box = layout.box()
        box.label(text="Settings", icon='PREFERENCES')
        
        row = box.row()
        row.prop(scene, "ai_model_style")
        
        row = box.row()
        row.prop(scene, "ai_model_resolution")
        
        row = box.row()
        row.prop(scene, "ai_model_material")
        
        layout.separator()
        
        # Quick primitives
        box = layout.box()
        box.label(text="Quick Primitives", icon='MODIFIER')
        
        row = box.row(align=True)
        row.operator("ai_model.create_primitive", text="Cube").primitive_type = 'cube'
        row.operator("ai_model.create_primitive", text="Sphere").primitive_type = 'sphere'
        
        row = box.row(align=True)
        row.operator("ai_model.create_primitive", text="Cylinder").primitive_type = 'cylinder'
        row.operator("ai_model.create_primitive", text="Torus").primitive_type = 'torus'
        
        layout.separator()
        
        # Enhancements
        box = layout.box()
        box.label(text="Enhancements", icon='MOD_SUBSURF')
        
        row = box.row()
        row.prop(scene, "ai_model_subdivision", text="Subdivision")
        
        row = box.row()
        row.operator("ai_model.optimize", text="Optimize Mesh", icon='MESH_DATA')

class GenerateFromTextOperator(Operator):
    """Generate Model from Text"""
    bl_idname = "ai_model.generate_from_text"
    bl_label = "Generate Model from Text"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        prompt = scene.ai_model_text_prompt
        
        if not prompt:
            self.report({'ERROR'}, "Please enter a description!")
            return {'CANCELLED'}
        
        try:
            from ..ai_model_generator import AIModelGenerator
            generator = AIModelGenerator()
            obj = generator.create_primitive_model("monkey", f"AI_{prompt[:10]}")
            
            if scene.ai_model_subdivision > 0:
                generator.apply_subdivision(obj, scene.ai_model_subdivision)
            
            generator.add_material(obj, scene.ai_model_material)
            
            self.report({'INFO'}, f"Created: {obj.name}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed: {e}")
        
        return {'FINISHED'}

class GenerateFromImageOperator(Operator):
    """Generate Model from Image"""
    bl_idname = "ai_model.generate_from_image"
    bl_label = "Generate Model from Image"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        image_path = scene.ai_model_image_path
        
        if not image_path:
            self.report({'ERROR'}, "Please select image path!")
            return {'CANCELLED'}
        
        self.report({'INFO'}, f"Processing: {image_path}")
        return {'FINISHED'}

class CreatePrimitiveOperator(Operator):
    """Create Primitive"""
    bl_idname = "ai_model.create_primitive"
    bl_label = "Create Primitive"
    bl_options = {'REGISTER', 'UNDO'}
    
    primitive_type: bpy.props.StringProperty(default='cube')
    
    def execute(self, context):
        try:
            from ..ai_model_generator import AIModelGenerator
            generator = AIModelGenerator()
            obj = generator.create_primitive_model(self.primitive_type)
            
            scene = context.scene
            if scene.ai_model_subdivision > 0:
                generator.apply_subdivision(obj, scene.ai_model_subdivision)
            
            generator.add_material(obj, scene.ai_model_material)
            
            self.report({'INFO'}, f"Created: {obj.name}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed: {e}")
        
        return {'FINISHED'}

class OptimizeMeshOperator(Operator):
    """Optimize Mesh"""
    bl_idname = "ai_model.optimize"
    bl_label = "Optimize Mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selected = context.selected_objects
        
        if not selected:
            self.report({'ERROR'}, "Please select an object!")
            return {'CANCELLED'}
        
        try:
            from ..ai_model_generator import AIModelGenerator
            generator = AIModelGenerator()
            
            for obj in selected:
                if obj.type == 'MESH':
                    generator.optimize_mesh(obj)
            
            self.report({'INFO'}, f"Optimized {len(selected)} objects")
        except Exception as e:
            self.report({'ERROR'}, f"Failed: {e}")
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AIModelGeneratorPanel)
    bpy.utils.register_class(GenerateFromTextOperator)
    bpy.utils.register_class(GenerateFromImageOperator)
    bpy.utils.register_class(CreatePrimitiveOperator)
    bpy.utils.register_class(OptimizeMeshOperator)
    
    bpy.types.Scene.ai_model_text_prompt = bpy.props.StringProperty(
        name="Prompt",
        description="Model description",
        default="red apple"
    )
    
    bpy.types.Scene.ai_model_image_path = bpy.props.StringProperty(
        name="Image Path",
        description="Image path",
        default="",
        subtype='FILE_PATH'
    )
    
    bpy.types.Scene.ai_model_style = bpy.props.EnumProperty(
        name="Style",
        items=[
            ('simple', 'Simple', 'Simple model'),
            ('detailed', 'Detailed', 'Detailed model'),
            ('realistic', 'Realistic', 'Realistic model'),
            ('stylized', 'Stylized', 'Stylized model'),
            ('cartoon', 'Cartoon', 'Cartoon model'),
        ],
        default='detailed'
    )
    
    bpy.types.Scene.ai_model_resolution = bpy.props.EnumProperty(
        name="Resolution",
        items=[
            ('low', 'Low', '1000 vertices'),
            ('medium', 'Medium', '5000 vertices'),
            ('high', 'High', '20000 vertices'),
            ('ultra', 'Ultra', '100000 vertices'),
        ],
        default='medium'
    )
    
    bpy.types.Scene.ai_model_material = bpy.props.EnumProperty(
        name="Material",
        items=[
            ('clay', 'Clay', 'Clay material'),
            ('metal', 'Metal', 'Metal material'),
            ('plastic', 'Plastic', 'Plastic material'),
        ],
        default='clay'
    )
    
    bpy.types.Scene.ai_model_subdivision = bpy.props.IntProperty(
        name="Subdivision Level",
        description="Subdivision surface levels",
        default=2,
        min=0,
        max=6
    )

def unregister():
    bpy.utils.unregister_class(AIModelGeneratorPanel)
    bpy.utils.unregister_class(GenerateFromTextOperator)
    bpy.utils.unregister_class(GenerateFromImageOperator)
    bpy.utils.unregister_class(CreatePrimitiveOperator)
    bpy.utils.unregister_class(OptimizeMeshOperator)
    
    del bpy.types.Scene.ai_model_text_prompt
    del bpy.types.Scene.ai_model_image_path
    del bpy.types.Scene.ai_model_style
    del bpy.types.Scene.ai_model_resolution
    del bpy.types.Scene.ai_model_material
    del bpy.types.Scene.ai_model_subdivision
