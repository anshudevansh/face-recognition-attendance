from tkinter import *
from tkinter import messagebox
import bcrypt
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from src.db_helper import DatabaseHelper

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """Setup window"""
        self.root.title("Check Attendance - Login")
        self.root.geometry("500x400")
        self.root.maxsize(500, 400)
        self.root.minsize(500, 400)
        self.root["bg"] = Config.BG_COLOR
    
    def create_widgets(self):
        """Create widgets"""
        # Title
        lbl_title = Label(
            self.root, 
            text="Check Attendance", 
            font="arial 24 bold",
            bg=Config.BG_COLOR
        )
        lbl_title.pack(pady=20)
        
        # Enrollment ID
        lbl_id = Label(
            self.root, 
            text="Enrollment ID:", 
            font="arial 14",
            bg=Config.BG_COLOR
        )
        lbl_id.place(x=50, y=100)
        
        self.entry_id = Entry(self.root, font="arial 14", width=25)
        self.entry_id.place(x=200, y=100)
        
        # Password
        lbl_pass = Label(
            self.root, 
            text="Password:", 
            font="arial 14",
            bg=Config.BG_COLOR
        )
        lbl_pass.place(x=50, y=160)
        
        self.entry_pass = Entry(self.root, font="arial 14", width=25, show="*")
        self.entry_pass.place(x=200, y=160)
        
        # Login button
        btn_login = Button(
            self.root, 
            text="Login", 
            font="arial 14 bold", 
            bd=8,
            padx=20,
            pady=5,
            bg='#4CAF50',
            fg='white',
            command=self.login
        )
        btn_login.place(x=120, y=240)
        
        # OR label
        lbl_or = Label(
            self.root, 
            text="OR", 
            font="arial 14 bold",
            bg=Config.BG_COLOR
        )
        lbl_or.place(x=230, y=245)
        
        # Signup button
        btn_signup = Button(
            self.root, 
            text="Signup", 
            font="arial 14 bold", 
            bd=8,
            padx=20,
            pady=5,
            bg='#2196F3',
            fg='white',
            command=self.open_signup
        )
        btn_signup.place(x=280, y=240)
    
    def login(self):
        """Handle login"""
        enrollment = self.entry_id.get().strip()
        password = self.entry_pass.get()
        
        if not enrollment or not password:
            messagebox.showwarning("Warning", "Please fill all fields")
            return
        
        # Hash password to compare with database
        # Note: In production, password should be hashed
        # For now, we'll try direct comparison first for backward compatibility
        user = DatabaseHelper.verify_user(enrollment, password)
        
        if user:
            messagebox.showinfo('Success', f"Login successful!\nWelcome {user[1]}")
            self.entry_id.delete(0, END)
            self.entry_pass.delete(0, END)
            
            # Open attendance viewer (to be implemented)
            messagebox.showinfo(
                "Attendance Records",
                "Attendance viewing feature will be implemented here.\n"
                "You can view your attendance history, statistics, etc."
            )
        else:
            messagebox.showerror("Error", "Invalid enrollment ID or password")
    
    def open_signup(self):
        """Open signup window"""
        import subprocess
        subprocess.Popen(['python', 'signup.py'])

def main():
    root = Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
