import os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np


class FaceDetector:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, '..', 'face_landmarker.task')

        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_faces=1
        )
        self.landmarker = vision.FaceLandmarker.create_from_options(options)

    def detect(self, rgb_frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        results = self.landmarker.detect(mp_image)
        if not results.face_landmarks:
            return None
        return results.face_landmarks[0]

    def get_landmarks(self, rgb_frame):
        landmarks = self.detect(rgb_frame)
        if landmarks is None:
            return None
        return np.array([(lm.x, lm.y, lm.z) for lm in landmarks])

    def close(self):
        self.landmarker.close()