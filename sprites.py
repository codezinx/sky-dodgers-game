"""
Name: Adore S.
Date: 5 Jan. 2026
Game: Sky Dodgers
Desc: A seperate Python file that stores all the necessary sprites and their logic.
"""

import pygame
import random as rand
import os

# Assets cache

## Initialize assets cache
ASSETS = {}

## Load all the necessary assets (images, fonts, sounds) during initialization.
### Solves performance-related issues.

def load_assets():
    global ASSETS

    ASSETS["Player"] = pygame.image.load("player.png")
    ASSETS["explosion_img"] = pygame.image.load("explosion.png")
    ASSETS["Mine"] = pygame.image.load("mine.png")
    ASSETS["EnemyPlane"] = pygame.image.load("EnemyPlane.png")
    ASSETS["FastEnemyPlane"] = pygame.image.load("FastEnemyPlane.png")
    ASSETS["Heart"] = pygame.image.load("heart.png")
    ASSETS["Health"] = pygame.image.load("health.png")
    ASSETS["explosion_sfx"] = pygame.mixer.Sound("explosion.mp3")
    ASSETS["explosion_sfx"].set_volume(0.5)
    ASSETS["heal_sfx"] = pygame.mixer.Sound("heal.wav")
    ASSETS["font_score"] = pygame.font.Font("press_start.ttf", 40)
    ASSETS["font_health"] = pygame.font.Font("press_start.ttf", 30)

# Player class

class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        """Initialization"""
        super().__init__()

        # Setup image and pass through the screen

        self.image = ASSETS["Player"]
        self.__screen = screen

        # Setup bounding rectangle for positioning

        self.rect = self.image.get_rect()
        ## Place the player to the left of the screen, centered vertically
        self.rect.left = 20
        self.rect.centery = self.__screen.get_height() // 2

        # Setup mask for accurate collision detection

        self.mask = pygame.mask.from_surface(self.image)

        # Movement attributes

        ## Determines max. up / down movement speed
        self.__dodge_speed = 10
        ## Determines current speed
        self.__current_vy = 0
        # Explosion image and sound effects
        self.__explosion_img = ASSETS["explosion_img"]
        self.__explosion_sfx = ASSETS["explosion_sfx"]

        # State attributes

        ## Determines whether player can move or not
        self.__freeze = False
        ## Has player blown up?
        self.__blown_up = False
        ## Keeps track of when the player has been blown up
        self.__blow_up_time = 0
        ## Constant that tells us after how long should the player despawn after it has blown up
        self.__despawn_delay = 1000 # in ms
    
    def move(self, ratio):
        """Move function"""

        # Ensure "ratio", or how much of the maximum speed cannot go over 1
        # Think of "ratio" as the % of the max. speed div. by 100%
        # A negative value indicates the plane will go up

        if ratio < -1:
            ratio = -1
        elif ratio > 1:
            ratio = 1

        # Set the current speed to a % of the max. speed        
        self.__current_vy = self.__dodge_speed * ratio
    
    def out_of_bounds(self):
        """Keep track of whether plane is out of bounds or not"""

        # Out of bounds at the top?
        if self.rect.top < 0:
            return -1
        # Or out of bounds at the bottom?
        elif self.rect.bottom > self.__screen.get_height():
            return 1
        # Return 0 if not out of bounds
        else:
            return 0
    
    def blow_up(self):
        """Blow up the plane"""

        # Only blow up if the player hasn't already blown up
        if not self.__blown_up:
            ## Get the last position of the player
            last_pos = self.rect.center

            ## Change the image of the player to an explosion image
            self.image = self.__explosion_img
            ## Re-init the bounding rectangle, mask, and position the player to the right spot
            self.rect = self.image.get_rect()
            self.rect.center = last_pos
            self.mask = pygame.mask.from_surface(self.image)
            
            ## Play the explosion sound effect
            self.__explosion_sfx.play()

            ## Freeze the player and indicate player has blown up
            self.__freeze = True
            self.__blown_up = True

            ## Save the time player has blown up
            self.__blow_up_time = pygame.time.get_ticks()

    def update(self):
        """Update function"""

        # If player has blown up,
        if self.__blown_up:
            ## Get the current time
            now = pygame.time.get_ticks()

            ## If the time elapsed has met / exceeded the despawn delay time
            if now - self.__blow_up_time >= self.__despawn_delay:
                # Despawn player
                self.kill()

        # Prevent movement if frozen 
        if self.__freeze:
            return

        # Move the player in accordance with the current speed
        self.rect.centery += self.__current_vy

        # Keep plane within bounds
        ## Ensures plane cannot move outside of bounds
        if self.out_of_bounds() == -1:
            self.rect.top = 0
        elif self.out_of_bounds() == 1:
            self.rect.bottom = self.__screen.get_height()

    """Freeze and unfreeze functions""" 

    def freeze(self):
        self.__freeze = True
    
    def unfreeze(self):
        self.__freeze = False

# Labels and Images

## Class to store label tools

class LabelTools:
    def __init__(self):
        pass
    
    @staticmethod
    def show_outlined_text(font: pygame.font.Font, msg: str, outline_width: int = 1, text_color="white", outline_color="black"):
        """Label tool to render a text w/ an outline"""

        # Make text renders
        text = font.render(msg, True, text_color)
        outline = font.render(msg, True, outline_color)

        # Setup outlined text render surface
        w, h = text.get_width(), text.get_height()
        surf = pygame.Surface((w + outline_width * 2, h + outline_width * 2), pygame.SRCALPHA)

        # Render outline, (blit in all directions up to outline_width)
        for ox in range(-outline_width, outline_width + 1):
            for oy in range(-outline_width, outline_width + 1):
                # Skip the center (that's where the main text goes)
                if ox == 0 and oy == 0:
                    continue
                surf.blit(outline, (outline_width + ox, outline_width + oy))
        
        # Blit the text in the center
        surf.blit(text, (outline_width, outline_width))

        return surf

## A Label class (for main menu and game over screen)

class Label(pygame.sprite.Sprite):
    def __init__(self, msg, pos, font_size, color="white"):
        """Initializer"""

        super().__init__()
        # Store font
        self.__font = pygame.font.Font("press_start.ttf", font_size)
        # Store message
        self.__msg = msg
        # Store position and color
        self.__pos = pos
        self.__color = color
    
    def change_text(self, msg):
        """Change text of label"""
        if type(msg) == str:
            self.__msg = msg
    
    def get_color(self):
        """Get label color"""
        return self.__color
    
    def change_color(self, color):
        """Change label color"""
        self.__color = color
    
    def update(self):
        """Update function"""

        # Update label w/ appropriate info
        self.image = LabelTools.show_outlined_text(self.__font, self.__msg, text_color=self.__color)
        # Update bounding rectangle and position
        self.rect = self.image.get_rect()
        self.rect.center = self.__pos

## An Image class (makes it easier to render images in main menu, pause screen, and game over screen)

class Image(pygame.sprite.Sprite):
    def __init__(self, img_loc, pos):
        """Initializer"""

        super().__init__()
        # Store image location
        self.__img_loc = img_loc
        # Store image position
        self.__pos = pos 
    
    def change_image(self, new_loc):
        """Change image"""

        # Change image as long as image exists
        if os.path.exists(new_loc):
            self.__img_loc = new_loc
    
    def update(self):
        """Update function"""

        # Update image
        self.image = pygame.image.load(self.__img_loc)
        # Update bounding rectangle
        self.rect = self.image.get_rect()
        # Update position
        self.rect.center = self.__pos
    
# Tracking sprites

## Score-tracking sprite

class ScoreKeeper(pygame.sprite.Sprite):
    def __init__(self, screen):
        """Initalizer"""

        super().__init__()

        # Store font and passed in screen
        self.__screen = screen
        self.__font = ASSETS["font_score"]
        # Store position
        self.__position = (self.__screen.get_width() // 2, 35)
        # Keep track of score
        self.__score = 0
        # Indicators of whether player is alive or game is frozen
        self.__alive = True
        self.__freeze = False

    def score(self):
        """Score!"""

        # Add score if player is alive and game is not frozen
        if self.__alive and not self.__freeze:
            self.__score += 1
    
    def get_score(self):
        """Get score"""

        return self.__score
    
    def player_died(self):
        """Indicate that player has died"""

        self.__alive = False

    """Freeze and unfreeze functions"""

    def freeze(self):
        self.__freeze = True
    
    def unfreeze(self):
        self.__freeze = False
    
    def update(self):
        """Update function"""

        # Update the score label with the appropriate information 
        msg = str(self.__score)
        self.image = LabelTools.show_outlined_text(self.__font, msg)
        # Re-initialize bounding rectangle
        self.rect = self.image.get_rect()
        # Re-position score.
        self.rect.center = self.__position

## Health-tracking sprite

class Health(pygame.sprite.Sprite):
    def __init__(self, screen):
        """Initializer"""

        super().__init__()

        # Store font, heart image, label and screen
        self.__screen = screen
        self.__font = ASSETS["font_health"]
        self.__label = LabelTools.show_outlined_text(self.__font, "0")
        self.__heart = ASSETS["Health"] # Heart image

        # Scale heart image down to be flush with text
        new_height = self.__label.get_height()
        scale = new_height / self.__heart.get_height()
        new_width = int(self.__heart.get_width() * scale)
        self.__heart = pygame.transform.smoothscale(self.__heart, (new_width, new_height))

        # Store Position
        self.__position = (30, self.__screen.get_height() - 30)

        # Variable to keep track of health
        self.__health = 100

        # Healing sound effect
        self.__heal_sfx = pygame.mixer.Sound("heal.wav")
    
    def take_damage(self):
        """Take damage"""

        # When function is called, take 40% away from player's health
        self.__health -= 40

        # Ensure player health cannot go below 0
        if self.__health < 0:
            self.__health = 0
    
    def heal(self):
        """Heal the player"""

        # Add 20% to player's health
        self.__health += 20

        # Ensure player health cannot exceed 100%
        if self.__health > 100:
            self.__health = 100

        # Play healing sound effect
        self.__heal_sfx.play()
    
    def get_health(self):
        """Get player health"""

        return self.__health
    
    def update(self):
        """Update function"""

        # Update the score label with the appropriate information 

        ## Make message from score
        msg = str(self.__health)
        ## Make label
        self.__label = LabelTools.show_outlined_text(self.__font, msg)
        ## Get width and height of combined surface where label and heart will be drawn
        gap = 10 if self.__health != 100 else 4
        surf_w = self.__heart.get_width() + self.__label.get_width() + gap
        surf_h = max(self.__heart.get_height(), self.__label.get_height())
        ## Create the combined surface
        self.image = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
        ## Blit heart onto combined surface
        self.image.blit(self.__heart, (0, 0))
        ## Blit label onto surface
        self.image.blit(self.__label, (self.__heart.get_width() + gap, 1))
        ## Create bounding rectangle
        self.rect = self.image.get_rect()
        ## Place health in appropriate spot
        self.rect.bottomleft = self.__position

# Enemy Frame

class EnemyFrame(pygame.sprite.Sprite):
    def __init__(self, screen, speed, next=False):
        """Initializer"""

        super().__init__()
        # Get the game's screen
        self.__screen = screen
        # Set image to transparent background the size of the screen
        self.image = pygame.Surface(self.__screen.get_size(), pygame.SRCALPHA, 32)
        # Create bounding rectangle
        self.rect = self.image.get_rect()

        # Set spawn location

        ## Place frame initially right on the outside of the screen, to the right.
        self.rect.top = 0
        self.rect.left = self.__screen.get_width()

        ## If next is True, place the frame further off right.
        if next:
            self.rect.left *= 2
        
        # Set enemy frame speed (will be player speed)
        self.set_speed(speed)
        # Store associated sprites in a sprite group
        self.__sprites = pygame.sprite.Group()
        # Is the frame frozen?
        self.__freeze = False
    
    def set_speed(self, speed):
        """Set frame speed (player speed)"""

        if speed >= 0:
            self.__speed = speed
    
    def get_speed(self):
        """Get speed"""

        return self.__speed
     
    def add_sprite(self, sprite):
        """Add a sprite associated with the enemy frame"""
        self.__sprites.add(sprite)
    
    def remove_sprite(self, sprite):
        """Remove an associated sprite"""
        self.__sprites.remove(sprite)
    
    def clear_sprites(self):
        """Get rid of all associated sprites"""
        self.__sprites.empty()
    
    def init_sprites(self, level):
        """Initalize the enemy frame with sprites, depending on level"""

        # Difficulty increases w/ a higher level

        if level == 1:
            # Add just 1 mine and 1 heart
            self.add_sprite(Mine(self))
            self.add_sprite(Heart(self))
        elif level == 2:
            # Add 2 mines and hearts
            for _ in range(2):
                self.add_sprite(Mine(self))
                self.add_sprite(Heart(self))
            # Add an enemy plane
            self.add_sprite(EnemyPlane(self))
        elif level == 3:
            # Add 3 mines
            for _ in range(3):
                self.add_sprite(Mine(self))
            # Add 2 Hearts
            for _ in range(2):
                self.add_sprite(Heart(self))
            # Add 1 enemy plane and 1 fast enemy plane
            self.add_sprite(EnemyPlane(self))
            self.add_sprite(FastEnemyPlane(self))
    
    def get_sprites(self):
        """Get all associated sprites"""
        return self.__sprites
    
    def get_enemy_sprites(self):
        """Get only the enemy sprites"""

        # Copy all of the sprites
        enemy_sprites = self.__sprites.copy()

        # Remove the unwanted sprites
        for sprite in enemy_sprites:
            if type(sprite) == Heart:
                enemy_sprites.remove(sprite)
        
        return enemy_sprites
    
    def get_hearts(self):
        """Get only the hearts"""

        # Make a new group storing only the hearts
        hearts = pygame.sprite.Group()

        # Add only the hearts to the group above
        for sprite in self.__sprites:
            if type(sprite) == Heart:
                hearts.add(sprite)
        
        return hearts

    """Freeze and unfreeze functions"""

    def freeze(self):
        self.__freeze = True
    
    def unfreeze(self):
        self.__freeze = False
    
    def update(self):
        """Update function"""

        # Move the frame toward the player, if not frozen.
        if not self.__freeze:
            self.rect.centerx -= self.__speed

# Enemy sprites and hearts

## Base Sprite: The Mine (all other sprites inherit from the Mine)

class Mine(pygame.sprite.Sprite):
    def __init__(self, enemy_frame: EnemyFrame):
        """Initializer"""

        super().__init__()
        # Setup image and parent enemy frame
        self.image = ASSETS["Mine"]
        self.__enemy_frame = enemy_frame
        # Setup bounding rectangle
        self.rect = self.image.get_rect()
        # Setup mask for accurate collision detection
        self.mask = pygame.mask.from_surface(self.image)
        # Randomly place mine
        self.place_sprite()
        # Store explosion image and sound effect
        self.__explosion_img = ASSETS["explosion_img"]
        self.__explosion_sfx = ASSETS["explosion_sfx"]
        # Keep track on how long a blown up enemy sprite should be shown before despawning
        self.__despawn_delay = 250 # in ms
        # Keep track of when enemy sprite has been deactivated (set off / blown up)
        self.__inactive_time = 0
        # Keep track of whether this sprite is harmful and dangerous
        self.__active = True
    
    def place_sprite(self):
        """Place the enemy sprite randomly"""

        # Get list of other sprites in parent enemy frame
        others = self.__enemy_frame.get_sprites()
        # Place sprite randomly within enemy frame (positions account for the sprite's dimensions)
        self.rect.centerx = rand.randint(self.__enemy_frame.rect.left + self.rect.width, self.__enemy_frame.rect.right - self.rect.width)
        self.rect.centery = rand.randint(self.__enemy_frame.rect.top + self.rect.height, self.__enemy_frame.rect.bottom - self.rect.height)
        # If the sprite overlaps with other sprites, keep trying new positions until there is no overlap
        while pygame.sprite.spritecollide(self, others, False):
            self.rect.centerx = rand.randint(self.__enemy_frame.rect.left + self.rect.width, self.__enemy_frame.rect.right - self.rect.width)
            self.rect.centery = rand.randint(self.__enemy_frame.rect.top + self.rect.height, self.__enemy_frame.rect.bottom - self.rect.height)
    
    def blow_up(self):
        """Blow the sprite up"""

        # Only blow the sprite up, if it hasn't blown up already
        if self.__active:
            ## Get position of sprite the moment it blows up
            last_pos = self.rect.center
            ## Change image of sprite to an explosion image
            self.image = self.__explosion_img
            ## Re-create bounding rectangle; Reposition the sprite to the correct spot
            self.rect = self.image.get_rect()
            self.rect.center = last_pos
            ## Re-create collision mask
            self.mask = pygame.mask.from_surface(self.image)
            ## Play explosion sound effect
            self.__explosion_sfx.play()
            ## Indicate sprite is no longer active
            self.__active = False
            ## Save the time when sprite has been deactivated
            self.__inactive_time = pygame.time.get_ticks()
    
    def is_active(self):
        """See whether mine is currently active or not"""
        return self.__active
    
    def update(self):
        """Update function"""

        # Just move mine in accordane with its enemy frame's motion
        self.rect.centerx -= self.__enemy_frame.get_speed()

        # Despawn mine if made inactive
        if not self.__active:
            ## Get current time
            now = pygame.time.get_ticks()

            ## If elapsed time has reached the despawn delay,
            if now - self.__inactive_time >= self.__despawn_delay:
                # Despawn mine
                self.kill()

    """Dummy freeze and unfreeze functions"""

    def freeze(self):
        # Dummy function, since freeze will be called recursively for all sprites
        return
    
    def unfreeze(self):
        # Dummy function, same reason as freeze()
        return

## Enemy plane

class EnemyPlane(Mine):
    def __init__(self, enemy_frame: EnemyFrame):
        """Initializer"""
        
        super().__init__(enemy_frame)
        # Setup image
        self.image = ASSETS["EnemyPlane"]
        # Setup bounding rectangle and random position
        self.rect = self.image.get_rect()
        self.place_sprite()
        # Setup mask for accurate collision detection
        self.mask = pygame.mask.from_surface(self.image)
        # New to EnemyPlane; it moves faster than its parent enemy frame
        ## Keep track of plane's speed w/ respect to frame
        self.__speed = 5 
        ## Keep track of current speed (set to zero if frozen)
        self.__curr_speed = self.__speed
     
    def update(self):
        """Update function"""

        # Move plane with its EnemyFrame and if active, make it faster by adding its speed
        self.rect.centerx -= self._Mine__enemy_frame.get_speed()

        if self._Mine__active:
            self.rect.centerx -= self.__curr_speed
        
        # Despawn plane if made inactive
        if not self._Mine__active:
            now = pygame.time.get_ticks()

            ## If elapsed time has reached the despawn delay,
            if now - self._Mine__inactive_time >= self._Mine__despawn_delay:
                # Despawn plane
                self.kill()
    
    """Freeze and unfreeze functions"""
    
    def freeze(self):
        # Set current speed to 0 to freeze
        self.__curr_speed = 0
    
    def unfreeze(self):
        # Set current speed to stored speed to unfreeze
        self.__curr_speed = self.__speed

## FastEnemyPlane (inherits from EnemyPlane)

class FastEnemyPlane(EnemyPlane):
    def __init__(self, enemy_frame: EnemyFrame):
        """Initializer"""

        super().__init__(enemy_frame)

        # Change image
        self.image = ASSETS["FastEnemyPlane"]
        # Change bounding rectangle
        self.rect = self.image.get_rect()
        # Place randomly
        self.place_sprite()
        # Change mask
        self.mask = pygame.mask.from_surface(self.image)
        # Change speed (faster than EnemyPlane)
        self._EnemyPlane__speed = 8

## Heart

class Heart(Mine):
    def __init__(self, enemy_frame: EnemyFrame):
        """Initalizer"""

        super().__init__(enemy_frame)
        # Setup image to be a heart
        self.image = ASSETS["Heart"]
        # Setup bounding rect. and place sprite randomly
        self.rect = self.image.get_rect()
        self.place_sprite()
    
    def blow_up(self):
        # Blowing up: Not applicable to heart
        return
    
    def deactivate(self):
        """Deactivate the heart (can no longer heal)"""
        self._Mine__active = False

    def update(self):
        """Update function"""

        # Just move heart in accordane with enemy frame
        self.rect.centerx -= self._Mine__enemy_frame.get_speed()