from tkinter import *
from tkinter import messagebox
import cv2
import time
import os
import sys
from PIL import Image, ImageTk

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from src.db_helper import DatabaseHelper

# Ensure directories exist
Config.ensure_directories()

class MainInterface:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """Setup main window"""
        self.root.title("Face Recognition Attendance System")
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.maxsize(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        self.root.minsize(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        self.root["bg"] = Config.BG_COLOR
        
        # Load and set background image
        self.load_background()
    
    def load_background(self):
        """Load background image"""
        try:
            bg_path = os.path.join(Config.ASSETS_DIR, "bg.jpg")
            if os.path.exists(bg_path):
                image = Image.open(bg_path)
                image = image.resize((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT), Image.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(image)
                
                bg_label = Label(self.root, image=self.bg_image)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Could not load background image: {e}")
    
    def create_widgets(self):
        """Create GUI widgets"""
        # Title
        lbl_title = Label(
            self.root, 
            text="Face Recognition Attendance System", 
            font="arial 30 bold",
            bg=Config.BG_COLOR
        )
        lbl_title.place(x=250, y=5)
        
        # Enrollment ID
        lbl_enroll = Label(
            self.root, 
            text="Enrollment ID:", 
            font="arial 18 bold",
            bg=Config.BG_COLOR
        )
        lbl_enroll.place(x=100, y=100)
        
        self.entry_enrollment = Entry(self.root, width=40, font="arial 18 bold")
        self.entry_enrollment.place(x=350, y=100)
        
        btn_clear_enroll = Button(
            self.root, 
            text="Clear", 
            padx=20, 
            pady=10, 
            bd=8, 
            bg='grey',
            command=lambda: self.entry_enrollment.delete(0, END)
        )
        btn_clear_enroll.place(x=950, y=100)
        
        # Name
        lbl_name = Label(
            self.root, 
            text="Name:", 
            font="arial 18 bold",
            bg=Config.BG_COLOR
        )
        lbl_name.place(x=100, y=200)
        
        self.entry_name = Entry(self.root, width=40, font="arial 18 bold")
        self.entry_name.place(x=350, y=200)
        
        btn_clear_name = Button(
            self.root, 
            text="Clear", 
            padx=20, 
            pady=10, 
            bd=8, 
            bg='grey',
            command=lambda: self.entry_name.delete(0, END)
        )
        btn_clear_name.place(x=950, y=200)
        
        # Buttons
        btn_takeimage = Button(
            self.root, 
            text="Register Student", 
            padx=30, 
            pady=20, 
            bd=8, 
            bg='#4CAF50',
            fg='white',
            font="arial 12 bold",
            command=self.take_image
        )
        btn_takeimage.place(x=100, y=380)
        
        btn_online_attendance = Button(
            self.root, 
            text="Online Attendance", 
            padx=30, 
            pady=20, 
            bd=8, 
            bg='#2196F3',
            fg='white',
            font="arial 12 bold",
            command=self.open_online_attendance
        )
        btn_online_attendance.place(x=366, y=380)
        
        btn_manual_attendance = Button(
            self.root, 
            text="Manual Attendance", 
            padx=30, 
            pady=20, 
            bd=8, 
            bg='#FF9800',
            fg='white',
            font="arial 12 bold",
            command=self.open_manual_attendance
        )
        btn_manual_attendance.place(x=632, y=380)
        
        btn_check_attendance = Button(
            self.root, 
            text="Check Attendance", 
            padx=30, 
            pady=20, 
            bd=8, 
            bg='#9C27B0',
            fg='white',
            font="arial 12 bold",
            command=self.open_login
        )
        btn_check_attendance.place(x=900, y=280)
    
    def take_image(self):
        """Capture image from webcam and register student"""
        enroll = self.entry_enrollment.get().strip()
        name = self.entry_name.get().strip()
        
        if not enroll or not name:
            messagebox.showerror("Error", "Please fill all the fields")
            return
        
        # Check if student already exists
        existing_student = DatabaseHelper.get_student_by_roll_no(enroll)
        if existing_student:
            messagebox.showerror("Error", f"Student with enrollment ID {enroll} already exists!")
            return
        
        try:
            # Capture image from webcam
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                messagebox.showerror("Error", "Could not open webcam")
                return
            
            start_time = time.time()
            image = None
            
            messagebox.showinfo("Info", f"Camera will capture in {Config.CAPTURE_DELAY} seconds. Please look at the camera!")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                cv2.imshow('Registration - Press Q to cancel', frame)
                
                if time.time() - start_time >= Config.CAPTURE_DELAY:
                    image = frame
                    break
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            
            if image is None:
                messagebox.showwarning("Cancelled", "Image capture cancelled")
                return
            
            # Save image
            image_filename = f"{enroll}.png"
            image_path = os.path.join(Config.IMAGES_DIR, image_filename)
            cv2.imwrite(image_path, image)
            
            # Convert image to binary for database
            retval, buffer = cv2.imencode('.png', image)
            binary_data = buffer.tobytes()
            
            # Insert into database
            if DatabaseHelper.insert_student(enroll, name, binary_data):
                messagebox.showinfo('Success', f"Student {name} registered successfully!")
                self.entry_enrollment.delete(0, END)
                self.entry_name.delete(0, END)
            else:
                messagebox.showerror('Error', "Failed to register student in database")
        
        except Exception as e:
            messagebox.showerror('Error', f"An error occurred: {str(e)}")
    
    def open_online_attendance(self):
        """Open online attendance window"""
        import subprocess
        subprocess.Popen(['python', os.path.join('src', 'online_attendance.py')])
    
    def open_manual_attendance(self):
        """Open manual attendance window"""
        import subprocess
        subprocess.Popen(['python', os.path.join('src', 'manual_attendance.py')])
    
    def open_login(self):
        """Open login window"""
        import subprocess
        subprocess.Popen(['python', os.path.join('src', 'login.py')])

def main():
    root = Tk()
    app = MainInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
