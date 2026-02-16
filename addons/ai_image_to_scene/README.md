# AI Image to 3D Scene

Transform any photo into a complete 3D scene with AI-powered analysis, depth generation, and automatic lighting/materials.

## ✨ Features

### 🖼️ One-Click Photo Import
- Load any JPG, PNG, or image file
- Automatic AI analysis of scene content
- Detects objects, colors, and lighting

### 🧠 AI Scene Analysis
- **Dominant Colors**: Extracts primary color palette
- **Object Detection**: Identifies objects in the scene
- **Depth Estimation**: Generates depth maps automatically
- **Lighting Analysis**: Estimates light direction and intensity
- **Scene Classification**: Categorizes as indoor/outdoor/mixed

### 🎯 Automatic 3D Generation
- **Ground Plane**: Creates matching ground surface
- **3D Objects**: Generates geometry from detected objects
- **Depth Displacement**: Creates detailed terrain from depth map
- **Materials**: Applies colors extracted from original image
- **Lighting**: Sets up 3-point lighting based on analysis

### 🎨 Smart Materials
- Color palette from original photo
- Texture mapping with UV coordinates
- Roughness/Metallic auto-adjustment
- World environment matching

## 🚀 How to Use

### Step 1: Import Your Photo
```
1. Open Blender
2. Go to View3D > Sidebar > AI Image Scene
3. Click "Load & Analyze Image"
4. Select your photo (JPG, PNG)
```

### Step 2: Generate Depth
```
1. Select depth quality (Low/Medium/High)
2. Adjust depth strength if needed
3. Click "Generate Depth Map"
```

### Step 3: Create 3D Scene
```
1. Choose options:
   - [x] Ground Plane - adds floor/ground
   - [x] Detect Objects - creates 3D objects
   - [x] Auto Lighting - sets up lights
2. Click "CREATE 3D SCENE"
3. Wait for generation (10-30 seconds)
```

## 📋 Requirements

- Blender 3.6 or higher
- OpenCV (auto-installed)
- NumPy (auto-installed)
- PIL (auto-installed)

## 🎮 Controls

| Option | Description |
|--------|-------------|
| **Depth Quality** | Higher = better but slower |
| **Depth Strength** | How much 3D displacement |
| **Mesh Detail** | Subdivision level (1-6) |
| **Use Colors** | Apply original image colors |

## 💡 Tips

### Best Photo Types:
- ✅ Landscapes (mountains, cities)
- ✅ Indoor scenes (rooms, buildings)
- ✅ Architecture (buildings, streets)
- ⚠️ Portraits (limited 3D info)
- ❌ Solid colors (no depth data)

### For Best Results:
1. Use photos with clear depth (foreground/background)
2. Good lighting helps detection
3. Higher resolution = better detail
4. Avoid blurry images

## 🔧 How It Works

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Photo     │───▶│   AI Analysis│───▶│  Depth Map  │
│   (2D)      │    │  (Colors,    │    │  (Grayscale)│
│             │    │  Objects)    │    │             │
└─────────────┘    └─────────────┘    └──────┬──────┘
                                              │
                                              ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Complete   │◄───│  Materials  │◄───│  3D Mesh   │
│  3D Scene   │    │  & Lighting  │    │  (Displacement)
│             │    │              │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 📸 Example Workflow

**Input**: Photo of mountain landscape

**Process**:
1. AI detects: sky, mountains, ground
2. Extracts: blue tones, brown earth
3. Generates: depth map (mountains closer)
4. Creates: 3D terrain with displacement
5. Adds: matching sky color, sun lighting

**Output**: Complete 3D scene ready to render!

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Image not found" | Check file path |
| Slow generation | Use "Low" quality |
| Flat result | Increase depth strength |
| Wrong colors | Enable "Use Colors" |

## 🆚 Comparison with Video-to-3D

| Feature | Image to 3D | Video to 3D |
|---------|-------------|-------------|
| Input | Single photo | Video file |
| Output | Static scene | Animated scene |
| Speed | Faster | Slower |
| Use Case | Architecture, landscapes | Motion, dynamic scenes |

## 📞 Support

- GitHub Issues: https://github.com/abdelsidi/blender-ai-integration/issues
- Documentation: See main project README

---

**Inspired by AI workflows combining ChatGPT + Blender**
