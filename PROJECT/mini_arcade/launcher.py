import tkinter as tk           # GUI library for building the interface
import subprocess              # Used to launch external Python scripts (games)
import threading               # Allows games to run in background threads
import os                      # For working with file paths
import sys                     # Gives access to the current Python interpreter

# Set base directory paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Root folder of the project
ASSETS_DIR = os.path.join(BASE_DIR, "gui_assets")                          # Folder for button images

# Prevent images from being garbage collected (keeps them in memory)
images = []

# Create main window
root = tk.Tk()
root.title("BitBox Arcade")               # Window title
root.geometry("800x750")                 # Window size
root.configure(bg="#1e1e1e")              # Background color (dark theme)

# Function to launch a game script
def launch_game(path):
    abs_path = os.path.abspath(path)      # Get absolute path to the game file
    print(f"Launching: {abs_path}")       # Print path for debugging
    if not os.path.exists(abs_path):      # Check if the file exists
        print(f"Game not found: {abs_path}")
        return

    # Run the game in a separate thread so GUI doesn't freeze
    def run_game():
        try:
            root.iconify()                # Minimize the launcher window
            proc = subprocess.Popen([sys.executable, abs_path])  # Launch game using Python
            proc.wait()                   # Wait for game to finish
        except Exception as e:
            print(f"Error launching game: {e}")  # Print any errors
        finally:
            root.deiconify()              # Restore the launcher window
            root.geometry("1000x700")     # Reset window size
            root.lift()                   # Bring window to front
            root.focus_force()            # Force focus
            root.attributes("-topmost", True)    # Temporarily keep window on top
            root.after(500, lambda: root.attributes("-topmost", False))  # Remove topmost after delay

    threading.Thread(target=run_game, daemon=True).start()  # Start game thread

# Function to open the About window
def open_about_window():
    about = tk.Toplevel(root)            # Create a new popup window
    about.title("About BitBox Arcade")
    about.geometry("500x400")            # Size of the About window
    about.configure(bg="#2e2e2e")        # Background color

    # Message with team info
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

    # Display message
    tk.Label(about, text=message, font=("Arial", 12), fg="white", bg="#2e2e2e", justify="center").pack(pady=40)

    # Close button
    tk.Button(about, text="Close", command=about.destroy, font=("Arial", 12),
              bg="#444", fg="white", activebackground="#666", activeforeground="white").pack(pady=20)

# Create side panel for About button
side_panel = tk.Frame(root, bg="#1e1e1e")
side_panel.pack(side="left", fill="y", padx=(20, 0), pady=20)

# Add About button to side panel
tk.Button(side_panel, text="About App", command=open_about_window,
          font=("Arial", 12), width=12, height=2,
          bg="#444", fg="white", activebackground="#666", activeforeground="white").pack(pady=10)

# Create main grid area for game buttons
grid = tk.Frame(root, bg="#1e1e1e")
grid.pack()

# Title label at the top
tk.Label(root, text="BlueTeam Arcade", font=("Arial", 32, "bold"), fg="white", bg="#1e1e1e").pack(pady=20)

# Instruction label
tk.Label(root, text="Click any image to launch its game.", font=("Arial", 14), fg="#cccccc", bg="#1e1e1e").pack(pady=(0, 20))

# === Game Buttons ===

# Froggy Jump (Alex's game)
frog_img = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "frog_button.png"))
images.append(frog_img)
frog_frame = tk.Frame(grid, bg="#1e1e1e")
frog_frame.grid(row=0, column=0, padx=40, pady=20)
tk.Button(frog_frame, image=frog_img, width=150, height=200,
          command=lambda: launch_game(os.path.join(BASE_DIR, "Alex", "froggy_jump", "main.py")),
          borderwidth=2, relief="raised", highlightthickness=2,
          bg="#1e1e1e", activebackground="#333333").pack()
tk.Label(frog_frame, text="Froggy Jump", font=("Arial", 14), fg="white", bg="#1e1e1e").pack(pady=10)

# Makayla's Game
mak_img = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "david_button.png"))
images.append(mak_img)
mak_frame = tk.Frame(grid, bg="#1e1e1e")
mak_frame.grid(row=0, column=1, padx=40, pady=20)
tk.Button(mak_frame, image=mak_img, width=150, height=200,
          command=lambda: launch_game(os.path.join(BASE_DIR, "Makayla", "David_&_Goliath", "main.py")),
          borderwidth=2, relief="raised", highlightthickness=2,
          bg="#1e1e1e", activebackground="#333333").pack()
tk.Label(mak_frame, text="David And Goliath", font=("Arial", 14), fg="white", bg="#1e1e1e").pack(pady=10)

# Craig's Game
craig_img = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "duck_button.png"))
images.append(craig_img)
craig_frame = tk.Frame(grid, bg="#1e1e1e")
craig_frame.grid(row=1, column=0, padx=40, pady=20)
tk.Button(craig_frame, image=craig_img, width=150, height=200,
          command=lambda: launch_game(os.path.join(BASE_DIR, "Craig", "duckhunt", "shoot.py")),
          borderwidth=2, relief="raised", highlightthickness=2,
          bg="#1e1e1e", activebackground="#333333").pack()
tk.Label(craig_frame, text="Duck Hunt", font=("Arial", 14), fg="white", bg="#1e1e1e").pack(pady=10)

# Brandon's Game
brandon_img = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "placeholder.png"))
images.append(brandon_img)
brandon_frame = tk.Frame(grid, bg="#1e1e1e")
brandon_frame.grid(row=1, column=1, padx=40, pady=20)
tk.Button(brandon_frame, image=brandon_img, width=150, height=200,
          command=lambda: launch_game(os.path.join(BASE_DIR, "Brandon", "tower_tactics", "main.py")),
          borderwidth=2, relief="raised", highlightthickness=2,
          bg="#1e1e1e", activebackground="#333333").pack()
tk.Label(brandon_frame, text="Brandon's Game", font=("Arial", 14), fg="white", bg="#1e1e1e").pack(pady=10)

# Start the GUI event loop
root.mainloop()
