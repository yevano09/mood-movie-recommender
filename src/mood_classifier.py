import numpy as np


class MoodClassifier:
    def __init__(self):
        self.moods = ["happy", "sad", "neutral", "angry", "surprised", "tired", "excited"]

    def calculate_ear(self, landmarks):
        def eye_aspect_ratio(eye_indices):
            left = landmarks[eye_indices[0]]
            right = landmarks[eye_indices[1]]
            top = landmarks[eye_indices[2]]
            bottom = landmarks[eye_indices[3]]
            horizontal = np.linalg.norm(right[:2] - left[:2])
            vertical = np.linalg.norm(top[:2] - bottom[:2])
            if horizontal == 0:
                return 0
            return vertical / horizontal

        left_eye = [33, 160, 158, 133, 153, 144]
        right_eye = [263, 387, 385, 362, 380, 373]
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        return (left_ear + right_ear) / 2

    def calculate_mouth_corner_angle(self, landmarks):
        upper_lip = landmarks[13]
        lower_lip = landmarks[14]
        left_corner = landmarks[61]
        right_corner = landmarks[291]

        mouth_center = (upper_lip[:2] + lower_lip[:2]) / 2
        left_vec = left_corner[:2] - mouth_center
        right_vec = right_corner[:2] - mouth_center

        left_angle = np.arctan2(left_vec[1], left_vec[0])
        right_angle = np.arctan2(right_vec[1], right_vec[0])

        return (left_angle + right_angle) / 2

    def calculate_eyebrow_position(self, landmarks):
        left_eyebrow_inner = landmarks[107]
        left_eyebrow_outer = landmarks[70]
        left_eye_top = landmarks[159]

        eyebrow_height = (left_eyebrow_inner[1] + left_eyebrow_outer[1]) / 2
        eye_height = left_eye_top[1]

        return eyebrow_height - eye_height

    def calculate_lip_compression(self, landmarks):
        upper_lip = landmarks[13]
        lower_lip = landmarks[14]
        left_corner = landmarks[61]
        right_corner = landmarks[291]

        lip_distance = np.linalg.norm(upper_lip[:2] - lower_lip[:2])
        mouth_width = np.linalg.norm(right_corner[:2] - left_corner[:2])

        if mouth_width == 0:
            return 0
        return lip_distance / mouth_width

    def classify(self, landmarks):
        if landmarks is None:
            return "neutral"

        ear = self.calculate_ear(landmarks)
        mouth_angle = self.calculate_mouth_corner_angle(landmarks)
        eyebrow_pos = self.calculate_eyebrow_position(landmarks)
        lip_compression = self.calculate_lip_compression(landmarks)

        scores = {mood: 0 for mood in self.moods}

        if ear < 0.2:
            scores["tired"] += 2
            scores["sad"] += 1
        elif ear > 0.35:
            scores["excited"] += 1
            scores["surprised"] += 1

        if mouth_angle > 0.1:
            scores["happy"] += 3
            scores["excited"] += 1
        elif mouth_angle < -0.1:
            scores["sad"] += 2
            scores["angry"] += 1
        else:
            scores["neutral"] += 2

        if eyebrow_pos < -0.02:
            scores["angry"] += 2
            scores["sad"] += 1
        elif eyebrow_pos > 0.02:
            scores["surprised"] += 2

        if lip_compression > 0.15:
            scores["angry"] += 1
            scores["tired"] += 1
        elif lip_compression < 0.08:
            scores["happy"] += 1

        detected_mood = max(scores, key=scores.get)
        return detected_mood

    def get_confidence(self, landmarks):
        if landmarks is None:
            return 0.0
        return 1.0