import pygame
import os
from random import randint

# === Setup ===
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HUNT THE DUCK")
clock = pygame.time.Clock()

# === Game States ===
GAME_STATE_TITLE = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2
GAME_STATE_WINNER = 3
current_game_state = GAME_STATE_TITLE

# === Asset Paths ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, "images")
SOUNDS_DIR = os.path.join(SCRIPT_DIR, "sounds")

# === Load Images ===
def load_image(name):
    path = os.path.join(IMAGES_DIR, name)
    try:
        return pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        print(f"Failed to load image '{name}': {e}")
        raise SystemExit

background = load_image("field.png")
duck_img = load_image("duckfly3.png")
duck2_img = load_image("duckfly4.png")
dead_duck_img = load_image("deadduck3.png")
sight_img = load_image("sight3.png")

# === Load Sounds ===
shoot_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "shoot.mp3"))
pygame.mixer.music.load(os.path.join(SOUNDS_DIR, "background.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop forever

# === Fonts ===
font_big = pygame.font.SysFont("Arial", 60)
font_med = pygame.font.SysFont("Arial", 30)
font_huge = pygame.font.SysFont("Arial", 90)

# === Duck Class ===
class Duck:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.vy = 0
        self.dead = False

    def draw(self):
        screen.blit(self.image, self.rect)

    def reset(self, x, y, image):
        self.image = image
        self.rect.center = (x, y)
        self.vy = 0
        self.dead = False

# === Game Objects ===
apple = Duck(duck_img, randint(10, 200), randint(300, 400))
duck2 = Duck(duck2_img, randint(480, 500), randint(300, 400))
duck2_active = False
sight_rect = sight_img.get_rect()

score = 0
game_over = False
GRAVITY = 0.5

# === Reset Functions ===
def reset_apple():
    apple.reset(randint(50, WIDTH - 50), randint(300, 400), duck_img)

def reset_duck2():
    duck2.reset(randint(480, 500), randint(300, 400), duck2_img)

# === Text Drawing Helper ===
def draw_text(text, font, color, center):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=center)
    screen.blit(surf, rect)

# === Main Game Loop ===
running = True
while running:
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()
    sight_rect.center = mouse_pos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and current_game_state == GAME_STATE_PLAYING and not game_over:
            shoot_sound.play()
            if apple.rect.collidepoint(mouse_pos):
                score += 1
                apple.dead = True
                apple.vy = 0
            elif duck2_active and duck2.rect.collidepoint(mouse_pos):
                score += 1
                duck2.dead = True
            else:
                current_game_state = GAME_STATE_GAME_OVER
                game_over = True

        elif event.type == pygame.KEYDOWN:
            if current_game_state == GAME_STATE_TITLE and event.key == pygame.K_SPACE:
                current_game_state = GAME_STATE_PLAYING
            elif current_game_state in [GAME_STATE_GAME_OVER, GAME_STATE_WINNER] and event.key == pygame.K_r:
                current_game_state = GAME_STATE_PLAYING
                game_over = False
                score = 0
                duck2_active = False
                reset_apple()
                reset_duck2()

    if current_game_state == GAME_STATE_TITLE:
        screen.fill((0, 100, 0))
        draw_text("Hunt The Duck!", font_huge, (255, 165, 0), (WIDTH // 2, HEIGHT // 3))
        draw_text("Press SPACE to Start", font_med, (255, 255, 255), (WIDTH // 2, HEIGHT // 1.5))

    elif current_game_state == GAME_STATE_PLAYING:
        screen.blit(background, (0, 0))
        draw_text(f"Score: {score}", font_med, (255, 255, 255), (70, 20))

        if not game_over:
            if not apple.dead:
                if 5 <= score <= 10:
                    apple.rect.x += 3
                    apple.rect.y -= 2
                elif 10 < score <= 15:
                    apple.rect.x += 4
                    apple.rect.y -= 3
                    duck2.rect.x -= 3
                    duck2.rect.y -= 2
                elif 15 < score <= 20:
                    apple.rect.x += 5
                    apple.rect.y -= 4
                    duck2.rect.x -= 4
                    duck2.rect.y -= 3
                elif 20 < score <= 25:
                    apple.rect.x += 6
                    apple.rect.y -= 5
                    duck2.rect.x -= 5
                    duck2.rect.y -= 4
                elif 25 < score <= 30:
                    apple.rect.x += 8
                    apple.rect.y -= 8
                    duck2.rect.x -= 8
                    duck2.rect.y -= 8
                else:
                    apple.rect.x += 2
                    apple.rect.y -= 1

                if apple.rect.left > WIDTH:
                    apple.rect.right = 0
                if apple.rect.top < 0:
                    reset_apple()
            else:
                apple.vy += GRAVITY
                apple.rect.y += apple.vy
                apple.image = dead_duck_img

            if duck2_active:
                if not duck2.dead:
                    if duck2.rect.right < 0:
                        duck2.rect.left = WIDTH
                    if duck2.rect.top < 0:
                        reset_duck2()
                else:
                    duck2.vy += GRAVITY
                    duck2.rect.y += duck2.vy
                    duck2.image = dead_duck_img

            if apple.rect.bottom > HEIGHT:
                reset_apple()
            if duck2.rect.bottom > HEIGHT:
                reset_duck2()

            if score >= 10 and not duck2_active:
                duck2_active = True
                reset_duck2()

            if score == 30:
                current_game_state = GAME_STATE_WINNER
                game_over = True

            apple.draw()
            if duck2_active:
                duck2.draw()

    elif current_game_state == GAME_STATE_GAME_OVER:
        screen.fill((0, 0, 0))
        draw_text("GAME OVER", font_big, (255, 0, 0), (WIDTH // 2, HEIGHT // 2 - 40))
        draw_text(f"Final Score: {score}", font_med, (255, 255, 255), (WIDTH // 2, HEIGHT // 2 + 10))
        draw_text("Hit 'R' to restart", font_med, (255, 255, 255), (WIDTH // 2, HEIGHT // 2 + 50))

    elif current_game_state == GAME_STATE_WINNER:
        screen.fill((0, 100, 0))
        draw_text("YOU WIN!!!", font_big, (255, 165, 0), (WIDTH // 2, HEIGHT // 2 - 40))
        draw_text(f"Final Score: {score}", font_med, (255, 255, 255), (WIDTH // 2, HEIGHT // 2 + 10))
        draw_text("Hit 'R' to restart", font_med, (255, 255, 255), (WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(sight_img, sight_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
