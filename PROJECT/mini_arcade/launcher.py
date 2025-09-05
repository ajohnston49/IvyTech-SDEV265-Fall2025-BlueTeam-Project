import tkinter as tk
import subprocess
import os

# Base paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "gui_assets")

# Prevent garbage collection
images = []

# Launch function
def launch_game(path):
    abs_path = os.path.abspath(path)
    print(f"Launching: {abs_path}")
    if os.path.exists(abs_path):
        subprocess.Popen(["python", abs_path])
    else:
        print(f"Game not found: {abs_path}")

# GUI setup
root = tk.Tk()
root.title("BitBox Arcade")
root.geometry("1000x700")
root.configure(bg="#1e1e1e")

tk.Label(root, text="BitBox Arcade", font=("Arial", 32, "bold"), fg="white", bg="#1e1e1e").pack(pady=20)
grid = tk.Frame(root, bg="#1e1e1e")
grid.pack()

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
craig_img = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "placeholder.png"))
images.append(craig_img)
craig_frame = tk.Frame(grid, bg="#1e1e1e")
craig_frame.grid(row=1, column=0, padx=40, pady=20)
tk.Button(craig_frame, image=craig_img, width=150, height=200,
          command=lambda: launch_game(os.path.join(BASE_DIR, "Craig", "pixel_racer", "main.py")),
          borderwidth=0, bg="#1e1e1e").pack()
tk.Label(craig_frame, text="Craig's Game", font=("Arial", 14), fg="white", bg="#1e1e1e").pack(pady=10)

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
