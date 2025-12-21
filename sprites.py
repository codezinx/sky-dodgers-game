import pygame
import random as rand

# Assets cache

ASSETS = {}

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

# Classes

class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        # Setup image and screen
        self.image = ASSETS["Player"]
        self.__screen = screen
        # Setup rect
        self.rect = self.image.get_rect()
        self.rect.left = 20
        self.rect.centery = self.__screen.get_height() // 2
        # Setup mask for accurate collision detection
        self.mask = pygame.mask.from_surface(self.image)
        # Other key attributes
        self.__dodge_speed = 10
        self.__current_vy = 0
        self.__explosion_img = ASSETS["explosion_img"]
        self.__explosion_sfx = ASSETS["explosion_sfx"]
        self.__freeze = False
        self.__blown_up = False
        self.__blow_up_time = 0
        self.__despawn_delay = 1000 # ms
    
    def move(self, ratio):
        if ratio < -1:
            ratio = -1
        elif ratio > 1:
            ratio = 1
        
        self.__current_vy = self.__dodge_speed * ratio
    
    def out_of_bounds(self):
        if self.rect.top < 0:
            return -1
        elif self.rect.bottom > self.__screen.get_height():
            return 1
        else:
            return 0
    
    def blow_up(self):
        if not self.__blown_up:
            last_pos = self.rect.center

            self.image = self.__explosion_img
            self.rect = self.image.get_rect()
            self.rect.center = last_pos
            self.mask = pygame.mask.from_surface(self.image)
            self.__explosion_sfx.play()

            self.__freeze = True
            self.__blown_up = True
            self.__blow_up_time = pygame.time.get_ticks()
        # self.kill()

    def update(self):
        if self.__blown_up:
            now = pygame.time.get_ticks()

            if now - self.__blow_up_time >= self.__despawn_delay:
                # despawn player
                self.kill()
        
        if self.__freeze:
            return

        self.rect.centery += self.__current_vy

        # Check whether plane is in bounds
        if self.out_of_bounds() == -1:
            self.rect.top = 0
        elif self.out_of_bounds() == 1:
            self.rect.bottom = self.__screen.get_height()
    
    def freeze(self):
        self.__freeze = True

class LabelTools:
    def __init__(self):
        pass
    
    @staticmethod
    def show_outlined_text(font: pygame.font.Font, msg: str, outline_width: int = 1, text_color="white", outline_color="black"):
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

class ScoreKeeper(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        # Store font and screen
        self.__screen = screen
        self.__font = ASSETS["font_score"]
        # Store Position
        self.__position = (self.__screen.get_width() // 2, 35)
        # Keep track of score
        self.__score = 0
        self.__alive = True

    def score(self):
        # Add score depending on color of brick broken
        if self.__alive:
            self.__score += 1
    
    def get_score(self):
        return self.__score
    
    def player_died(self):
        self.__alive = False
    
    def update(self):
        # Update the score label with the appropriate information 
        msg = str(self.__score)
        self.image = LabelTools.show_outlined_text(self.__font, msg)
        # Rect
        self.rect = self.image.get_rect()
        self.rect.center = self.__position

class Health(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        # Store font, heart, label and screen
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
        # Keep track of health
        self.__health = 100
        self.__heal_sfx = pygame.mixer.Sound("heal.wav")
    
    def take_damage(self):
        self.__health -= 40

        if self.__health < 0:
            self.__health = 0
    
    def heal(self):
        self.__health += 20

        if self.__health > 100:
            self.__health = 100

        self.__heal_sfx.play()
    
    def get_health(self):
        return self.__health
    
    def update(self):
        # Update the score label with the appropriate information 
        ## Make message from score
        msg = str(self.__health)
        ## Make label
        self.__label = LabelTools.show_outlined_text(self.__font, msg)
        ## Get width and height of combined surface
        gap = 10 if self.__health != 100 else 4
        surf_w = self.__heart.get_width() + self.__label.get_width() + gap
        surf_h = max(self.__heart.get_height(), self.__label.get_height())
        ## Blit heart
        self.image = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
        self.image.blit(self.__heart, (0, 0))
        ## Blit label
        self.image.blit(self.__label, (self.__heart.get_width() + gap, 1))
        # Rect
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.__position

class EnemyFrame(pygame.sprite.Sprite):
    def __init__(self, screen, speed, next=False):
        super().__init__()
        self.__screen = screen
        # Image - transparent b.g.
        self.image = pygame.Surface(self.__screen.get_size(), pygame.SRCALPHA, 32)
        # Rectangle
        self.rect = self.image.get_rect()
        # Default spawn location (outside of screen)
        self.rect.top = 0
        self.rect.left = self.__screen.get_width()

        if next:
            self.rect.left *= 2
        # Key attributes
        self.set_speed(speed)
        self.__sprites = pygame.sprite.Group()
        self.__freeze = False
    
    def set_speed(self, speed):
        if speed >= 0:
            self.__speed = speed
    
    def get_speed(self):
        return self.__speed
     
    def add_sprite(self, sprite):
        self.__sprites.add(sprite)
    
    def remove_sprite(self, sprite):
        self.__sprites.remove(sprite)
    
    def clear_sprites(self):
        self.__sprites.empty()
    
    def init_sprites(self, level):
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
        return self.__sprites
    
    def get_enemy_sprites(self):
        enemy_sprites = self.__sprites.copy()

        for sprite in enemy_sprites:
            if type(sprite) == Heart:
                enemy_sprites.remove(sprite)
        
        return enemy_sprites
    
    def get_hearts(self):
        hearts = pygame.sprite.Group()

        for sprite in self.__sprites:
            if type(sprite) == Heart:
                hearts.add(sprite)
        
        return hearts
    
    def freeze(self):
        self.__freeze = True
    
    def update(self):
        if not self.__freeze:
            self.rect.centerx -= self.__speed

# Base-case enemy sprite
class Mine(pygame.sprite.Sprite):
    def __init__(self, enemy_frame: EnemyFrame):
        super().__init__()
        # Setup image and parent enemy frame
        self.image = ASSETS["Mine"]
        self.__enemy_frame = enemy_frame
        # Setup rect
        self.rect = self.image.get_rect()
        # Setup mask for accurate collision detection
        self.mask = pygame.mask.from_surface(self.image)
        # Randomly place mine
        self.place_sprite()
        # Other key attributes
        self.__explosion_img = ASSETS["explosion_img"]
        self.__explosion_sfx = ASSETS["explosion_sfx"]
        self.__despawn_delay = 250 # in ms
        self.__inactive_time = 0
        self.__active = True
    
    def place_sprite(self):
        # Get list of other sprites
        others = self.__enemy_frame.get_sprites()
        # Place sprite randomly
        self.rect.centerx = rand.randint(self.__enemy_frame.rect.left + self.rect.width, self.__enemy_frame.rect.right - self.rect.width)
        self.rect.centery = rand.randint(self.__enemy_frame.rect.top + self.rect.height, self.__enemy_frame.rect.bottom - self.rect.height)
        # Prevent overlaps; try new positions until there is no overlap
        while pygame.sprite.spritecollide(self, others, False):
            self.rect.centerx = rand.randint(self.__enemy_frame.rect.left + self.rect.width, self.__enemy_frame.rect.right - self.rect.width)
            self.rect.centery = rand.randint(self.__enemy_frame.rect.top + self.rect.height, self.__enemy_frame.rect.bottom - self.rect.height)
    
    def blow_up(self):
        if self.__active:
            last_pos = self.rect.center

            self.image = self.__explosion_img
            self.rect = self.image.get_rect()
            self.rect.center = last_pos
            self.mask = pygame.mask.from_surface(self.image)
            self.__explosion_sfx.play()

            self.__active = False
            self.__inactive_time = pygame.time.get_ticks()
    
    def is_active(self):
        return self.__active
    
    def update(self):
        # Just move mine in accordane with enemy frame
        self.rect.centerx -= self.__enemy_frame.get_speed()
        # Despawn mine if made inactive
        if not self.__active:
            now = pygame.time.get_ticks()

            if now - self.__inactive_time >= self.__despawn_delay:
                # despawn mine
                self.kill()
    
    def freeze(self):
        # Dummy function, since freeze will be called recursively for all sprites
        return


class EnemyPlane(Mine):
    def __init__(self, enemy_frame: EnemyFrame):
        super().__init__(enemy_frame)
        # Setup image and parent enemy frame
        self.image = ASSETS["EnemyPlane"]
        # Setup rect and position
        self.rect = self.image.get_rect()
        self.place_sprite()
        # Setup mask for accurate collision detection
        self.mask = pygame.mask.from_surface(self.image)
        # New key attributes
        self.__speed = 5
     
    def update(self):
        # Move plane with its EnemyFrame and if active, its speed
        self.rect.centerx -= self._Mine__enemy_frame.get_speed()

        if self._Mine__active:
            self.rect.centerx -= self.__speed
        
        # Despawn mine if made inactive
        if not self._Mine__active:
            now = pygame.time.get_ticks()

            if now - self._Mine__inactive_time >= self._Mine__despawn_delay:
                # despawn mine
                self.kill()
    
    def freeze(self):
        self.__speed = 0

class FastEnemyPlane(EnemyPlane):
    def __init__(self, enemy_frame: EnemyFrame):
        super().__init__(enemy_frame)
        # Change image
        self.image = ASSETS["FastEnemyPlane"]
        # Change rect
        self.rect = self.image.get_rect()
        self.place_sprite()
        # Change mask
        self.mask = pygame.mask.from_surface(self.image)
        # Change speed
        self._EnemyPlane__speed = 8

class Heart(Mine):
    def __init__(self, enemy_frame: EnemyFrame):
        super().__init__(enemy_frame)
        # Setup image
        self.image = ASSETS["Heart"]
        # Setup rect and position
        self.rect = self.image.get_rect()
        self.place_sprite()
    
    def blow_up(self):
        # Not applicable to heart
        return
    
    def deactivate(self):
        self._Mine__active = False

    def update(self):
        # Just move heart in accordane with enemy frame
        self.rect.centerx -= self._Mine__enemy_frame.get_speed()