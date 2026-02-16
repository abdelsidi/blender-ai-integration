# 🖼️ AI Image to 3D Scene

Transform any photo into a complete 3D scene with AI-powered depth analysis, automatic object detection, and intelligent lighting.

## ✨ Features

### 🎯 Core Features
- **Image Analysis**: AI analyzes your photo for colors, objects, and lighting
- **Depth Generation**: Creates depth maps from single images
- **3D Scene Generation**: Converts 2D photos into interactive 3D environments
- **Object Detection**: Automatically identifies and creates 3D objects
- **Smart Lighting**: Sets up lighting based on image analysis
- **Displacement Mapping**: Creates realistic terrain and surfaces

### 🚀 How It Works

#### Step 1: Import Your Photo
- Load any image (JPG, PNG)
- AI automatically analyzes colors, lighting, and composition

#### Step 2: AI Analysis
- Detects dominant colors
- Identifies objects and their positions
- Estimates lighting direction
- Classifies scene type (indoor, outdoor, etc.)

#### Step 3: Generate 3D Scene
- Creates ground plane with proper materials
- Generates 3D objects from detected elements
- Applies displacement based on depth map
- Sets up lighting matching the original photo
- Creates camera with optimal angle

## 📦 Installation

1. Download `blender_ai_complete.zip` from releases
2. Open Blender
3. Edit > Preferences > Add-ons > Install
4. Select the ZIP file
5. Enable "AI Image to 3D Scene"

## 🎮 Usage

### Quick Start

1. **Open the Panel**: Press N in 3D viewport, find "AI Scene" tab

2. **Load Image**:
   - Click "Browse" next to Image Path
   - Select your photo
   - Click "Load & Analyze Image"

3. **Review Analysis**:
   - Scene type (indoor/outdoor)
   - Number of detected objects
   - Dominant colors

4. **Configure Settings**:
   - Enable/disable ground plane
   - Toggle object creation
   - Adjust displacement strength
   - Set quality level

5. **Generate**:
   - Click "GENERATE 3D SCENE"
   - Wait for processing
   - Enjoy your 3D scene!

### Settings Explained

- **Ground Plane**: Creates a floor that matches image colors
- **Detected Objects**: Creates 3D shapes for objects found in image
- **Depth Displacement**: Adds 3D depth using generated depth map
- **Auto Lighting**: Creates lights matching original photo lighting
- **Clear Scene**: Removes existing objects before generation

## 🎨 Example Workflows

### Landscape Photo
```
Input: Mountain landscape photo
Output: 3D terrain with mountains, matching sky color, proper lighting
```

### Indoor Room
```
Input: Living room photo
Output: Room with furniture objects, walls, floor, matching lighting
```

### Product Photo
```
Input: Product on table
Output: Product as 3D object with table, studio lighting setup
```

## 🔧 Requirements

- Blender 3.6 or newer
- Python dependencies (auto-installed):
  - OpenCV (cv2)
  - NumPy
  - Pillow (PIL)

## 🛠️ Advanced Features

### Manual Controls
- **Camera Setup**: One-click camera positioning
- **Lighting Tools**: Add three-point lighting
- **Depth Tools**: Add displacement to any object
- **Reset**: Clear all settings and start over

### Quality Settings
- **Low**: Fast generation, basic details
- **Medium**: Balanced quality and speed
- **High**: Best quality, slower processing

## 📝 Tips

1. **Best Results**: Use clear, well-lit photos
2. **Resolution**: Higher resolution images give better depth maps
3. **Composition**: Photos with clear foreground/background work best
4. **Colors**: Images with distinct color areas create better materials

## 🐛 Troubleshooting

**Image won't load**:
- Check file format (JPG/PNG only)
- Verify file path has no special characters

**No objects detected**:
- Try images with clear, distinct objects
- Increase image contrast

**Blender freezes**:
- Use "Low" quality setting for large images
- Reduce image size before importing

## 🔮 Future Features

- [ ] AI-powered texture generation
- [ ] Sky/background replacement
- [ ] Automatic material creation from image
- [ ] Integration with Stable Diffusion
- [ ] Cloud processing for faster results

## 📄 License

MIT License - See LICENSE file

---

Made with ❤️ for the Blender community
