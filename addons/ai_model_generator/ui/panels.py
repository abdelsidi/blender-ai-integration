import bpy
from bpy.types import Panel, Operator
from bpy.props import StringProperty, EnumProperty, BoolProperty

class AIModelGeneratorPanel(Panel):
    """لوحة مولد النماذج ثلاثية الأبعاد"""
    bl_label = "🎨 AI Model Generator"
    bl_idname = "VIEW3D_PT_ai_model_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # عنوان القسم
        box = layout.box()
        box.label(text="توليد من نص", icon='FONT_DATA')
        
        # حقل النص
        row = box.row()
        row.prop(scene, "ai_model_text_prompt", text="الوصف")
        
        # زر التوليد من نص
        row = box.row()
        row.scale_y = 1.3
        row.operator("ai_model.generate_from_text", 
                     text="توليد من النص", 
                     icon='MESH_CUBE')
        
        layout.separator()
        
        # قسم الصور
        box = layout.box()
        box.label(text="توليد من صورة", icon='IMAGE_DATA')
        
        row = box.row()
        row.prop(scene, "ai_model_image_path", text="مسار الصورة")
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("ai_model.generate_from_image", 
                     text="توليد من الصورة", 
                     icon='IMAGE_PLANE')
        
        layout.separator()
        
        # الإعدادات
        box = layout.box()
        box.label(text="⚙️ الإعدادات", icon='PREFERENCES')
        
        row = box.row()
        row.prop(scene, "ai_model_style")
        
        row = box.row()
        row.prop(scene, "ai_model_resolution")
        
        row = box.row()
        row.prop(scene, "ai_model_material")
        
        layout.separator()
        
        # النماذج البدائية السريعة
        box = layout.box()
        box.label(text="⚡ نماذج سريعة", icon='MODIFIER')
        
        row = box.row(align=True)
        row.operator("ai_model.create_primitive", text="مكعب").primitive_type = 'cube'
        row.operator("ai_model.create_primitive", text="كرة").primitive_type = 'sphere'
        
        row = box.row(align=True)
        row.operator("ai_model.create_primitive", text="أسطوانة").primitive_type = 'cylinder'
        row.operator("ai_model.create_primitive", text="حلقة").primitive_type = 'torus'
        
        layout.separator()
        
        # التحسينات
        box = layout.box()
        box.label(text="🔧 تحسينات", icon='MOD_SUBSURF')
        
        row = box.row()
        row.prop(scene, "ai_model_subdivision", text="التقسيم")
        
        row = box.row()
        row.operator("ai_model.optimize", text="تحسين الشبكة", icon='MESH_DATA')

class GenerateFromTextOperator(Operator):
    """توليد نموذج من نص"""
    bl_idname = "ai_model.generate_from_text"
    bl_label = "Generate Model from Text"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        prompt = scene.ai_model_text_prompt
        
        if not prompt:
            self.report({'ERROR'}, "يرجى إدخال وصف للنموذج!")
            return {'CANCELLED'}
        
        try:
            # إنشاء نموذج بدائي كمثال
            from ..ai_model_generator import AIModelGenerator
            generator = AIModelGenerator()
            obj = generator.create_primitive_model("monkey", f"AI_{prompt[:10]}")
            
            # تطبيق التحسينات
            if scene.ai_model_subdivision > 0:
                generator.apply_subdivision(obj, scene.ai_model_subdivision)
            
            # إضافة المادة
            generator.add_material(obj, scene.ai_model_material)
            
            self.report({'INFO'}, f"✅ تم إنشاء النموذج: {obj.name}")
        except Exception as e:
            self.report({'ERROR'}, f"❌ فشل التوليد: {e}")
        
        return {'FINISHED'}

class GenerateFromImageOperator(Operator):
    """توليد نموذج من صورة"""
    bl_idname = "ai_model.generate_from_image"
    bl_label = "Generate Model from Image"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        image_path = scene.ai_model_image_path
        
        if not image_path:
            self.report({'ERROR'}, "يرجى تحديد مسار الصورة!")
            return {'CANCELLED'}
        
        self.report({'INFO'}, f"🔄 جاري معالجة الصورة: {image_path}")
        return {'FINISHED'}

class CreatePrimitiveOperator(Operator):
    """إنشاء نموذج بدائي"""
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
            
            self.report({'INFO'}, f"✅ تم إنشاء: {obj.name}")
        except Exception as e:
            self.report({'ERROR'}, f"❌ فشل: {e}")
        
        return {'FINISHED'}

class OptimizeMeshOperator(Operator):
    """تحسين شبكة النموذج"""
    bl_idname = "ai_model.optimize"
    bl_label = "Optimize Mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selected = context.selected_objects
        
        if not selected:
            self.report({'ERROR'}, "يرجى تحديد كائن!")
            return {'CANCELLED'}
        
        try:
            from ..ai_model_generator import AIModelGenerator
            generator = AIModelGenerator()
            
            for obj in selected:
                if obj.type == 'MESH':
                    generator.optimize_mesh(obj)
            
            self.report({'INFO'}, f"✅ تم تحسين {len(selected)} كائن")
        except Exception as e:
            self.report({'ERROR'}, f"❌ فشل التحسين: {e}")
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AIModelGeneratorPanel)
    bpy.utils.register_class(GenerateFromTextOperator)
    bpy.utils.register_class(GenerateFromImageOperator)
    bpy.utils.register_class(CreatePrimitiveOperator)
    bpy.utils.register_class(OptimizeMeshOperator)
    
    # خصائص المشهد
    bpy.types.Scene.ai_model_text_prompt = bpy.props.StringProperty(
        name="Prompt",
        description="وصف النموذج المطلوب",
        default="تفاحة حمراء"
    )
    
    bpy.types.Scene.ai_model_image_path = bpy.props.StringProperty(
        name="Image Path",
        description="مسار الصورة",
        default="",
        subtype='FILE_PATH'
    )
    
    bpy.types.Scene.ai_model_style = bpy.props.EnumProperty(
        name="الأسلوب",
        items=[
            ('simple', 'بسيط', 'نموذج بسيط'),
            ('detailed', 'تفصيلي', 'نموذج مع التفاصيل'),
            ('realistic', 'واقعي', 'نموذج واقعي'),
            ('stylized', 'أسلوبي', 'نموذج أسلوبي'),
            ('cartoon', 'كرتوني', 'نموذج كرتوني'),
        ],
        default='detailed'
    )
    
    bpy.types.Scene.ai_model_resolution = bpy.props.EnumProperty(
        name="الدقة",
        items=[
            ('low', 'منخفضة', '1000 رأس'),
            ('medium', 'متوسطة', '5000 رأس'),
            ('high', 'عالية', '20000 رأس'),
            ('ultra', 'فائقة', '100000 رأس'),
        ],
        default='medium'
    )
    
    bpy.types.Scene.ai_model_material = bpy.props.EnumProperty(
        name="المادة",
        items=[
            ('clay', 'طين', 'مادة طينية'),
            ('metal', 'معدن', 'مادة معدنية'),
            ('plastic', 'بلاستيك', 'مادة بلاستيكية'),
        ],
        default='clay'
    )
    
    bpy.types.Scene.ai_model_subdivision = bpy.props.IntProperty(
        name="مستوى التقسيم",
        description="عدد مستويات تقسيم الأسطح",
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
