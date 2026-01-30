"""Train face recognition model from registered images."""
from __future__ import annotations

import tkinter as tk
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from PIL import Image

from config import CASCADE_PATH, MODEL_PATH, TRAINING_DIR
from utils.logger import log_info, log_error


def train_model_background() -> bool:
    """Train model in background without GUI (for auto-training after registration)."""
    try:
        log_info("Starting background model training...")
        
        # Delete old model to force fresh training
        if MODEL_PATH.exists():
            try:
                MODEL_PATH.unlink()
                log_info("Old model deleted for fresh training")
            except:
                pass
        
        # Collect images
        image_paths = list(TRAINING_DIR.glob("*.jpg"))
        if not image_paths:
            log_error("No training images found")
            return False

        # Extract faces and IDs with proper hash function
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        cascade = cv2.CascadeClassifier(str(CASCADE_PATH))
        
        faces, ids = [], []
        enrollment_to_id_map = {}  # Map enrollment strings to sequential IDs
        next_id = 0
        
        print(f"Training with {len(image_paths)} images...")
        
        for img_path in image_paths:
            try:
                pil_img = Image.open(img_path).convert('L')
                img_array = np.array(pil_img, 'uint8')
                
                # Extract enrollment ID from filename (name.enrollment.sample.jpg)
                parts = img_path.stem.split('.')
                if len(parts) >= 2:
                    enrollment_str = parts[1]  # Keep as string: "22155151024"
                    
                    # Map string enrollment to sequential ID
                    if enrollment_str not in enrollment_to_id_map:
                        enrollment_to_id_map[enrollment_str] = next_id
                        next_id += 1
                    
                    model_id = enrollment_to_id_map[enrollment_str]
                    print(f"  Image {img_path.name}: Enrollment '{enrollment_str}' -> Model ID {model_id}")
                else:
                    continue

                # Detect faces
                detected_faces = cascade.detectMultiScale(img_array)
                for (x, y, w, h) in detected_faces:
                    faces.append(img_array[y:y+h, x:x+w])
                    ids.append(model_id)

            except Exception as e:
                log_error(f"Error processing {img_path}: {e}")
                continue

        if not faces:
            log_error("No faces detected in training images")
            return False

        print(f"Training model with {len(faces)} faces from {len(enrollment_to_id_map)} students")
        print(f"Enrollment to Model ID mapping: {enrollment_to_id_map}")
        
        # Train model
        recognizer.train(faces, np.array(ids))
        
        # Save model
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        recognizer.save(str(MODEL_PATH))
        
        # Save the mapping for later use
        import json
        mapping_file = MODEL_PATH.parent / "enrollment_map.json"
        with open(mapping_file, 'w') as f:
            json.dump(enrollment_to_id_map, f)
        
        log_info(f"Background training complete: {len(faces)} faces, {len(enrollment_to_id_map)} students")
        log_info(f"Enrollment mapping saved: {enrollment_to_id_map}")
        return True

    except Exception as exc:
        log_error(f"Background training error: {exc}")
        return False


def train_model(master: Optional[tk.Tk] = None) -> None:
    """Train LBPH face recognizer on student images."""
    
    win = tk.Toplevel(master) if master else tk.Tk()
    win.title("Model Training")
    win.geometry("600x300")
    win.configure(bg="#1e3a5f")

    tk.Label(win, text="🧠 Face Recognition Model Training", bg="#2c5f8d", fg="white",
             font=("Arial", 18, "bold"), pady=10).pack(fill="x")

    status_var = tk.StringVar(value="Ready to train...")
    status_label = tk.Label(win, textvariable=status_var, bg="#28a745", fg="white",
                            font=("Arial", 11, "bold"), pady=8, wraplength=500)
    status_label.pack(fill="x", padx=10, pady=10)

    progress_var = tk.IntVar(value=0)
    progress_bar = tk.Canvas(win, bg="#0c1b2a", height=30, relief="sunken", bd=2)
    progress_bar.pack(fill="x", padx=10, pady=10)

    def do_training():
        status_var.set("⚡ Collecting training images...")
        status_label.config(bg="#0d6efd")
        win.update()

        try:
            # Delete old model to force fresh training
            if MODEL_PATH.exists():
                try:
                    MODEL_PATH.unlink()
                    log_info("Old model deleted for fresh training")
                except:
                    pass
            
            # Collect images
            image_paths = list(TRAINING_DIR.glob("*.jpg"))
            if not image_paths:
                status_var.set("❌ No training images found in TrainingImage folder!")
                status_label.config(bg="#dc3545")
                log_error("No training images found")
                return

            status_var.set(f"📂 Found {len(image_paths)} images. Extracting features...")
            status_label.config(bg="#0d6efd")
            win.update()

            # Extract faces and IDs with proper hash function
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            cascade = cv2.CascadeClassifier(str(CASCADE_PATH))
            
            faces, ids = [], []
            enrollment_to_id_map = {}  # Map enrollment strings to sequential IDs
            next_id = 0
            
            for idx, img_path in enumerate(image_paths):
                try:
                    pil_img = Image.open(img_path).convert('L')
                    img_array = np.array(pil_img, 'uint8')
                    
                    # Extract enrollment ID from filename (name.enrollment.sample.jpg)
                    parts = img_path.stem.split('.')
                    if len(parts) >= 2:
                        enrollment_str = parts[1]  # Keep as string: "22155151024"
                        
                        # Map string enrollment to sequential ID
                        if enrollment_str not in enrollment_to_id_map:
                            enrollment_to_id_map[enrollment_str] = next_id
                            next_id += 1
                        
                        model_id = enrollment_to_id_map[enrollment_str]
                    else:
                        continue

                    # Detect faces
                    detected_faces = cascade.detectMultiScale(img_array)
                    for (x, y, w, h) in detected_faces:
                        faces.append(img_array[y:y+h, x:x+w])
                        ids.append(model_id)

                    # Update progress
                    progress = int((idx + 1) / len(image_paths) * 100)
                    progress_var.set(progress)
                    progress_bar.delete("all")
                    progress_bar.create_rectangle(0, 0, progress * 6, 30, fill="#28a745", outline="")
                    progress_bar.create_text(300, 15, text=f"{progress}%", fill="white", font=("Arial", 12, "bold"))
                    win.update()

                except Exception as e:
                    log_error(f"Error processing {img_path}: {e}")
                    continue

            if not faces:
                status_var.set("❌ No faces detected in training images!")
                status_label.config(bg="#dc3545")
                return

            # Train model
            status_var.set(f"🧠 Training model on {len(faces)} face samples...")
            status_label.config(bg="#0d6efd")
            win.update()

            recognizer.train(faces, np.array(ids))
            
            # Save model
            MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
            recognizer.save(str(MODEL_PATH))
            
            # Save the mapping for later use
            import json
            mapping_file = MODEL_PATH.parent / "enrollment_map.json"
            with open(mapping_file, 'w') as f:
                json.dump(enrollment_to_id_map, f)

            log_info(f"Model trained successfully: {len(faces)} faces, {len(enrollment_to_id_map)} unique students")
            log_info(f"Enrollment mapping: {enrollment_to_id_map}")
            status_var.set(f"✅ Training complete! {len(faces)} faces trained from {len(enrollment_to_id_map)} students")
            status_label.config(bg="#28a745")

        except Exception as exc:
            log_error(f"Training error: {exc}")
            status_var.set(f"❌ Error: {exc}")
            status_label.config(bg="#dc3545")

    train_btn = tk.Button(win, text="🚀 START TRAINING", command=do_training,
                          bg="#6f42c1", fg="white", font=("Arial", 13, "bold"),
                          relief="raised", bd=3, cursor="hand2", padx=20, pady=8)
    train_btn.pack(pady=15)

    info_text = tk.Label(win, 
                        text="Training uses LBPH (Local Binary Patterns Histograms)\nfor efficient, real-time face recognition.",
                        bg="#1e3a5f", fg="#b5d3ff", font=("Arial", 10), justify="center")
    info_text.pack(pady=10)

    win.mainloop()


if __name__ == "__main__":
    train_model()
