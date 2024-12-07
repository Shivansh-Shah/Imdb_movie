import customtkinter as ctk
from tkinter import messagebox
import time
import mysql.connector

# Function to connect to MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",  # your MySQL server host
        user="root",       # your MySQL username
        password="shivansh6165",  # your MySQL password
        database="cinephile_app"  # your MySQL database name
    )

# Function for login button
def login():
    user_id = user_id_entry.get()
    password = password_entry.get()

    # Show "Loading..." and add a time delay
    loading_label.grid(row=3, column=0, columnspan=2, pady=20)
    app.update()  # Update the GUI to display the loading message immediately
    time.sleep(3)  # Add a 3-second delay
    loading_label.grid_forget()  # Hide the loading label after the delay

    # Verify user credentials after the delay
    verify_credentials(user_id, password)

# Verify user credentials
def verify_credentials(user_id, password):
    # Connect to DB and verify user credentials
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user_id, password))
    user = cursor.fetchone()
    db.close()

    if user:
        messagebox.showinfo("Login", "Login Successful")
    else:
        messagebox.showerror("Login", "Invalid User ID or Password")

# Function for sign-up button
def sign_up():
    login_frame.grid_forget()
    sign_up_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    sign_up_button.grid_forget()

# Function for submitting the sign-up form
def submit_sign_up():
    username = sign_up_username_entry.get()
    password = sign_up_password_entry.get()
    confirm_password = sign_up_confirm_password_entry.get()

    if password != confirm_password:
        messagebox.showerror("Sign Up", "Passwords do not match!")
    else:
        # Save data to MySQL database
        db = connect_db()
        cursor = db.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            messagebox.showinfo("Sign Up", "Sign-Up Successful!")
        except mysql.connector.IntegrityError:
            messagebox.showerror("Sign Up", "Username already exists!")

        db.close()
        sign_up_frame.grid_forget()
        login_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        sign_up_button.grid(row=3, column=1, pady=(10, 5), sticky="w")

# Function for forget password
def forget_password():
    login_frame.grid_forget()
    forget_password_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# Function for resetting the password
def reset_password():
    username = forget_username_entry.get()

    # Generate a new random password
    new_password = ''.join(choice(string.ascii_letters + string.digits) for i in range(8))

    # Update password in MySQL database
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
    db.commit()
    db.close()

    messagebox.showinfo("Password Reset", f"Your new password is: {new_password}")
    forget_password_frame.grid_forget()
    login_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# Function to toggle light/dark mode
def toggle_mode():
    current_mode = ctk.get_appearance_mode()
    new_mode = "light" if current_mode == "dark" else "dark"
    ctk.set_appearance_mode(new_mode)

# Initialize customtkinter and set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Create the main application window
app = ctk.CTk()
app.title("Cinephile App Login")
app.geometry("400x400")

# Logo and Title
title_label = ctk.CTkLabel(
    app,
    text="🎥 Cinephile App 🎥",
    font=ctk.CTkFont(size=20, weight="bold")
)
title_label.grid(row=0, column=0, padx=20, pady=30, sticky="nsew")

# Loading indicator (initially hidden)
loading_label = ctk.CTkLabel(app, text="Loading...", font=ctk.CTkFont(size=14))
loading_label.grid_forget()

# Login Frame
login_frame = ctk.CTkFrame(app)
login_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

# User ID Field
user_id_label = ctk.CTkLabel(login_frame, text="USER ID", font=ctk.CTkFont(size=14))
user_id_label.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")
user_id_entry = ctk.CTkEntry(login_frame, placeholder_text="Enter your User ID")
user_id_entry.grid(row=0, column=1, padx=10, pady=(20, 10))

# Password Field
password_label = ctk.CTkLabel(login_frame, text="PASSWORD", font=ctk.CTkFont(size=14))
password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
password_entry = ctk.CTkEntry(login_frame, placeholder_text="Enter your Password", show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Buttons
login_button = ctk.CTkButton(login_frame, text="LOGIN", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=20)

sign_up_label = ctk.CTkLabel(login_frame, text="New User?")
sign_up_label.grid(row=3, column=0, pady=(10, 5), sticky="e")
sign_up_button = ctk.CTkButton(login_frame, text="SIGN UP", command=sign_up, width=100)
sign_up_button.grid(row=3, column=1, pady=(10, 5), sticky="w")

# Forget Password Button
forget_password_button = ctk.CTkButton(login_frame, text="Forgot Password?", command=forget_password)
forget_password_button.grid(row=4, column=0, columnspan=2, pady=10)

# Light/Dark mode toggle button
mode_button = ctk.CTkButton(app, text="Toggle Light/Dark Mode", command=toggle_mode)
mode_button.grid(row=2, column=0, pady=10, sticky="nsew")

# Create the Sign-Up Frame
sign_up_frame = ctk.CTkFrame(app)

# Sign-Up Fields
sign_up_username_label = ctk.CTkLabel(sign_up_frame, text="Username", font=ctk.CTkFont(size=14))
sign_up_username_label.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")
sign_up_username_entry = ctk.CTkEntry(sign_up_frame, placeholder_text="Choose a Username")
sign_up_username_entry.grid(row=0, column=1, padx=10, pady=(20, 10))

sign_up_password_label = ctk.CTkLabel(sign_up_frame, text="Password", font=ctk.CTkFont(size=14))
sign_up_password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
sign_up_password_entry = ctk.CTkEntry(sign_up_frame, placeholder_text="Choose a Password", show="*")
sign_up_password_entry.grid(row=1, column=1, padx=10, pady=10)

sign_up_confirm_password_label = ctk.CTkLabel(sign_up_frame, text="Confirm Password", font=ctk.CTkFont(size=14))
sign_up_confirm_password_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
sign_up_confirm_password_entry = ctk.CTkEntry(sign_up_frame, placeholder_text="Confirm Password", show="*")
sign_up_confirm_password_entry.grid(row=2, column=1, padx=10, pady=10)

# Sign-Up Submit Button
sign_up_submit_button = ctk.CTkButton(sign_up_frame, text="SUBMIT", command=submit_sign_up)
sign_up_submit_button.grid(row=3, column=0, columnspan=2, pady=(10, 20))

# Forget Password Frame
forget_password_frame = ctk.CTkFrame(app)

# Forget Password Fields
forget_username_label = ctk.CTkLabel(forget_password_frame, text="Username", font=ctk.CTkFont(size=14))
forget_username_label.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")
forget_username_entry = ctk.CTkEntry(forget_password_frame, placeholder_text="Enter your Username")
forget_username_entry.grid(row=0, column=1, padx=10, pady=(20, 10))

# Reset Password Button
reset_password_button = ctk.CTkButton(forget_password_frame, text="RESET PASSWORD", command=reset_password)
reset_password_button.grid(row=1, column=0, columnspan=2, pady=(10, 20))

# Run the application
app.mainloop()


