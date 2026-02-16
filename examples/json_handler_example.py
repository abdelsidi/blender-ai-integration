"""
JSON Handler Example
How to use JSON files in Blender AI Integration
"""

import json
import os
from pathlib import Path

class JSONHandler:
    """Handle JSON configuration and data files"""
    
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.config_dir = self.base_path / "config"
        self.assets_dir = self.base_path / "assets" / "presets"
        self.cache_dir = self.base_path / ".cache"
    
    # ==================== SETTINGS ====================
    
    def load_settings(self):
        """Load project settings"""
        settings_path = self.config_dir / "settings.json"
        
        if not settings_path.exists():
            print("Settings file not found, using defaults")
            return self.get_default_settings()
        
        with open(settings_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_default_settings(self):
        """Return default settings"""
        return {
            "project": {
                "name": "Blender AI Integration",
                "version": "1.0.0"
            },
            "features": {
                "material_generator": True,
                "model_generator": True
            }
        }
    
    # ==================== USER PREFERENCES ====================
    
    def load_user_preferences(self):
        """Load user preferences"""
        prefs_path = self.config_dir / "user_preferences.json"
        
        if not prefs_path.exists():
            return self.get_default_preferences()
        
        with open(prefs_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_default_preferences(self):
        """Return default preferences"""
        return {
            "user": {"name": "Default", "language": "en"},
            "preferences": {"default_material": "clay"},
            "recent_prompts": []
        }
    
    def save_user_preferences(self, prefs):
        """Save user preferences"""
        prefs_path = self.config_dir / "user_preferences.json"
        
        with open(prefs_path, 'w', encoding='utf-8') as f:
            json.dump(prefs, f, indent=2, ensure_ascii=False)
    
    def add_recent_prompt(self, prompt):
        """Add prompt to recent list"""
        prefs = self.load_user_preferences()
        
        # Add to beginning, remove duplicates, keep max 10
        recent = prefs.get("recent_prompts", [])
        if prompt in recent:
            recent.remove(prompt)
        recent.insert(0, prompt)
        recent = recent[:10]  # Keep only 10
        
        prefs["recent_prompts"] = recent
        self.save_user_preferences(prefs)
    
    # ==================== MATERIALS ====================
    
    def load_material_presets(self):
        """Load material presets"""
        materials_path = self.assets_dir / "materials.json"
        
        if not materials_path.exists():
            return {"materials": [], "categories": []}
        
        with open(materials_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_material_preset(self, name, material_data):
        """Save a new material preset"""
        data = self.load_material_presets()
        
        # Create new material entry
        new_material = {
            "id": f"mat_{len(data['materials']) + 1:03d}",
            "name": name,
            "type": material_data.get("type", "custom"),
            "color": material_data.get("color", [0.5, 0.5, 0.5, 1.0]),
            "roughness": material_data.get("roughness", 0.5),
            "metallic": material_data.get("metallic", 0.0),
            "prompt": material_data.get("prompt", "")
        }
        
        data["materials"].append(new_material)
        
        # Save back
        materials_path = self.assets_dir / "materials.json"
        with open(materials_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return new_material["id"]
    
    def get_material_by_name(self, name):
        """Get material by name"""
        data = self.load_material_presets()
        
        for mat in data["materials"]:
            if mat["name"].lower() == name.lower():
                return mat
        
        return None
    
    # ==================== MODELS ====================
    
    def load_model_presets(self):
        """Load model presets"""
        models_path = self.assets_dir / "models.json"
        
        if not models_path.exists():
            return {"models": []}
        
        with open(models_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # ==================== CACHE ====================
    
    def load_cache(self):
        """Load AI cache"""
        cache_path = self.cache_dir / "ai_responses.json"
        
        if not cache_path.exists():
            return {"cache": {"entries": []}}
        
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_cache(self, cache_data):
        """Save AI cache"""
        cache_path = self.cache_dir / "ai_responses.json"
        
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
    
    def get_cached_result(self, prompt, cache_type="model"):
        """Get cached result for prompt"""
        cache = self.load_cache()
        
        for entry in cache.get("cache", {}).get("entries", []):
            if entry["prompt"] == prompt and entry["type"] == cache_type:
                return entry["result"]
        
        return None
    
    def add_to_cache(self, prompt, result, cache_type="model"):
        """Add result to cache"""
        cache = self.load_cache()
        
        from datetime import datetime, timedelta
        
        new_entry = {
            "id": f"cache_{len(cache['cache']['entries']) + 1:03d}",
            "prompt": prompt,
            "type": cache_type,
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "expires": (datetime.now() + timedelta(days=1)).isoformat()
        }
        
        cache["cache"]["entries"].append(new_entry)
        self.save_cache(cache)
    
    def clear_cache(self):
        """Clear all cache entries"""
        cache = {"cache": {"entries": [], "version": "1.0"}}
        self.save_cache(cache)


# ==================== USAGE EXAMPLE ====================

if __name__ == "__main__":
    # Initialize handler
    handler = JSONHandler("/path/to/blender-ai-integration")
    
    # Load settings
    settings = handler.load_settings()
    print(f"Project: {settings['project']['name']}")
    
    # Load user preferences
    prefs = handler.load_user_preferences()
    print(f"User: {prefs['user']['name']}")
    print(f"Recent prompts: {prefs['recent_prompts']}")
    
    # Add a recent prompt
    handler.add_recent_prompt("golden sphere")
    
    # Load materials
    materials = handler.load_material_presets()
    print(f"Available materials: {len(materials['materials'])}")
    for mat in materials['materials']:
        print(f"  - {mat['name']}")
    
    # Get material by name
    red_metal = handler.get_material_by_name("Red Metallic")
    if red_metal:
        print(f"Found material: {red_metal['color']}")
    
    # Check cache
    cached = handler.get_cached_result("red apple", "model")
    if cached:
        print(f"Cache hit: {cached}")
    else:
        print("Not in cache")
