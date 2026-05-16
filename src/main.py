import cv2
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from webcam_capture import WebcamCapture
from face_detector import FaceDetector
from mood_classifier import MoodClassifier
from movie_recommender import MovieRecommender
from crew import MoodCrew


class MoodMovieApp:
    def __init__(self):
        self.webcam = WebcamCapture(camera_index=0)
        self.face_detector = FaceDetector()
        self.mood_classifier = MoodClassifier()
        self.movie_recommender = MovieRecommender()
        self.current_mood = "neutral"
        self.current_movies = []
        self.crew = None
        self.frame_count = 0
        self.mood_display_duration = 0

    def init_ollama(self):
        try:
            self.crew = MoodCrew()
            return True
        except Exception as e:
            print(f"Ollama not available: {e}")
            return False

    def draw_text_with_background(self, img, text, x, y, font_scale=0.7, thickness=2, bg_color=(50, 50, 50), text_color=(255, 255, 255)):
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
        cv2.rectangle(img, (x, y - text_size[1] - 10), (x + text_size[0] + 10, y + 10), bg_color, -1)
        cv2.putText(img, text, (x + 5, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, thickness)

    def create_side_panel(self, width=350):
        panel = np.ones((480, width, 3), dtype=np.uint8) * 30

        cv2.putText(panel, "MOOD-BASED MOVIE", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(panel, "RECOMMENDER", (70, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.line(panel, (20, 90), (330, 90), (100, 100, 100), 2)

        y_pos = 130
        cv2.putText(panel, f"Current Mood:", (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (150, 150, 150), 1)

        mood_colors = {
            "happy": (0, 255, 0),
            "sad": (255, 100, 100),
            "neutral": (200, 200, 200),
            "angry": (255, 0, 0),
            "surprised": (0, 165, 255),
            "tired": (128, 128, 128),
            "excited": (0, 255, 255)
        }
        mood_color = mood_colors.get(self.current_mood, (255, 255, 255))

        cv2.putText(panel, self.current_mood.upper(), (20, y_pos + 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, mood_color, 3)

        cv2.line(panel, (20, y_pos + 60), (330, y_pos + 60), (100, 100, 100), 1)

        y_pos = 220
        cv2.putText(panel, "Recommended Movies:", (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (150, 150, 150), 1)
        y_pos += 30

        for i, movie in enumerate(self.current_movies[:5], 1):
            if y_pos > 450:
                break
            cv2.putText(panel, f"{i}.", (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

            if len(movie) > 25:
                movie = movie[:25] + "..."
            cv2.putText(panel, movie, (50, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)
            y_pos += 35

        if self.crew is None:
            cv2.putText(panel, "Ollama not connected", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 100), 1)
            cv2.putText(panel, "Install Ollama for", (20, 475), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 100), 1)
            cv2.putText(panel, "enhanced results", (20, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 100), 1)

        return panel

    def draw_face_mesh(self, frame, landmarks):
        if landmarks is None:
            return frame

        h, w = frame.shape[:2]
        for lm in landmarks:
            x = int(lm[0] * w)
            y = int(lm[1] * h)
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

        nose_tip = landmarks[1]
        nose_x = int(nose_tip[0] * w)
        nose_y = int(nose_tip[1] * h)

        mood_colors = {
            "happy": (0, 255, 0),
            "sad": (255, 100, 100),
            "neutral": (200, 200, 200),
            "angry": (255, 0, 0),
            "surprised": (0, 165, 255),
            "tired": (128, 128, 128),
            "excited": (0, 255, 255)
        }
        mood_color = mood_colors.get(self.current_mood, (255, 255, 255))

        cv2.rectangle(frame, (nose_x - 80, nose_y - 40), (nose_x + 80, nose_y + 20), mood_color, 2)
        cv2.putText(frame, self.current_mood.upper(), (nose_x - 60, nose_y - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, mood_color, 2)

        return frame

    def run(self):
        print("=" * 60)
        print("  Mood-Based Movie Recommender (Real-time)")
        print("  Press 'q' to quit")
        print("=" * 60)

        print("\n[1/4] Initializing webcam...")
        try:
            self.webcam.open()
            print("    [OK] Webcam initialized")
        except Exception as e:
            print(f"    [X] Error: {e}")
            return

        print("\n[2/4] Initializing face detector...")
        print("    [OK] Face detector ready")

        print("\n[3/4] Initializing Ollama...")
        ollama_available = self.init_ollama()
        if ollama_available:
            print("    [OK] Ollama connected")
        else:
            print("    [--] Ollama not available (install from ollama.ai)")

        print("\n[4/4] Starting real-time capture...")
        print("    Press 'q' to exit")

        print("\n" + "=" * 60)
        print("  Running... Move your face in front of camera!")
        print("=" * 60)
        print("\nIf no window appears, check camera permissions.")

        cv2.namedWindow("Mood Movie Recommender")

        landmarks = None
        while True:
            try:
                rgb_frame, bgr_frame = self.webcam.capture_rgb()
            except Exception as e:
                print(f"Camera error: {e}")
                break

            self.frame_count += 1

            if self.frame_count % 5 == 0:
                landmarks = self.face_detector.get_landmarks(rgb_frame)
                if landmarks is not None:
                    self.current_mood = self.mood_classifier.classify(landmarks)
                    self.current_movies = self.movie_recommender.recommend(self.current_mood)
                    self.mood_display_duration = 30

            if self.mood_display_duration > 0:
                self.mood_display_duration -= 1
            else:
                self.current_mood = "neutral"

            frame_with_mesh = self.draw_face_mesh(bgr_frame.copy(), landmarks)

            side_panel = self.create_side_panel()

            combined = np.hstack([frame_with_mesh, side_panel])

            cv2.putText(combined, "Press 'q' to quit", (10, combined.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            cv2.imshow("Mood Movie Recommender", combined)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.webcam.release()
        self.face_detector.close()
        cv2.destroyAllWindows()

        print("\n" + "=" * 60)
        print("  Session ended!")
        print("=" * 60)


def main():
    app = MoodMovieApp()
    app.run()


if __name__ == "__main__":
    main()