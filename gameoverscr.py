"""
Note: This file was only used as an aid to create the game over screen in game.py.

This file is not being used by the game in any shape or form.
"""

# I - Import and Initialize
import pygame, sys, sprites
pygame.init()

# D - Display configuration
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hello, World!")

# E - Entities

game_over_bg = pygame.Surface(screen.get_size())
game_over_bg.fill("#550000") # maroon color

game_over_txt = sprites.Label("GAME OVER!", (screen.get_width() // 2, 70), 60, "yellow")

score_label = sprites.Label("SCORE", (screen.get_width() // 2, 160), 30)
score_display = sprites.Label("100", (screen.get_width() // 2, 225), 60)

hi_score_label = sprites.Label("HIGH SCORE", (screen.get_width() // 2, 315), 30)
hi_score_display = sprites.Label("100", (screen.get_width() // 2, 380), 60)

game_over_group = pygame.sprite.Group(game_over_txt, score_label, score_display, hi_score_label, hi_score_display)

# A - Action (broken into ALTER steps)

# A - Assign values to key variables
clock = pygame.time.Clock()
keepGoing = True

# L - Loop
while keepGoing:
    # T - Timer to set frame rate
    clock.tick(30)
    # E - Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepGoing = False
            break
        # R - Refresh display
        screen.blit(game_over_bg, (0, 0))

        game_over_group.clear(screen, game_over_bg)
        game_over_group.update()
        game_over_group.draw(screen)

        pygame.display.flip()

pygame.quit()