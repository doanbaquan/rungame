#####################################################
#                                                   #
#       TITLE:  Skater Jump                         #
#       BY:     Quan Doan                           #
#       DESC:   Play as a skater in 2D endless      #
#               2 dimensional side-scroller game    #
#               where players jump over obstacles   #
#               and the speed increases.            #
#                                                   #
#####################################################

import pygame, math, random, time
pygame.init()

#Screen constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
clock = pygame.time.Clock() 

bg_img = pygame.image.load('background.jpg')
bg_img = pygame.transform.scale(bg_img,(SCREEN_WIDTH, SCREEN_HEIGHT))
ground = pygame.Rect(0,445,800,200)

class Player:
    def __init__(self):
        self.width = 75
        self.height = 120
        self.x = 350
        self.y = 355
        self.jumping = False
        self.falling = False
        self.jump_velocity = 3
        self.points = 0
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.skaterjump = pygame.image.load('skaterjump.png')
        self.skaterfall = pygame.image.load('skaterfall.png')
        self.skaterdefault = pygame.image.load('skaterdefault.png')

    def jump(self):
        self.jumping = True

    def collide(self):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                obstacle.speed = 0
                self.jump_velocity = 0 

                #game over end text
                text2 = self.font.render("GAME OVER", True, (0, 0, 0))
                textRect2 = text2.get_rect()
                textRect2.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT*0.25)
                screen.blit(text2, textRect2)

                #final score end text
                text = self.font.render("Final Score: " + str(self.points), True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT*0.3)
                screen.blit(text, textRect)
                break

    def move(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
         
        if self.y <= 150:
            self.jumping  = False
            self.falling = True

        if self.y >=355:
            self.y = 355
            self.falling = False
            screen.blit(self.skaterdefault, self.rect)

        if self.jumping:
            self.y -= self.jump_velocity
            screen.blit(self.skaterjump, self.rect)
        elif self.falling:
            self.y += self.jump_velocity
            screen.blit(self.skaterfall, self.rect)

    def score(self):
        if self.jump_velocity != 0:
            self.points += 1
        text = self.font.render("Score: " + str(self.points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (100, 50)
        screen.blit(text, textRect)


class Obstacle:

    def __init__(self,speed):
        self.width = 55
        self.height = 100
        self.x = 900
        self.y = 355
        self.speed = speed
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.obstacleimg = pygame.image.load('stopsign.png')
        obstacles.append(self)
    def move(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        screen.blit(self.obstacleimg, self.rect)
        self.x -= self.speed
        if self.x -self.width <= 0:
            obstacles.remove(self)
    


obstacles = []
player = Player()

while True:
    clock.tick(100)
    screen.fill((255,255,255))

    pygame.draw.rect(screen,(61,149,67), ground)
    screen.blit(bg_img,(0,0))
    if len(obstacles) == 0:
        Obstacle(3.5)
    player.move()
    player.collide()
    player.score()
    for obstacle in obstacles:
        obstacle.move()
        #print(obstacle.x,obstacle.y)
    #print(player.jumping,player.falling)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and player.jumping == False and player.falling == False and player.jump_velocity != 0:
                player.jump()
    
    

    pygame.display.update()