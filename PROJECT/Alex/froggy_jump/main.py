import tkinter as tk
import random
import os
import ctypes
import winsound

# Constants
WIDTH, HEIGHT = 400, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 40
PLATFORM_WIDTH, PLATFORM_HEIGHT = 60, 10
GRAVITY = 0.6
JUMP_VELOCITY = -1009999
MOVE_SPEED = 5
NUM_PLATFORMS = 6

# Asset directory
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")

# Loop background music (Windows only)
background_path = os.path.join(ASSET_DIR, "background.mp3")
ctypes.windll.winmm.mciSendStringW(f'open "{background_path}" type mpegvideo alias bgm', None, 0, None)
ctypes.windll.winmm.mciSendStringW("play bgm repeat", None, 0, None)

# Setup
root = tk.Tk()
root.title("Endless Jumper")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# Load images
background_img = tk.PhotoImage(file=os.path.join(ASSET_DIR, "background.png"))
player_img = tk.PhotoImage(file=os.path.join(ASSET_DIR, "player.png"))
platform_img = tk.PhotoImage(file=os.path.join(ASSET_DIR, "platform.png"))

# Draw background
canvas.create_image(0, 0, anchor="nw", image=background_img)

# Score setup
score = 0
score_text = canvas.create_text(10, 10, anchor="nw", font=("Arial", 16), fill="black", text=f"Score: {score}")

class Platform:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.id = canvas.create_image(x + PLATFORM_WIDTH // 2, y + PLATFORM_HEIGHT // 2,
                                      anchor="center", image=platform_img)

    def coords(self):
        return self.canvas.coords(self.id)

    def move(self, dy):
        self.canvas.move(self.id, 0, dy)

    def recycle_if_needed(self):
        x, y = self.coords()
        if y > HEIGHT:
            new_x = random.randint(0, WIDTH - PLATFORM_WIDTH)
            new_y = random.randint(-50, 0)
            self.canvas.coords(self.id, new_x + PLATFORM_WIDTH // 2, new_y + PLATFORM_HEIGHT // 2)

class Player:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = canvas.create_image(WIDTH // 2, HEIGHT - 80, anchor="center", image=player_img)
        self.vy = 0
        self.vx = 0
        self.on_ground = False

    def move(self):
        global score
        self.vy += GRAVITY
        self.canvas.move(self.id, self.vx, self.vy)
        x, y = self.canvas.coords(self.id)
        x1, y1 = x - PLAYER_WIDTH // 2, y - PLAYER_HEIGHT // 2
        x2, y2 = x + PLAYER_WIDTH // 2, y + PLAYER_HEIGHT // 2

        self.on_ground = False
        for plat in platforms:
            px, py = plat.coords()
            px1 = px - PLATFORM_WIDTH // 2
            px2 = px + PLATFORM_WIDTH // 2
            py1 = py - PLATFORM_HEIGHT // 2
            py2 = py + PLATFORM_HEIGHT // 2
            if x2 > px1 and x1 < px2 and abs(y2 - py1) <= 5 and self.vy >= 0:
                self.canvas.move(self.id, 0, py1 - y2)
                self.vy = 0
                self.on_ground = True

        if y1 < HEIGHT // 3:
            dy = HEIGHT // 3 - y1
            self.canvas.move(self.id, 0, dy)
            for plat in platforms:
                plat.move(dy)
                plat.recycle_if_needed()
            score += int(dy)
            canvas.itemconfig(score_text, text=f"Score: {score}")

        if y2 > HEIGHT:
            self.reset()

    def reset(self):
        global score
        self.canvas.coords(self.id, WIDTH // 2, HEIGHT - 80)
        self.vy = 0
        score = 0
        canvas.itemconfig(score_text, text=f"Score: {score}")
        platforms[0].canvas.coords(platforms[0].id,
                                   WIDTH // 2, HEIGHT - 55)
        for plat in platforms[1:]:
            plat.recycle_if_needed()

    def jump(self):
        if self.on_ground:
            self.vy = JUMP_VELOCITY
            winsound.PlaySound(os.path.join(ASSET_DIR, "jump.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)

    def set_direction(self, direction):
        self.vx = direction * MOVE_SPEED

def update():
    player.move()
    root.after(20, update)

def key_press(event):
    if event.keysym.lower() == 'w':
        player.jump()
    elif event.keysym.lower() == 'a':
        player.set_direction(-1)
    elif event.keysym.lower() == 'd':
        player.set_direction(1)

def key_release(event):
    if event.keysym.lower() in ['a', 'd']:
        player.set_direction(0)

def generate_platforms(canvas, count):
    platforms = []
    platforms.append(Platform(canvas, WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - 60))
    for _ in range(count - 1):
        x = random.randint(0, WIDTH - PLATFORM_WIDTH)
        y = random.randint(50, HEIGHT - 150)
        platforms.append(Platform(canvas, x, y))
    return platforms

platforms = generate_platforms(canvas, NUM_PLATFORMS)
player = Player(canvas)

root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

update()
root.mainloop()
