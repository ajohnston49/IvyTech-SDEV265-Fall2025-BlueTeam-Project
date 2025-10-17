import tkinter as tk
import random
import os
from PIL import Image, ImageTk
from enemies import Enemy, load_enemy_sprites
from levels import LEVELS, get_enemy_x_position, get_enemy_y_position


# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 96  # Increased from 48 to 96 (200%)
TILE_SIZE = 32
MOVE_SPEED = 4
SCROLL_THRESHOLD = HEIGHT // 3

# Asset directory
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
SPRITE_DIR = os.path.join(ASSET_DIR, "Tiny Swords (Free Pack)")


# Setup
root = tk.Tk()
root.title("Tower Tactics")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#7ec4a8")
canvas.pack()

# Load enemy sprites after Tkinter window is created
load_enemy_sprites()

def load_boat_frames(frame_width, frame_height):
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, "assets", "boat_idle.png")
    sheet = Image.open(path)
    frames = []
    for i in range(sheet.width // frame_width):
        frame = sheet.crop((i * frame_width, 0, (i + 1) * frame_width, frame_height))
        frames.append(ImageTk.PhotoImage(frame))
    return frames

boat_frames = load_boat_frames(64, 64)


# Load heart sprite for health display (5 frames: full, 3/4, half, 1/4, empty)
heart_img = Image.open(os.path.join(ASSET_DIR, "heart_animated_1.png"))
heart_frames = []
for i in range(5):
    frame = heart_img.crop((i * 17, 0, (i + 1) * 17, 17))
    frame = frame.resize((34, 34), Image.Resampling.NEAREST)  # 2x scale
    heart_frames.append(ImageTk.PhotoImage(frame))

# Load and prepare images
def load_sprite_frames(path, frame_width, frame_height, num_frames):
    """Split a sprite sheet into individual frames"""
    sprite_sheet = Image.open(path)
    frames = []
    frames_flipped = []

    for i in range(num_frames):
        # Extract frame
        frame = sprite_sheet.crop((i * frame_width, 0, (i + 1) * frame_width, frame_height))
        # Resize to player size
        frame = frame.resize((PLAYER_SIZE, PLAYER_SIZE), Image.Resampling.NEAREST)
        frames.append(ImageTk.PhotoImage(frame))

        # Create flipped version
        frame_flipped = frame.transpose(Image.FLIP_LEFT_RIGHT)
        frames_flipped.append(ImageTk.PhotoImage(frame_flipped))

    return frames, frames_flipped

# Load player sprite frames (192x192 per frame)
player_idle_frames, player_idle_frames_left = load_sprite_frames(
    os.path.join(SPRITE_DIR, "Units/Blue Units/Warrior/Warrior_Idle.png"), 192, 192, 6)

player_run_frames, player_run_frames_left = load_sprite_frames(
    os.path.join(SPRITE_DIR, "Units/Blue Units/Warrior/Warrior_Run.png"), 192, 192, 6)

player_attack1_frames, player_attack1_frames_left = load_sprite_frames(
    os.path.join(SPRITE_DIR, "Units/Blue Units/Warrior/Warrior_Attack1.png"), 192, 192, 4)

player_attack2_frames, player_attack2_frames_left = load_sprite_frames(
    os.path.join(SPRITE_DIR, "Units/Blue Units/Warrior/Warrior_Attack2.png"), 192, 192, 4)

player_guard_frames, player_guard_frames_left = load_sprite_frames(
    os.path.join(SPRITE_DIR, "Units/Blue Units/Warrior/Warrior_Guard.png"), 192, 192, 6)

# Load individual terrain tiles
TERRAIN_DIR = os.path.join(ASSET_DIR, "Terrain")

def load_terrain_tile(filename, scale_size=TILE_SIZE):
    """Load a single terrain tile and scale it"""
    img = Image.open(os.path.join(TERRAIN_DIR, filename))
    img = img.resize((scale_size, scale_size), Image.Resampling.NEAREST)
    return ImageTk.PhotoImage(img)

# Organize terrain tiles by color/type
terrain_tiles = {
    'color1': {  # Grass/green terrain
        'top_solo': load_terrain_tile('Color1_Top_Solo.png'),
        'top_middle': load_terrain_tile('Color1_Top_Middle.png'),
        'top_corner_left': load_terrain_tile('Color1_Top_Corner_Left.png'),
        'top_corner_right': load_terrain_tile('Color1_Top_Corner_Right.png'),
        'middle': load_terrain_tile('Color1_Middle.png'),
        'middle_horizontal_solo': load_terrain_tile('Color1_Middle_Horizontal_Solo.png'),
        'middle_vertical_solo': load_terrain_tile('Color1_Middle_Verticle_Solo.png'),
        'bottom_solo': load_terrain_tile('Color1_Bottom_Solo.png'),
        'bottom_middle': load_terrain_tile('Color1_Bottom_Middle.png'),
        'bottom_corner_left': load_terrain_tile('Color1_Bottom_Corner_Left.png'),
        'bottom_corner_right': load_terrain_tile('Color1_Bottom_Corner_Right.png'),
        'left_solo': load_terrain_tile('Color1_Left_Solo.png'),
        'right_solo': load_terrain_tile('Color1_Right_Solo.png'),
        'side_left': load_terrain_tile('Color1_Side_Left.png'),
        'side_right': load_terrain_tile('Color1_Side_Right.png'),
        'only_solo': load_terrain_tile('Color1_Only_Solo.png'),
        'ramp_left_top': load_terrain_tile('Color1_Ramp_Left_Top.png'),
        'ramp_left_bottom': load_terrain_tile('Color1_Ramp_Left_Bottom.png'),
        'ramp_right_top': load_terrain_tile('Color1_Ramp_Right_Top.png'),
        'ramp_right_bottom': load_terrain_tile('Color1_Ramp_Right_Bottom.png'),
        'lifted_left': load_terrain_tile('Lifted_Left.png'),
        'lifted_middle': load_terrain_tile('Lifted_Middle.png'),
        'lifted_right': load_terrain_tile('Lifted_Right.png'),
    },
    'color2': {  # Stone/gray terrain
        'top_solo': load_terrain_tile('Color2_Top_Solo.png'),
        'top_middle': load_terrain_tile('Color2_Top_Middle.png'),
        'top_corner_left': load_terrain_tile('Color2_Top_Corner_Left.png'),
        'top_corner_right': load_terrain_tile('Color2_Top_Corner_Right.png'),
        'middle': load_terrain_tile('Color2_Middle.png'),
        'middle_horizontal_solo': load_terrain_tile('Color2_Middle_Horizontal_Solo.png'),
        'middle_vertical_solo': load_terrain_tile('Color2_Middle_Verticle_Solo.png'),
        'bottom_solo': load_terrain_tile('Color2_Bottom_Solo.png'),
        'bottom_middle': load_terrain_tile('Color2_Bottom_Middle.png'),
        'bottom_corner_left': load_terrain_tile('Color2_Bottom_Corner_Left.png'),
        'bottom_corner_right': load_terrain_tile('Color2_Bottom_Corner_Right.png'),
        'left_solo': load_terrain_tile('Color2_Left_Solo.png'),
        'right_solo': load_terrain_tile('Color2_Right_Solo.png'),
        'side_left': load_terrain_tile('Color2_Side_Left.png'),
        'side_right': load_terrain_tile('Color2_Side_Right.png'),
        'only_solo': load_terrain_tile('Color2_Only_Solo.png'),
        'ramp_left_top': load_terrain_tile('Color2_Ramp_Left_Top.png'),
        'ramp_left_bottom': load_terrain_tile('Color2_Ramp_Left_Bottom.png'),
        'ramp_right_top': load_terrain_tile('Color2_Ramp_Right_Top.png'),
        'ramp_right_bottom': load_terrain_tile('Color2_Ramp_Right_Bottom.png'),
        'lifted_left': load_terrain_tile('Lifted_Left.png'),
        'lifted_middle': load_terrain_tile('Lifted_Middle.png'),
        'lifted_right': load_terrain_tile('Lifted_Right.png'),
    },
    'color3': {  # Dark/purple terrain
        'top_solo': load_terrain_tile('Color3_Top_Solo.png'),
        'top_middle': load_terrain_tile('Color3_Top_Middle.png'),
        'top_corner_left': load_terrain_tile('Color3_Top_Corner_Left.png'),
        'top_corner_right': load_terrain_tile('Color3_Top_Corner_Right.png'),
        'middle': load_terrain_tile('Color3_Middle.png'),
        'middle_horizontal_solo': load_terrain_tile('Color3_Middle_Horizontal_Solo.png'),
        'middle_vertical_solo': load_terrain_tile('Color3_Middle_Verticle_Solo.png'),
        'bottom_solo': load_terrain_tile('Color3_Bottom_Solo.png'),
        'bottom_middle': load_terrain_tile('Color3_Bottom_Middle.png'),
        'bottom_corner_left': load_terrain_tile('Color3_Bottom_Corner_Left.png'),
        'bottom_corner_right': load_terrain_tile('Color3_Bottom_Corner_Right.png'),
        'left_solo': load_terrain_tile('Color3_Left_Solo.png'),
        'right_solo': load_terrain_tile('Color3_Right_Solo.png'),
        'side_left': load_terrain_tile('Color3_Side_Left.png'),
        'side_right': load_terrain_tile('Color3_Side_Right.png'),
        'only_solo': load_terrain_tile('Color3_Only_Solo.png'),
        'ramp_left_top': load_terrain_tile('Color3_Ramp_Left_Top.png'),
        'ramp_left_bottom': load_terrain_tile('Color3_Ramp_Left_Bottom.png'),
        'ramp_right_top': load_terrain_tile('Color3_Ramp_Right_Top.png'),
        'ramp_right_bottom': load_terrain_tile('Color3_Ramp_Right_Bottom.png'),
        'lifted_left': load_terrain_tile('Lifted_Left.png'),
        'lifted_middle': load_terrain_tile('Lifted_Middle.png'),
        'lifted_right': load_terrain_tile('Lifted_Right.png'),
    },
    'lifted': {  # Floating platform tiles
        'left': load_terrain_tile('Lifted_Left.png'),
        'middle': load_terrain_tile('Lifted_Middle.png'),
        'right': load_terrain_tile('Lifted_Right.png'),
        'solo': load_terrain_tile('Lifted_Solo.png'),
    },
}

# Load water animation frames (all 12 frames for each type)
def load_water_animations():
    """Load all 12 frames for each water animation type"""
    water_animations = {}
    for i in range(1, 4):  # Load water #1, #2, #3
        water_img = Image.open(os.path.join(TERRAIN_DIR, f"Water_FlatGround_#{i}_(12frames).png"))
        frames = []
        # Extract all 12 frames (64x64 each)
        for frame_num in range(12):
            frame = water_img.crop((frame_num * 64, 0, (frame_num + 1) * 64, 64))
            # Scale to tile size
            frame = frame.resize((TILE_SIZE, TILE_SIZE), Image.Resampling.NEAREST)
            frames.append(ImageTk.PhotoImage(frame))
        water_animations[i] = frames
    return water_animations

water_animations = load_water_animations()

# Load decorations
def load_decoration(filename, scale=None, frame_width=None, frame_height=None):
    """Load decoration, extracting first frame if it's a sprite sheet"""
    img = Image.open(os.path.join(SPRITE_DIR, "Decorations", filename))

    # If frame_width is specified, extract first frame from sprite sheet
    if frame_width and frame_height:
        # Crop to get first frame and create a new image to avoid lazy evaluation
        cropped = img.crop((0, 0, frame_width, frame_height))
        # Create a new image with the same mode and copy the data
        img = Image.new(cropped.mode, cropped.size)
        img.paste(cropped, (0, 0))

    if scale:
        img = img.resize(scale, Image.Resampling.NEAREST)

    return ImageTk.PhotoImage(img)

# Load terrain trees (single frame images from Terrain folder)
TERRAIN_DIR = os.path.join(SPRITE_DIR, "Terrain")

def load_terrain_tree(filename, scale_size):
    """Load tree from Terrain folder (not sprite sheets)"""
    img = Image.open(os.path.join(ASSET_DIR, "Terrain", filename))
    img = img.resize(scale_size, Image.Resampling.NEAREST)
    return ImageTk.PhotoImage(img)

# Load decoration assets
decorations = {
    'tree1': load_terrain_tree("Tree1.png", (64, 96)),  # 128x192 scaled to 64x96
    'tree2': load_terrain_tree("Tree2.png", (64, 122)),  # 128x243 scaled proportionally
    'tree3': load_terrain_tree("Tree3.png", (64, 84)),   # 128x168 scaled proportionally
    'tree4': load_terrain_tree("Tree4.png", (64, 64)),   # 128x128 scaled to 64x64
    'rock1': load_decoration("Rocks/Rock1.png", (32, 32)),
    'rock2': load_decoration("Rocks/Rock2.png", (32, 32)),
    'rock3': load_decoration("Rocks/Rock3.png", (32, 32)),
    'rock4': load_decoration("Rocks/Rock4.png", (32, 32)),
    'bush1': load_decoration("Bushes/Bushe1.png", (32, 32), frame_width=128, frame_height=128),  # 8 frames, extract first
    'bush2': load_decoration("Bushes/Bushe2.png", (32, 32), frame_width=128, frame_height=128),  # 8 frames, extract first
}

# Score setup
score = 0
score_text = canvas.create_text(10, 10, anchor="nw", font=("Arial", 16), fill="white", text=f"Height: {score}")

def restart_game():
    canvas.delete("all")
    game.player = None  # Force player to be recreated
    game.load_level(game.current_level_index)

flag_image = tk.PhotoImage(file=r"C:\Users\ajpot\Documents\IVY TECH\IvyTech-SDEV265-Fall2025-BlueTeam-Project\PROJECT\Brandon\tower_tactics\assets\flag_white.png")
print("Flag image loaded:", flag_image)
cloud_image = tk.PhotoImage(file=r"C:\Users\ajpot\Documents\IVY TECH\IvyTech-SDEV265-Fall2025-BlueTeam-Project\PROJECT\Brandon\tower_tactics\assets\cloud.png")

class Player:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.facing_right = True
        self.moving = False
        self.current_frame = 0
        self.frame_counter = 0
        self.animation_speed = 8
        self.state = 'idle'
        self.animation_lock = False
        self.current_platform = None
        self.health = 3
        self.freeze = False
        self.id = canvas.create_image(x, y, anchor="center", image=player_idle_frames[0])

        # Combat system
        self.invincible = False
        self.invincibility_timer = 0
        self.combo_hits = 0
        self.guarding = False

    def set_velocity(self, vx, vy):
        if self.freeze:
            self.vx = 0
            self.vy = 0
        else:
            self.vx = vx
            self.vy = vy
            if vx > 0:
                self.facing_right = True
            elif vx < 0:
                self.facing_right = False

    def set_platform(self, platform):
        self.current_platform = platform

    def take_damage(self):
        if self.invincible or self.guarding:
            return False

        self.combo_hits += 1
        if self.combo_hits >= 2:
            self.combo_hits = 0
            self.health -= 1

        self.invincible = True
        self.invincibility_timer = 60  # ~1 second

        if self.health <= 0:
            self.handle_player_death()
            return True

        return False

    def handle_player_death(self):
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 40, text="Game Over", font=("Arial", 32), fill="red")
        retry_button = tk.Button(self.canvas.master, text="Retry", font=("Arial", 16), command=restart_game)
        self.canvas.create_window(WIDTH // 2, HEIGHT // 2 + 20, window=retry_button)

    def update(self, platforms):
        if self.invincible:
            self.invincibility_timer -= 1
            if self.invincibility_timer <= 0:
                self.invincible = False

        if not self.animation_lock:
            intended_x = self.x + self.vx
            intended_y = self.y + self.vy

            def is_colliding_with_solid(x, y, solids):
                for obj in solids:
                    if abs(x - obj['x']) < obj['width'] // 2 and abs(y - obj['y']) < obj['height'] // 2:
                        return True
                return False

            if self.current_platform and is_colliding_with_solid(intended_x, intended_y, self.current_platform.solid_objects):
                self.vx = 0
                self.vy = 0
            else:
                if self.current_platform and self.current_platform.tile_map:
                    col = int((intended_x - self.current_platform.rect_x) // TILE_SIZE)
                    row = int((intended_y - self.current_platform.rect_y) // TILE_SIZE)
                    tile = self.current_platform.tile_map.get((col, row))

                    if tile and tile.get('tile_type') != 'invisible_wall':
                        self.x = intended_x
                        self.y = intended_y
                    else:
                        self.vx = 0
                        self.vy = 0
                else:
                    self.x = max(0, min(intended_x, WIDTH))
                    self.y = max(0, min(intended_y, HEIGHT))

        self.update_sprite()
        self.canvas.coords(self.id, self.x, self.y)

    def update_sprite(self):
        is_moving = self.vx != 0 or self.vy != 0
        if not self.animation_lock:
            if self.guarding:
                self.state = 'guard'
            else:
                self.state = 'run' if is_moving else 'idle'

        if self.state == 'idle':
            frames = player_idle_frames if self.facing_right else player_idle_frames_left
            max_frames = 6
        elif self.state == 'run':
            frames = player_run_frames if self.facing_right else player_run_frames_left
            max_frames = 6
        elif self.state == 'attack1':
            frames = player_attack1_frames if self.facing_right else player_attack1_frames_left
            max_frames = 4
        elif self.state == 'attack2':
            frames = player_attack2_frames if self.facing_right else player_attack2_frames_left
            max_frames = 4
        elif self.state == 'guard':
            frames = player_guard_frames if self.facing_right else player_guard_frames_left
            max_frames = 6
        else:
            frames = player_idle_frames if self.facing_right else player_idle_frames_left
            max_frames = 6

        self.frame_counter += 1
        speed = 10 if self.state in ['attack1', 'attack2'] else self.animation_speed
        if self.frame_counter >= speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % max_frames
            if self.animation_lock and self.current_frame == 0:
                self.animation_lock = False
                self.state = 'idle'
                self.guarding = False

        self.canvas.itemconfig(self.id, image=frames[self.current_frame], state='normal')

    def attack1(self):
        if not self.animation_lock:
            self.state = 'attack1'
            self.animation_lock = True
            self.current_frame = 0
            self.frame_counter = 0
            return True
        return False

    def attack2(self):
        if not self.animation_lock:
            self.state = 'attack2'
            self.animation_lock = True
            self.current_frame = 0
            self.frame_counter = 0

    def guard(self):
        if not self.animation_lock:
            self.state = 'guard'
            self.animation_lock = True
            self.current_frame = 0
            self.frame_counter = 0
            self.guarding = True

    def hide(self):
        self.canvas.itemconfig(self.id, state='hidden')

    def show(self):
        self.canvas.itemconfig(self.id, state='normal')



class Platform:
    def __init__(self, canvas, x, y, width, height, terrain_color=None, terrain_layout=None):
        """Create a rectangular contained platform"""
        self.canvas = canvas

        # Store position for external access (e.g. boat logic)
        self.x = x
        self.y = y

        # Internal rect values (used for layout logic)
        self.rect_x = x
        self.rect_y = y
        self.rect_width = width
        self.rect_height = height

        self.tiles = []
        self.solid_objects = []  # Track solid decorations like trees
        self.decorations = []
        self.water_tiles = []
        self.terrain_layout = terrain_layout
        self.tile_map = {}  # Track walkable tiles by (col, row) -> bounds

        # Use specified terrain type or choose random
        self.terrain_type = terrain_color if terrain_color else random.choice(['color1', 'color2', 'color3'])

        if terrain_layout:
            self.create_custom_platform()
            self.add_water_below()  # Add water for custom platforms too
        else:
            self.create_platform()
            self.add_water_below()
            self.add_trees_at_edges()

    def create_platform(self):
        """Create a rectangular platform filled with tiles"""
        tileset = terrain_tiles[self.terrain_type]

        tiles_wide = self.rect_width // TILE_SIZE
        tiles_tall = self.rect_height // TILE_SIZE

        for row in range(tiles_tall):
            for col in range(tiles_wide):
                x = self.rect_x + col * TILE_SIZE + TILE_SIZE // 2
                y = self.rect_y + row * TILE_SIZE + TILE_SIZE // 2

                # Determine which tile to use based on position
                is_top = row == 0
                is_bottom = row == tiles_tall - 1
                is_left = col == 0
                is_right = col == tiles_wide - 1

                # Select appropriate tile
                if is_top and is_left:
                    tile_img = tileset['top_corner_left']
                    tile_type = 'top_corner_left'
                elif is_top and is_right:
                    tile_img = tileset['top_corner_right']
                    tile_type = 'top_corner_right'
                elif is_bottom and is_left:
                    tile_img = tileset['bottom_corner_left']
                    tile_type = 'bottom_corner_left'
                elif is_bottom and is_right:
                    tile_img = tileset['bottom_corner_right']
                    tile_type = 'bottom_corner_right'
                elif is_top:
                    tile_img = tileset['top_middle']
                    tile_type = 'top_middle'
                elif is_bottom:
                    tile_img = tileset['bottom_middle']
                    tile_type = 'bottom_middle'
                elif is_left:
                    tile_img = tileset['side_left']
                    tile_type = 'side_left'
                elif is_right:
                    tile_img = tileset['side_right']
                    tile_type = 'side_right'
                else:
                    # Interior tile
                    tile_img = tileset['middle']
                    tile_type = 'middle'

                tile = self.canvas.create_image(x, y, anchor="center", image=tile_img)
                self.tiles.append(tile)

                # Track tile in tile_map for consistent movement handling
                tile_left = self.rect_x + col * TILE_SIZE
                tile_right = tile_left + TILE_SIZE
                tile_top = self.rect_y + row * TILE_SIZE
                tile_bottom = tile_top + TILE_SIZE

                # Determine allowed movement directions
                allow_up = True
                allow_down = True
                allow_left = True
                allow_right = True

                if tile_type == 'top_corner_left':
                    allow_up = False
                    allow_left = False
                elif tile_type == 'top_corner_right':
                    allow_up = False
                    allow_right = False
                elif tile_type == 'bottom_corner_left':
                    allow_down = False
                    allow_left = False
                elif tile_type == 'bottom_corner_right':
                    allow_down = False
                    allow_right = False
                elif tile_type == 'top_middle':
                    allow_up = False
                elif tile_type == 'bottom_middle':
                    allow_down = False
                elif tile_type == 'side_left':
                    allow_left = False
                elif tile_type == 'side_right':
                    allow_right = False

                self.tile_map[(col, row)] = {
                    'left': tile_left,
                    'right': tile_right,
                    'top': tile_top,
                    'bottom': tile_bottom,
                    'center_x': x,
                    'center_y': y,
                    'is_ramp': False,
                    'ramp_direction': None,
                    'tile_type': tile_type,
                    'allow_up': allow_up,
                    'allow_down': allow_down,
                    'allow_left': allow_left,
                    'allow_right': allow_right
                }

                # Add decorations on top row only
                if is_top and random.random() > 0.7:
                    self.add_decoration(x, y)

    def create_custom_platform(self):
        """Create a platform from a custom terrain layout"""
        tileset = terrain_tiles[self.terrain_type]

        # Track lifted tile positions for collision detection
        lifted_coords = set()

        # Render each tile specified in the layout
        for col, row, tile_type in self.terrain_layout:
            x = self.rect_x + col * TILE_SIZE + TILE_SIZE // 2
            y = self.rect_y + row * TILE_SIZE + TILE_SIZE // 2

            tile_img = tileset[tile_type]
            tile = self.canvas.create_image(x, y, anchor="center", image=tile_img)
            self.tiles.append(tile)

            # Track lifted tiles (non-walkable cliff faces)
            if tile_type in ['lifted_left', 'lifted_middle', 'lifted_right']:
                lifted_coords.add((col, row))
                continue  # Don't add to tile_map

            # All other tiles are walkable
            is_walkable = True

            if is_walkable:
                tile_left = self.rect_x + col * TILE_SIZE
                tile_right = tile_left + TILE_SIZE
                tile_top = self.rect_y + row * TILE_SIZE
                tile_bottom = tile_top + TILE_SIZE

                # Check if this is a ramp tile
                is_ramp = 'ramp' in tile_type
                ramp_direction = None
                if is_ramp:
                    if 'left' in tile_type:
                        ramp_direction = 'left'  # Ramp going up to the left
                    elif 'right' in tile_type:
                        ramp_direction = 'right'  # Ramp going down to the right

                # Determine allowed movement directions based on tile type
                # By default, all directions allowed
                allow_up = True
                allow_down = True
                allow_left = True
                allow_right = True

                # Restrict based on specific tile types (only restrict platform edges)
                if tile_type == 'top_corner_left':
                    allow_up = False
                    allow_left = False
                elif tile_type == 'top_corner_right':
                    allow_up = False
                    allow_right = False
                elif tile_type == 'bottom_corner_left':
                    allow_down = False
                    allow_left = False
                elif tile_type == 'bottom_corner_right':
                    allow_down = False
                    allow_right = False
                elif tile_type == 'top_middle':
                    allow_up = False
                elif tile_type == 'bottom_middle':
                    allow_down = False
                elif tile_type == 'side_left':
                    allow_left = False
                elif tile_type == 'side_right':
                    allow_right = False
                # All other tiles (middle, ramps, etc.) have no restrictions - all directions allowed

                self.tile_map[(col, row)] = {
                    'left': tile_left,
                    'right': tile_right,
                    'top': tile_top,
                    'bottom': tile_bottom,
                    'center_x': x,
                    'center_y': y,
                    'is_ramp': is_ramp,
                    'ramp_direction': ramp_direction,
                    'tile_type': tile_type,
                    'allow_up': allow_up,
                    'allow_down': allow_down,
                    'allow_left': allow_left,
                    'allow_right': allow_right
                }

        # Post-processing: Block movement into lifted edges
        self._apply_lifted_restrictions(lifted_coords)

    def _apply_lifted_restrictions(self, lifted_coords):
        """
        Update adjacent walkable tiles to block movement into lifted edge tiles.
        Lifted tiles are non-walkable cliff faces that should act as collision walls.
        """
        for (col, row), tile_data in self.tile_map.items():
            # Block movement LEFT if a lifted tile is immediately to the left
            if (col - 1, row) in lifted_coords:
                tile_data['allow_left'] = False

            # Block movement RIGHT if a lifted tile is immediately to the right
            if (col + 1, row) in lifted_coords:
                tile_data['allow_right'] = False

            # Block movement DOWN if a lifted tile is immediately below
            if (col, row + 1) in lifted_coords:
                tile_data['allow_down'] = False

            # Block movement UP if a lifted tile is immediately above
            # (Usually lifted tiles are below raised platforms, but handle all cases)
            if (col, row - 1) in lifted_coords:
                tile_data['allow_up'] = False

    def get_tile_at_position(self, x, y):
        """Get the tile at the given position"""
        if not self.tile_map:
            return None

        # Convert position to tile coordinates
        col = int((x - self.rect_x) / TILE_SIZE)
        row = int((y - self.rect_y) / TILE_SIZE)

        if (col, row) in self.tile_map:
            return (col, row, self.tile_map[(col, row)])
        return None

    def get_tile_area(self, col, row):
        """Get walkable area for a specific tile, searching connected tiles in the same row"""
        if not self.tile_map:
            # No tile map, use full platform bounds
            return None

        if (col, row) not in self.tile_map:
            return None

        # Find all connected walkable tiles in the same row
        left_col = col
        right_col = col

        # Search left
        while (left_col - 1, row) in self.tile_map:
            left_col -= 1

        # Search right
        while (right_col + 1, row) in self.tile_map:
            right_col += 1

        # Return bounds of the connected tile area
        left_bound = self.tile_map[(left_col, row)]['left'] + TILE_SIZE * 0.75
        right_bound = self.tile_map[(right_col, row)]['right'] - TILE_SIZE * 0.75

        return {
            'left': left_bound,
            'right': right_bound,
            'center_x': self.tile_map[(col, row)]['center_x'],
            'center_y': self.tile_map[(col, row)]['center_y']
        }

    def add_decoration(self, x, y, deco_name=None):
        # If no decoration name provided, choose randomly (no trees in random selection)
        if deco_name is None:
            deco_choices = ['rock1', 'rock2', 'rock3', 'rock4', 'bush1', 'bush2']
            deco_name = random.choice(deco_choices)

        deco_img = decorations[deco_name]

        # Trees need to be raised above the ground
        y_offset = -16 if 'tree' in deco_name else 0

        # Place decoration centered on the tile
        deco = self.canvas.create_image(x, y + y_offset, anchor="center", image=deco_img)
        self.decorations.append(deco)

    def add_water_below(self):
        """Add water tiles along the bottom edge of the platform"""
        tiles_wide = self.rect_width // TILE_SIZE
        bottom_y = self.rect_y + self.rect_height + TILE_SIZE // 2

        for col in range(tiles_wide):
            x = self.rect_x + col * TILE_SIZE + TILE_SIZE // 2

            # Determine which water animation to use based on position
            if col == 0:
                # Left corner - use water #1
                water_type = 1
            elif col == tiles_wide - 1:
                # Right corner - use water #3
                water_type = 3
            else:
                # Middle - use water #2
                water_type = 2

            # Create water tile with first frame
            water_tile = self.canvas.create_image(x, bottom_y, anchor="center", image=water_animations[water_type][0])
            # Store tile ID and its animation type
            self.water_tiles.append({'id': water_tile, 'type': water_type})

    def animate_water(self, frame_index):
        """Update water tiles to show the current frame"""
        for water_info in self.water_tiles:
            water_type = water_info['type']
            water_id = water_info['id']
            # Update to current frame
            self.canvas.itemconfig(water_id, image=water_animations[water_type][frame_index])

    def add_trees_at_edges(self):
    
    # Get platform edges
        left_x = self.rect_x + TILE_SIZE * 2
        right_x = self.rect_x + self.rect_width - TILE_SIZE * 2
        top_y = self.rect_y + TILE_SIZE // 2

        # Top-left: tree1
        self.add_decoration(left_x, top_y, 'tree1')
        self.solid_objects.append({'x': left_x, 'y': top_y, 'width': 64, 'height': 96})

        # Top-right: tree2
        self.add_decoration(right_x, top_y, 'tree2')
        self.solid_objects.append({'x': right_x, 'y': top_y, 'width': 64, 'height': 122})

        # Mid-left: tree3
        mid_left_x = self.rect_x + TILE_SIZE * 4
        self.add_decoration(mid_left_x, top_y, 'tree3')
        self.solid_objects.append({'x': mid_left_x, 'y': top_y, 'width': 64, 'height': 84})

        # Mid-right: tree4
        mid_right_x = self.rect_x + self.rect_width - TILE_SIZE * 4
        self.add_decoration(mid_right_x, top_y, 'tree4')
        self.solid_objects.append({'x': mid_right_x, 'y': top_y, 'width': 64, 'height': 64})


    def move(self, dy):
        """Move the platform vertically for scrolling"""
        self.rect_y += dy
        for tile in self.tiles:
            self.canvas.move(tile, 0, dy)
        for deco in self.decorations:
            self.canvas.move(deco, 0, dy)
        for water_info in self.water_tiles:
            self.canvas.move(water_info['id'], 0, dy)

    def is_offscreen(self):
        """Check if platform has scrolled off screen"""
        return self.rect_y > HEIGHT + self.rect_height


class Boat:
    def __init__(self, canvas, x, y, image, mode="intro"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.vx = 4 if mode == "intro" else 0  # Moves only during intro or exit ride
        self.image = image
        self.sprite = canvas.create_image(x, y, anchor="center", image=image)
        self.active = False
        self.player_attached = False
        self.mode = mode
        self.arrived = False
        self.departing = False  # Exit trigger

    def start(self):
        self.active = True

    def update(self, player, platform=None):
        if not self.active:
            return False

        # --- INTRO MODE ---
        if self.mode == "intro":
            self.x += self.vx
            self.canvas.coords(self.sprite, self.x, self.y)

            player.x = self.x
            player.y = self.y - 10
            player.show()
            self.canvas.coords(player.id, player.x, player.y)
            self.canvas.tag_raise(player.id)

            if platform and self.x >= platform.x + 64 and not self.arrived:
                self.arrived = True
                player.freeze = False
                player.x = self.x
                player.y = self.y - TILE_SIZE  # 1 tile north of boat
                player.set_platform(platform)
                self.canvas.coords(player.id, player.x, player.y)

                # ✅ Switch to exit mode and stop moving
                self.mode = "exit"
                self.vx = 0
                return True

            return False

        # --- EXIT MODE ---
        if not self.departing:
            # Wait for player to walk into boat
            dx = player.x - self.x
            dy = player.y - self.y
            if (dx**2 + dy**2) ** 0.5 < 32:
                self.player_attached = True
                self.departing = True
                self.vx = 2  # Start moving
                player.set_velocity(0, 0)
                player.freeze = True
                player.hide()

        if self.departing:
            self.x += self.vx
            self.canvas.coords(self.sprite, self.x, self.y)

            if self.player_attached:
                player.x = self.x
                player.y = self.y - 10
                self.canvas.coords(player.id, player.x, player.y)
                self.canvas.tag_raise(player.id)

            if self.x > self.canvas.winfo_width() + 100:
                return True  # ✅ Boat exited with player

        return False

class Game:
    def __init__(self):
        self.platforms = []
        self.camera_y = 0
        self.score = 0
        self.water_frame = 0
        self.water_frame_counter = 0
        self.water_animation_speed = 8

        self.current_level_index = 0
        self.level_name_text = None
        self.enemies = []
        self.player = None
        self.game_over = False
        self.boat = None
        self.intro_done = False
        self.victory_flag_shown = False

        self.keys = {'w': False, 'a': False, 's': False, 'd': False}
        self.action_keys = {'j': False, 'k': False, 'l': False}

        self.heart_sprites = []
        for i in range(3):
            heart = canvas.create_image(WIDTH - 40 - (i * 40), 30, anchor="center", image=heart_frames[0])
            self.heart_sprites.append(heart)

        self.load_level(0)

    def load_level(self, level_index):
        if level_index >= len(LEVELS):
            self.show_victory()
            return

        self.current_level_index = level_index
        level = LEVELS[level_index]
        self.game_over = False
        self.boat = None
        self.intro_done = False
        self.victory_flag_shown = False

        canvas.delete("all")

        self.heart_sprites = []
        for i in range(3):
            heart = canvas.create_image(WIDTH - 40 - (i * 40), 30, anchor="center", image=heart_frames[0])
            self.heart_sprites.append(heart)

        self.platforms = []
        self.enemies = []

        platform_x = (WIDTH - level['platform_width']) // 2
        platform_y = HEIGHT - 300
        start_platform = Platform(
            canvas,
            platform_x,
            platform_y,
            level['platform_width'],
            level['platform_height'],
            terrain_color=level['terrain_color'],
            terrain_layout=level.get('terrain_layout')
        )
        self.platforms.append(start_platform)

        player_start_x = -100
        player_start_y = platform_y + TILE_SIZE // 2

        self.player = Player(canvas, player_start_x, player_start_y)
        self.player.set_platform(start_platform)
        canvas.tag_raise(self.player.id)

        for enemy_data in level['enemies']:
            if 'tile_col' in enemy_data and 'tile_row' in enemy_data:
                area = start_platform.get_tile_area(enemy_data['tile_col'], enemy_data['tile_row'])
                if area:
                    enemy_x = area['center_x']
                    enemy_y = area['center_y']
                    enemy = Enemy(canvas, enemy_x, enemy_y, start_platform,
                                  enemy_type=enemy_data['type'],
                                  tile_col=enemy_data['tile_col'],
                                  tile_row=enemy_data['tile_row'])
                else:
                    continue
            else:
                enemy_x = get_enemy_x_position(enemy_data['position'], platform_x, level['platform_width'])
                enemy_y = get_enemy_y_position(platform_y, level['platform_height'])
                enemy = Enemy(canvas, enemy_x, enemy_y, start_platform, enemy_type=enemy_data['type'])

            self.enemies.append(enemy)
            canvas.tag_raise(enemy.sprite)

        self.level_name_text = canvas.create_text(
            WIDTH // 2, 50,
            text=f"Level {level['id']}: {level['name']}",
            font=("Arial", 20, "bold"),
            fill="white",
            anchor="center"
        )

        self.start_intro_boat_sequence()

    def start_intro_boat_sequence(self):
        platform = self.platforms[0]
        boat_y = platform.y + platform.rect_height + 16
        self.boat = Boat(canvas, -100, boat_y, boat_frames[0], mode="intro")
        self.boat.start()
        self.player.freeze = True

    def show_level_flag(self):
        if self.platforms:
            flag_x = WIDTH // 2
            flag_y = self.platforms[0].y + self.platforms[0].rect_height // 2
            canvas.create_image(flag_x, flag_y, anchor="center", image=flag_image)

    def show_cloud_message(self):
        self.cloud_sprite = canvas.create_image(-200, HEIGHT // 4, anchor="center", image=cloud_image)
        self.cloud_phase = "entering"
        self.cloud_x = -200
        self.cloud_target_x = WIDTH // 2
        self.cloud_timer = 0

        def animate_cloud():
            if self.cloud_phase == "entering":
                self.cloud_x += 12
                if self.cloud_x >= self.cloud_target_x:
                    self.cloud_x = self.cloud_target_x
                    self.cloud_phase = "pausing"
                    self.cloud_timer = 180

            elif self.cloud_phase == "pausing":
                self.cloud_timer -= 3
                self.cloud_x += 0.5
                if self.cloud_timer <= 0:
                    self.cloud_phase = "exiting"

            elif self.cloud_phase == "exiting":
                self.cloud_x += 16
                if self.cloud_x > WIDTH + 200:
                    canvas.delete(self.cloud_sprite)
                    return

            canvas.coords(self.cloud_sprite, self.cloud_x, HEIGHT // 4)
            root.after(16, animate_cloud)

        animate_cloud()

    def show_victory(self):
        canvas.create_text(WIDTH // 2, HEIGHT // 2 - 40, text="Victory!", font=("Arial", 32), fill="white")
        if self.platforms:
            flag_x = WIDTH // 2
            flag_y = self.platforms[0].y + self.platforms[0].rect_height // 2
            canvas.create_image(flag_x, flag_y, anchor="center", image=flag_image)

        retry_button = tk.Button(canvas.master, text="Play Again", font=("Arial", 16), command=self.restart_game)
        canvas.create_window(WIDTH // 2, HEIGHT // 2 + 20, window=retry_button)
        print("Victory screen triggered")

    def restart_game(self):
        self.player = None
        self.game_over = False
        self.load_level(0)

    def update(self):
        if self.game_over:
            root.after(16, self.update)
            return

        if not self.intro_done:
            if self.boat and self.boat.update(self.player, self.platforms[0]):
                self.intro_done = True
            root.after(16, self.update)
            return

        vx = 0
        vy = 0
        if self.keys['a']: vx -= MOVE_SPEED
        if self.keys['d']: vx += MOVE_SPEED
        if self.keys['w']: vy -= MOVE_SPEED
        if self.keys['s']: vy += MOVE_SPEED

        self.player.set_velocity(vx, vy)
        self.player.update(self.platforms)

        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if not enemy.is_dead:
                dx = self.player.x - enemy.x
                dy = self.player.y - enemy.y
                distance = (dx**2 + dy**2) ** 0.5
                if distance < 50:
                    if self.player.take_damage():
                        self.game_over = True
                        self.show_game_over()
                    else:
                        self.update_hearts()

        if self.intro_done and all(enemy.is_dead for enemy in self.enemies) and self.enemies:
            if not self.victory_flag_shown:
                self.victory_flag_shown = True
                self.show_level_flag()
                self.show_cloud_message()

            if self.boat and self.boat.update(self.player):
                self.load_level(self.current_level_index + 1)

        self.water_frame_counter += 1
        if self.water_frame_counter >= self.water_animation_speed:
            self.water_frame_counter = 0
            self.water_frame = (self.water_frame + 1) % 12
            for platform in self.platforms:
                platform.animate_water(self.water_frame)

        root.after(16, self.update)

    def key_press(self, event):
        key = event.keysym.lower()
        if key in self.keys:
            self.keys[key] = True

    def key_release(self, event):
        key = event.keysym.lower()
        if key in self.keys:
            self.keys[key] = False

    def mouse_click(self, event):
        if self.player.attack1():
            for enemy in self.enemies:
                if not enemy.is_dead:
                    dx = self.player.x - enemy.x
                    dy = self.player.y - enemy.y
                    distance = (dx**2 + dy**2) ** 0.5
                    if distance < 70:
                        enemy.take_damage(1)

    def mouse_right_click(self, event):
        self.player.guard()

    def update_hearts(self):
        for i in range(3):
            if i < self.player.health:
                canvas.itemconfig(self.heart_sprites[i], image=heart_frames[0])
            else:
                canvas.itemconfig(self.heart_sprites[i], image=heart_frames[4])

    
# Initialize game
game = Game()

root.bind("<KeyPress>", game.key_press)
root.bind("<KeyRelease>", game.key_release)
root.bind("<Button-1>", game.mouse_click)  # Left mouse click
root.bind("<Button-2>", game.mouse_right_click)  # Right mouse click (Button-2 on Mac, Button-3 on Windows/Linux)
root.bind("<Button-3>", game.mouse_right_click)  # Also bind Button-3 for cross-platform compatibility

game.update()
root.mainloop()
