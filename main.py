# I - Import and Initialize
import pygame, sys, os, sprites

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
    enemy_frame.init_sprites(1) # Init. w/ level 1

    enemy_frame_next = sprites.EnemyFrame(screen, player_speed, True)
    enemy_frame_next.init_sprites(1) # Init. w/ level 1

    ##### Add sprites to lists or groups

    enemy_sprites.add(enemy_frame.get_enemy_sprites(), enemy_frame_next.get_enemy_sprites())
    hearts.add(enemy_frame.get_hearts(), enemy_frame_next.get_hearts())

    #### Main game sprite groups (excl. enemies and hearts)

    all_sprites = pygame.sprite.Group(player, score, health, enemy_frame, enemy_frame_next)

    #### Background Music
    pygame.mixer.music.load("bgmusic.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    #### Game over screen

    game_over_bg = pygame.Surface(screen.get_size())
    game_over_bg.fill("#550000") # maroon color

    game_over_txt = sprites.Label("GAME OVER!", (screen.get_width() // 2, 70), 60, "yellow")

    go_score_label = sprites.Label("SCORE", (screen.get_width() // 2, 160), 30)
    go_score_display = sprites.Label("100", (screen.get_width() // 2, 225), 60)

    go_hi_score_label = sprites.Label("HIGH SCORE", (screen.get_width() // 2, 315), 30)
    go_hi_score_display = sprites.Label("100", (screen.get_width() // 2, 380), 60)

    game_over_group = pygame.sprite.Group(game_over_txt, go_score_label, go_score_display, go_hi_score_label, go_hi_score_display)

    # A - Action (broken into ALTER steps)

    # A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    ## Constants
    score_rate = 1 # sec
    ## Score counter
    score_clock = 0
    ## Level tracker
    level = 1
    ## Game over and clock
    game_over = False
    game_over_delay = 2 # sec
    game_over_clock = 0
    hi_score_flash_clock = 0

    # High score logic ---
    high_score = 0

    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as score_file:
            try:
                high_score = int(score_file.readline())
            except ValueError:
                pass

    hi_score_beat = False
    hi_score_flash_rate = 0.5 # sec

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
        ### Also update high score if necessary

        if score_clock >= score_rate * 30:
            score.score()
            score_clock = 0

            if score.get_score() > high_score:
                high_score = score.get_score()

                #### Update high score file

                with open("highscore.txt", "w") as score_file:
                    score_file.write(str(high_score))
                
                #### High score beaten

                hi_score_beat = True
        
        # Increment score clock
        
        score_clock += 1

        ### Collision logic with sprites

        #### With mine or enemy planes
        collided_enemies = pygame.sprite.spritecollide(player, enemy_sprites, False, pygame.sprite.collide_mask)

        if collided_enemies and not game_over:
            for enemy in collided_enemies:
                if enemy.is_active():
                    health.take_damage()
                
                enemy.blow_up() 
        
        #### With hearts
        collided_hearts = pygame.sprite.spritecollide(player, hearts, True, pygame.sprite.collide_mask)

        if collided_hearts and not game_over:
            for heart in collided_hearts:
                if heart.is_active():
                    health.heal()
        
        ### Update level and speed after every 10 points, assuming game isn't over

        if score.get_score() == 10 and not game_over:
            level = 2
        elif score.get_score() == 20 and not game_over:
            level = 3
        elif score.get_score() == 30 and not game_over:
            player_speed = 15
            enemy_frame.set_speed(player_speed)
            enemy_frame_next.set_speed(player_speed)

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
            enemy_frame.init_sprites(level)
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
            enemy_frame_next.init_sprites(level)
            enemy_sprites.add(enemy_frame_next.get_enemy_sprites())
            hearts.add(enemy_frame_next.get_hearts())
         
        ### Is the game over?

        if health.get_health() <= 0:
            game_over = True
        
        #### If game is over, stop the game

        if game_over:
            player.blow_up()
            player_speed = 0
            enemy_frame.set_speed(player_speed)
            enemy_frame_next.set_speed(player_speed)
            score.player_died()

            ### Recursively freeze all enemy sprites (no need for hearts)
            for sprite in enemy_sprites:
                sprite.freeze()
            
            #### Set the text for the scores in game over screen

            go_score_display.change_text(str(score.get_score()))
            go_hi_score_display.change_text(str(high_score))
            
            #### Increment a game over clock; it should reach a certain time before game over screen is reached
            game_over_clock += 1
        
        #### If high score is beaten, change high score text and make text flash

        if game_over and game_over_clock >= game_over_delay * 30 and hi_score_beat:
            go_hi_score_label.change_text("NEW HIGH SCORE!")
            hi_score_flash_clock += 1
        
        if hi_score_flash_clock >= hi_score_flash_rate * 30:
            hi_score_flash_clock = 0

            if go_hi_score_label.get_color() == "yellow":
                go_hi_score_label.change_color("white")
                go_hi_score_display.change_color("white")
            else:
                go_hi_score_label.change_color("yellow")
                go_hi_score_display.change_color("yellow")

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

        ### Show game over screen after game is over and certain time has passed

        if game_over and game_over_clock >= game_over_delay * 30:
            screen.blit(game_over_bg, (0, 0))
            game_over_group.clear(screen, game_over_bg)
            game_over_group.update()
            game_over_group.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()