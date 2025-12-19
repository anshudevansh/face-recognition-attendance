from tkinter import *
from tkinter import ttk, messagebox
import os
import sys
from datetime import date

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from src.db_helper import DatabaseHelper

class ManualAttendance:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """Setup window"""
        self.root.title("Manual Attendance")
        self.root.geometry("800x600")
        self.root.maxsize(800, 600)
        self.root.minsize(800, 600)
        self.root["bg"] = Config.BG_COLOR
    
    def create_widgets(self):
        """Create widgets"""
        # Title
        lbl_title = Label(
            self.root, 
            text="Manual Attendance", 
            font="arial 30 bold",
            bg=Config.BG_COLOR
        )
        lbl_title.pack(pady=10)
        
        # Enrollment ID
        lbl_enroll = Label(
            self.root, 
            text="Enrollment ID:", 
            font="arial 18",
            bg=Config.BG_COLOR
        )
        lbl_enroll.place(x=100, y=100)
        
        self.entry_enroll = Entry(self.root, font="arial 18", width=30)
        self.entry_enroll.place(x=320, y=100)
        
        # Name
        lbl_name = Label(
            self.root, 
            text="Name:", 
            font="arial 18",
            bg=Config.BG_COLOR
        )
        lbl_name.place(x=100, y=170)
        
        self.entry_name = Entry(self.root, font="arial 18", width=30)
        self.entry_name.place(x=320, y=170)
        
        # Auto-fill button
        btn_autofill = Button(
            self.root,
            text="Auto-fill",
            font="arial 12",
            bd=5,
            bg='#2196F3',
            fg='white',
            command=self.autofill_student
        )
        btn_autofill.place(x=680, y=100)
        
        # Subject Name
        lbl_subject = Label(
            self.root, 
            text="Subject:", 
            font="arial 18",
            bg=Config.BG_COLOR
        )
        lbl_subject.place(x=100, y=240)
        
        # Get subjects from database
        subjects = DatabaseHelper.get_all_subjects()
        self.subject_dict = {f"{sub[2]}": sub[0] for sub in subjects} if subjects else {}
        
        self.subject_var = StringVar()
        self.subject_combo = ttk.Combobox(
            self.root,
            textvariable=self.subject_var,
            values=list(self.subject_dict.keys()),
            font="arial 16",
            state="readonly",
            width=28
        )
        self.subject_combo.place(x=320, y=240)
        if self.subject_dict:
            self.subject_combo.current(0)
        
        # Status
        lbl_status = Label(
            self.root, 
            text="Status:", 
            font="arial 18",
            bg=Config.BG_COLOR
        )
        lbl_status.place(x=100, y=310)
        
        self.status_var = StringVar()
        status_combo = ttk.Combobox(
            self.root,
            textvariable=self.status_var,
            values=["Present", "Absent"],
            font="arial 16",
            state="readonly",
            width=28
        )
        status_combo.place(x=320, y=310)
        status_combo.current(0)
        
        # Date display
        lbl_date = Label(
            self.root,
            text=f"Date: {date.today().strftime('%Y-%m-%d')}",
            font="arial 14",
            bg=Config.BG_COLOR,
            fg='#555'
        )
        lbl_date.place(x=100, y=380)
        
        # Submit button
        btn_submit = Button(
            self.root, 
            text="Submit Attendance", 
            font="arial 16 bold", 
            bd=8,
            padx=20,
            pady=10,
            bg='#4CAF50',
            fg='white',
            command=self.submit_attendance
        )
        btn_submit.place(x=280, y=450)
    
    def autofill_student(self):
        """Auto-fill student name from enrollment ID"""
        enroll_id = self.entry_enroll.get().strip()
        if not enroll_id:
            messagebox.showwarning("Warning", "Please enter enrollment ID first")
            return
        
        student = DatabaseHelper.get_student_by_roll_no(enroll_id)
        if student:
            self.entry_name.delete(0, END)
            self.entry_name.insert(0, student[2])  # student[2] is name
        else:
            messagebox.showwarning("Not Found", f"No student found with enrollment ID: {enroll_id}")
            self.entry_name.delete(0, END)
    
    def submit_attendance(self):
        """Submit manual attendance"""
        enroll_id = self.entry_enroll.get().strip()
        name = self.entry_name.get().strip()
        subject_name = self.subject_var.get()
        status = self.status_var.get().lower()
        
        if not enroll_id or not name:
            messagebox.showerror("Error", "Please fill enrollment ID and name")
            return
        
        if not subject_name:
            messagebox.showerror("Error", "Please select a subject")
            return
        
        # Get or create student
        student = DatabaseHelper.get_student_by_roll_no(enroll_id)
        if not student:
            # Create new student
            if DatabaseHelper.insert_student(enroll_id, name):
                student = DatabaseHelper.get_student_by_roll_no(enroll_id)
            else:
                messagebox.showerror("Error", "Failed to create student record")
                return
        
        student_id = student[0]
        subject_id = self.subject_dict[subject_name]
        
        # Mark attendance
        if DatabaseHelper.mark_attendance(student_id, subject_id, status, 'manual'):
            messagebox.showinfo(
                "Success", 
                f"Attendance marked for {name}\n"
                f"Subject: {subject_name}\n"
                f"Status: {status.capitalize()}\n"
                f"Date: {date.today().strftime('%Y-%m-%d')}"
            )
            
            # Clear fields
            self.entry_enroll.delete(0, END)
            self.entry_name.delete(0, END)
            self.status_var.set("Present")
        else:
            messagebox.showerror("Error", "Failed to mark attendance")

def main():
    root = Tk()
    app = ManualAttendance(root)
    root.mainloop()

if __name__ == "__main__":
    main()
