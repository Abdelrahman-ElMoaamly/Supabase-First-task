import os
import tkinter as tk
from dotenv import load_dotenv
from tkinter import filedialog, messagebox
from supabase import create_client, Client
import global_vars

load_dotenv()
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)

def open_profile():
    profile = tk.Toplevel()
    profile.title("Profile Page")
    profile.geometry("360x640")
    session = global_vars.session
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n response:", session)
    user = global_vars.data
    profile_data = supabase.table("profiles").select("*").eq("user_id", global_vars.data.user.id).eq("role", "admin").execute()
    def fetch_profile_data(entry_username):
        try:
            if user:
                entry_username.insert(0, profile_data.data[0]["username"])
                entry_phone.insert(0, profile_data.data[0]["phone"])
            else:
                messagebox.showerror("Error", "User is not authenticated.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_profile():
        username = entry_username.get()
        new_phone = entry_phone.get()
        try:
            print(user, global_vars.data.user.id)
            if user:  # Check if user is authenticated
                response = (supabase.table("profiles").update({"username": username, "phone": new_phone})
                            .eq("user_id", global_vars.data.user.id).execute())
                if response:
                    print(f"Updated username: {username}, Updated Phone: {new_phone}")
                else:
                    print("Update failed")
            else:
                messagebox.showerror("Error", "User is not authenticated.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def upload_image():
        file_path = filedialog.askopenfilename()
        if file_path:
            print(f"Selected file: {file_path}")
            try:
                if user:  # Check if user is authenticated
                    with open(file_path, 'rb') as f:
                        supabase.storage.from_("avatars").upload(file=f,path="a/avatar.jpg", file_options={"content-type": "image/*"})
                else:
                    messagebox.showerror("Error", "User is not authenticated.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    label_image = tk.Label(profile, text="Profile Image")
    label_image.pack(pady=10)

    button_upload_image = tk.Button(profile, text="Upload Image", command=upload_image)
    button_upload_image.pack(pady=10)

    label_email = tk.Label(profile, text="Name")
    label_email.pack(pady=10)

    entry_username = tk.Entry(profile)
    entry_username.pack(pady=10)

    label_phone = tk.Label(profile, text="Phone")
    label_phone.pack(pady=10)

    entry_phone = tk.Entry(profile)
    entry_phone.pack(pady=10)

    fetch_profile_data(entry_username)

    button_update = tk.Button(profile, text="Update", command=update_profile)
    button_update.pack(pady=20)