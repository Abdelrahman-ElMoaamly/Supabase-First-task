import os
import re
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
from supabase import create_client, Client
from ProfilePage import open_profile
load_dotenv()
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)

def open_signup(root):  # Accept root as a parameter
    signup_Email = tk.Toplevel()
    signup_Email.title("Sign Up With Email")
    signup_Email.geometry("360x640")

    label_signup_username = tk.Label(signup_Email, text="Email")
    label_signup_username.pack(pady=10)
    entry_signup_username = tk.Entry(signup_Email)
    entry_signup_username.pack(pady=10)

    label_signup_password = tk.Label(signup_Email, text="Password")
    label_signup_password.pack(pady=10)
    entry_signup_password = tk.Entry(signup_Email, show="*")
    entry_signup_password.pack(pady=10)



    def is_email_valid(email):
        email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        return email_regex.match(email)

    def is_password_valid(password):
        password_regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
        return password_regex.match(password)
    
    def sign_up_With_Email():
        email = entry_signup_username.get()
        password = entry_signup_password.get()

        if not is_email_valid(email):
            messagebox.showerror("Invalid email", "Invalid email address")
            return
        if not is_password_valid(password):
            messagebox.showerror("Invalid password", "Password must be at least 8 characters long and contain an uppercase letter, a lowercase letter, a number, and a special character")
            return
        try:
            response = supabase.auth.sign_up({"email": email, "password": password})
            if response.user:
                supabase.table("profiles").insert({"user_id": response.user.id, "username": " "}).execute()
                messagebox.showinfo("Signup", "Signup successful")
            else:
                messagebox.showerror("Signup", "Signup failed")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    button_signup = tk.Button(signup_Email, text="Sign Up", command=sign_up_With_Email)
    button_signup.pack(pady=10)

    def return_to_login():
        root.deiconify()  # Show the login window again
        signup_Email.destroy()  # Close the sign-up window

    button_return_to_login = tk.Button(signup_Email, text="Return to Login", command=return_to_login)
    button_return_to_login.pack(pady=10)
