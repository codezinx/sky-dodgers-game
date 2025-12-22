# I - Import and Initialize
import pygame, sys, sprites
import game

pygame.init()
pygame.mixer.init()
sprites.load_assets()

def main():
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

    ### Background
    main_menu_bg = pygame.Surface(screen.get_size())
    main_menu_bg.fill("#550000") # maroon color

    ### Main menu elements
    logo = sprites.Image("logo.png", (screen.get_width() // 2, 100))
    mm_start_txt = sprites.Label("PRESS SPACE TO PLAY", (screen.get_width() // 2, 240), 35)
    mm_controls = sprites.Image("controls_kb.png", (screen.get_width() // 2, 410))

    main_menu_group = pygame.sprite.Group(logo, mm_start_txt, mm_controls)

    ### Lobby music

    pygame.mixer.music.load("lobbymusic.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # A - Action (broken into ALTER steps)

    # A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    gameStarted = False

    # L - Loop
    while keepGoing:
        # T - Timer to set frame rate
        clock.tick(30)
        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                break
            # Start game when right key or button (controller) is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not gameStarted:
                    gameStarted = True
                    game.main()
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0 and not gameStarted:
                    gameStarted = True
                    game.main()
        
        ### Show the appropriate image depending on whether controller or keyboard is used

        if len(joysticks) > 0: 
            mm_start_txt.change_text("PRESS [A] TO PLAY") 
            mm_controls.change_image("controls_joy.png") 

        # R - Refresh display
        screen.blit(main_menu_bg, (0, 0))

        main_menu_group.clear(screen, main_menu_bg)
        main_menu_group.update()
        main_menu_group.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()