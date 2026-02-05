import cv2
import numpy as np
import os

class FaceRecognitionUtils:
    def __init__(self):
        self.camera = None
        # Load OpenCV's pre-trained face detector
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def capture_face_encoding(self):
        """Simplified face capture for demo - returns a dummy encoding"""
        try:
            # Try different camera indices for Docker compatibility
            cap = None
            for i in range(3):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    break
                cap.release()
            
            if cap is None or not cap.isOpened():
                print("Camera not available - using demo mode")
                # Return a random encoding for demo purposes
                return np.random.rand(128)
            
            print("Capturing face for demo...")
            
            frame_count = 0
            while frame_count < 30:  # Try for 30 frames
                ret, frame = cap.read()
                if not ret:
                    frame_count += 1
                    continue
                
                # Convert to grayscale for face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                
                if len(faces) > 0:
                    # Face detected - return a unique encoding based on face position
                    x, y, w, h = faces[0]
                    # Create a simple "encoding" based on face characteristics
                    encoding = np.array([x, y, w, h] + [np.random.rand() for _ in range(124)])
                    cap.release()
                    return encoding
                
                frame_count += 1
            
            cap.release()
            # If no face detected, return random encoding for demo
            return np.random.rand(128)
            
        except Exception as e:
            print(f"Camera error: {e}")
            # Return dummy encoding for demo
            return np.random.rand(128)
    
    def detect_faces_in_frame(self, frame):
        """Detect faces using OpenCV"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        return faces, []
    
    def compare_faces(self, known_encodings, face_encoding, tolerance=0.6):
        """Simple face comparison for demo"""
        if len(known_encodings) == 0:
            return None, None
        
        # Simple distance calculation for demo
        distances = []
        for known_encoding in known_encodings:
            # Calculate Euclidean distance
            distance = np.linalg.norm(np.array(known_encoding) - np.array(face_encoding))
            distances.append(distance)
        
        min_distance_index = np.argmin(distances)
        min_distance = distances[min_distance_index]
        
        # For demo purposes, accept if distance is reasonable
        if min_distance < 50:  # Arbitrary threshold for demo
            return min_distance_index, min_distance
        
        return None, None
    
    def process_image_for_encoding(self, image_array):
        """Process captured image and generate face encoding"""
        try:
            # Convert to grayscale for face detection
            if len(image_array.shape) == 3:
                gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = image_array
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                # Get the first detected face
                x, y, w, h = faces[0]
                # Create a simple "encoding" based on face characteristics
                face_region = gray[y:y+h, x:x+w]
                
                # Generate encoding based on face region statistics
                encoding = np.array([
                    x, y, w, h,  # Position and size
                    np.mean(face_region),  # Average intensity
                    np.std(face_region),   # Standard deviation
                    np.min(face_region),   # Min intensity
                    np.max(face_region)    # Max intensity
                ] + [np.random.rand() for _ in range(120)])  # Random features for demo
                
                return encoding
            else:
                return None
                
        except Exception as e:
            print(f"Error processing image: {e}")
            return None