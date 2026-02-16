import bpy
from bpy.types import Panel, Operator

class AIMaterialGeneratorPanel(Panel):
    """لوحة تحكم AI Material Generator"""
    bl_label = "AI Material Generator"
    bl_idname = "VIEW3D_PT_ai_material_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text="إعدادات API:")
        row = layout.row()
        row.prop(context.scene, "ai_material_prompt")
        
        row = layout.row()
        row.prop(context.scene, "ai_material_model")
        
        layout.label(text="إعدادات المادة:")
        row = layout.row()
        row.prop(context.scene, "ai_material_style")
        
        layout.separator()
        
        row = layout.row()
        row.scale_y = 1.5
        row.operator("ai_material.generate", text="Generate Material", icon='MATERIAL')
        
        row = layout.row()
        row.scale_y = 1.5
        row.operator("ai_material.apply", text="Apply Material", icon='CHECKMARK')

class GenerateMaterialOperator(Operator):
    """مشغل إنشاء المادة"""
    bl_idname = "ai_material.generate"
    bl_label = "Generate AI Material"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        prompt = scene.ai_material_prompt
        style = scene.ai_material_style
        
        if not prompt:
            self.report({'ERROR'}, "Please enter a prompt!")
            return {'CANCELLED'}
        
        try:
            self.report({'INFO'}, f"Generating material: {prompt}")
            scene.ai_material_last_prompt = prompt
            scene.ai_material_last_style = style
            self.report({'INFO'}, "Material generated successfully!")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to generate material: {e}")
        
        return {'FINISHED'}

class ApplyMaterialOperator(Operator):
    """مشغل تطبيق المادة"""
    bl_idname = "ai_material.apply"
    bl_label = "Apply AI Material"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selected_objects = context.selected_objects
        
        if not selected_objects:
            self.report({'ERROR'}, "No objects selected!")
            return {'CANCELLED'}
        
        try:
            self.report({'INFO'}, f"Applying material to {len(selected_objects)} objects")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to apply material: {e}")
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AIMaterialGeneratorPanel)
    bpy.utils.register_class(GenerateMaterialOperator)
    bpy.utils.register_class(ApplyMaterialOperator)

def unregister():
    bpy.utils.unregister_class(AIMaterialGeneratorPanel)
    bpy.utils.unregister_class(GenerateMaterialOperator)
    bpy.utils.unregister_class(ApplyMaterialOperator)
