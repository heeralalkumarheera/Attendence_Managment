"""Face detection and recognition engine using OpenCV and LBPH."""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple

import cv2
import numpy as np

from config import CASCADE_PATH, MODEL_PATH


class FaceEngine:
    """Real-world face detection and recognition engine."""

    def __init__(self):
        self.cascade = cv2.CascadeClassifier(str(CASCADE_PATH))
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.model_loaded = False
        if MODEL_PATH.exists():
            try:
                self.recognizer.read(str(MODEL_PATH))
                self.model_loaded = True
            except Exception:
                pass

    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect faces in image.
        
        Returns list of (x, y, w, h) tuples for each detected face.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(gray, 1.3, 5)
        return [(int(x), int(y), int(w), int(h)) for x, y, w, h in faces]

    def recognize_face(self, image: np.ndarray, x: int, y: int, w: int, h: int) -> Tuple[int, float]:
        """Recognize a face.
        
        Returns (enrollment_id, confidence).
        Confidence < 70 is considered a match.
        """
        if not self.model_loaded:
            return -1, 999.0
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_roi = gray[y:y+h, x:x+w]
        enrollment_id, confidence = self.recognizer.predict(face_roi)
        return int(enrollment_id), float(confidence)

    def draw_detection(self, image: np.ndarray, x: int, y: int, w: int, h: int, 
                      label: str = "Face", color: Tuple[int,int,int] = (0, 255, 0)):
        """Draw rectangle and label on image."""
        cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
        cv2.putText(image, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        return image

    def save_face_image(self, image: np.ndarray, path: Path) -> bool:
        """Save grayscale face image for training."""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(str(path), gray)
            return True
        except Exception:
            return False
