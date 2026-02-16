# AI Image to 3D Scene - Blender Addon

[![Blender](https://img.shields.io/badge/Blender-3.6+-green.svg)](https://www.blender.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **🚀 Transform any photo into a complete 3D scene with AI**

Transform flat 2D images into immersive 3D environments using AI-powered depth estimation, object detection, and automatic scene generation.

![Workflow](docs/images/workflow.jpg)

## ✨ What It Does

This addon converts **any photo** into a **complete 3D scene** in Blender:

1. 📸 **Import** - Load your JPG/PNG photo
2. 🧠 **Analyze** - AI extracts colors, objects, and lighting
3. 🗺️ **Depth** - Generate depth map automatically  
4. 🎨 **Create** - Build 3D scene with geometry, materials & lighting

## 🎯 Perfect For

- 🏠 **Architects** - Turn photos into 3D walkthroughs
- 🎮 **Game Devs** - Quick environment prototyping
- 🎬 **Filmmakers** - Create 3D backgrounds from photos
- 🎨 **Artists** - Experiment with photo-based 3D art

## ⚡ Quick Start

### Installation

1. Download `ai_image_to_scene.zip` from [Releases](../../releases)
2. In Blender: `Edit > Preferences > Add-ons > Install`
3. Select the ZIP file
4. Enable "AI Image to 3D Scene"

### Usage

```
1. Press N in 3D Viewport
2. Open "AI Image Scene" tab
3. Click "Load & Analyze Image"
4. Select your photo
5. Click "CREATE 3D SCENE"
```

That's it! Your photo is now a 3D scene.

## 🎬 How It Works

```
Photo Input → AI Analysis → Depth Map → 3D Mesh → Complete Scene
    (2D)        (Colors,       (B&W)     (Displaced    (Materials +
                Objects)                Terrain)       Lighting)
```

### AI Analysis Includes:
- 🎨 **Color Extraction** - Dominant colors from photo
- 🔍 **Object Detection** - Identifies main elements
- 🗺️ **Depth Estimation** - Calculates distance info
- 💡 **Lighting Direction** - Estimates light source
- 🏷️ **Scene Type** - Classifies indoor/outdoor

## 📦 Features

### Core Features
- ✅ **One-click import** of any JPG/PNG
- ✅ **Automatic depth** generation from single image
- ✅ **Smart object detection** and 3D placement
- ✅ **Color-matched materials** from photo
- ✅ **Auto lighting** setup (3-point system)
- ✅ **Ground plane** generation
- ✅ **Displacement mapping** for terrain detail
- ✅ **Camera setup** with optimal angle

### Advanced Options
- Adjustable depth strength (0.1x - 3.0x)
- Mesh detail control (1-6 subdivision levels)
- Quality modes (Fast/Balanced/Best)
- Toggle ground/objects/lighting individually

## 🖼️ Example Scenes

| Input Photo | Output Scene |
|-------------|--------------|
| Mountain landscape | 3D terrain with peaks/valleys |
| City street | Buildings with depth + street lights |
| Living room | Furniture as 3D objects + proper lighting |
| Beach sunset | Ocean plane + sun lighting + sky color |

## 📋 Requirements

- **Blender** 3.6 or higher
- **OpenCV** (auto-installed)
- **NumPy** (auto-installed)  
- **PIL** (auto-installed)

## 🎮 UI Overview

```
┌─────────────────────────────┐
│  AI Image to 3D Scene       │
├─────────────────────────────┤
│  Step 1: Import Image       │
│  [Browse...] [Load Photo]   │
├─────────────────────────────┤
│  Step 2: Generate Depth     │
│  Quality: [Medium ▼]        │
│  Strength: [────●───] 1.0   │
│  [Generate Depth Map]       │
├─────────────────────────────┤
│  Step 3: Create 3D Scene    │
│  [✓] Ground Plane           │
│  [✓] Detect Objects         │
│  [✓] Auto Lighting          │
│                             │
│  [ CREATE 3D SCENE ]        │
└─────────────────────────────┘
```

## 🆚 vs Video-to-3D

| | Image to 3D | Video to 3D |
|---|-------------|-------------|
| **Input** | Single photo | Video file |
| **Output** | Static scene | Animated scene |
| **Speed** | 10-30 seconds | 2-5 minutes |
| **Best For** | Architecture, landscapes | Motion, characters |

## 🛠️ Technical Details

### Scene Generation Pipeline
1. **Image Loading** - OpenCV reads image
2. **K-Means Clustering** - Extracts dominant colors
3. **Contour Detection** - Identifies objects
4. **Gradient Analysis** - Estimates depth
5. **Mesh Displacement** - Creates 3D terrain
6. **Material Nodes** - Builds shader networks
7. **Lighting Setup** - 3-point lighting system

### Generated Elements
- **Ground Plane** - 20x20 units with subdivision
- **Depth Mesh** - 50x subdivided displaced plane
- **Detected Objects** - Cubes/cylinders based on shape
- **Materials** - Principled BSDF with image textures
- **Lights** - Sun + Area + Spot lights
- **Camera** - Positioned at optimal angle

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Image not found" | Check file exists and path is correct |
| Slow generation | Use "Low" quality setting |
| Flat 3D result | Increase "Depth Strength" slider |
| Wrong colors | Enable "Use Image Colors" checkbox |
| No objects created | Photo may lack clear objects - try landscapes |

## 📸 Best Photo Tips

✅ **Works Great:**
- Landscapes with foreground/background
- Architecture photos
- Rooms with furniture
- City streets

⚠️ **Okay Results:**
- Close-ups
- Portraits
- Abstract images

❌ **Avoid:**
- Solid color images
- Very blurry photos
- Logos/text only

## 📝 License

MIT License - See [LICENSE](../LICENSE)

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md)

## 🙏 Credits

Inspired by AI workflows combining computer vision with 3D graphics.

---

**[Download Latest Release](../../releases)** | **[Full Documentation](../docs)** | **[Report Issues](../../issues)**

*Transform your photos into worlds.*
