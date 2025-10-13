import pgzrun
import pygame
from random import randint
import time
import os

# Set the environment variable to center the window
os.environ['SDL_VIDEO_CENTERED'] = '1'

WIDTH = 500
HEIGHT = 500

TITLE = "HUNT THE DUCK"

GAME_STATE_TITLE = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2
GAME_STATE_WINNER = 3
current_game_state = GAME_STATE_TITLE

background = Actor('field')
apple = Actor('duckfly3')
sight = Actor('sight3')
duck2 = Actor("duckfly4")
game_over = False
score = 0
duck2_active = False
apple.dead = False
duck2.dead = False
apple.vy = 0 # Vertical velocity
duck2.vy = 0
GRAVITY = 0.5 # Adjust this value for desired fall speed
pygame.mouse.set_visible(False)

def draw():
    global score
    screen.clear()

    if current_game_state == GAME_STATE_TITLE:
        screen.fill("darkgreen")
        screen.draw.text("Hunt The Duck!", center=(WIDTH // 2, HEIGHT // 3), fontsize=90, color="orange")
        screen.draw.text("Press SPACE to Start", center=(WIDTH // 2, HEIGHT // 1.5), fontsize=30, color="white")
    elif current_game_state == GAME_STATE_PLAYING:

        if not game_over:
            background.draw()
            screen.draw.text("Score is " + str(score), topleft=(10,10), fontsize=30)
            apple.draw()
            sight.draw()
            if duck2_active:
                duck2.draw()

        else:
            screen.draw.text("GAME OVER", (WIDTH // 2 - 100, HEIGHT // 2 - 20), color="red", fontsize=60)
            screen.draw.text(f"Final Score: {score}", (WIDTH // 2 - 80, HEIGHT // 2 + 30), color="white", fontsize=30)
            screen.draw.text("Hit 'R' to resart", (WIDTH // 2 - 80, HEIGHT // 2 + 60), color="white", fontsize=30)
    
    elif current_game_state == GAME_STATE_WINNER:
        screen.fill("darkgreen")
        screen.draw.text("YOU WIN!!!", (WIDTH // 2 - 100, HEIGHT // 2 - 20), color="orange", fontsize=60)
        screen.draw.text(f"Final Score: {score}", (WIDTH // 2 - 80, HEIGHT // 2 + 30), color="white", fontsize=30)
        screen.draw.text("Hit 'R' to resart", (WIDTH // 2 - 80, HEIGHT // 2 + 60), color="white", fontsize=30)

def update():
    sight.pos = pygame.mouse.get_pos()
    global score
    global duck2_active
    global current_game_state
    global game_over
    apple.x += 2
    apple.y -= 1

    if score == 30:
        current_game_state = GAME_STATE_WINNER
        game_over = True
      
    if score >= 10 and not duck2_active:
        place_duck2()
        duck2_active = True

    if duck2_active:
        duck2.x -= 2
        duck2.y -= 1

    if not apple.dead:
        if score >= 5 and score <=10:
            apple.x += 3
            apple.y -= 2
        elif score > 10 and score <= 15:
            apple.x += 4
            apple.y -= 3
            duck2.x -=3
            duck2.y -= 2
        elif score > 15 and score <=20:
            apple.x += 5
            apple.y -= 4
            duck2.x -= 4
            duck2.y -= 3
        elif score > 20 and score <=25:
            apple.x += 6
            apple.y -= 5
            duck2.x -= 5
            duck2.y -= 4
        elif score > 25 and score <=30:
            apple.x += 8
            apple.y -= 8
            duck2.x -= 8
            duck2.y -= 8


        if apple.left > WIDTH:
            apple.right = 0
        if apple.y < 0:
            reset_apple()

    else:
        apple.vy += GRAVITY
        apple.y += apple.vy
        apple.image = 'deadduck3'

    if not duck2.dead:
        if duck2.right < 0:
            duck2.left = WIDTH
        if duck2.y < 0:
            reset_duck2()

    else:
        duck2.vy += GRAVITY
        duck2.y += duck2.vy
        duck2.image = 'deadduck3'

    if apple.y > HEIGHT:
        reset_apple()
    if duck2.y > HEIGHT:
        reset_duck2()

def reset_apple():
    apple.x = randint(50, WIDTH - 50)
    apple.y = randint(300, 400)
    apple.y_velocity = 0
    apple.dead = False
    apple.image = 'duckfly3'

def reset_duck2():
    duck2.image = "duckfly4"
    duck2.x = randint(480, 500)
    duck2.y = randint(300, 400)
    duck2.y_velocity = 0
    duck2.dead = False

def place_apple():
    apple.image = 'duckfly3'
    apple.x = randint(10,200)
    apple.y = randint(300,400)

def place_duck2():
    duck2.image = "duckfly4"
    duck2.x = randint(480, 500)
    duck2.y = randint(300, 400)

def on_mouse_down(pos):
    global score
    global game_over
    if apple.collidepoint(pos):
        score += 1
        apple.dead = True
        apple.vy = 0
    elif duck2.collidepoint(pos):
        score += 1
        duck2.dead = True
    else:
        current_game_state = GAME_STATE_GAME_OVER
        game_over = True
        

def on_key_down(key):
    global current_game_state
    global game_over, score, duck2_active
    global apple, duck2

    if not game_over:
        if current_game_state == GAME_STATE_TITLE:
            if key == keys.SPACE:
                current_game_state = GAME_STATE_PLAYING
    else:
        if key == keys.R:
            current_game_state = GAME_STATE_PLAYING
            game_over = False
            score = 0
            duck2_active = False
            apple.dead = False
            duck2.dead = False
            apple.vy = 0
            duck2.vy = 0
            place_apple()
            #reset_duck2()

place_apple()

pgzrun.go()