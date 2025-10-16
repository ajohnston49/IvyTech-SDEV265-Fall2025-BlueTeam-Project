import tkinter as tk
import random
from PIL import Image, ImageTk
import os
import pygame

 


#-------Get The Folder----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR,"assets")



#-------Setup Main Game Window-------
window = tk.Tk()
window.title("David and Golaith")
WIDTH = 695
HEIGHT = 420
# Create canvas where game object will be drawn
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT)
canvas.pack()

#Sound system
pygame.init() #Initialize the pygame sound system
pygame.mixer.init()

#load background music
background_music = os.path.join(ASSETS_DIR, "gameplay_music.mp3")
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1) #loops forever

#Load sound effects
attack_sound_1 = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "attack1.wav")) #Slingshot release
attack_sound_2 = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "attack2.wav")) #hit sound

# Background Load resize Tile
bg_image = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "Groundtilebg.png"))
background = canvas.create_image (4,4, image=bg_image, anchor="nw")
window.bg_image = bg_image #Prevent garbage collection

# Menu Screen Assets
menu_bg_image = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "menu_background.png"))
play_button_image = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "play_button.png"))



#player positioned Right
david_image_right = tk.PhotoImage(file= os.path.join(ASSETS_DIR,"david_idle.png"))
david_walk1_right = tk.PhotoImage(file = os.path.join(ASSETS_DIR, "david_walk1.png"))

#Player Positoned Left
david_idle_left = tk.PhotoImage(file= os.path.join(ASSETS_DIR, "david_idle_left.png"))
david_walk1_left = tk.PhotoImage(file = os.path.join(ASSETS_DIR,"david_walk1_left.png"))

#David attack sprites
david_attack_image = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "david_attack.png"))
david_attack_left_image = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "david_attack_left.png"))

#david attack2 sprite 2
david_attack_image2 = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "david_attack2.png"))
david_attack_left_image2 = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "david_attack2_left.png"))

#Stone Icon and UI
stone_image = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "stone_icon.png"))
stone_icon = canvas.create_image(620, 20, image=stone_image) #adjust x/y to place top-right
stone_text = canvas.create_text (650, 20, text="10", font=("Arial", 17, "bold"), fill="black") #next to icon

#Win and lose Screens
win_image = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "win_screen.png"))
lose_image = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "lose_screen.png"))

#Stone Count
MAX_STONES = 10
stone_count = MAX_STONES


#put in a list of animation
david_facing_right = True
david_frames_right = [david_image_right, david_walk1_right]
david_frames_left = [david_idle_left, david_walk1_left]
david_frame_index = 0
david_animation_counter = 0

#start with idle frame
david = canvas.create_image(250, 365, image = david_image_right)

#Get David Image dimension for accurate collusion and bounds
david_width = david_image_right.width()
david_height = david_image_right.height()

#Enemy
goliath_image = tk.PhotoImage(file= os.path.join(ASSETS_DIR,"Goliath_walk1_left.png"))
goliath_walk = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "Goliath_walk2_left.png"))
goliath_walk1 = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "Goliath_walk1.png"))
goliath_walk2 = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "Goliath_walk2.png"))

#HealthBar Images
goliath_health_image = [tk.PhotoImage(file=os.path.join(ASSETS_DIR, f"health{i}.png")) for i in range (1, 7)]


#Put them into a list of animation
goliath_frames = [ goliath_walk1, goliath_walk2]
goliath_frame_index = 0 
goliath_animation_counter = 0

#Count the images you have (used for scaling health)
HEALTH_IMAGE_COUNT = len (goliath_health_image)

#start with idle
goliath = canvas.create_image(250, 75, image = goliath_image)

#Goliath HealthBar on Canvas
global goliath_health_bar
goliath_health_bar = canvas.create_image( 100, 20, image=goliath_health_image[HEALTH_IMAGE_COUNT -1] ) # you can change (250, 40) to plave it higher or lower
canvas.create_text(180, 20, text="HEALTH", font=("Arial", 17, "bold"), fill="black", anchor="w")


#Get Goliath Image dimension for accurate collusion and bounds
goliath_width = goliath_image.width()
goliath_height = goliath_image.height()

# Soldier sprites
soldier_idle_right = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "soldier_idle_right.png"))
soldier_idle_left = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "soldier_idle_left.png"))
soldier_walk_right = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "soldier_walk_right.png"))
soldier_walk_left = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "soldier_walk_left.png"))
soldier_attack_right = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "soldier_attack_right.png"))
soldier_attack_left = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "soldier_attack_left.png"))


#-------Game Variable-------
stones = [] #List to track all the fires stones
david_speed = 0 #Left/right movement speed for David
goliath_direction = 1 #Goliath moves hortizontally 

#Health Sys
MAX_GOLIATH_HEALTH = 6 #You can change this anytime to make Goliath stronger or weaker
goliath_health = MAX_GOLIATH_HEALTH #Goliath starts at full health
soldiers = []  # List to store active soldiers


#-------Functions-------
def restart_game(): #Restart function for game
    global goliath_health, stones, david, goliath, goliath_health_bar, stone_count, stone_icon, stone_text
   
    pygame.mixer.music.play(-1)

    goliath_health= MAX_GOLIATH_HEALTH #Restart Goliath health to full
    stone_count= MAX_STONES
    stones.clear() #clear the list properly
    

    canvas.delete("all")



    bg_image = tk.PhotoImage(file=os.path.join(ASSETS_DIR, "Groundtilebg.png"))
    canvas.create_image(0,0, image=bg_image, anchor="nw")
    window.bg_image = bg_image

    #redraw all players
    david = canvas.create_image (250, 365, image=david_image_right)
    goliath = canvas.create_image (250, 75, image = goliath_image)

    #Redraw the goliath health bar
    goliath_health_bar = canvas.create_image (100, 20, image=goliath_health_image[HEALTH_IMAGE_COUNT -1])
    canvas.create_text(180, 20, text="HEALTH", font=("Arial", 17, "bold"), fill="black", anchor="w")

    #Redraw stone Ui
    global stone_icon, stone_text
    stone_icon = canvas.create_image(620, 20, image=stone_image)
    stone_text = canvas.create_text(650, 20, text = str(stone_count), font= ("Arial", 17, "bold"), fill="black")

    update_game()


def move_david():  #Move left and right based on the current speed
    global david_speed, david_frame_index, david_animation_counter, david_facing_right
    canvas.move(david, david_speed, 0)
    x,y = canvas.coords(david)

    #Prevent David from leaving screen

    if x - david_width // 2 < 0:
        canvas.move(david, -(x - david_width //2), 0)
    elif x + david_width //2 > WIDTH:
        canvas.move(david, WIDTH -(x + david_width // 2), 0)


#Handle facing direction
    if david_speed > 0: #Moving right
        david_facing_right = True
    elif david_speed < 0: #Moving Left
        david_facing_right = False

    #Animation Handling
    if david_speed != 0:
        david_animation_counter +=1
        if david_animation_counter % 3 ==0: #Change every 3 ticks
            david_frame_index = (david_frame_index + 1) % 2 # toggle bewteen 0 and 1

    #Choosing the correct set
            if david_facing_right:
                canvas.itemconfig(david, image = david_frames_right[david_frame_index])
            else:
                canvas.itemconfig(david, image=david_frames_left[david_frame_index])



#-------Fire a stone upward from David's position-------

def shoot_stone(event = None):
    global stone_count

    if stone_count <= 0:
        return #Dont shhot if no stones left
    

    #Play slingshot release sound
    attack_sound_1.play()



    x,y = canvas.coords(david)
    stone = canvas.create_oval(x-5, y-20, x+5, y-10, fill = "grey")
    stones.append(stone)

    #Decrease stone count and update text
    stone_count -= 1
    canvas.itemconfig(stone_text, text=str(stone_count))


    #STAGE 1: Play attack2 sprite
    if david_facing_right:
        canvas.itemconfig(david, image=david_attack_image2)
    else:
        canvas.itemconfig(david, image=david_attack_left_image2)
    
    #STAGE 2: After 150ms play attack1
    def play_attack1():
        if david_facing_right:
            canvas.itemconfig(david, image=david_attack_image)
        else:
            canvas.itemconfig(david, image=david_attack_left_image)

    window.after(200, play_attack1) #Delay before switching to attack1




    #Revert back to idle image after short delay
    def reset_to_idle():
        if david_facing_right:
            canvas.itemconfig(david, image=david_frames_right[0]) #idle right
        else:
            canvas.itemconfig(david, image=david_frames_left[0]) #idle left

    window.after(300, reset_to_idle) #show attack image for 200ms


#Move all stones upward, check for off-screen or collision with Goliath
def move_stones():
    global goliath_health
    for stone in stones [:]: # Copy the list to aviod modifying while iterating 
        canvas.move(stone, 0, -10)
        x1,y1,x2,y2, = canvas.coords(stone)


#Remove stone if it goes off screen
        if y2 < 0:
            canvas.delete(stone)
            stones.remove(stone)
            continue

#Get Goliath center position and calculate bounding box
        gx, gy = canvas.coords(goliath)
        gx1 = gx - goliath_width // 2
        gx2 = gx + goliath_width // 2
        gy1 = gy - goliath_height // 2
        gy2 = gy + goliath_height // 2

        # Check for collision with soldiers
        hit_soldier = False
        for soldier in soldiers:
            sx1, sy1, sx2, sy2 = soldier.get_bbox()
            if sx1 < x1 < sx2 and sy1 < y1 < sy2:
                canvas.delete(stone)
                stones.remove(stone)
                hit_soldier = True
                break  # Stop checking after one hit

        if hit_soldier:
            continue  # Skip Goliath check if soldier blocked it
    

        #Check if stone hits Goliath
        if gx1 < x1 < gx2 and gy1 < y1 < gy2:
            attack_sound_2.play() #play sound when stone collides with Goliath
            goliath_health -= 1 #Reduce Goliath Health by 1
            canvas.delete(stone) #Remove the stone
            stones.remove(stone)

            #Stop health so it wont go below zero
            goliath_health = max (0, goliath_health)

            #-------HEALTH BAR UPDATE

            #Convert current health to a value between 0 and (HEALTH_IMAGE_COUNT-1)
            #This lets any number of health points work with a fixed number of images
            ratio = goliath_health / MAX_GOLIATH_HEALTH
            health_index = int(ratio * (HEALTH_IMAGE_COUNT -1)) 

            #Prevent health index from going out of range (0 to max index)
            health_index = max (0, min(HEALTH_IMAGE_COUNT -1, health_index))
                               

            #update the health bar image
            canvas.itemconfig(goliath_health_bar, image=goliath_health_image[health_index])

            #Print Goliath Health
            print(f"Goliath health: {goliath_health} | health bar index: {health_index}")

            #If Goliath has no health left, display win message
            if goliath_health <= 0: #health bar
                canvas.create_text(WIDTH // 2, HEIGHT // 2, text = "David! Wins!", font = ("Ariel", 24), fill = "black")

                #Create restart button
                restart_btn = tk.Button(window, text = "Play Again", font= ("Arial", 14), command = restart_game)
                canvas.create_window (WIDTH // 2, HEIGHT //2 + 40, window = restart_btn)
                return

#Move goliath back and forth on screen (((YOU ARE HERE)))
def move_goliath():
    global goliath_direction, goliath_frame_index, goliath_animation_counter, goliath_frames


    #Move left and right
    move_amount = goliath_direction * 6
    canvas.move(goliath, move_amount, 0)
    
    gx, gy = canvas.coords(goliath)

    #Small movement range in middle of screen

    left_limit = WIDTH // 2 - 100
    right_limit = WIDTH // 2 + 100


   # Change direction and frames at limits
    if gx <= left_limit:
        goliath_direction = 1
        goliath_frames = [goliath_walk1, goliath_walk2]  # Facing right
        goliath_frame_index = 0
    elif gx >= right_limit:
        goliath_direction = -1
        goliath_frames = [goliath_image, goliath_walk]  # Facing left
        goliath_frame_index = 0
    

    #animation handling
    goliath_animation_counter += 1
    if goliath_animation_counter % 5 == 0: #change frame every 10 ticks
        goliath_frame_index = (goliath_frame_index + 1) % len(goliath_frames)
        canvas.itemconfig(goliath, image=goliath_frames[goliath_frame_index])


class Soldier:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # 1 for right, -1 for left
        self.frame_index = 0
        self.animation_counter = 0

        if direction == 1:
            self.frames = [soldier_idle_right, soldier_walk_right]
        else:
            self.frames = [soldier_idle_left, soldier_walk_left]

        self.image = canvas.create_image(x, y, image=self.frames[0])
        self.width = self.frames[0].width()
        self.height = self.frames[0].height()

    def move(self):
        self.x += self.direction * 2
        canvas.move(self.image, self.direction * 2, 0)

        # Animate
        self.animation_counter += 1
        if self.animation_counter % 8 == 0:
            self.frame_index = (self.frame_index + 1) % 2
            canvas.itemconfig(self.image, image=self.frames[self.frame_index])

    def get_bbox(self):
        return (
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.x + self.width // 2,
            self.y + self.height // 2,
        )

    def destroy(self):
        canvas.delete(self.image)

def spawn_soldier():
    if len(soldiers) < 3:  # Limit number of soldiers on screen
        x = random.randint(100, 600)
        direction = random.choice([-1, 1])
        y = 260  # Between David and Goliath
        soldier = Soldier(x, y, direction)
        soldiers.append(soldier)

def start_game():
    canvas.delete("all")  # Clear menu
    pygame.mixer.music.play(-1)  # Restart background music
    restart_game()  # Start the game loop



#Main game loop: Update all movements
def update_game():
    move_david()
    move_goliath()
    move_stones()

     # Move all soldiers
    for soldier in soldiers:
        soldier.move()

    # Occasionally spawn new soldier
    if random.randint(1, 50) == 1:  # Adjust spawn rate here
        spawn_soldier()

     # Remove off-screen soldiers
    for soldier in soldiers[:]:
        if soldier.x < -50 or soldier.x > WIDTH + 50:
            soldier.destroy()
            soldiers.remove(soldier)


    if goliath_health <= 0: # Keep running until goliath defeated
        show_win_screen()
        return
    elif stone_count <=0 and goliath_health > 0:
        show_lose_screen()
        return
   
    window.after (50, update_game) #Repeat after 50 ms


#-----------Key Bindings------------

#Detect when keys are passed
def key_press(event):
    global david_speed
    if event.keysym == "Left":
        david_speed = -10
    elif event.keysym == "Right":
        david_speed = 10

# Stop movement when keys are released
def key_release(event):
    global david_speed
    if event.keysym in ("Left","Right"):
        david_speed = 0

def show_menu():
    canvas.delete("all")  # Clear everything

    # Show the menu background
    canvas.create_image(WIDTH // 2, HEIGHT // 2, image=menu_bg_image)

    # Create the play button on top of the background
    play_button = tk.Button(
        window,
        image=play_button_image,
        command=start_game,
        borderwidth=0,
        highlightthickness=0,
        bg="orange",  # Match menu or make transparent
        activebackground="orange"  # Match on hover
    )

    # Place it centered below the title
    canvas.create_window(WIDTH // 2, HEIGHT // 2 + 70, window=play_button)


#Add win and lose screen functions
def show_win_screen():
    canvas.delete("all")
    canvas.create_image(WIDTH // 2, HEIGHT // 2, image=win_image)
    restart_btn = tk.Button(window, text="Play Again", font=("Arial, 14"), command=restart_game)
    canvas.create_window(WIDTH //2, HEIGHT // 2 + 100, window=restart_btn)

def show_lose_screen():
    canvas.delete("all")
    canvas.create_image(WIDTH // 2, HEIGHT // 2, image=lose_image)
    restart_btn = tk.Button(window, text="Play Again", font=("Arial, 14"), command=restart_game)
    canvas.create_window(WIDTH //2, HEIGHT // 2 + 100, window=restart_btn)




#Bind keys to movement and shooting
window.bind("<KeyPress>", key_press)
window.bind("<KeyRelease>", key_release)
window.bind("<space>",shoot_stone)






# ------- Start the Game -------
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  # loops forever

# update_game()
show_menu()  # Show menu instead of jumping right into game
window.mainloop()
