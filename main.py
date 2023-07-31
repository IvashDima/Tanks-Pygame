import pygame
import os
import random
from modules.classes import *
from modules.mapsetting import map

pygame.init()  # initialize pygame modules

background = pygame.image.load(os.path.join(DIR_PATH, 'images/background.png'))
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.Font(None, 120)
winner1_text = font.render('BLUE WIN', True, (0,0,255))
winner2_text = font.render('RED WIN', True, (255,0,0))


sound_back = pygame.mixer.Sound(os.path.join(DIR_PATH, 'sounds', 'back.mp3'))
sound_dead = pygame.mixer.Sound(os.path.join(DIR_PATH, 'sounds', 'dead.mp3'))
sound_win = pygame.mixer.Sound(os.path.join(DIR_PATH, 'sounds', 'win.mp3'))

# blocks creation
x = 0
y = 0
block_list = []

wall_image1 = os.path.join(DIR_PATH, 'images/wall.png')
wall_image2 = os.path.join(DIR_PATH, 'images/wall1.png')

for row in map:
    for i in row:
        if i == 1:
            block_list.append(Block(x, y, 1, wall_image1))
        elif i == 2:
            block_list.append(Block(x, y, 2, wall_image2))
        x += STEP
    y += STEP
    x = 0

player1 = Player1(1, 1)
player2 = Player2(1, 3)
clock = pygame.time.Clock()

is_game_running = True
is_winner = False
#sound_back.play()
winner = None
while is_game_running:
    window.blit(background, (0, 0))
    # window.fill((255,0,0))  # all window red
    for block in block_list:
        block.blit()
        if block.colliderect(player1.bullet):
            player1.bullet.stop()
            if block.type_block == 1:
                map[block.y // STEP][block.x // STEP] = 0
                block.x = 1000000
        if block.colliderect(player2.bullet):
            player2.bullet.stop()
            if block.type_block == 1:
                map[block.y // STEP][block.x // STEP] = 0
                block.x = 1000000

    player1.bullet.move()
    player2.bullet.move()
    player1.blit()
    player2.blit()

    if player1.colliderect(player2.bullet):
        winner = 2
        is_game_running = False
        sound_back.stop()
        is_winner = True
        sound_dead.play(loops=0, maxtime=0, fade_ms=0)
    elif player2.colliderect(player1.bullet):
        winner = 1
        is_game_running = False
        sound_back.stop()
        is_winner = True
        sound_dead.play(loops=0, maxtime=0, fade_ms=0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game_running = False
    clock.tick(10)
    pygame.display.flip()  # clear all screen and write new. update - clear part of screen

cors = (SCREEN_WIDTH // 2 - winner1_text.get_width() // 2,
        SCREEN_HEIGHT // 2 - winner1_text.get_height() // 2)

while is_winner:
    window.blit(background, (0, 0))
    sound_win.play()
    if winner == 1:
        window.blit(winner1_text, cors)
    elif winner == 2:
        window.blit(winner2_text, cors)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_winner = False
            sound_win.stop()
    pygame.display.flip()