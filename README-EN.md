# Galgame Scene Editor

A powerful, user-friendly Galgame scene editor designed to help game developers easily create and edit visual novel game scenes.

## 🚀 Features

### Scene Editing
- **Background Management**: Support for selecting and switching between different background images
- **Character Sprite System**: Support for displaying multiple sprites simultaneously, with scaling and drag positioning
- **Audio Control**: BGM, sound effects, and voice management, with automatic BGM loop playback
- **Text Editing**: Character name and dialogue content editing, with font and font size adjustment
- **Narrator Mode**: Support for setting narrator text without character names

### Project Management
- **Project Operations**: Create, open, and save projects
- **Multiple Format Support**: JSON and XML format project files
- **Continuation Function**: Support for appending new scenes to existing project files

### Resource Management
- **Automatic Resource Scanning**: Automatically scan and load various resources from the resources folder
- **Voice Import**: Support for importing new voice files into the resource library

### User Experience
- **Real-time Preview**: Real-time scene editing preview functionality
- **Full-screen Mode**: Support for switching to full-screen preview
- **Responsive Design**: Interface adapts to window size changes

## 🛠️ Technology Stack

- **Development Language**: Python
- **GUI Framework**: PyQt5
- **File Formats**: JSON, XML
- **Audio Support**: MP3, WAV, OGG

## 📥 Installation Instructions

### Environment Requirements
- Python 3.6+
- PyQt5 5.15.9+

### Installation Steps

1. **Clone the Project**
   ```bash
   git clone https://your-repository-url/GalSceneEditor.git
   cd GalSceneEditor
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python src/main.py
   ```

## 📖 User Guide

### Basic Operations

1. **Create New Project**: Click the "New Project" button, select save path and file format
2. **Open Project**: Click the "Open Project" button, select an existing project file
3. **Save Project**: Click the "Save Project" button to save current edits

### Scene Editing

1. **Set Background**: Select a background image from the "Background" dropdown menu on the left
2. **Add Character Sprite**: Select the sprite image to display in the "Character Sprites" section, use the slider to adjust size
3. **Adjust Sprite Position**: Drag the sprite directly in the preview area to the desired position
4. **Add Audio**:
   - Select BGM, sound effects, and voice in the "Audio" section
   - Click the "Import" button to add new voice files
5. **Edit Text**:
   - Enter character name and click "Update"
   - Enter dialogue content in the text box
   - Select font and adjust font size

### Full-screen Preview

Press `Alt+Enter` to switch to full-screen preview mode, press again to exit full-screen.

## 📁 Project Structure

```
GalSceneEditor/
├── logs/                  # Log files
├── output/                # Output folder
├── requirements.txt       # Project dependencies
├── resources/             # Resource folder
│   ├── background/        # Background images
│   ├── background_music/  # Background music
│   ├── font/              # Font files
│   ├── icon/              # Icon files
│   ├── portrait/          # Character sprites
│   ├── sound/             # Sound effects
│   └── voice/             # Voice files
└── src/                   # Source code directory
    ├── assets/            # Application resources
    ├── config/            # Configuration
    ├── controllers/       # Controllers
    ├── main.py            # Main program entry
    ├── models/            # Data models
    ├── services/          # Service layer
    ├── utils/             # Utility functions
    └── views/             # User interface
```

## 🔧 Configuration Instructions

Application configuration is located in the `src/config/settings.py` file. You can modify the following main configurations:

- `app`: Basic application information
- `editor`: Editor configuration, such as supported number of sprites, default font, etc.
- `paths`: Resource, output, and log paths
- `logging`: Log level and file size configuration

## 🤝 Contribution Guidelines

1. Create your feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to the branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

## 📝 Notes

- Please ensure all resource files are placed in the correct directories
- For large projects, it is recommended to save regularly to avoid data loss due to unexpected closure
- If adding new resource types, ensure to update the corresponding resource handling code

## 📧 Contact Me

For questions or suggestions, please contact me through:
- Email: xuyehui2023@gmail.com
- GitHub: [TymRina](https://github.com/TymRina)
