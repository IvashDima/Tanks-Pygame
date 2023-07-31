import pygame
import os

pygame.init()
DIR_PATH = os.path.abspath(__file__ + '/../..')
#PATH = os.path.join(DIR_PATH, 'sounds', 'strike.wav')
#sound_strike = pygame.mixer.Sound(PATH)
sound_strike = pygame.mixer.Sound(os.path.join(DIR_PATH, 'sounds', 'strike.wav'))
sound_strike.play()
# sound_strike.play(-1)
