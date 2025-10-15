import tkinter as tk
import subprocess
import threading
import os
import sys

# Base paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "gui_assets")

# Prevent garbage collection
images = []

# GUI setup
root = tk.Tk()
root.title("BitBox Arcade")
root.geometry("1000x700")
root.configure(bg="#1e1e1e")

# Launch function
def launch_game(path):
    abs_path = os.path.abspath(path)
    print(f"Launching: {abs_path}")
    if not os.path.exists(abs_path):
        print(f"Game not found: {abs_path}")
        return

    def run_game():
        try:
            root.iconify()
            proc = subprocess.Popen([sys.executable, abs_path])
            proc.wait()
        except Exception as e:
            print(f"Error launching game: {e}")
        finally:
            root.deiconify()
            root.geometry("1000x700")
            root.lift()
            root.focus_force()
            root.attributes("-topmost", True)
            root.after(500, lambda: root.attributes("-topmost", False))

    threading.Thread(target=run_game, daemon=True).start()

# About window
def open_about_window():
    about = tk.Toplevel(root)
    about.title("About BitBox Arcade")
    about.geometry("500x400")
    about.configure(bg="#2e2e2e")

    message = (
        "This application was developed by the Blue Team\n"
        "Ivy Tech Community College – Fall 2025\n"
        "Course: SDEV 265\n\n"
        "Developers:\n"
        "• Makayla Harrison\n"
        "• Craig Andrew Hutson\n"
        "• Alex Michael Johnston\n"
        "• Brandon Kesner"
    )

    tk.Label(about, text=message, font=("Arial", 12), fg="white", bg="#2e2e2e", justify="center").pack(pady=40)
    tk.Button(about, text="Close", command=about.destroy, font=("Arial", 12),
              bg="#444", fg="white", activebackground="#666", activeforeground="white").pack(pady=20)

# Side panel for About button
side_panel = tk.Frame(root, bg="#1e1e1e")
side_panel.pack(side="left", fill="y", padx=(20, 0), pady=20)

tk.Button(side_panel, text="About Game", command=open_about_window,
          font=("Arial", 12), width=12, height=2,
          bg="#444", fg="white", activebackground="#666", activeforeground="white").pack(pady=10)

# Main grid for game buttons
grid = tk.Frame(root, bg="#1e1e1e")
grid.pack()

# Arcade title
tk.Label(root, text="BitBox Arcade", font=("Arial", 32, "bold"), fg="white", bg="#1e1e1e").pack(pady=20)

# Froggy Jump
frog_img = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "frog_button.png"))
images.append(frog_img)
frog_frame = tk.Frame(grid, bg="#1e1e1e")
frog_frame.grid(row=0, column=0, padx=40, pady=20)
tk.Button(frog_frame, image=frog_img, width=150, height=200,
          command=lambda: launch_game(os.path.join(BASE_DIR, "Alex", "froggy_jump", "main.py")),
          borderwidth=0, bg="#1e1e1e").pack()
tk.Label(frog_frame, text="Froggy Jump", font=("Arial", 14), fg="white", bg="#1e1e1e").pack(pady=10)

# Makayla's Game
mak_img = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "placeholder.png"))
images.append(mak_img)
mak_frame = tk.Frame(grid, bg="#1e1e1e")
mak_frame.grid(row=0, column=1, padx=40, pady=20)
tk.Button(mak_frame, image=mak_img, width=150, height=200,
          command=lambda: launch_game(os.path.join(BASE_DIR, "Makayla", "space_blaster", "main.py")),
          borderwidth=0, bg="#1e1e1e").pack()
tk.Label(mak_frame, text="Makayla's Game", font=("Arial", 14), fg="white", bg="#1e1e1e").pack(pady=10)

# Craig's Game
craig_img = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "duck_button.png"))
images.append(craig_img)
craig_frame = tk.Frame(grid, bg="#1e1e1e")
craig_frame.grid(row=1, column=0, padx=40, pady=20)
tk.Button(craig_frame, image=craig_img, width=150, height=200,
          command=lambda: launch_game(os.path.join(BASE_DIR, "Craig", "duckhunt", "shoot.py")),
          borderwidth=0, bg="#1e1e1e").pack()
tk.Label(craig_frame, text="Duck Hunt", font=("Arial", 14), fg="white", bg="#1e1e1e").pack(pady=10)

# Brandon's Game
brandon_img = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "placeholder.png"))
images.append(brandon_img)
brandon_frame = tk.Frame(grid, bg="#1e1e1e")
brandon_frame.grid(row=1, column=1, padx=40, pady=20)
tk.Button(brandon_frame, image=brandon_img, width=150, height=200,
          command=lambda: launch_game(os.path.join(BASE_DIR, "Brandon", "tower_tactics", "main.py")),
          borderwidth=0, bg="#1e1e1e").pack()
tk.Label(brandon_frame, text="Brandon's Game", font=("Arial", 14), fg="white", bg="#1e1e1e").pack(pady=10)

root.mainloop()
