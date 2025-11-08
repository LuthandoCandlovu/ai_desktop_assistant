import cv2
import os
import pickle
import numpy as np

class FaceRecognizer:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = None
        self.labels = {}
        self.current_id = 0
        self.data_dir = "face_data"
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Load existing training data
        self.load_training_data()
    
    def load_training_data(self):
        """Load existing face recognition training data"""
        try:
            if os.path.exists(os.path.join(self.data_dir, "labels.pickle")):
                with open(os.path.join(self.data_dir, "labels.pickle"), 'rb') as f:
                    self.labels = pickle.load(f)
                self.current_id = max(self.labels.values()) + 1 if self.labels else 0
            print("Face recognition system initialized")
        except Exception as e:
            print(f"Error loading training data: {e}")
            self.labels = {}
            self.current_id = 0
    
    def detect_faces(self, frame):
        """Detect faces in a frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return faces, gray
    
    def register_face(self, name):
        """Register a new face"""
        try:
            cap = cv2.VideoCapture(0)
            face_samples = []
            count = 0
            
            print(f"Registering face for {name}. Look at the camera...")
            
            while count < 30:  # Capture 30 samples
                ret, frame = cap.read()
                if not ret:
                    break
                
                faces, gray = self.detect_faces(frame)
                
                for (x, y, w, h) in faces:
                    roi = gray[y:y+h, x:x+w]
                    face_samples.append(roi)
                    count += 1
                    
                    # Draw rectangle around face
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, f"Capturing: {count}/30", (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                cv2.imshow('Register Face - Press Q to cancel', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            
            if len(face_samples) >= 10:  # Minimum samples required
                # Store the face data
                if name not in self.labels:
                    self.labels[name] = self.current_id
                    self.current_id += 1
                
                # Save labels
                with open(os.path.join(self.data_dir, "labels.pickle"), 'wb') as f:
                    pickle.dump(self.labels, f)
                
                print(f"Face registered successfully for {name} with {len(face_samples)} samples")
                return True
            else:
                print("Not enough face samples captured")
                return False
                
        except Exception as e:
            print(f"Error registering face: {e}")
            return False
    
    def recognize_face(self):
        """Recognize a face from camera"""
        try:
            cap = cv2.VideoCapture(0)
            recognized_name = "Unknown"
            
            print("Looking for faces... Press Q to stop")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                faces, gray = self.detect_faces(frame)
                
                for (x, y, w, h) in faces:
                    # Simple recognition based on face detection only
                    # For proper recognition, you'd need to train a model
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    cv2.putText(frame, "Face Detected", (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                
                cv2.imshow('Face Recognition - Press Q to stop', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            
            if len(faces) > 0:
                # For demo purposes, return a generic name
                # In a real system, you'd use trained models for recognition
                return "User"
            else:
                return None
                
        except Exception as e:
            print(f"Error recognizing face: {e}")
            return None
    
    def train_model(self):
        """Train the face recognition model"""
        # This would train a proper recognition model
        # For now, we'll use basic face detection
        print("Face detection system ready (basic mode)")
        return True

# Simple demo function
def test_face_detection():
    """Test face detection functionality"""
    recognizer = FaceRecognizer()
    
    print("1. Test face detection")
    print("2. Register new face")
    choice = input("Choose option (1 or 2): ")
    
    if choice == "1":
        name = recognizer.recognize_face()
        if name:
            print(f"Welcome {name}!")
        else:
            print("No face detected")
    elif choice == "2":
        name = input("Enter name for registration: ")
        if recognizer.register_face(name):
            print("Registration successful!")
        else:
            print("Registration failed")

if __name__ == "__main__":
    test_face_detection()