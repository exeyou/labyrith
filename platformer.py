from typing import Any
from pygame import *


'''Необхідні класи'''
 
#клас-батько для спрайтів
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Treasure(GameSprite):
    def __init__(self, treasure_image, treasure_x, treasure_y):
        super().__init__(treasure_image, treasure_x, treasure_y, 0)

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed + 1  # Increase player's speed slightly
        if keys[K_RIGHT] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.speed + 1  # Increase player's speed slightly
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed + 1  # Increase player's speed slightly
        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed + 1  # Increase player's speed slightly

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_haight):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.haight = wall_haight
        self.image = Surface((self.width, self.haight))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))




class Enemy(GameSprite):

    def update(self):
        self.speed = 6
        if self.rect.x <= 170:
            self.direction = "right"
            
        if self.rect.x >= 600:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

 
#Ігрова сцена:
win_width = 700
win_height = 500
 
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))
 
#Персонажі гри:
player = Player('hero.png', 300, win_height - 80, 1)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('reward.jpg', win_width - 570, win_height - 290, 0)
walls = [
    Wall(0, 0, 0, 200, 300, 20, 200),
    Wall(0, 0, 0, 200, 100, 20, 200),
    Wall(0, 0, 1, 200, 100, 200, 20),
    Wall(0, 0, 0, 100, 300, 200, 200),
    Wall(0, 0, 0, 400, 300, 40, 500),
    Wall(0, 0, 0, 300, 100, 20, 100),
    Wall(0, 0, 0, 200, 150, 20, 200),
    Wall(0, 0, 0, 100, 200, 20, 100),
]

# Add walls to a sprite group
wall_group = sprite.Group()
wall_group.add(walls)

game = True
clock = time.Clock()
FPS = 60
#музика
mixer.init() # Створює музичний плеєр
mixer.music.load('sneaky.mp3') # завантажує музику
mixer.music.play() # зациклює і програє її
# Create walls for the labyrinth


# Inside the game loop, you can reset and update the walls just like other sprites
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    window.blit(background, (0, 0))
    
    # Check for collisions with walls
    if sprite.spritecollide(player, wall_group, False):
        game = False  # Quit the game
    
    # Check for collision with cyborg
    if sprite.collide_rect(player, monster):
        game = False  # Quit the game when player touches the cyborg
    
    player.reset()
    monster.reset()
    final.reset()
    if sprite.collide_rect(player, final):
        quit()
    player.update()
    monster.update()
    final.update()
    # Update and reset walls
    for wall in walls:
        wall.reset()
    
    
    display.update()
    clock.tick(FPS)
