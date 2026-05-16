# Mood Movie Recommender

[![Python](https://img.shields.io/badge/python-3.8+-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A real-time application that detects your mood through your webcam using facial landmark detection and recommends movies based on your current emotional state.

## Features

- **Real-time Face Detection**: Uses MediaPipe to detect faces and extract 478 facial landmarks
- **Mood Classification**: Analyzes facial expressions to classify 7 different moods (happy, sad, neutral, angry, surprised, tired, excited)
- **Movie Recommendations**: Suggests 5 movies tailored to your detected mood
- **Optional AI Enhancement**: Integrates with Ollama (llama3.2) and CrewAI for personalized AI-powered recommendations
- **Visual Feedback**: Displays real-time mood detection with facial mesh overlay and side panel

## Prerequisites

- **Python**: 3.8 or higher (tested with 3.13)
- **Webcam**: Built-in or external camera
- **Optional**: [Ollama](https://ollama.ai) with llama3.2 model for AI features

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd testbot-cew
```

### 2. Create a Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Install Ollama for AI Features

If you want AI-powered recommendations:

1. Download and install Ollama from [ollama.ai](https://ollama.ai)
2. Pull the llama3.2 model:
   ```bash
   ollama pull llama3.2
   ```
3. Start Ollama in the background:
   ```bash
   ollama serve
   ```

## Running the Application

```bash
python src/main.py
```

### Controls

- **q**: Quit the application

### Expected Output

```
============================================================
  Mood-Based Movie Recommender (Real-time)
  Press 'q' to quit
============================================================

[1/4] Initializing webcam...
    [OK] Webcam initialized

[2/4] Initializing face detector...
    [OK] Face detector ready

[3/4] Initializing Ollama...
    [--] Ollama not available (install from ollama.ai)

[4/4] Starting real-time capture...
    Press 'q' to exit

============================================================
  Running... Move your face in front of camera!
============================================================

If no window appears, check camera permissions.
```

## Configuration

### Changing Camera Index

If you have multiple cameras or your webcam is not at index 0, modify `src/main.py`:

```python
# Line 17 - Change camera_index to your webcam's index
self.webcam = WebcamCapture(camera_index=0)  # Try 1, 2, etc.
```

### Modifying Movie Database

Edit `data/movies.json` to customize movie recommendations:

```json
{
  "happy": ["Your Movie 1", "Your Movie 2", ...],
  "sad": ["Your Movie 3", "Your Movie 4", ...],
  ...
}
```

### Changing Mood Detection Sensitivity

Edit thresholds in `src/mood_classifier.py`:

- **Eye Aspect Ratio (EAR)**: Lines 75-80 control tired/excited detection
- **Mouth Corner Angle**: Lines 82-89 control happy/sad detection
- **Eyebrow Position**: Lines 91-95 control angry/surprised detection

### Changing AI Model

In `src/crew.py`, modify the Ollama model:

```python
# Line 7 - Change to different model
self.llm = OllamaLLM(model="llama3.2")  # Try "mistral", "codellama", etc.
```

## Project Structure

```
testbot-cew/
├── src/
│   ├── __init__.py           # Package initializer
│   ├── main.py               # Main application entry point
│   ├── webcam_capture.py     # Webcam capture and frame handling
│   ├── face_detector.py      # MediaPipe face landmark detection
│   ├── mood_classifier.py    # Facial expression analysis and mood classification
│   ├── movie_recommender.py  # Movie database and recommendation logic
│   └── crew.py               # Ollama + CrewAI integration (optional AI features)
├── data/
│   └── movies.json           # Movie database categorized by mood
├── face_landmarker.task      # MediaPipe face landmarker model file
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT License
└── README.md                 # This file
```

## Troubleshooting

### Webcam Not Found

1. **Check camera index**: Try changing `camera_index` in `main.py` to 1, 2, etc.
2. **Check permissions**: Ensure your app has camera access
3. **Check device**: Verify webcam works in other applications
4. **On Linux**: Add yourself to the video group: `sudo usermod -a -G video $USER`

### Face Detection Not Working

1. **Lighting**: Ensure good lighting on your face
2. **Distance**: Position yourself 30-60cm from the camera
3. **Framing**: Ensure your face is centered and visible

### Ollama Connection Failed

1. **Verify Ollama is running**: `ollama serve`
2. **Check model installed**: `ollama list`
3. **Try pulling model again**: `ollama pull llama3.2`
4. **Check port**: Ollama typically runs on port 11434

### Installation Errors

1. **Upgrade pip**: `pip install --upgrade pip`
2. **Check Python version**: `python --version`
3. **Install system dependencies**:
   - **Ubuntu/Debian**: `sudo apt-get install libgl1-mesa-glx libglib2.0-0`
   - **macOS**: `brew install opencv`
   - **Windows**: Usually automatic with opencv-python

### MediaPipe Model Not Found

Ensure `face_landmarker.task` is in the project root directory (same level as README.md).

## Customization

### Adding New Moods

1. **Modify mood_classifier.py** (line 6): Add new mood to the list
2. **Modify movie_recommender.py**: Add movie list for new mood
3. **Update data/movies.json**: Add new mood category with movies

### Adding More Movie Recommendations

Edit `data/movies.json` - you can add more than 5 movies per mood:

```json
"happy": [
  "Movie 1",
  "Movie 2",
  "Movie 3",
  "Movie 4",
  "Movie 5",
  "Movie 6",
  "Movie 7"
]
```

The app will display the first 5 from the list.

### Changing Display Panel

Modify `create_side_panel()` method in `src/main.py`:
- Panel width: Line 40
- Colors: Lines 51-59 (mood_colors dictionary)
- Text positions: Various y_pos variables

## How It Works

### 1. Face Detection
The app uses MediaPipe's Face Landmarker to detect faces and extract 478 3D facial landmarks in real-time.

### 2. Mood Classification
The `MoodClassifier` class analyzes:
- **Eye Aspect Ratio (EAR)**: Detects eye openness (tired vs excited)
- **Mouth Corner Angle**: Detects smiling/frowning (happy vs sad)
- **Eyebrow Position**: Detects raised/lowered eyebrows (surprised vs angry)
- **Lip Compression**: Detects tension (angry vs neutral)

### 3. Movie Recommendation
Based on the detected mood, the `MovieRecommender` class fetches the predefined list of movies from `movies.json`.

### 4. AI Enhancement (Optional)
When Ollama is available, the CrewAI agents provide personalized movie introductions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [MediaPipe](https://mediapipe.dev) - Face landmark detection
- [OpenCV](https://opencv.org) - Computer vision
- [CrewAI](https://crewai.com) - AI agent framework
- [Ollama](https://ollama.ai) - Local LLM runtime