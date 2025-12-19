from tkinter import *
from tkinter import messagebox
import cv2
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from src.db_helper import DatabaseHelper

class OnlineAttendance:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """Setup window"""
        self.root.title("Online Attendance - Face Detection")
        self.root.geometry("600x400")
        self.root.maxsize(600, 400)
        self.root.minsize(600, 400)
        self.root["bg"] = Config.BG_COLOR
    
    def create_widgets(self):
        """Create widgets"""
        lbl_title = Label(
            self.root, 
            text="Automatic Attendance", 
            font="arial 28 bold",
            bg=Config.BG_COLOR
        )
        lbl_title.pack(pady=20)
        
        # Subject selection
        lbl_subject = Label(
            self.root, 
            text="Subject Name:", 
            font="arial 20 bold",
            bg=Config.BG_COLOR
        )
        lbl_subject.place(x=50, y=100)
        
        # Get subjects from database
        subjects = DatabaseHelper.get_all_subjects()
        self.subject_dict = {f"{sub[2]}": sub[0] for sub in subjects} if subjects else {}
        
        from tkinter import ttk
        self.subject_var = StringVar()
        self.subject_combo = ttk.Combobox(
            self.root,
            textvariable=self.subject_var,
            values=list(self.subject_dict.keys()),
            font="arial 16",
            state="readonly",
            width=25
        )
        self.subject_combo.place(x=50, y=150)
        if self.subject_dict:
            self.subject_combo.current(0)
        
        # Submit button
        btn_submit = Button(
            self.root, 
            text="Start Attendance", 
            padx=30, 
            pady=15, 
            bd=8,
            bg='#4CAF50',
            fg='white',
            font="arial 14 bold",
            command=self.start_attendance
        )
        btn_submit.place(x=200, y=250)
        
        # Info label
        lbl_info = Label(
            self.root,
            text="Note: Face detection will start. Press 'P' to stop.",
            font="arial 10",
            bg=Config.BG_COLOR,
            fg='#555'
        )
        lbl_info.place(x=100, y=330)
    
    def start_attendance(self):
        """Start face detection based attendance"""
        subject_name = self.subject_var.get()
        
        if not subject_name:
            messagebox.showerror("Error", "Please select a subject")
            return
        
        subject = DatabaseHelper.get_subject_by_name(subject_name)
        if not subject:
            messagebox.showerror("Error", "Subject not found in database")
            return
        
        subject_id = subject[0]
        
        try:
            # Load cascade classifier
            cascade_path = Config.FACE_CASCADE_PATH
            if not os.path.exists(cascade_path):
                # Fallback to OpenCV's built-in cascade
                cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            
            face_cascade = cv2.CascadeClassifier(cascade_path)
            
            # Start video capture
            vid = cv2.VideoCapture(0)
            if not vid.isOpened():
                messagebox.showerror("Error", "Could not open webcam")
                return
            
            detected_faces = []
            
            messagebox.showinfo("Info", "Face detection started. Press 'P' to stop and mark attendance.")
            
            while True:
                ret, frame = vid.read()
                if not ret:
                    break
                
                # Convert to grayscale for detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                
                # Draw rectangles around faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, "Face Detected", (x, y-10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Display frame
                cv2.imshow("Online Attendance - Press 'P' to stop", frame)
                
                # Store detected faces count
                if len(faces) > 0:
                    detected_faces.append(len(faces))
                
                # Press 'P' to stop
                if cv2.waitKey(1) & 0xFF == ord('p'):
                    break
            
            vid.release()
            cv2.destroyAllWindows()
            
            if detected_faces:
                messagebox.showinfo(
                    "Detection Complete", 
                    f"Detected faces in {len(detected_faces)} frames.\n\n"
                    "Note: In a complete system, this would:\n"
                    "1. Recognize specific students\n"
                    "2. Automatically mark their attendance\n"
                    "3. Store records in database"
                )
            else:
                messagebox.showwarning("No Detection", "No faces were detected")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = Tk()
    app = OnlineAttendance(root)
    root.mainloop()

if __name__ == "__main__":
    main()
