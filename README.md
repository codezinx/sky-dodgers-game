# **Sky Dodgers: Game**

---

# **Brief Description**

In *Sky Dodgers*, you are a solo pilot of a fighter jet during a war. You have been tasked with gathering aerial information about the enemy by flying over their territory. However, you are flying alone and are in danger of hitting hazards like airborne mines and other planes. *Sky Dodgers* has been designed to be a single-player game where the objective is to survive for as long as possible, which translates to getting a score as high as possible. One point is earned for every second the player survives in this hostile battlefield. The plane will move forward without user input; however, the player inputs W or up to move the plane up and S or down to move the plane down. If one desires to use a controller, they can also move the left thumbstick up and down to achieve the same effect. However, the player is limited by a finite health starting at 100%. Crashing into a mine or an enemy plane reduces the player's health by 40%. However, colliding with a floating heart restores the player's health by 20%. The game ends when the player's health reaches 0%.

---

# How to Setup

1. Download the source code to a folder
    1. `git clone https://github.com/codezinx/sky-dodgers-game.git`
2. Enter the `sky-dodgers-game` folder
3. Install dependencies: `pip install -r requirements.txt`
4. Run the game: `python main.py`

---

# The Game Proposal

# **Diagram of Game**

## **Figure 1**

*Diagram of the main game window*  
![][image2]  
*Note*. Sprite class names are being used in the diagram. They are explained in more detail below. In addition, excluding the heart in the bottom-left corner, sprites with the same image are copies of the same sprite.

# **Sprite Blueprints**

## **Sprite 1: Player**

### ***Purpose***

The main player sprite of the game. Its purpose is to "move forward," survive, and score as much of a high score as possible. This is the only sprite of the game which is directly controlled by the player. However, in reality, the Player's x-coordinate is not being changed, to give an appearance of the game's camera following the Player.

### ***Attributes***

#### **image**

Responsible for storing the image of a fighter jet representing the player. It is also used to generate the sprite's bounding rectangle. In addition, the background of the fighter jet will be transparent by default, eliminating the need for the unreliable self.image.set\_colorkey(...).

#### **rect**

Responsible for storing the bounding rectangle for the sprite, which is used to determine the spatial position of the sprite, as well as detect collisions with other sprites in the main game loop. The rectangle is created using self.image.get\_rect().

#### **\_\_screen**

Responsible for storing a copy of the screen object. This attribute allows the sprite methods to check whether the Player sprite is within bounds or not.

#### **\_\_dodge\_speed**

A constant attribute which is used to set the maximum vertical movement speed of the plane. Creating a constant attribute allows for an easy change of the dodging speed if needed.

#### **\_\_current\_vy**

A mutable attribute that sets the current vertical movement speed of the plane. It is zero by default, and changes when the user gives input.

#### **\_\_explosion\_sfx**

Stores the sound effect of an explosion that is played when the plane loses all of its health and blows up in the skies.

#### **\_\_freeze**

A boolean value that, if set to True, prevents the Player from moving. It is False by default but set to True when the player blows up and the game is over.

### ***Methods***

#### **\_\_init\_\_(screen)**

This method is responsible for initializing the sprite with the correct attributes given. The screen is passed in, so the program can check whether the player is within bounds.

#### **move(up, ratio)**

Determines the current vertical speed of the plane by setting \_\_current\_vy. The parameter up is a boolean that determines whether the plane will move up or down, and the parameter ratio determines by how much of \_\_dodge\_speed should \_\_current\_vy be set to. \_\_current\_vy is set to \_\_dodge\_speed \* ratio, and made negative if up is True. In addition, \_\_current\_vy is set back to zero if \_\_freeze \== True, to freeze the Player's movement.

#### **blow\_up()**

Responsible for "blowing up" a sprite when called. It works by first freezing or deactivating the sprite (self.\_\_freeze \= True), then changing the image of the sprite to an image of an explosion, playing \_\_explosion\_sfx next, and finally, despawning or hiding the sprite from view. When blow\_up() is called on the player, the game is over.

#### **update()**

Responsible for actually handling plane movement and triggering blow\_up() when the player's health runs out. Whereas move() simply sets \_\_current\_vy and ensures \_\_current\_vy can only be set to non-zero values during a non-frozen state and during user input, update() actually uses \_\_current\_vy to move the sprite up and down. It does this by adding \_\_current\_vy to self.rect.centery. In addition, update() is also responsible for ensuring the plane is unable to move outside the window. 

#### **freeze()**

Sets self.\_\_freeze to True to stop the motion of the Player, in order to take away the ability of the real-life player to move the Player. This will be run when the Player blows up and the game is over, since there is no need for player control when the game is done.

## **Sprite 2: EnemyFrame**

### ***Purpose***

A helper sprite that helps determine the spawn and the movement of enemy sprites, like the Mine and EnemyPlane, discussed after this sprite. It determines the rate the enemy sprites should approach the player, if they are stationary relative to the Earth, and not the player's movement.

### ***Attributes***

#### **image**

Responsible for storing the image of a transparent surface whose dimensions equal the screen's dimensions. It itself does not need to be a visible sprite on the screen, since it is a helper sprite. It also determines this sprite's bounding rectangles.

#### **rect**

Responsible for storing the bounding rectangle for the sprite, which is used to determine the spatial position of the sprite, which will be used in the main game logic to determine when the next EnemyFrame will be spawned. The rectangle is created using self.image.get\_rect().

#### **\_\_screen**

Responsible for storing a copy of the screen object. This attribute allows the sprite to spawn right outside the game window to the right, and approach the player as the player continues to move forward. It will initially be outside the screen, and then come inside the screen.

#### **\_\_speed**

Determines the rate at which the EnemyFrame will approach the Player sprite, which in turn will determine the rate of approach of all enemy sprites, if they are stationary relative to the Earth. It can be thought of as the player's horizontal speed, but since the "game camera" follows the player, it makes more logical sense to move the frame towards the player, rather than move the player towards the frame.

#### **\_\_freeze**

A boolean value that, if set to True, stops the EnemyFrame from approaching the player. This is useful when the game is over, since the Player will blow up and be unable to move.

### ***Methods***

#### **\_\_init\_\_(screen)**

This method is responsible for initializing the sprite with the correct attributes given. The screen is passed in, so that the EnemyFrame can spawn in the right location.

#### **update()**

Responsible for making the EnemyFrame approach the player while the player is alive and moving. In more technical terms, it will keep moving towards the player as long as self.\_\_freeze \== True. The frame will eventually stop moving and despawn once it moves completely out of the window to the left.

#### **get\_speed()**

Returns self.\_\_speed, or the current speed of the EnemyFrame. It is necessary, so that sprites associated with this EnemyFrame are able to move at a minimum of the frame's speed toward the player.

#### **freeze()**

Sets self.\_\_freeze to True to stop the motion of the Frame, in order to represent that the player is no longer moving. This will give the appearance the player stopped moving horizontally.

## **Sprite 3: Mine**

### ***Purpose***

Floats in the skies as a "stationary" object, relative to the Earth. (In reality, it is being moved closer to the player). It acts as an obstacle standing in the player's way and blows up when the Player touches it to inflict damage.

### ***Attributes***

#### **image**

Responsible for storing the image of an air mine. It is also used to generate the sprite's bounding rectangle. In addition, the background of the air mine will be transparent by default, eliminating the need for the unreliable self.image.set\_colorkey(...).

#### **rect**

Responsible for storing the bounding rectangle for the sprite, which is used to determine the spatial position of the sprite, as well as detect collisions with other sprites in the main game loop. The rectangle is created using self.image.get\_rect().

#### **\_\_enemy\_frame**

Responsible for storing the object of the EnemyFrame the sprite is bound to. Allows the program to determine the random spawning of the sprite within the frame's boundaries, and coincide the movement of the sprite towards the player.

#### **\_\_active**

A boolean responsible for determining whether a mine is active and dangerous. It is active when it is in bounds and hasn't blown up. It is True by default.

#### **\_\_explosion\_sfx**

Stores the sound effect of an explosion that is played when the mine blows up in the skies.

### ***Methods***

#### **\_\_init\_\_(enemy\_frame)**

This method is responsible for initializing the sprite with the correct attributes given. The enemy frame is passed in order for proper spawning and movement.

#### **blow\_up()**

Responsible for "blowing up" a sprite when called. It works by first deactivating the sprite (self.\_\_active \= False), so it no longer has an effect on the game, then changing the image of the sprite to an image of an explosion, playing \_\_explosion\_sfx next, and finally, despawning or hiding the sprite from view.

#### **update()**

Responsible for moving the mine sprite from right to left, closer to the player. If the player is able to dodge the mine, it will move past the player. Its movement is determined by the motion of the EnemyFrame it is associated with, since relative to the Earth, it is stationary.

## **Sprite 4: EnemyPlane**

### ***Purpose***

An enemy plane sprite. It is responsible for patrolling your enemy's skies and disrupting your ability to move forward in the game. It takes away the same health as a collision with the mine, but unlike the mine, it actually moves in the skies and approaches the player faster.

### ***Attributes***

#### **image**

Responsible for storing the image of an enemy plane. It is also used to generate the sprite's bounding rectangle. In addition, the background of the air mine will be transparent by default, eliminating the need for the unreliable self.image.set\_colorkey(...).

#### **rect**

Responsible for storing the bounding rectangle for the sprite, which is used to determine the spatial position of the sprite, as well as detect collisions with other sprites in the main game loop. The rectangle is created using self.image.get\_rect().

#### **\_\_enemy\_frame**

Responsible for storing the object of the EnemyFrame the sprite is bound to. Allows the program to determine the random spawning of the sprite within the frame's boundaries, and coincide the movement of the sprite towards the player.

#### **\_\_active**

A boolean responsible for determining whether the plane is active and moving. It is active when it is in bounds and hasn't blown up. It is True by default.

#### **\_\_explosion\_sfx**

Stores the sound effect of an explosion that is played when the plane blows up in the skies.

#### **\_\_speed**

A constant variable that determines how fast the plane should move toward the player, relative to the Earth. From the player's POV, the enemy plane will be moving toward the player faster than the stationary mine.

### ***Methods***

#### **\_\_init\_\_(screen)**

This method is responsible for initializing the sprite with the correct attributes given. The enemy frame is passed in order for proper spawning and movement.

#### **blow\_up()**

Responsible for "blowing up" a sprite when called. It works by first deactivating the sprite (self.\_\_active \= False), so it no longer has an effect on the game, then changing the image of the sprite to an image of an explosion, playing \_\_explosion\_sfx next, and finally, despawning or hiding the sprite from view.

#### **update()**

Responsible for moving the sprite from right to left, closer to the player. If the player is able to dodge this plane, it will move past the player. Its movement is determined by the motion of the EnemyFrame it is associated with, plus \_\_speed, since it is not a stationary sprite. However, \_\_speed will no longer be added to the plane once the plane is inactive.

## **Sprite 5: FastEnemyPlane**

### ***Purpose***

A faster variant of the enemy plane sprite, which inherits from EnemyPlane. Its purpose and the majority of its attributes and methods remain identical to EnemyPlane.

### ***Inherits from***

Sprite: EnemyPlane

### ***Change in Attributes***

#### **image**

The image of FastEnemyPlane will be changed to that of a fighter jet different from the player, to differentiate it from the slower EnemyPlane.

#### **rect**

A bounding rectangle will have to be re-created for FastEnemyPlane, since the image of FastEnemyPlane will most likely not have the same dimensions as EnemyPlane's image.

## **Sprite 6: Heart**

### ***Purpose***

Floats in the skies as a "stationary" object, relative to the Earth. (In reality, it is being moved closer to the player). Unlike the mine, and despite being associated with EnemyFrame, it gives the player health upon contact.

### ***Attributes***

#### **image**

Responsible for storing the image of a heart. It is also used to generate the sprite's bounding rectangle. In addition, the background of the heart will be transparent by default, eliminating the need for the unreliable self.image.set\_colorkey(...).

#### **rect**

Responsible for storing the bounding rectangle for the sprite, which is used to determine the spatial position of the sprite, as well as detect collisions with other sprites in the main game loop. The rectangle is created using self.image.get\_rect().

#### **\_\_enemy\_frame**

Responsible for storing the object of the EnemyFrame the sprite is bound to. Allows the program to determine the random spawning of the sprite within the frame's boundaries, and coincide the movement of the sprite towards the player.

#### **\_\_active**

A boolean responsible for determining whether a heart is active and useful. It is active when it is in bounds and the player hasn't collided with it yet. It is True by default.

### ***Methods***

#### **\_\_init\_\_(enemy\_frame)**

This method is responsible for initializing the sprite with the correct attributes given. The enemy frame is passed in order for proper spawning and movement.

#### **deactivate()**

Responsible for setting \_\_active to False upon being called. This helps prevent the player from healing twice from the same collision.

#### **is\_active()**

Returns self.\_\_active, or whether the heart is active or not, so a different sprite can use it to determine whether the player's health should increase or not.

#### **update()**

Responsible for moving the heart sprite from right to left, closer to the player. If the player misses the heart, it will move past the player. Its movement is determined simply by the motion of the EnemyFrame it is associated with, since relative to the Earth, it is stationary.

## **Sprite 7: ScoreKeeper**

### ***Purpose***

Responsible for determining, keeping track of, and showing the player's current score on screen. Its image is simply a Label showing the current score.

### ***Attributes***

#### **image**

Responsible for storing the image of the rendered score label when the label has been set to the correct value. It is set to the image created by \_\_font.render(...), and it also determines the score label's bounding rectangle.

#### **rect**

Responsible for storing the bounding rectangle for the sprite, which is used to determine the position of the sprite on screen. The rectangle is created using self.image.get\_rect().

#### **\_\_position**

A tuple constant that determines the location of the centre of the score label. It is helpful to reset the position of the score label every time it is updated.

#### **\_\_font**

Determines the font and the font size that will be used to render the score label. It utilizes pygame.font.Font(...) to accomplish this task.

#### **\_\_score**

Determines and keeps track of the player's current score. This is the backbone of the ScoreKeeper sprite's functionality.

### ***Methods***

#### **\_\_init\_\_()**

This method is responsible for initializing the sprite with the correct attributes given.

#### **update()**

Responsible for reading the current score from \_\_score every frame, reupdating self.image with the correct score, then reupdating self.rect with the correct \_\_position.

#### **score()**

When called, score() adds 1 to the current score (self.\_\_score \+= 1). It is supposed to be run for every second after the game starts and until the game is over, so that the score increases by the second of the player's survival.

## **Sprite 8: Health**

### ***Purpose***

Responsible for determining, keeping track of, and showing the player's current health on screen. Its image is a label showing the player's health and a heart to the left of the label.

### ***Attributes***

#### **image**

Responsible for storing the image when an image of a heart and the rendered score label are combined into one Surface object. This new Surface object determines Health's bounding rectangle.

#### **rect**

Responsible for storing the bounding rectangle for the sprite, which is used to determine the position of the sprite on screen. The rectangle is created using self.image.get\_rect().

#### **\_\_position**

A tuple constant that determines the location of the centre of Health. It is helpful to reset the position of Health every time the label is updated to account for the new health.

#### **\_\_font**

Determines the font and the font size that will be used to render the health label. It utilizes pygame.font.Font(...) to accomplish this task.

#### **\_\_heart**

Stores the image of the heart that will be placed beside the health label. It is more beautiful to use an image to represent health rather than using "Health: "

#### **\_\_label**

Stores the rendered label containing the data necessary to show the current player health on screen.

#### **\_\_health**

Determines and keeps track of the player's current health. Health keeps track of the player's health rather than the Player itself. This is the backbone of the Health sprite's functionality.

#### **\_\_heal\_sfx**

Stores the sound effect that will be played when the player gains health from a Heart collision.

### ***Methods***

#### **\_\_init\_\_()**

This method is responsible for initializing the sprite with the correct attributes given.

#### **update()**

Responsible for reading the current health from \_\_health, reupdating \_\_label with the correct health, recombining \_\_label and \_\_health to make the new rendered image for self.image, and finally, reupdating self.rect with the correct \_\_position.

#### **take\_damage()**

When called, this function will reduce the player's health by 40% (self.\_\_health \-= 40). This function will be run when the Player collides with a Mine or an EnemyPlane. This function also ensures the health can never go below 0%.

#### **heal()**

When called, this function will increase the player's health by 20% (self.\_\_health \+= 20). This function will be run when the Player collides with a Heart. This function also ensures the health can never go above 100%. In addition, \_\_heal\_sfx will be played to indicate that the player has gained health.

## **Final Notes**

The attributes and methods may change as necessary, in order to make the game's functionality work. Additional sprites may also be created to add additional functionality of the game. However, the core game mechanic should remain the same.

# **Implementation Steps and Schedule**

The steps are written in second-person, since they are to guide me on what to do:

## **December 8-10: Initialize code and create moving background**

* Set up the IDEA/ALTER framework of the game code  
* Create all necessary files, including a main loop and a sprites file  
* Download and organize all necessary images and fonts needed to run game  
* Download all necessary music and sound effects  
* Ensure game logo is within program files  
* Implement moving background logic from previous assignments  
  * The moving background was implemented in an in-class activity related to space and planets.  
* Moving background will make game appear to "move"  
* Setup pygame.mixer, and write the code to play background music

## **December 11-15: Set up Player object and movement**

* Write the class to set up Player sprite  
* Write code to handle joystick and keyboard input  
* Start creating sprite groups to store the Player, enemy sprites, and on screen information labels  
* Set up Events section of IDEA/ALTER  
* In events section,  
  * Utilize Player's move() object to make Player move  
  * Ensure move() is called again with a ratio of 0 to make the player stop when there is no user input  
* Keyboard and joystick should be able to be used in tandem

## **December 16-17: Create ScoreKeeper, Health, and show them on screen**

* Write all the classes necessary to create these information sprites  
* Make sure appropriate fonts and images are downloaded before creating  
* Implement all necessary methods. They will be used later on in the collision logic.  
* Display these sprites on screen, above all other sprites

## **December 18-20: Create enemy sprites and Heart**

* Ensure appropriate images are downloaded  
* Create the class that will set up the EnemyFrame  
* Write all the classes for the enemy sprites in the sprites Python file  
* Set up the methods and attributes beforehand, so that handling logic becomes easier later on  
* Figure out a way to make the movement of enemy sprites and hearts coincide with the EnemyFrame's movement

## **December 21-26: Set up spawning / despawning of EnemyFrames and their associated sprites**

* Write code that handles the spawning of EnemyFrames  
* ***EnemyFrame spawning logic***  
  * An EnemyFrame will be spawned right outside the screen (to the right)  
  * All the associated sprites like Mines, and EnemyPlanes will be spawned within the boundaries of the EnemyFrame  
  * The EnemyFrame will move across the screen, carrying along its associated objects  
  * When the EnemyFrame is centred on screen, a new EnemyFrame will be spawned and follow the same procedure  
  * When the EnemyFrame goes all the way left outside the screen, it will be despawned, along with the rest of its associated objects  
* Depending on current score, the number of Mines, EnemyPlanes, FastEnemyPlanes, and Hearts spawned will be determined for each frame spawned  
* Difficulty increases with a higher score  
* Spawning logic will continue working as long as player health is above 0

## **December 27 to January 2: Create collision, damage, healing and scoring logic**

* Implement primarily sprite-on-group collisions, since they will allow for the same logic to be reused  
* Implement a clock that resets after every second  
  * After the clock resets, the player's score will increase by 1 by calling ScoreKeeper.score\_one()  
* Implement destruction and damage logic  
  * When Player collides with a Mine and EnemyPlane  
  * The Mine and EnemyPlane must blow\_up()  
  * The explosion must be shown and heard, if class methods have been written properly  
  * Player's health must decrease from this incident  
  * Player will blow\_up() when its health is 0  
* Implement logic to heal player  
  * Detect collision with a Heart  
  * Make Heart inactive upon collision  
  * Run Health.heal() upon collision to give player health  
  * Ensure sound effect is played when healing

## **January 3-5: Implement pausing functionality *(optional feature)***

* Detect a key press (i.e. P) or, better yet, create a pause button that will detect when a user clicks on it.  
* When the user requests the game to be paused, find a way to "freeze" the game and the score in place.  
* Then, overlay another surface that will show "PAUSED" or the Pause icon  
* Ensure there is a way to resume the game: either by a button or by pressing P again  
  * The game should resume from the same state it was paused from  
* This feature may be skipped if time does not allow for

## **January 6-8: Implement a game over screen**

* Design and create the game over screen, including all the necessary labels  
* Find a way to stop all game logic and make it reset from zero  
* Find a way to save the user's score  
* Show user's score on game over screen  
* May also implement saving user's score to a file to save user's high score (high\_score.txt)

## **January 9-12: Implement a main menu *(Optional feature)***

* Ensure the logo of the game is present. It should be placed at the top of the screen.  
* Design labels and drawing that will show controls  
* Design drawings and labels that show the objective of the game, what to avoid (Mine, EnemyPlane, FastEnemyPlane), and how to gain health (Heart)  
* Design a PLAY button that will enter the game when clicked  
* Implement code to show all the main menu elements on screen  
* Play a different background music (less intense) for the main menu  
  * "Lobby music"  
* Ensure main menu doesn't break game functionality

## **January 13-14: Testing**

* Test full game functionality  
* Ensure game code has proper comments and documentation  
* Fix any remaining bugs

## **Closing Notes**

The schedule is a general guideline for when to do which steps to finish the game within the deadline. However, I may work ahead of schedule, or push certain steps behind to accommodate for other tasks.

**References (Image Sources)**  
Elchin ArtsTM. (n.d.). *Pixel Heart*. Vecteezy. https\://www\.vecteezy.com/png/13640968-pixel-heart-pixelart  
Heart (and \_\_heart for Health)  
*Pixel Art Sky Background*. (n.d.). Indonesian-recipes. http\://artpictures.club/view.php?img=https\://static.vecteezy.com/system/resources/previews/023/330/830/original/blue-sky-background-in-pixel-art-style-vector.jpg  
Background image  
*Pixel Art Space Invaders Retro Fighter Jet Design PNG*. (n.d.). PNG ALL. https\://www\.pngall.com/space-invaders-png/download/114439/  
FastEnemyPlane  
retro59. (2022, November 15). *F-15 Fighter Jet*. Dinopixel. https\://dinopixel.com/f-15-fighter-jet-pixel-art-20271  
Player  
yugg0. (n.d.). *Pixel Planes WW2*. itch.io. https\://yugg0.itch.io/pixel-planes-ww2  
		EnemyPlane

* Image of Mine generated using AI  
* *Font used in game and logo:* Press Start 2P from Google Fonts

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,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>