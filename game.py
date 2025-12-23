"""
Name: Adore S.
Date: 5 Jan. 2026
Game: Sky Dodgers
Desc: The actual game component of my game.
        The game involves moving a fighter jet up and down and trying to avoid hitting mines and other enemy planes.
        The game is played for as long as you have health.
"""

# I - Import and Initialize
import pygame, sys, os, sprites

pygame.init()
pygame.mixer.init()
sprites.load_assets()

def main():
    ## player_speed is in initializing section, and not assign section
    ## because player_speed is needed to create enemy sprites

    ## The speed of the player relative to the Earth (needs to be a global variable)
    player_speed = 10

    # D - Display configuration
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Sky Dodgers")

    # E - Entities

    ## Setup joysticks

    joysticks = []

    for joystick_no in range(pygame.joystick.get_count()):
        j = pygame.joystick.Joystick(joystick_no)
        j.init()
        joysticks.append(j)

    ## Background

    background = pygame.image.load("bg.jpg") # Load background
    ### Resize background to have same dimensions as screen
    background = pygame.transform.scale(background, screen.get_size())
    ### Create a transparent "canvas" above the background, where the rest of the game elements will be drawn
    canvas = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    ### Initialize variables to keep track of a moving background (2 images moving and repositioning)
    bg_x1 = 0 # First background location
    bg_x2 = screen.get_width() # 2nd b.g. location

    ## Game sprites

    ### Player object
    player = sprites.Player(screen)

    ### Score and health tracking objects
    score = sprites.ScoreKeeper(screen)
    health = sprites.Health(screen)

    ### Enemy and Heart objects

    #### Initialize sprite groups to hold enemy sprites and hearts
    enemy_sprites = pygame.sprite.Group()
    hearts = pygame.sprite.Group()

    #### Initalize 2 moving enemy sprites and fill them initially with appropriate enemy sprites and hearts.
    enemy_frame = sprites.EnemyFrame(screen, player_speed)
    enemy_frame.init_sprites(1) # Init. w/ level 1

    enemy_frame_next = sprites.EnemyFrame(screen, player_speed, True)
    enemy_frame_next.init_sprites(1) # Init. w/ level 1

    #### Add sprites to lists or groups
    enemy_sprites.add(enemy_frame.get_enemy_sprites(), enemy_frame_next.get_enemy_sprites())
    hearts.add(enemy_frame.get_hearts(), enemy_frame_next.get_hearts())

    ### Sprite group to hold all other sprites (excl. enemy sprites and hearts)

    all_sprites = pygame.sprite.Group(player, score, health, enemy_frame, enemy_frame_next)

    ## Load and Play: Background Music

    pygame.mixer.music.load("bgmusic.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    ## Game over screen (elements)

    ### Create the background
    game_over_bg = pygame.Surface(screen.get_size())
    game_over_bg.fill("#550000") # fill w/ maroon color

    ### Text saying "GAME OVER!"
    game_over_txt = sprites.Label("GAME OVER!", (screen.get_width() // 2, 70), 60, "yellow")

    ### Pair of labels showing the score the player reached before dying
    go_score_label = sprites.Label("SCORE", (screen.get_width() // 2, 160), 30)
    go_score_display = sprites.Label("100", (screen.get_width() // 2, 225), 60)

    ### Pair of labels showing the highest achieved score
    go_hi_score_label = sprites.Label("HIGH SCORE", (screen.get_width() // 2, 315), 30)
    go_hi_score_display = sprites.Label("100", (screen.get_width() // 2, 380), 60)

    ### Put all "game over" elements in a group
    game_over_group = pygame.sprite.Group(game_over_txt, go_score_label, go_score_display, go_hi_score_label, go_hi_score_display)

    ## Pause screen (elements)

    ### Create the background
    pause_bg = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    pause_bg.fill((130, 200, 229, 50)) # fill w/ sky blue color, 50% opacity

    ### Create a pause icon
    pause_icon = sprites.Image("pause.png", (screen.get_width() // 2, screen.get_height() // 2))

    ### Put pause screen elements in a group
    pause_group = pygame.sprite.Group(pause_icon)

    # A - Action (broken into ALTER steps)

    # A - Assign values to key variables

    ## Basic game variables
    clock = pygame.time.Clock()
    keepGoing = True

    ## Score tracking

    ### Rate at which the score should increment, in seconds
    score_rate = 1 
    ### Keeps track of how much time has passed (in frames) until the time to score has reached
    score_clock = 0

    ## Level tracking; difficulty increases as level increases
    level = 1

    ## Track whether game is paused

    paused = False
    ### player_speed is set to 0 when game is paused. This variable ensures the game is resumed at the same speed.
    saved_player_speed = player_speed

    ## Game over tracking

    game_over = False
    ### How long to wait before showing game over screen?
    game_over_delay = 2 # in seconds
    ### Keeps track of time passed before game over screen needs to be shown
    game_over_clock = 0 # in frames

    ## High score tracking

    high_score = 0

    ### The high score is saved on a file. Retrieve high score if file exists and value is valid.

    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as score_file:
            try:
                high_score = int(score_file.readline())
            except ValueError:
                pass

    ### Track whether high score has been beaten

    hi_score_beat = False
    #### The rate at which a new high score in the game over screen should flash. (flash means change color between yellow and white)
    hi_score_flash_rate = 0.5 # in seconds
    #### Keeps track of time passed before high score color changes.
    hi_score_flash_clock = 0

    # L - Loop
    while keepGoing:
        # T - Timer to set frame rate
        clock.tick(30)
        # E - Event handling
        for event in pygame.event.get():
            ## Quit game if 'X' is clicked
            if event.type == pygame.QUIT:
                keepGoing = False
                pygame.quit()
                sys.exit()
            ## Player movement with joystick (left thumbstick)
            elif event.type == pygame.JOYAXISMOTION:
                ### Move player object up or down, depending on the left thumbstick input
                if event.axis == 1:
                    player.move(event.value)
            ## Toggle paused state if right key / button is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7: # START button on F310 controller
                    paused = not paused
        
        ## Player movement with keyboard (only functional if no joysticks are plugged in)

        if len(joysticks) <= 0: # No joysticks detected
            ### Keep track of all keys pressed
            keys = pygame.key.get_pressed()

            ### Move player up if W / up is pressed
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.move(-1)
            ### Move player down if S / down is pressed
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.move(1)
            ### Stop player if no key is pressed
            else:
                player.move(0)
        
        ## Keep track of how much time passed. Update score after right time has passed, as well as high score, if needed.

        ### If the score clock has reached the score rate
        if score_clock >= score_rate * 30:
            #### Add 1 to the player's score
            score.score()
            #### Reset the clock to zero
            score_clock = 0

            #### If the score has beat the high score
            if score.get_score() > high_score:
                ##### Update high score
                high_score = score.get_score()

                ##### Update high score file
                with open("highscore.txt", "w") as score_file:
                    score_file.write(str(high_score))
                
                ##### Let game know that high score has been beaten
                hi_score_beat = True
        
        ### Increment score clock 
        score_clock += 1

        ## Collision logic with sprites

        ### (a) With mine or enemy planes

        #### Get list of enemies player has collided with
        collided_enemies = pygame.sprite.spritecollide(player, enemy_sprites, False, pygame.sprite.collide_mask)

        #### If a collision has occured and the game is not over,
        if collided_enemies and not game_over:
            ##### For every enemy the player collided with,
            for enemy in collided_enemies:
                ###### Take damage from the collision. Check whether enemy is active to prevent double damage.
                if enemy.is_active():
                    health.take_damage()

                ###### Blow the enemy up. 
                enemy.blow_up() 
        
        ### (b) With hearts

        #### Get list of hearts player has collided with. Also make hearts disappear on collision.
        collided_hearts = pygame.sprite.spritecollide(player, hearts, True, pygame.sprite.collide_mask)

        #### If a collision has occured and the game is not over,
        if collided_hearts and not game_over:
            ##### For every heart the player collided with,
            for heart in collided_hearts:
                ###### Heal from the collision. Check whether heart is active to prevent double healing.
                if heart.is_active():
                    health.heal()
        
        ## Update level and speed after every 10 point interval, if game isn't over and isn't paused

        ### Move to level 2 when 10 pts. has been reached
        if score.get_score() == 10 and not game_over and not paused:
            level = 2
        ### Move to level 3 when 20 pts. has been reached
        elif score.get_score() == 20 and not game_over and not paused:
            level = 3
        ### Move to level 4 when 30 pts. has been reached
        #### Level is not updated here, since the 'level' variable only affects spawning patterns.
        elif score.get_score() == 30 and not game_over and not paused:
            #### Make player move faster through the skies
            player_speed = 15
            saved_player_speed = 15
            enemy_frame.set_speed(player_speed)
            enemy_frame_next.set_speed(player_speed)
        
        ## Moving background logic

        ### Change location of moving backgrounds, in accordance with player_speed
        bg_x1 -= player_speed
        bg_x2 -= player_speed
        ### Move background back to the end when it goes off the left end of the screen
        if bg_x1 < -screen.get_width():
            bg_x1 = screen.get_width()
        if bg_x2 < -screen.get_width():
            bg_x2 = screen.get_width()
        
        ## Keep track of enemy frames and spawning

        ### Reposition enemy frames when it goes off left end of screen

        #### Enemy Frame 1

        if enemy_frame.rect.left < -screen.get_width():
            ##### Re-position
            enemy_frame.rect.left = screen.get_width()
            ##### Remove old sprites
            enemy_sprites.remove(enemy_frame.get_enemy_sprites())
            hearts.remove(enemy_frame.get_hearts())
            enemy_frame.clear_sprites()
            ##### Reinitialize sprites with the appropriate level
            enemy_frame.init_sprites(level)
            enemy_sprites.add(enemy_frame.get_enemy_sprites())
            hearts.add(enemy_frame.get_hearts())

        #### Enemy Frame 2        

        if enemy_frame_next.rect.left < -screen.get_width():
            ##### Re-position
            enemy_frame_next.rect.left = screen.get_width()
            ##### Remove old sprites
            enemy_sprites.remove(enemy_frame_next.get_enemy_sprites())
            hearts.remove(enemy_frame_next.get_hearts())
            enemy_frame_next.clear_sprites()
            ##### Reinitialize sprites w/ the appropriate level
            enemy_frame_next.init_sprites(level)
            enemy_sprites.add(enemy_frame_next.get_enemy_sprites())
            hearts.add(enemy_frame_next.get_hearts())
        
        ## On pause, freeze the game (if game is not over)

        if paused and not game_over:
            ### Stop game movement
            player_speed = 0
            enemy_frame.set_speed(player_speed)
            enemy_frame_next.set_speed(player_speed)

            ### Freeze the player
            player.freeze()

            ### Stop score incrementation
            score.freeze()

            ### Recursively freeze all enemy sprites
            for sprite in enemy_sprites:
                sprite.freeze()
        
        ## Unfreeze game when unpaused (if game is not over)

        elif not game_over:
            ### Resume game movement
            player_speed = saved_player_speed
            enemy_frame.set_speed(player_speed)
            enemy_frame_next.set_speed(player_speed)

            ### Unfreeze the player
            player.unfreeze()

            ### Resume score incrementation
            score.unfreeze()

            ### Recursively unfreeze all enemy sprites
            for sprite in enemy_sprites:
                sprite.unfreeze()
         
        ## Game over logic

        ### Let game know game is over when health reaches zero
        if health.get_health() <= 0:
            game_over = True
        
        ### If game is over, stop the game
        if game_over:
            #### Blow the player up
            player.blow_up()

            #### Stop game movement
            player_speed = 0
            enemy_frame.set_speed(player_speed)
            enemy_frame_next.set_speed(player_speed)

            #### Stop score incrementation. Let scorekeeper know player is dead.
            score.player_died()

            #### Ensure the game cannot be paused when the game is over.
            paused = False

            #### Recursively freeze all enemy sprites (no need for hearts)
            for sprite in enemy_sprites:
                sprite.freeze()
            
            #### Set the text to score labels to show the appropriate scores in game over screen
            go_score_display.change_text(str(score.get_score()))
            go_hi_score_display.change_text(str(high_score))
            
            #### Increment a game over clock; it should reach a certain time before game over screen is reached
            game_over_clock += 1
        
        ### If high score is beaten, change high score text and make text flash

        if game_over and game_over_clock >= game_over_delay * 30 and hi_score_beat:
            #### Change high score text and start flash incrementation
            go_hi_score_label.change_text("NEW HIGH SCORE!")
            hi_score_flash_clock += 1

        #### If high score clock reaches flash rate, 
        if hi_score_flash_clock >= hi_score_flash_rate * 30:
            ##### Reset high score clock
            hi_score_flash_clock = 0

            ##### Change high score color to white if yellow
            if go_hi_score_label.get_color() == "yellow":
                go_hi_score_label.change_color("white")
                go_hi_score_display.change_color("white")
            ##### Otherwise, change it to yellow
            else:
                go_hi_score_label.change_color("yellow")
                go_hi_score_display.change_color("yellow")

        # R - Refresh display

        ## Blit background and canvas
        screen.blit(background, (bg_x1, 0))
        screen.blit(background, (bg_x2, 0))
        screen.blit(canvas, (0, 0))

        ## Remove "old" sprites
        hearts.clear(screen, canvas)
        enemy_sprites.clear(screen, canvas)
        all_sprites.clear(screen, canvas)

        ## Update sprites
        hearts.update()
        enemy_sprites.update()
        all_sprites.update()

        ## Draw new sprites
        hearts.draw(screen)
        enemy_sprites.draw(screen)
        all_sprites.draw(screen)

        ## Show pause screen if game is paused
        if paused:
            screen.blit(pause_bg, (0, 0))
            pause_group.clear(screen, pause_bg)
            pause_group.update()
            pause_group.draw(screen)

        ## Show game over screen after game is over and certain time has passed
        if game_over and game_over_clock >= game_over_delay * 30:
            screen.blit(game_over_bg, (0, 0))
            game_over_group.clear(screen, game_over_bg)
            game_over_group.update()
            game_over_group.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()