# I - Import and Initialize
import pygame, sys, sprites

pygame.init()
pygame.mixer.init()
sprites.load_assets()

def main():
    # In initializing section, and not assign section
    # because player speed is needed to create enemy sprites

    # The speed of the player relative to the Earth (needs to be a global variable)
    player_speed = 10 

    # D - Display configuration
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Sky Dodgers")

    # E - Entities

    #### Setup joysticks

    joysticks = []

    for joystick_no in range(pygame.joystick.get_count()):
        j = pygame.joystick.Joystick(joystick_no)
        j.init()
        joysticks.append(j)

    #### Background
    background = pygame.image.load("bg.jpg")
    background = pygame.transform.scale(background, screen.get_size())
    canvas = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    ##### Variables for moving background
    bg_x1 = 0 # First background location
    bg_x2 = screen.get_width() # 2nd b.g. location

    #### Player object

    player = sprites.Player(screen)

    #### Score and health tracking objects

    score = sprites.ScoreKeeper(screen)
    health = sprites.Health(screen)

    #### Enemy and Heart objects

    ##### Initialize enemy frame and their sprites, as well as lists / groups to hold them

    enemy_sprites = pygame.sprite.Group()
    hearts = pygame.sprite.Group()

    enemy_frame = sprites.EnemyFrame(screen, player_speed)
    enemy_frame.init_sprites()

    enemy_frame_next = sprites.EnemyFrame(screen, player_speed, True)
    enemy_frame_next.init_sprites()

    ##### Add sprites to lists or groups

    enemy_sprites.add(enemy_frame.get_enemy_sprites(), enemy_frame_next.get_enemy_sprites())
    hearts.add(enemy_frame.get_hearts(), enemy_frame_next.get_hearts())

    #### Sprite groups

    all_sprites = pygame.sprite.Group(player, score, health, enemy_frame, enemy_frame_next)

    #### Background Music
    pygame.mixer.music.load("bgmusic.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # A - Action (broken into ALTER steps)

    # A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    # Score counter
    score_clock = 0

    # L - Loop
    while keepGoing:
        # T - Timer to set frame rate
        clock.tick(30)
        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 1:
                    player.move(event.value)
        
        ### Keyboard input (only functional if no joysticks are plugged in)

        if len(joysticks) <= 0:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.move(-1)
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.move(1)
            # elif keys[pygame.K_1]:
                # player.blow_up()
            else:
                player.move(0)
        
        ### Keep track of how much time passed. Update score after every second (30 frames)
        if score_clock >= 30:
            score.score()
            score_clock = 0
        
        score_clock += 1

        ### Change location of moving backgrounds
        bg_x1 -= player_speed
        bg_x2 -= player_speed
        #### Move background back to the end when it goes off the left end of the screen
        if bg_x1 < -screen.get_width():
            bg_x1 = screen.get_width()
        if bg_x2 < -screen.get_width():
            bg_x2 = screen.get_width()
        
        ### Keep track of enemy frames and spawning

        #### Reposition enemy frames when it goes off left end of screen

        if enemy_frame.rect.left < -screen.get_width():
            # Re-position
            enemy_frame.rect.left = screen.get_width()
            # Remove old sprites
            enemy_sprites.remove(enemy_frame.get_enemy_sprites())
            hearts.remove(enemy_frame.get_hearts())
            enemy_frame.clear_sprites()
            # Reinitialize sprites
            enemy_frame.init_sprites()
            enemy_sprites.add(enemy_frame.get_enemy_sprites())
            hearts.add(enemy_frame.get_hearts())
        
        if enemy_frame_next.rect.left < -screen.get_width():
            # Re-position
            enemy_frame_next.rect.left = screen.get_width()
            # Remove old sprites
            enemy_sprites.remove(enemy_frame_next.get_enemy_sprites())
            hearts.remove(enemy_frame_next.get_hearts())
            enemy_frame_next.clear_sprites()
            # Reinitialize sprites
            enemy_frame_next.init_sprites()
            enemy_sprites.add(enemy_frame_next.get_enemy_sprites())
            hearts.add(enemy_frame_next.get_hearts())

        # R - Refresh display
        screen.blit(background, (bg_x1, 0))
        screen.blit(background, (bg_x2, 0))
        screen.blit(canvas, (0, 0))

        hearts.clear(screen, canvas)
        enemy_sprites.clear(screen, canvas)
        all_sprites.clear(screen, canvas)

        hearts.update()
        enemy_sprites.update()
        all_sprites.update()

        hearts.draw(screen)
        enemy_sprites.draw(screen)
        all_sprites.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()