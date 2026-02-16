import bpy
from bpy.types import Panel, Operator

class AIRenderOptimizerPanel(Panel):
    """AI Render Optimizer Panel"""
    bl_label = "AI Render Optimizer"
    bl_idname = "RENDER_PT_ai_render_optimizer"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Scene analysis
        box = layout.box()
        box.label(text="Scene Analysis", icon='VIEWZOOM')
        
        row = box.row()
        row.operator("ai_render.analyze", text="Analyze Complexity")
        
        if scene.ai_render_analysis:
            col = box.column()
            col.label(text=scene.ai_render_analysis, icon='INFO')
        
        layout.separator()
        
        # Quality presets
        box = layout.box()
        box.label(text="Render Quality", icon='RENDER_STILL')
        
        row = box.row()
        row.prop(scene, "ai_render_quality", text="")
        
        row = box.row()
        row.scale_y = 1.3
        row.operator("ai_render.optimize", text="Apply Settings", icon='CHECKMARK')
        
        row = box.row()
        row.operator("ai_render.auto_optimize", text="Auto Optimize", icon='SHADERFX')
        
        layout.separator()
        
        # Time estimate
        box = layout.box()
        box.label(text="Render Time", icon='TIME')
        
        row = box.row()
        row.operator("ai_render.estimate_time", text="Estimate Time")
        
        if scene.ai_render_time_estimate:
            col = box.column()
            col.label(text=scene.ai_render_time_estimate, icon='INFO')
        
        layout.separator()
        
        # Additional optimizations
        box = layout.box()
        box.label(text="Enhancements", icon='MODIFIER')
        
        row = box.row()
        row.operator("ai_render.optimize_lighting", text="Optimize Lighting")

class AnalyzeSceneOperator(Operator):
    """Analyze Scene"""
    bl_idname = "ai_render.analyze"
    bl_label = "Analyze Scene"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            from ..ai_render_optimizer import AIRenderOptimizer
            optimizer = AIRenderOptimizer()
            stats = optimizer.analyze_scene_complexity(context.scene)
            
            analysis = f"Objects: {stats['objects']} | Vertices: {stats['vertices']} | Complexity: {stats['complexity_score']:.1f}"
            context.scene.ai_render_analysis = analysis
            
            self.report({'INFO'}, f"Analyzed - Complexity: {stats['complexity_score']:.1f}")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        
        return {'FINISHED'}

class OptimizeSettingsOperator(Operator):
    """Optimize Settings"""
    bl_idname = "ai_render.optimize"
    bl_label = "Optimize Settings"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        quality = context.scene.ai_render_quality
        
        try:
            from ..ai_render_optimizer import AIRenderOptimizer
            optimizer = AIRenderOptimizer()
            settings = optimizer.optimize_settings(context.scene, quality)
            
            self.report({'INFO'}, f"Applied: {quality} - Samples: {settings.get('samples', 'N/A')}")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        
        return {'FINISHED'}

class AutoOptimizeOperator(Operator):
    """Auto Optimize"""
    bl_idname = "ai_render.auto_optimize"
    bl_label = "Auto Optimize"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            from ..ai_render_optimizer import AIRenderOptimizer
            optimizer = AIRenderOptimizer()
            result = optimizer.auto_optimize(context.scene)
            
            context.scene.ai_render_quality = result['quality_level']
            
            self.report({'INFO'}, f"Auto optimized: {result['quality_level']}")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        
        return {'FINISHED'}

class EstimateTimeOperator(Operator):
    """Estimate Render Time"""
    bl_idname = "ai_render.estimate_time"
    bl_label = "Estimate Render Time"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            from ..ai_render_optimizer import AIRenderOptimizer
            optimizer = AIRenderOptimizer()
            estimate = optimizer.estimate_render_time(context.scene)
            
            time_text = f"Estimated: {estimate['estimated_minutes']} minutes"
            context.scene.ai_render_time_estimate = time_text
            
            self.report({'INFO'}, f"{time_text}")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        
        return {'FINISHED'}

class OptimizeLightingOperator(Operator):
    """Optimize Lighting"""
    bl_idname = "ai_render.optimize_lighting"
    bl_label = "Optimize Lighting"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            from ..ai_render_optimizer import AIRenderOptimizer
            optimizer = AIRenderOptimizer()
            optimizations = optimizer.optimize_lighting_for_render(context.scene)
            
            count = len(optimizations)
            self.report({'INFO'}, f"Optimized {count} lights")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AIRenderOptimizerPanel)
    bpy.utils.register_class(AnalyzeSceneOperator)
    bpy.utils.register_class(OptimizeSettingsOperator)
    bpy.utils.register_class(AutoOptimizeOperator)
    bpy.utils.register_class(EstimateTimeOperator)
    bpy.utils.register_class(OptimizeLightingOperator)
    
    bpy.types.Scene.ai_render_quality = bpy.props.EnumProperty(
        name="Render Quality",
        items=[
            ('draft', 'Draft', 'Fast for testing'),
            ('preview', 'Preview', 'Medium quality'),
            ('production', 'Production', 'High quality'),
            ('cinematic', 'Cinematic', 'Highest quality'),
        ],
        default='production'
    )
    
    bpy.types.Scene.ai_render_analysis = bpy.props.StringProperty(default="")
    bpy.types.Scene.ai_render_time_estimate = bpy.props.StringProperty(default="")

def unregister():
    bpy.utils.unregister_class(AIRenderOptimizerPanel)
    bpy.utils.unregister_class(AnalyzeSceneOperator)
    bpy.utils.unregister_class(OptimizeSettingsOperator)
    bpy.utils.unregister_class(AutoOptimizeOperator)
    bpy.utils.unregister_class(EstimateTimeOperator)
    bpy.utils.unregister_class(OptimizeLightingOperator)
    
    del bpy.types.Scene.ai_render_quality
    del bpy.types.Scene.ai_render_analysis
    del bpy.types.Scene.ai_render_time_estimate
