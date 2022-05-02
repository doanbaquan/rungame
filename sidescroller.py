#################################################################
#                                                               #
#       TITLE:  Skater Jump                                     #
#       DESC:   Play as a skater in 2D endless 2 dimensional    #
#               side-scroller game where players jump over      #
#               obstacles and gain points. Input it received    #
#               with the keyboard with the spacebar. Pressing   #
#               space will cause the player to jump. A list is  #
#               used to organize the obstacles presented to     #
#               the player. Once code is run, pygame window     #
#               titled "Skater Jump" will pop up, and user will # 
#               be able to play as a skater character jumping   #
#               over obstacles. If the player collides with an  #
#               obstacle, the game stops and the player inputs  #
#               result in no output. At that point, the game is #
#               over and the final score is displayed.          #
#                                                               #
#################################################################

import pygame, math, random, time
pygame.init()

#screen constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption('Skater Jump')

clock = pygame.time.Clock() 
font = pygame.font.Font('freesansbold.ttf', 20)

bg_img = pygame.image.load('background.jpg')
bg_img = pygame.transform.scale(bg_img,(SCREEN_WIDTH, SCREEN_HEIGHT))

#object that user plays as, when spacebar is pressed, the skater jumps
class Player:
    #variable initialization
    def __init__(self, lives):
        self.width = 75
        self.height = 120
        self.x = 350
        self.y = 340
        self.jumping = False
        self.falling = False
        self.jump_velocity = 3
        self.points = 0
        self.lives = lives
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.collided = False

        #skater animations and font
        self.skaterjump = pygame.image.load('skaterjump.png')
        self.skaterfall = pygame.image.load('skaterfall.png')
        self.skaterdefault = pygame.image.load('skaterdefault.png')
        
    #checks if Player has collided with Object
    def collide(self):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect) and self.collided == False:
                #sets the speed of obstacle and jump to zero so that position of either does not change
                self.collided = True
                self.lives -= 1
            elif self.rect.colliderect(obstacle.rect)==False:
                self.collided = False

    #Sets jumping to true
    def jump(self):
        self.jumping = True

    #Moves Player up when jumping is true, and lowers Player once y-value reaches 140px
    def move(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        
        #upper limit of jump
        if self.y <= 140:
            self.jumping  = False
            self.falling = True

        #upon getting to initial state, end fall and blit image as default skating position
        if self.y >=340:
            self.y = 340
            self.falling = False
            screen.blit(self.skaterdefault, self.rect)

        #jump motion and animation set to jumping position
        if self.jumping:
            self.y -= self.jump_velocity
            screen.blit(self.skaterjump, self.rect)

        #falling motion and animation set to falling position
        elif self.falling:
            self.y += self.jump_velocity
            screen.blit(self.skaterfall, self.rect)

    #Increases and displays score depending on how long player survives
    def score(self):
        if self.jump_velocity != 0:
            self.points += 1

        text = font.render("Score: " + str(self.points), True, (0, 0, 0))
        lifecount = font.render("Lives: " + str(self.lives), True, (0, 0, 0))
        
        textRect = text.get_rect()
        textRect.center = (100, 100)
        screen.blit(text, textRect)

        textRect2 = text.get_rect()
        textRect2.center = (100, 50)
        screen.blit(lifecount, textRect2)

#obstacle class that takes a parameter of obstacle speed
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

    #moves the obstacle depending on the speed parameter that is inputed
    def move(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        screen.blit(self.obstacleimg, self.rect)
        self.x -= self.speed
        if self.x -self.width <= 0:
            obstacles.remove(self)

            
obstacles = []
player = Player(3)

#indexing position of the background
bg_imgX = 0

while True:
    
    clock.tick(100)

    if player.lives == 0:
        obstacle.speed = 0
        player.jump_velocity = 0  #jump_velocity variable also acts as indicator of game over for ending text to appear

        #game over end text
        text2 = font.render("GAME OVER", True, (0, 0, 0))
        textRect2 = text2.get_rect()
        textRect2.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT*0.25)
        screen.blit(text2, textRect2)

        #final score end text
        text = font.render("Final Score: " + str(player.points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT*0.3)
        screen.blit(text, textRect)
    else:
        #continuous background that loops infinitely
        screen.blit(bg_img,(bg_imgX,0))
        screen.blit(bg_img, (SCREEN_WIDTH + bg_imgX,0))
        if bg_imgX == -SCREEN_WIDTH:
            screen.blit(bg_img,(SCREEN_WIDTH+bg_imgX, 0))
            bg_imgX = 0
        bg_imgX-=0.5

        #Obstacle generation
        if len(obstacles) == 0:
            Obstacle(3)

        player.move()
        player.collide()
        player.score()

        #Obstacle motion
        for obstacle in obstacles:
            obstacle.move()

    for event in pygame.event.get():
        #Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #Keybinds, when space is clicked, skater jumps
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            #when jump_velocity is not 0, the game is still running, when it is 0, game has ended
            if keys[pygame.K_SPACE] and player.jumping == False and player.falling == False and player.jump_velocity != 0:
                player.jump()
    
    pygame.display.update()
