import pygame
from random import randint
import os
import sys

# Inisialisasi pygame
pygame.init()
pygame.mixer.init()

# Ukuran layar
WIDTH = 800
HEIGHT = 480
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hip-Hop Dance")

# Load image dari folder images/
def load_image(name):
    return pygame.image.load(os.path.join("images", name)).convert_alpha()

# Load musik
music = pygame.mixer.Sound("music/dance.wav")

# Simulasi Actor dari pgzero
class Actor:
    def __init__(self, image_name):
        self.set_image(image_name)
        self.pos = (0, 0)

    def set_image(self, name):
        self.image_name = name
        self.image = load_image(name + ".png")

    def draw(self):
        rect = self.image.get_rect(center=self.pos)
        screen.blit(self.image, rect)

# Simulasi keys
class Keys:
    UP = pygame.K_UP
    RIGHT = pygame.K_RIGHT
    DOWN = pygame.K_DOWN
    LEFT = pygame.K_LEFT
keys = Keys()

# Simulasi clock.schedule
scheduled_function = None
scheduled_time = 0

def schedule(func, delay):
    global scheduled_function, scheduled_time
    scheduled_function = func
    scheduled_time = pygame.time.get_ticks() + int(delay * 1000)

# Setup aktor
dancer = Actor("start")
dancer.pos = (CENTER_X + 5, CENTER_Y - 40)

up = Actor("up")
up.pos = (CENTER_X, CENTER_Y + 110)

right = Actor("right")
right.pos = (CENTER_X + 60, CENTER_Y + 170)

down = Actor("down")
down.pos = (CENTER_X, CENTER_Y + 230)

left = Actor("left")
left.pos = (CENTER_X - 60, CENTER_Y + 170)

# Variabel game
move_list = []
display_list = []
score = 0
current_move = 0
count = 4
dance_lenght = 4
say_dance = False
show_countdown = True
moves_complete = False
game_over = False

# Fungsi game
def reset_dancer():
    global game_over
    if not game_over:
        dancer.set_image("start")
        up.set_image("up")
        right.set_image("right")
        down.set_image("down")
        left.set_image("left")

def update_dancer(move):
    if move == 0:
        up.set_image("up-lit")
        dancer.set_image("dancer-up")
    elif move == 1:
        right.set_image("right-lit")
        dancer.set_image("dancer-right")
    elif move == 2:
        down.set_image("down-lit")
        dancer.set_image("dancer-down")
    else:
        left.set_image("left-lit")
        dancer.set_image("dancer-left")
    schedule(reset_dancer, 0.5)

def countdown():
    global count, show_countdown
    if count > 1:
        count -= 1
        schedule(countdown, 1)
    else:
        show_countdown = False
        display_moves()

def generate_moves():
    global move_list, display_list, count, say_dance, show_countdown
    count = 4
    move_list.clear()
    display_list.clear()
    say_dance = False
    for _ in range(dance_lenght):
        rand_move = randint(0, 3)
        move_list.append(rand_move)
        display_list.append(rand_move)
    show_countdown = True
    countdown()

def next_move():
    global current_move, moves_complete
    if current_move < dance_lenght - 1:
        current_move += 1
    else:
        moves_complete = True

def display_moves():
    global display_list, say_dance, show_countdown
    if display_list:
        this_move = display_list.pop(0)
        update_dancer(this_move)
        schedule(display_moves, 1)
    else:
        say_dance = True
        show_countdown = False

def handle_key(key):
    global score, game_over, move_list, current_move
    if not say_dance or game_over:
        return

    move = -1
    if key == keys.UP:
        move = 0
    elif key == keys.RIGHT:
        move = 1
    elif key == keys.DOWN:
        move = 2
    elif key == keys.LEFT:
        move = 3

    if move != -1:
        update_dancer(move)
        if move == move_list[current_move]:
            score += 1
            next_move()
        else:
            game_over = True
            music.stop()

# Mulai permainan
generate_moves()
music.play(-1)

# Loop utama pygame
clock = pygame.time.Clock()
running = True

while running:
    now = pygame.time.get_ticks()
    if scheduled_function and now >= scheduled_time:
        f = scheduled_function
        scheduled_function = None
        f()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            handle_key(event.key)

    screen.fill((255, 255, 255))
    screen.blit(load_image("stage.png"), (0, 0))

    if not game_over:
        dancer.draw()
        up.draw()
        down.draw()
        left.draw()
        right.draw()

        font = pygame.font.SysFont(None, 40)
        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        if say_dance:
            big_font = pygame.font.SysFont(None, 60)
            dance_text = big_font.render("Dance!", True, (0, 0, 0))
            screen.blit(dance_text, (CENTER_X - 65, 35))

        if show_countdown:
            big_font = pygame.font.SysFont(None, 60)
            count_text = big_font.render(str(count), True, (0, 0, 0))
            screen.blit(count_text, (CENTER_X - 8, 150))

    else:
        font = pygame.font.SysFont(None, 60)
        screen.blit(font.render("Game Over!", True, (0, 0, 0)), (CENTER_X - 130, 180))
        screen.blit(font.render("Score: " + str(score), True, (0, 0, 0)), (CENTER_X - 100, 240))
    
    if moves_complete and not game_over:
        current_move = 0
        moves_complete = False
        generate_moves()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()