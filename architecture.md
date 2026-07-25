# Mood Movie Recommender — Architecture

Real-time webcam mood detection with facial landmark analysis, geometric mood classification, and AI-enriched movie recommendations via CrewAI + Ollama.

## Components

| Node | Role | Tech | Description |
|------|------|------|-------------|
| **User** | user | Webcam | Person sitting in front of camera |
| **WebcamCapture** | orch | OpenCV `VideoCapture` | Captures 640×480 frames at ~30fps, converts BGR→RGB |
| **FaceDetector** | orch | MediaPipe Face Landmarker | Extracts 478 3D facial landmarks from each frame |
| **MoodClassifier** | embed | NumPy geometry | Analyzes 4 facial features to score 7 moods |
| **MovieRecommender** | vector | JSON lookup | Returns 5 movies per mood from `movies.json` |
| **Display** | user | OpenCV GUI | Side panel with mood, movies, and AI details |
| **MoodCrew** | compute | CrewAI Agent + Task | Orchestrates LLM calls for detail generation |
| **Ollama** | compute | llama3.2 | Local LLM runtime for movie descriptions |
| **Cache** | seed | `movie_details.json` | Pre-generated LLM content, loaded at startup |

## Flows

### Flow 1: Real-time Detection (main loop)

The core loop runs every frame (~33ms). Face detection and mood classification happen every 5th frame to keep CPU usage manageable.

| Step | From → To | What happens |
|------|-----------|--------------|
| 1 | User → WebcamCapture | `cv2.VideoCapture.read()` grabs a BGR frame, converts to RGB |
| 2 | WebcamCapture → FaceDetector | MediaPipe detects face and returns 478 landmarks as `(x, y, z)` tuples |
| 3 | FaceDetector → MoodClassifier | 4 geometry features computed: EAR (eye ratio), mouth angle, eyebrow height, lip compression |
| 4 | MoodClassifier → MovieRecommender | Dictionary lookup: `movies.json[mood][:5]` |
| 5 | MovieRecommender → Display | `np.hstack()` combines webcam frame (with mesh overlay) + side panel (mood, movies, AI details) |

### Flow 2: Cache Generation (first run, Ollama required)

One-time process that generates LLM-enriched movie details for all 7 moods. Takes ~3 minutes.

| Step | From → To | What happens |
|------|-----------|--------------|
| 1 | MovieRecommender → MoodCrew | Passes all 7 mood→movie mappings to CrewAI agent |
| 2 | MoodCrew → Ollama | Creates a Task per mood asking for tagline, mood-fit, fun fact per movie |
| 3 | Ollama → MoodCrew | Returns enriched text (capped at 600 chars per mood) |
| 4 | MoodCrew → Cache | `json.dump()` saves to `data/movie_details.json` |

### Flow 3: Cache Load (startup)

Instant load of pre-generated details. No LLM calls at runtime.

| Step | From → To | What happens |
|------|-----------|--------------|
| 1 | Cache → MovieRecommender | `json.load()` reads `movie_details.json` into `self.movie_details` dict |
| 2 | MovieRecommender → Display | Dict lookup per mood: `self.movie_details[current_mood]` |

## Modes

### With Ollama (default)
- All 9 nodes visible
- Cache generation flow available
- Side panel shows AI-enriched movie details (taglines, fun facts)
- First run generates cache; subsequent runs load instantly

### Without Ollama
- Ollama, MoodCrew, and Cache nodes hidden
- Only real-time detection flow works
- Side panel shows movie list only (no AI details)
- App works fully offline with just the deterministic pipeline

## Key Design Decisions

1. **Deterministic mood classification** — Uses facial geometry (EAR, mouth angle, eyebrow position, lip compression) instead of an ML model. Fast (<1ms), no training data needed, works offline.

2. **Pre-computed LLM content** — CrewAI generates details once and caches to JSON. The LLM is never called during the frame loop, keeping the UI responsive at 30fps.

3. **Proxy bypass** — Corporate proxies intercept `localhost:11434` requests. Solved by setting `NO_PROXY` env var and using `base_url="http://127.0.0.1:11434"` explicitly.

4. **CrewAI 1.14.4 native LLM** — Uses `crewai.LLM` (litellm-based) instead of `langchain_ollama.OllamaLLM`. The `ollama/llama3.2` model prefix routes through litellm's Ollama provider.

5. **Frame throttling** — Face detection runs every 5th frame (`frame_count % 5 == 0`) to balance accuracy vs CPU usage. Mood display persists for 30 frames (~1 second) after last detection.

## File Structure

```
testbot-cew/
├── src/
│   ├── main.py               # App entry point, frame loop, GUI
│   ├── webcam_capture.py     # OpenCV webcam wrapper
│   ├── face_detector.py      # MediaPipe face landmark detection
│   ├── mood_classifier.py    # Geometric mood scoring (7 moods)
│   ├── movie_recommender.py  # JSON movie database lookup
│   └── crew.py               # CrewAI + Ollama integration
├── data/
│   ├── movies.json           # Movie lists by mood (5 per mood)
│   └── movie_details.json    # Pre-generated LLM details (cache)
├── face_landmarker.task      # MediaPipe model file
├── architecture.html         # Interactive diagram (this file)
└── architecture.md           # This document
```
