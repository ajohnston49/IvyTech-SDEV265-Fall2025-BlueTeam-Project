import pygame, random, os  # Import game engine, randomness, and file path tools

# === Game Constants ===
WIDTH, HEIGHT = 400, 600                 # Window size
PLAYER_W, PLAYER_H = 40, 40              # Player size
PLATFORM_W, PLATFORM_H = 60, 10          # Platform size
GRAVITY = .6                             # Gravity strength
JUMP_VEL = -20                           # Jump velocity
MOVE_SPEED = 4                           # Horizontal movement speed
NUM_PLATFORMS = 8                        # Number of platforms in play

# === Load Assets ===
ASSETS = os.path.join(os.path.dirname(__file__), "assets")  # Path to assets folder

# Background and platform images
bg_img = pygame.image.load(os.path.join(ASSETS, "background.png"))
plat_img = pygame.image.load(os.path.join(ASSETS, "platform.png"))

# Spider enemy images
spider_img = pygame.image.load(os.path.join(ASSETS, "spider.png"))
spider_flip = pygame.image.load(os.path.join(ASSETS, "spider_flipped.png"))

# Player movement sprites
player_left = pygame.image.load(os.path.join(ASSETS, "player.png"))
player_right = pygame.image.load(os.path.join(ASSETS, "player_flipped.png"))
player_jump_left = pygame.image.load(os.path.join(ASSETS, "player_jump_flipped.png"))
player_jump_right = pygame.image.load(os.path.join(ASSETS, "player_jump.png"))
player_fall_left = pygame.image.load(os.path.join(ASSETS, "player_fall_flipped.png"))
player_fall_right = pygame.image.load(os.path.join(ASSETS, "player_fall.png"))

# Start and death screens
start_menu_img = pygame.image.load(os.path.join(ASSETS, "start_menu.png"))
death_screens = [pygame.image.load(os.path.join(ASSETS, f"gameover{i}.png")) for i in range(1, 13)]

# === Sound Setup ===
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create game window
clock = pygame.time.Clock()                        # Control frame rate
font = pygame.font.SysFont("Arial", 16)            # Score font

# Background music
pygame.mixer.music.load(os.path.join(ASSETS, "background.mp3"))
pygame.mixer.music.play(-1)  # Loop forever

# Sound effects
jump_sfx = pygame.mixer.Sound(os.path.join(ASSETS, "jump.wav"))
hurt_sfx = pygame.mixer.Sound(os.path.join(ASSETS, "hurt.wav"))
die_sfx = pygame.mixer.Sound(os.path.join(ASSETS, "die.wav"))

# === Game State Variables ===
score = 0
game_active = False
game_over = False
start_menu_shown = False
current_death_screen = None

# === Spider Enemy Class ===
class Spider:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLATFORM_W, PLATFORM_H)  # Position and size
        self.images = [spider_img, spider_flip]                # Animation frames
        self.current = 0                                       # Current frame index
        self.last_switch = pygame.time.get_ticks()             # Last animation switch
        self.interval = random.randint(3000, 5000)             # Time between switches

    def draw(self):
        screen.blit(self.images[self.current], self.rect.topleft)  # Draw spider

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_switch > self.interval:  # Time to switch image
            self.current ^= 1                       # Flip between 0 and 1
            self.last_switch = now
            self.interval = random.randint(3000, 5000)

    def move(self, dy):
        self.rect.y += dy  # Move spider vertically

    def reposition_above(self, platform):
        self.rect.topleft = (platform.draw_rect.x, platform.draw_rect.y - PLATFORM_H)

# === Platform Class ===
class Platform:
    def __init__(self, x, y, has_spider=True):
        self.draw_rect = pygame.Rect(x, y, PLATFORM_W, PLATFORM_H)  # Visual platform
        self.rect = pygame.Rect(x + 10, y + PLATFORM_H // 2, PLATFORM_W - 20, 4)  # Collision zone
        self.spider = Spider(x, y - PLATFORM_H) if has_spider else None  # Optional spider

    def draw(self):
        screen.blit(plat_img, self.draw_rect.topleft)
        if self.spider:
            self.spider.update()
            self.spider.draw()

    def move(self, dy):
        self.draw_rect.y += dy
        self.rect.y += dy
        if self.spider:
            self.spider.move(dy)

    def recycle(self):
        # Move platform back to top with new random position
        new_x = random.randint(0, WIDTH - PLATFORM_W)
        new_y = random.randint(-120, -40)
        self.draw_rect.topleft = (new_x, new_y)
        self.rect.topleft = (new_x + 10, new_y + PLATFORM_H // 4)
        # Random chance to spawn spider
        if random.random() < 0.08:
            if not self.spider:
                self.spider = Spider(new_x, new_y - PLATFORM_H)
            else:
                self.spider.reposition_above(self)
        else:
            self.spider = None

# === Player Class ===
class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2, HEIGHT-80, PLAYER_W, PLAYER_H)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.disabled = False
        self.facing_right = True
        self.image = player_right

    def move(self):
        global score, game_active, game_over, current_death_screen
        self.vy += GRAVITY
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Check for spider collision
        for plat in platforms:
            if plat.spider and self.rect.colliderect(plat.spider.rect):
                hurt_sfx.play()
                self.vy = max(0, self.vy)
                self.disabled = True

        # Check for platform landing
        if not self.disabled:
            self.on_ground = False
            for plat in platforms:
                if self.rect.colliderect(plat.rect) and self.vy >= 0:
                    self.rect.bottom = plat.rect.top
                    self.vy = 0
                    self.on_ground = True

        # Scroll screen upward if player climbs
        if self.rect.top < HEIGHT//3:
            dy = HEIGHT//3 - self.rect.top
            self.rect.top += dy
            for plat in platforms:
                plat.move(dy)
                if plat.draw_rect.top > HEIGHT:
                    plat.recycle()
            score += int(dy)

        # Check for falling off screen
        if self.rect.bottom > HEIGHT:
            die_sfx.play()
            game_active = False
            game_over = True
            score = 0
            current_death_screen = random.choice(death_screens)

        self.update_image()

    def jump(self):
        if self.on_ground:
            self.vy = JUMP_VEL
            jump_sfx.play()

    def set_dir(self, d):
        self.vx = d * MOVE_SPEED
        if d != 0:
            self.facing_right = d > 0

    def update_image(self):
        # Choose sprite based on movement direction and velocity
        if self.vy < -1:
            self.image = player_jump_right if self.facing_right else player_jump_left
        elif self.vy > 1:
            self.image = player_fall_right if self.facing_right else player_fall_left
        else:
            self.image = player_right if self.facing_right else player_left

# === Platform Generator ===
def generate():
    plats = []
    spacing = HEIGHT // NUM_PLATFORMS
    for i in range(NUM_PLATFORMS):
        x = random.randint(0, WIDTH - PLATFORM_W)
        y = HEIGHT - (i + 1) * spacing
        has_spider = i != 0 and random.random() < 0.08
        plat = Platform(x, y, has_spider)
        plats.append(plat)
        if i == 0:
            player.rect.midbottom = plat.rect.midtop  # Start player on bottom platform
    return plats

# === Game Setup ===
player = Player()
platforms = generate()

# === Main Game Loop ===
running = True
while running:
    # Show start menu first
    if not start_menu_shown:
        screen.blit(start_menu_img, (0, 0))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_s:
                game_active = True
                start_menu_shown = True
                player = Player()
                platforms = generate()
        continue

    # Show death screen or restart menu
    if not game_active:
        if game_over and current_death_screen:
            screen.blit(current_death_screen, (0, 0))
        else:
            screen.blit(start_menu_img, (0, 0))  # Show start menu again if not game over
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_s:
                # Restart game
                game_active = True
                game_over = False
                player = Player()
                platforms = generate()
        continue

    # === Active Gameplay ===
    screen.blit(bg_img, (0, 0))  # Draw background

    # Handle input events
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w: player.jump()       # Jump
            elif e.key == pygame.K_a: player.set_dir(-1) # Move left
            elif e.key == pygame.K_d: player.set_dir(1)  # Move right
        elif e.type == pygame.KEYUP:
            if e.key in [pygame.K_a, pygame.K_d]: player.set_dir(0)  # Stop moving

    # Update player and platforms
    player.move()
    for plat in platforms:
        plat.draw()

    # Draw player and score
    screen.blit(player.image, player.rect.topleft)
    screen.blit(font.render(f"Score: {score}", True, (0, 0, 0)), (10, 10))

    # Refresh display and control frame rate
    pygame.display.flip()
    clock.tick(50)

# === Exit Game ===
pygame.quit()
