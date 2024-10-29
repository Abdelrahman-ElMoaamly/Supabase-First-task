import os
import tkinter as tk
from dotenv import load_dotenv
from tkinter import messagebox
from supabase import create_client, Client
from SignUpWithEmail import open_signup  # Import your function
from ProfilePage import open_profile  # Import your profile function
import webbrowser
import global_vars

global user

load_dotenv()
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)

def login():
    email = entry_email.get()
    password = entry_password.get()
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response:
            print("User Logged In")
            global_vars.data = supabase.auth.get_user()  # Get user session
            global_vars.session = supabase.auth.get_session()
            print (global_vars.session)
            root.withdraw()  # Hide the login window
            open_profile()  # Open the profile page
        else:
            print("Log In failed")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def sign_up_With_GitHub():
    webbrowser.open("https://dlngxmthtfeuzecgurqf.supabase.co/auth/v1/authorize?code_challenge=TpDAFShpmyomIasm7h9OyFg7UNd_824dAQ1x5Ef4zX4&code_challenge_method=s256&provider=github")

def open_signup_with_hide():
    root.withdraw()  # Hide the login window
    open_signup(root)  # Pass root to the function

def get_user():
    user = supabase.auth.get_user()
    return user

root = tk.Tk()
root.title("Log In")
root.geometry("360x640")

label_username = tk.Label(root, text="Email")
label_username.pack(pady=10)
entry_email = tk.Entry(root)
entry_email.pack(pady=10)

label_password = tk.Label(root, text="Password")
label_password.pack(pady=10)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=10)

button_login = tk.Button(root, text="Log In", command=login)
button_login.pack(pady=20)

button_signup_page = tk.Button(root, text="Sign Up With Email", command=open_signup_with_hide)
button_signup_page.pack(pady=20)

button_signup_page = tk.Button(root, text="Sign Up With GitHub", command=sign_up_With_GitHub)
button_signup_page.pack(pady=20)

root.mainloop()