import pygame, random

from pygame.locals import (
    RLEACCEL,
    K_f,
    K_a,
    K_s,
    K_d,
    K_w,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768



# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        
        super(Player, self).__init__()
        self.surf = pygame.image.load("spaceship.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -1.5)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 1.5)
        if pressed_keys[K_a]:
            self.rect.move_ip(-1.5, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(1.5, 0)
        # The afterburner.
        if pressed_keys[K_f]:
            self.rect.move_ip(2.3, 0)


        # Keep player on the screen
        if self.rect.left < 100:
            self.rect.left = 100
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 90
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

            # function inside Player-class

    def getPosition(self):
        return self.rect.center

""" This creates a "missile." In reality this is the guns and bullets.
It was a mistake on my part to allow for such a mistake. A real missile is on it's
way and will be called "Sidewinder" instead. """

class Missile(pygame.sprite.Sprite):

    def __init__(self, position):
        super(Missile, self).__init__()
        self.surf = pygame.image.load("missile.png").convert_alpha()
        self.rect = self.surf.get_rect(
            center=position
            )
        self.mask = pygame.mask.from_surface(self.surf )
        
    def update(self):
        self.rect.move_ip(5, 0)
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

# This creates an enemy AI player.
    
class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, elementId):

        """ The line below is the cause of the issue with the asteriod animation
        continuing to duplicate. However I could use this as a way"""
        
        self.crashPics = createPicList("enemy_crashing", 15)
        
        super(Enemy, self).__init__()
        self.elementId = elementId
        self.surf = pygame.image.load("asteroid.png").convert_alpha()

        loadedImages = []
        for img in self.crashPics:
            loadedImages.append(pygame.image.load(img).convert_alpha())
        self.crashSprite = loadedImages

        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 100, SCREEN_WIDTH + 200),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.mask = pygame.mask.from_surface(self.surf )
        self.speed = 4
        self.crashed = False
        self.picNumber = 0
        

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def updatePic(self):

        if self.crashed == True:
        
            if self.picNumber == len(self.crashSprite):
                self.picNumber = 0
                
            self.surf = self.crashSprite[self.picNumber]
            self.picNumber = self.picNumber + 1
            self.mask = pygame.mask.from_surface(self.surf)
            
        
        if self.picNumber == len(self.crashSprite):
            self.kill() 
                
    def update(self):
        if self.crashed is False:
            self.rect.move_ip(-self.speed, 0)

        else:
            self.rect.move_ip(-5, 0)

        if self.rect.right < 0:
            self.kill()


            
    def getId(self):
        return self.elementId

    def crash(self):
        # self.surf = pygame.image.load("asteroid_hit.png").convert_alpha()
        self.crashed = True
        self.mask = pygame.mask.from_surface(self.surf)
        self.picNumber = 0

    def isCrashed(self):
        return self.crashed

# This is the funtion for the background image of the video game.

class Background_2(pygame.sprite.Sprite):
    def __init__(self):

        super(Background, self).__init__()
        self.surf = pygame.image.load("background.png").convert_alpha()
        
        self.rect = self.surf.get_rect(

        )

class Background(pygame.sprite.Sprite):
    def __init__(self):

        super(Background, self).__init__()
        self.surf = pygame.image.load("space.png").convert_alpha()
        
        self.rect = self.surf.get_rect(

        )

# This is the funtion to create an animation for the exploding bogey.

def createPicList(folder, frames):

    

    picList = []

    for i in range(1,frames):

        s1, s3 = "/000", ".png"

        if(i<10):

            picList.append("%s%s%s%s" % (folder,s1, i, s3))

        if(i>9):

            picList.append("%s%s%s%s" % (folder,"/00", i, s3))

            

    return picList
