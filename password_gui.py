import tkinter as tk
from tkinter import messagebox, ttk
from zxcvbn import zxcvbn
from itertools import permutations
import re

# --- Leetspeak conversion ---
def leetspeak(word):
    return word.replace('a', '@').replace('e', '3').replace('i', '1').replace('o', '0').replace('s', '$')

# --- Wordlist Generator ---
def generate_wordlist(data):
    words = list(data.values())
    variations = []

    for word in words:
        variations.extend([
            word.lower(), word.upper(), word.capitalize(),
            word + "123", word + "@2024", word[::-1],
            leetspeak(word)
        ])

    for i in range(2, len(words) + 1):
        for combo in permutations(words, i):
            joined = "".join(combo)
            variations.append(joined)
            variations.append(leetspeak(joined))

    years = [str(y) for y in range(2000, 2026)]
    for word in list(variations):
        for year in years:
            variations.append(word + year)

    final_wordlist = list(set(filter(lambda w: re.match(r'^[a-zA-Z0-9@$.]+$', w), variations)))

    with open("enhanced_wordlist.txt", "w") as f:
        for item in final_wordlist:
            f.write(item + "\n")

    return len(final_wordlist)

# --- Password Analysis ---
def analyze_password():
    password = entry_password.get()
    if not password:
        messagebox.showwarning("Input Missing", "Please enter a password.")
        return

    result = zxcvbn(password)
    score = result['score']
    crack_time = result['crack_times_display']['offline_slow_hashing_1e4_per_second']
    strength_text = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"][score]

    result_label.config(text=f"Score: {score}/4 ({strength_text})\nCrack Time: {crack_time}")
    strength_bar['value'] = score

    if score <= 1:
        strength_bar.configure(style="Red.Horizontal.TProgressbar")
    elif score == 2:
        strength_bar.configure(style="Yellow.Horizontal.TProgressbar")
    else:
        strength_bar.configure(style="Green.Horizontal.TProgressbar")

    messagebox.showinfo("Done", f"Password analyzed.\nScore: {score}/4\nStrength: {strength_text}\nCrack Time: {crack_time}")

# --- Wordlist Generation Trigger ---
def generate():
    name = entry_name.get()
    dob = entry_dob.get()
    pet = entry_pet.get()

    if not name or not dob or not pet:
        messagebox.showwarning("Input Missing", "Please fill in all fields.")
        return

    data = {"name": name, "dob": dob, "pet": pet}
    count = generate_wordlist(data)
    messagebox.showinfo("Wordlist Generated", f"{count} entries saved to enhanced_wordlist.txt")

# --- Show/Hide password ---
def toggle_password():
    entry_password.config(show="" if show_var.get() else "*")

# --- Dark Mode ---
def apply_dark_mode():
    root.configure(bg="#2E2E2E")
    for widget in root.winfo_children():
        try:
            widget.configure(bg="#2E2E2E", fg="white", insertbackground="white")
        except:
            pass

def apply_light_mode():
    root.configure(bg="SystemButtonFace")
    for widget in root.winfo_children():
        try:
            widget.configure(bg="SystemButtonFace", fg="black", insertbackground="black")
        except:
            pass

def toggle_theme_popup():
    if dark_mode_var.get():
        apply_dark_mode()
    else:
        apply_light_mode()

# --- Open Settings Popup ---
def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("250x100")

    settings_window.resizable(False, False)
    settings_window.configure(bg="white")

    tk.Checkbutton(settings_window, text="Enable Dark Mode", variable=dark_mode_var,
                   command=toggle_theme_popup).pack(pady=20)

# --- GUI Setup ---
root = tk.Tk()
root.title("🔐 Password Strength & Wordlist Tool")
root.geometry("420x500")

# ⚙ Settings Button at top-left
settings_button = tk.Button(root, text="⚙️", command=open_settings)
settings_button.place(x=5, y=5)

# Password Input
tk.Label(root, text="Enter Password:").pack(pady=(40, 0))
password_var = tk.StringVar()
entry_password = tk.Entry(root, textvariable=password_var, show="*")
entry_password.pack()

show_var = tk.BooleanVar()
tk.Checkbutton(root, text="Show Password", variable=show_var, command=toggle_password).pack()

# Analyze Button
tk.Button(root, text="Analyze Password", command=analyze_password).pack(pady=5)
result_label = tk.Label(root, text="", fg="blue")
result_label.pack()

# Strength Bar
strength_bar = ttk.Progressbar(root, length=300, mode='determinate', maximum=4)
strength_bar.pack(pady=5)

# Inputs for Wordlist
tk.Label(root, text="Name:").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="DOB (YYYY):").pack()
entry_dob = tk.Entry(root)
entry_dob.pack()

tk.Label(root, text="Pet Name:").pack()
entry_pet = tk.Entry(root)
entry_pet.pack()

tk.Button(root, text="Generate Wordlist", command=generate, bg="#4CAF50", fg="white").pack(pady=15)

# Hidden Dark Mode Toggle Variable
dark_mode_var = tk.BooleanVar()

# Progress Bar Style
style = ttk.Style()
style.theme_use('default')
style.configure("Red.Horizontal.TProgressbar", troughcolor='white', background='red')
style.configure("Yellow.Horizontal.TProgressbar", troughcolor='white', background='orange')
style.configure("Green.Horizontal.TProgressbar", troughcolor='white', background='green')

root.mainloop()
