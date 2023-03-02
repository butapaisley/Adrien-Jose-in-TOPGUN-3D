import pygame, random, math
from pygame import mixer
from mygame_utils import Player, Asteroid, Background, Missile
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    K_1,
    K_2,
    QUIT,
)

clock = pygame.time.Clock()
FPS = 60

# Init missiles
missiles = pygame.sprite.Group()
# Init font
pygame.font.init()
my_font = pygame.font.SysFont(None, 16)
# Init counters
asteroidsHit = 0
asteroidsDestroyed = 0

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
         
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top Gun 2D")

# Load background image
bg_image = pygame.image.load('background2.png').convert()

bg_width = bg_image.get_width()
titles = math.ceil(SCREEN_WIDTH/ bg_width)
scroll= 0

# Set up the font
font = pygame.font.SysFont(None, 64)

# Set up the menu text
menu_text = font.render("My Game Menu", True, (255, 255, 255))

# Set up the menu text position
text_pos = menu_text.get_rect(centerx=SCREEN_WIDTH/2, centery=SCREEN_HEIGHT/2)
    
def main_menu():
    menu_options = ["Press 1 to Start Game", "Press 2 to Quit"]
    selected_option = 0
    
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_1:
                    return
                elif event.key == K_2:
                    pygame.quit()
                    quit()
        
        # Render menu options
        screen.fill((0, 0, 0))
        for i, option in enumerate(menu_options):
            text_color = (255, 255, 255) if i == selected_option else (128, 128, 128)
            text = my_font.render(option, True, text_color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + i*20))
            screen.blit(text, text_rect)
        
        pygame.display.flip()


# Show main menu
main_menu()

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

player = Player()
background = Background()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
asteroids = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(background)


# Main loop
running = True

collidedItems = []
elementId = 0
isBig = False
isLarge = False

Goose = pygame.mixer.Sound("goose.mp3")
mixer.music.load('audio.mp3')
mixer.music.play(-1)

#ChatGPT said to change this to 0
updatePicFrame = 0


while running:

    pressed_keys = pygame.key.get_pressed()
    
    #draw scrolling background
    for i in range(0, titles):
        screen.blit(bg_image, (i * bg_width + scroll, 0))
    scroll -= -5


    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                player.kill()
                break;
    
        elif event.type == QUIT:
            running = False

            # Add a new asteroid
        elif event.type == ADDENEMY:
            # newAsteroid = createNewAsteroid(elementId, isBig, isLarge)
            newAsteroid = Asteroid(elementId)
            asteroids.add(newAsteroid)
            all_sprites.add(newAsteroid)
            elementId = elementId+1

        ## Add following inside while-loop


        # If button "space bar" is hit
        if pressed_keys[K_SPACE] and len(missiles) == 0:
            newMissile = Missile(player.getPosition())
            missiles.add(newMissile)
            all_sprites.add(newMissile)

        # Count asteroids white

        asteroidsHit = asteroidsHit + 1


    missiles.update()

    
    # When missile collides asteroid
    for asteroid in asteroids:
        for missile in missiles:
            collidedMissile = pygame.sprite.collide_mask(missile, asteroid)
            if collidedMissile:
                missile.kill()
                asteroid.crash()

        
    # Update enemy position
    asteroids.update()

    for elem in asteroids:
        updatePicFrame = updatePicFrame+1
        if updatePicFrame == 50:
            elem.updatePic()
            updatePicFrame = 10
            
    
    screen.fill((0, 0, 0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
            
    # Check if any enemies have collided with the player
    isPlayerKilled = False
    for elem in asteroids:
        mixer.init()
        collide = pygame.sprite.collide_mask(elem, player)
        if collide and elem.crashed == True:
            screen.fill('red')
            # If so, then play "Goose"
            mixer.music.stop()
            mixer.music.load("failed.mp3")
            mixer.music.play(1)
            Goose.play()
            player.kill()
            isPlayerKilled = True
            running = False
            
    if isPlayerKilled == True:
        break;
    
    player.update(pressed_keys)
    screen.blit(player.surf, player.rect)

    pygame.display.flip()
        
# Stop the game and play "Goose"
mixer.music.stop()
mixer.music.load("failed.mp3")
mixer.music.play(1)
Goose.play()

# Quit the game
pygame.display.quit()

