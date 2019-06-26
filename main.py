import sys, pygame, random, pandas as pd
from Spaceship import Ship
from asteroid import Asteroid
from pygame.locals import *

pygame.init()
screen_info = pygame.display.Info()

#set the weight and height to the size of the screen
size = (width, height) = (int(screen_info.current_w*0.5), int(screen_info.current_h*0.5))

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
color = (30, 0, 30)
screen.fill(color)

#read and store game data
df = pd.read_csv('game_info.csv')

#setup game variables
asteroids = pygame.sprite.Group()
numLevels = df['LevelNum'].max()
level = df['LevelNum'].min()
levelData = df.iloc[level]
asteroidCount = levelData['AsteroidCount']
player = Ship((levelData['PlayerX'], levelData['PlayerY']))

def init():
    global asteroidCount, asteroids, levelData
    levelData = df.iloc[level]
    player.reset((levelData['PlayerX'], levelData['PlayerY']))
    asteroids.empty()
    asteroidCount = levelData['AsteroidCount']
    for i in range(asteroidCount):
        asteroids.add(Asteroid((random.randint(50, width-50),
                                random.randint(50, height-50)),random.randint(15,16)))

def win():
    font = pygame.font.SysFont(None, 70)
    text = font.render("You Escaped!", True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (width/2, height/2)
    while True:
        screen.fill(color)
        screen.blit(text, text_rect)
        pygame.display.flip()

def main():
    global level
    init()
    while level <= numLevels:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.speed[0] = 10
            if event.key == pygame.K_LEFT:
                player.speed[0] = -10
            if event.key == pygame.K_UP:
                player.speed[1] = 10
            if event.key == pygame.K_DOWN:
                player.speed[-1] = -10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.speed[0] = 0
            if event.key == pygame.K_LEFT:
                player.speed[0] = 0
            if event.key == pygame.K_UP:
                player.speed[1] = 0
            if event.key == pygame.K_DOWN:
                player.speed[-1] = 0
        screen.fill(color)
        player.update()
        asteroids.update()
        gets_hit = pygame.sprite.spritecollide(player, Asteroid, False)
        Asteroid.draw(screen)
        screen.blit(player.image, player.rect)
        pygame.display.flip()

        if player.checkReset(width):
            if level == numLevels:
                break
            else:
                level += 1
                init()
        elif gets_hit:
            player.reset((levelData['PlayerX'], levelData['PlayerY']))
    win()
if __name__ == ' main ':
    main()

