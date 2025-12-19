from tkinter import *
from tkinter import messagebox
import bcrypt
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from src.db_helper import DatabaseHelper

class SignupWindow:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """Setup window"""
        self.root.title("Signup - Create Account")
        self.root.geometry("600x500")
        self.root.maxsize(600, 500)
        self.root.minsize(600, 500)
        self.root["bg"] = Config.BG_COLOR
    
    def create_widgets(self):
        """Create widgets"""
        # Title
        lbl_title = Label(
            self.root, 
            text="Create Account", 
            font="arial 24 bold",
            bg=Config.BG_COLOR
        )
        lbl_title.pack(pady=20)
        
        # Username
        lbl_user = Label(
            self.root, 
            text="Username:", 
            font="arial 14",
            bg=Config.BG_COLOR
        )
        lbl_user.place(x=80, y=100)
        
        self.entry_user = Entry(self.root, font="arial 14", width=30)
        self.entry_user.place(x=250, y=100)
        
        # Enrollment ID
        lbl_id = Label(
            self.root, 
            text="Enrollment ID:", 
            font="arial 14",
            bg=Config.BG_COLOR
        )
        lbl_id.place(x=80, y=160)
        
        self.entry_id = Entry(self.root, font="arial 14", width=30)
        self.entry_id.place(x=250, y=160)
        
        # Password
        lbl_pass = Label(
            self.root, 
            text="Password:", 
            font="arial 14",
            bg=Config.BG_COLOR
        )
        lbl_pass.place(x=80, y=220)
        
        self.entry_pass = Entry(self.root, font="arial 14", width=30, show="*")
        self.entry_pass.place(x=250, y=220)
        
        # Confirm Password
        lbl_cpass = Label(
            self.root, 
            text="Confirm Password:", 
            font="arial 14",
            bg=Config.BG_COLOR
        )
        lbl_cpass.place(x=80, y=280)
        
        self.entry_cpass = Entry(self.root, font="arial 14", width=30, show="*")
        self.entry_cpass.place(x=250, y=280)
        
        # Signup button
        btn_signup = Button(
            self.root, 
            text="Create Account", 
            font="arial 14 bold", 
            bd=8,
            padx=30,
            pady=10,
            bg='#4CAF50',
            fg='white',
            command=self.signup
        )
        btn_signup.place(x=200, y=360)
    
    def signup(self):
        """Handle signup"""
        username = self.entry_user.get().strip()
        enrollment = self.entry_id.get().strip()
        password = self.entry_pass.get()
        confirm_password = self.entry_cpass.get()
        
        # Validation
        if not username or not enrollment or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        if password != confirm_password:
            messagebox.showwarning("Error", "Passwords don't match")
            return
        
        if len(password) < 6:
            messagebox.showwarning("Error", "Password must be at least 6 characters long")
            return
        
        # Hash password using bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        password_hash_str = password_hash.decode('utf-8')
        
        # Insert user into database
        if DatabaseHelper.insert_user(username, enrollment, password_hash_str):
            messagebox.showinfo(
                'Success', 
                f"Account created successfully!\n\n"
                f"Username: {username}\n"
                f"Enrollment ID: {enrollment}\n\n"
                "You can now login with your credentials."
            )
            
            # Clear fields
            self.entry_user.delete(0, END)
            self.entry_id.delete(0, END)
            self.entry_pass.delete(0, END)
            self.entry_cpass.delete(0, END)
        else:
            messagebox.showerror(
                'Error', 
                "Failed to create account.\n"
                "Username or Enrollment ID may already exist."
            )

def main():
    root = Tk()
    app = SignupWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
