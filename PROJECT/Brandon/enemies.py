import os
from PIL import Image, ImageTk

# Constants
TILE_SIZE = 32
ENEMY_SIZE = 96

def load_sprite_frames(path, frame_width, frame_height, num_frames):
    """Split a sprite sheet into individual frames"""
    sprite_sheet = Image.open(path)
    frames = []
    frames_flipped = []

    for i in range(num_frames):
        frame = sprite_sheet.crop((i * frame_width, 0, (i + 1) * frame_width, frame_height))
        frame = frame.resize((ENEMY_SIZE, ENEMY_SIZE), Image.Resampling.NEAREST)
        frames.append(ImageTk.PhotoImage(frame))
        frame_flipped = frame.transpose(Image.FLIP_LEFT_RIGHT)
        frames_flipped.append(ImageTk.PhotoImage(frame_flipped))
    return frames, frames_flipped

# Asset directory
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
ENEMY_DIR = os.path.join(ASSET_DIR, "Tiny Swords (Enemy Pack)", "Enemy Pack")

# Enemy sprite storage (loaded after Tkinter window is created)
paddle_fish_idle = None
paddle_fish_idle_flipped = None
paddle_fish_run = None
paddle_fish_run_flipped = None
paddle_fish_attack = None
paddle_fish_attack_flipped = None

troll_idle = None
troll_idle_flipped = None
troll_walk = None
troll_walk_flipped = None
troll_attack = None
troll_attack_flipped = None
troll_dead = None
troll_dead_flipped = None

def load_enemy_sprites():
    """Load all enemy sprites - must be called after Tkinter root is created"""
    global paddle_fish_idle, paddle_fish_idle_flipped
    global paddle_fish_run, paddle_fish_run_flipped
    global paddle_fish_attack, paddle_fish_attack_flipped
    global troll_idle, troll_idle_flipped
    global troll_walk, troll_walk_flipped
    global troll_attack, troll_attack_flipped
    global troll_dead, troll_dead_flipped

    # Load Paddle Fish sprites - Idle: 8 frames (1536x192), Run: 6 frames (1152x192), Attack: 6 frames (1152x192)
    paddle_fish_idle, paddle_fish_idle_flipped = load_sprite_frames(
        os.path.join(ENEMY_DIR, "Paddle Fish", "PaddleFish_Idle.png"), 192, 192, 8
    )
    paddle_fish_run, paddle_fish_run_flipped = load_sprite_frames(
        os.path.join(ENEMY_DIR, "Paddle Fish", "PaddleFish_Run.png"), 192, 192, 6
    )
    paddle_fish_attack, paddle_fish_attack_flipped = load_sprite_frames(
        os.path.join(ENEMY_DIR, "Paddle Fish", "PaddleFish_Attack.png"), 192, 192, 6
    )

    # Load Troll sprites - Idle: 12 frames (4608x384), Walk: 10 frames (3840x384), Attack: 6 frames (2304x384), Dead: 10 frames (3840x384)
    troll_idle, troll_idle_flipped = load_sprite_frames(
        os.path.join(ENEMY_DIR, "Troll", "Troll_Idle.png"), 384, 384, 12
    )
    troll_walk, troll_walk_flipped = load_sprite_frames(
        os.path.join(ENEMY_DIR, "Troll", "Troll_Walk.png"), 384, 384, 10
    )
    troll_attack, troll_attack_flipped = load_sprite_frames(
        os.path.join(ENEMY_DIR, "Troll", "Troll_Attack.png"), 384, 384, 6
    )
    troll_dead, troll_dead_flipped = load_sprite_frames(
        os.path.join(ENEMY_DIR, "Troll", "Troll_Dead.png"), 384, 384, 10
    )

class Enemy:
    def __init__(self, canvas, x, y, platform, enemy_type='paddle_fish', tile_col=None, tile_row=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.platform = platform
        self.enemy_type = enemy_type
        self.state = 'idle'
        self.current_frame = 0
        self.frame_counter = 0
        self.facing_right = False
        self.speed = 1  # Slower movement speed
        self.health = 3  # Enemy health
        self.is_dead = False
        self.death_animation_complete = False
        self.hit_flash = False
        self.hit_flash_timer = 0
        self.tile_col = tile_col
        self.tile_row = tile_row
        self.tile_bounds = None

        # Get tile bounds if tile position specified
        if tile_col is not None and tile_row is not None:
            self.tile_bounds = platform.get_tile_area(tile_col, tile_row)

        # Load appropriate sprites based on enemy type
        if enemy_type == 'paddle_fish':
            self.idle_frames = paddle_fish_idle
            self.idle_frames_flipped = paddle_fish_idle_flipped
            self.run_frames = paddle_fish_run
            self.run_frames_flipped = paddle_fish_run_flipped
            self.attack_frames = paddle_fish_attack
            self.attack_frames_flipped = paddle_fish_attack_flipped
            self.dead_frames = None
            self.dead_frames_flipped = None
        elif enemy_type == 'troll':
            self.idle_frames = troll_idle
            self.idle_frames_flipped = troll_idle_flipped
            self.run_frames = troll_walk
            self.run_frames_flipped = troll_walk_flipped
            self.attack_frames = troll_attack
            self.attack_frames_flipped = troll_attack_flipped
            self.dead_frames = troll_dead
            self.dead_frames_flipped = troll_dead_flipped

        self.sprite = canvas.create_image(x, y, anchor="center", image=self.idle_frames[0])

    def take_damage(self, damage=1):
        """Enemy takes damage"""
        if not self.is_dead:
            self.health -= damage
            self.hit_flash = True
            self.hit_flash_timer = 10  # Flash for 10 frames
            if self.health <= 0:
                self.health = 0
                self.is_dead = True
                self.state = 'dead'
                self.current_frame = 0
                return True  # Enemy died
        return False

    def update(self):
        """Update enemy AI and animation"""
        # Handle hit flash effect
        if self.hit_flash:
            self.hit_flash_timer -= 1
            # Toggle visibility every 2 frames for flashing effect
            if self.hit_flash_timer % 4 < 2:
                self.canvas.itemconfig(self.sprite, state='hidden')
            else:
                self.canvas.itemconfig(self.sprite, state='normal')

            if self.hit_flash_timer <= 0:
                self.hit_flash = False
                self.canvas.itemconfig(self.sprite, state='normal')

        # If dead, only play death animation once
        if self.is_dead:
            if not self.death_animation_complete and self.dead_frames:
                self.frame_counter += 1
                if self.frame_counter >= 6:
                    self.frame_counter = 0
                    if self.current_frame < len(self.dead_frames) - 1:
                        self.current_frame += 1
                        frame = self.dead_frames_flipped[self.current_frame] if not self.facing_right else self.dead_frames[self.current_frame]
                        self.canvas.itemconfig(self.sprite, image=frame)
                    else:
                        self.death_animation_complete = True
            return  # Don't move or do anything else when dead

        # Simple patrol behavior - move back and forth on platform
        if self.state == 'idle':
            self.state = 'run'

        if self.state == 'run':
            # Move in current direction
            if self.facing_right:
                new_x = self.x + self.speed
            else:
                new_x = self.x - self.speed

            # Use tile bounds if specified, otherwise use platform bounds
            if self.tile_bounds:
                # Bounce at tile edges
                if new_x < self.tile_bounds['left']:
                    new_x = self.tile_bounds['left']
                    self.facing_right = True
                elif new_x > self.tile_bounds['right']:
                    new_x = self.tile_bounds['right']
                    self.facing_right = False
            else:
                # Check platform boundaries (same insets as player)
                inset_left = TILE_SIZE * 0.75
                inset_right = TILE_SIZE * 1.25
                platform_left = self.platform.rect_x + inset_left
                platform_right = self.platform.rect_x + self.platform.rect_width - inset_right

                # Bounce at edges
                if new_x < platform_left:
                    new_x = platform_left
                    self.facing_right = True
                elif new_x > platform_right:
                    new_x = platform_right
                    self.facing_right = False

            self.x = new_x
            self.canvas.coords(self.sprite, self.x, self.y)

        # Update animation
        self.frame_counter += 1
        if self.frame_counter >= 6:
            self.frame_counter = 0

            if self.state == 'idle':
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                frame = self.idle_frames_flipped[self.current_frame] if not self.facing_right else self.idle_frames[self.current_frame]
            elif self.state == 'run':
                self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                frame = self.run_frames_flipped[self.current_frame] if not self.facing_right else self.run_frames[self.current_frame]

            self.canvas.itemconfig(self.sprite, image=frame)
