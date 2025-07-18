import pygame, asyncio
from random import randint
from time import sleep
import os
#Snake game

#Importing the commands of they keys that the user will press
from pygame.locals import (
    RLEACCEL, #for image loading
    K_UP, #for moving up 
    K_DOWN, #for moving down
    K_LEFT, #for moving left
    K_RIGHT, #for moving right
    K_w, #for moving up
    K_s, #for moving down
    K_a, #for moving left
    K_d, ##for moving right
)

class Text(pygame.sprite.Sprite): #Class for any Text boxes we want to display
    def __init__(self, text, size, color, width, height):
        # Call the parent class (Sprite) constructor  
        pygame.sprite.Sprite.__init__(self)
        #set up the text object
        self.font = pygame.font.SysFont("Arial", size)
        #create the text object
        self.textSurf = self.font.render(text, 1, color)
        #set up the box behind the text
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(center=(400,300,))
        #get width and height of text and store in variables
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        #blit the text onto the textbox (in the center)
        self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self, size, color, width, height, locationY):
        #set CurrentScore to 0
        CurrentScore = 0
        #set score as a string
        score = "Score: "+str(CurrentScore)
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        #set up the text object
        self.font = pygame.font.SysFont("Arial", size)
        #create the text object
        self.textSurf = self.font.render(score, 1, color)
        #set up the box behind the text
        self.image = pygame.Surface((width, height))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect(center=(100,locationY))
        #get width and height of text and store in variables
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        #blit the text onto the textbox (in the center)
        self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])

    def update(self, CurrentScore, size, color, width, height):
        #increment CurrentScore by 1 
        CurrentScore += 1
        #set text1 as a string
        text1 = "Score: "+str(CurrentScore)
        #set up the text object
        self.font = pygame.font.SysFont("Arial", size)
        #create the text object
        self.textSurf = self.font.render(text1, 1, color)
        #set up the box behind the text
        self.image = pygame.Surface((width, height))
        self.image.fill((0,0,255))
        #get width and height of text and store in variables
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        #blit the text onto the textbox (in the center)
        self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])
        #returns the CurrentScore so it can be incremented again
        #when player scores another point
        return CurrentScore

class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        #set up the sprite's surf
        image_path = os.path.join(os.path.dirname(__file__), "fruit.png")
        #load the image of the fruit
        self.surf = pygame.image.load(image_path).convert()
        self.surf.set_colorkey((0, 0, 255), RLEACCEL)
        #randomise x and y coordinates for the fruit to spawn 
        locationX = randint(140,635)
        locationY = randint(128,485)
        #set up the fruit as a rectangle
        self.rect = self.surf.get_rect(center=(locationX,locationY,))


class Player(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)
        # Load the original image
        self.original_image = pygame.image.load(image_file).convert()
        self.original_image.set_colorkey((0, 0, 255), RLEACCEL)

        # Create the surface we'll actually use
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(400, 300))

        # Movement properties
        self.direction = 0  # 0=right, 90=up, 180=left, 270=down
        self.next_direction = 0
        self.is_moving = False  # Add this flag to control movement

    def start_moving(self):
        self.is_moving = True

    def update(self, pressed_keys):
        if not self.is_moving:
            return  # Don't move until game starts
        # Handle direction changes
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            if self.direction not in (90, 270):  # Can't reverse vertically
                self.next_direction = 90
        elif pressed_keys[K_DOWN] or pressed_keys[K_s]:
            if self.direction not in (90, 270):  # Can't reverse vertically
                self.next_direction = 270
        elif pressed_keys[K_LEFT] or pressed_keys[K_a]:
            if self.direction not in (0, 180):  # Can't reverse horizontally
                self.next_direction = 180
        elif pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            if self.direction not in (0, 180):  # Can't reverse horizontally
                self.next_direction = 0

        # Only change direction at center of tile for smoother movement
        if (self.rect.centerx % 20 == 0 and self.rect.centery % 20 == 0):
            self.direction = self.next_direction

        # Move based on current direction
        if self.direction == 0:  # Right
            self.rect.move_ip(5, 0)
        elif self.direction == 90:  # Up
            self.rect.move_ip(0, -5)
        elif self.direction == 180:  # Left
            self.rect.move_ip(-5, 0)
        elif self.direction == 270:  # Down
            self.rect.move_ip(0, 5)

        # Rotate the image to match direction
        self.image = pygame.transform.rotate(self.original_image, self.direction)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Screen boundary checks
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 600:
            self.rect.bottom = 600

    #the method for the player growing
    def grow(self, length):
        # Increment the length
        length += 10

        # Scale the original image (not the rotated one)
        self.original_image = pygame.transform.scale(
            self.original_image,
            (length, self.original_image.get_height())
        )

        # Update the current image with proper rotation
        self.image = pygame.transform.rotate(self.original_image, self.direction)
        self.rect = self.image.get_rect(center=self.rect.center)

        return length # Return length so it can be updated again


class StartOverlay(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load(image_file)
        self.surf.fill((255, 255, 255, 200), None, pygame.BLEND_RGBA_MULT)
        self.rect = self.surf.get_rect(center=(location))
    
class VerticalWall(pygame.sprite.Sprite):
    def __init__(self,location):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        #sets up the surf of the wall
        self.surf = pygame.Surface((25, 50))
        #set up the wall as a blue rectangle
        self.surf.fill((0,0,255))
        #sets up the wall as a rectangle
        self.rect = self.surf.get_rect(center=(location))

class HorizontalWall(pygame.sprite.Sprite):
    def __init__(self,location):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        #sets up the surf of the wall
        self.surf = pygame.Surface((50, 25))
        #set up the wall as a blue rectangle
        self.surf.fill((0,0,255))
        #sets up the wall as a rectangle
        self.rect = self.surf.get_rect(center=(location))

#opens the files for the wall coordinates
file1_path = os.path.join(os.path.dirname(__file__), "Vertical_walls.txt")
file2_path = os.path.join(os.path.dirname(__file__), "Horizontal_walls.txt")
file1 = open(file1_path,'r')
file2 = open(file2_path,'r')
#sets the default length and score
length = 50
CurrentScore = 0
game_started = False

#initiate pygame
pygame.init()

#set the window up with title
win = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake in python")

#instantiate sprites
player_image_path = os.path.join(os.path.dirname(__file__), "snake.png")
player = Player(player_image_path)
scoreBoard = Scoreboard(12,"white",100,50,25)
fruit = Fruit()
starting_image_path = os.path.join(os.path.dirname(__file__), "start.png")
startingOverlay = StartOverlay(starting_image_path, [400,300])
gameOver = Text("Game Over",30,"white",200,100)

#set up sprite groups
all_sprites = pygame.sprite.Group()
all_fruit = pygame.sprite.Group()
walls = pygame.sprite.Group()

#add sprites to groups
all_sprites.add(player)
all_sprites.add(scoreBoard)
all_sprites.add(fruit)
all_sprites.add(gameOver)
all_fruit.add(fruit)

clock = pygame.time.Clock()
FPS = 60

#initite a FOR loop for each line in the first file
for line in file1:
    #store location as an array of the line of the file split at the comma
    location = line.strip().split(",")
    #take each item in the location array and store it as an integer variable
    num1 = int(location[0])
    num2 = int(location[1])
    #instantiate the vertical wall sprite with the coordinates from the file
    wall = VerticalWall([num1,num2])
    #add this wall to the walls group
    walls.add(wall)

#initite a FOR loop for each line in the second file
for line in file2:
    #store location as an array of the line of the file split at the comma
    location = line.strip().split(",")
    #take each item in the location array and store it as an integer variable
    num1 = int(location[0])
    num2 = int(location[1])
    #instantiate the horizontal wall sprite with the coordinates from the file
    wall = HorizontalWall([num1,num2])
    #add this wall to the walls group
    walls.add(wall)


async def main():
    clock = pygame.time.Clock()
    FPS = 60

    global fruit, CurrentScore, length

    # Game state variables
    first_run = True  # Track if this is the first time running the game
    game_active = False
    game_over = False
    restart_timer = 0

    # Create the starting overlay once
    starting_overlay = StartOverlay(starting_image_path, [400, 300])
    all_sprites.add(starting_overlay)  # Add to sprites group immediately

    while True:  # Outer loop for game restarts
        # Reset game state for new games
        game_active = False
        CurrentScore = 0
        length = 50

        # Recreate player and fruit
        player = Player(player_image_path)
        all_sprites.add(player)  # Add player to sprites group

        fruit = Fruit()
        all_fruit = pygame.sprite.Group(fruit)

        # Main game loop
        running = True
        while running:
            clock.tick(FPS)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and not game_active:
                    # Mouse click starts/restarts game
                    game_active = True
                    player.start_moving()  # Only start moving after click
                    if first_run:
                        starting_overlay.kill()
                        first_run = False

            # Game over handling
            if game_over:
                restart_timer += 1
                if restart_timer >= FPS * 2:  # 2 seconds
                    game_over = False
                    restart_timer = 0
                    running = False  # Exit inner loop to restart game

            # Game logic when active
            if game_active and not game_over:
                pressed_keys = pygame.key.get_pressed()
                player.update(pressed_keys)

                # Check collisions
                if pygame.sprite.spritecollideany(player, walls):
                    game_over = True
                    game_active = False

                if pygame.sprite.spritecollideany(player, all_fruit):
                    fruit.kill()
                    fruit = Fruit()
                    all_fruit.add(fruit)
                    CurrentScore = scoreBoard.update(CurrentScore, 12, "white", 100, 50)
                    length = player.grow(length)

            # Drawing
            win.fill((0, 0, 0))

            # Draw walls
            for wall in walls:
                win.blit(wall.surf, wall.rect)

            # Draw game elements - player is always visible unless first game hasn't started
            if not (first_run and not game_active):
                win.blit(player.image, player.rect)

            # Draw fruit except at first run before game starts
            if game_active or not first_run:
                win.blit(fruit.surf, fruit.rect)

            win.blit(scoreBoard.image, scoreBoard.rect)

            # Draw UI overlays
            if first_run and not game_active:
                win.blit(starting_overlay.surf, starting_overlay.rect)
            elif game_over:
                win.blit(gameOver.image, gameOver.rect)

            pygame.display.update()
            await asyncio.sleep(0)

asyncio.run(main()) #runs the main function