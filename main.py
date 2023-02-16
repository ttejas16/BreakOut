import pygame,sys,random
from pygame.locals import *

clk=pygame.time.Clock()

pygame.init()

windowSize=(800,600)

screen=pygame.display.set_mode(windowSize,0,32)
pygame.display.set_caption("test")

display = pygame.Surface((400,300))

sliderImg = pygame.image.load('slider.png')
sliderImg.set_colorkey((255,255,255))
sliderLoc = [40,290]
sliderRect = pygame.Rect(sliderLoc[0],sliderLoc[1],sliderImg.get_width(),sliderImg.get_height())
run=True
movingRight = False
movingLeft = False

def moveSlider(slider,movement):
    sliderLoc[0] += movement[0]
    return slider

def generateRects(y):
    rects = []
    k=0
    for i in range(17):
        rects.append(pygame.Rect(6+k*20+k*3,y,20,5))
        k+=1
    k=0
    for i in range(17):
        rects.append(pygame.Rect(6+k*20+k*3,y+10,20,5))
        k+=1
    k=0
    for i in range(17):
        rects.append(pygame.Rect(6+k*20+k*3,y+20,20,5))
        k+=1
    k=0
    for i in range(17):
        rects.append(pygame.Rect(6+k*20+k*3,y+30,20,5))
        k+=1
    return rects
bricks = generateRects(10)

def randomColor():
    return (random.randint(1,255),random.randint(1,255),random.randint(1,255))

class Ball():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.velocity = [2,2]
        self.color = (255,255,255)

    def draw(self):
        self.circle = pygame.draw.circle(display,self.color,(self.x,self.y),3,0)
        return self.circle

    def move(self):
        self.y += self.velocity[1]
        self.x += self.velocity[0]
        if self.y <= 5 :
            self.velocity[1] = -self.velocity[1]
        if self.x >= 398:
            self.velocity[0] = -self.velocity[0]
        if self.x <= 5 :
            self.velocity[0] = -self.velocity[0]
        
    def collide(self):
        if self.circle.colliderect(sliderRect):
            self.velocity[1] = -2
            
    def checkBrickCollision(self,ballObj):
        score = 0
        for brick in bricks:
            if brick.colliderect(ballObj):
                score += 10
                self.color = randomColor()
                bricks.remove(brick)
                if random.randint(0,1) == 0:
                    self.velocity[0] = -self.velocity[0]
                    self.velocity[1] = self.velocity[1]
                else:
                    self.velocity[0] = self.velocity[0]
                    self.velocity[1] = -self.velocity[1] 
        return score           
        
Score = 0
ball = Ball(25,100)
# print(ball.x)
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Score : ', True,(255,255,255),(0,0,0))
textRect = text.get_rect()
textRect.center = ((400 // 2) - 20, 300 // 2)

while run:
    display.fill((0,0,0)) #reset display
    display.blit(text, textRect)


    for brick in bricks:
        pygame.draw.rect(display,(255,0,255),brick,0)

    ballRect = ball.draw()
    ball.move()
    movement = [0,0]

    if movingRight and sliderRect.x <= 400 - 18 :
        movement[0] += 5
    if movingLeft and sliderRect.x >=0 :
        movement[0] -= 5


    sliderImg = moveSlider(sliderImg,movement)
    display.blit(sliderImg,(sliderLoc[0],sliderLoc[1]))

    sliderRect.x = sliderLoc[0]
    sliderRect.y = sliderLoc[1]    

    ball.collide()
    Score += ball.checkBrickCollision(ballRect)
    if ball.y >= 299:
        text = font.render(('Your score was : %d'%(Score)), True,(255,255,255),(0,0,0))
        textRect = text.get_rect()
        textRect.center = ((400 // 2) - 5, 300 // 2)
    else:
        text = font.render(('Score : %d'%(Score)), True,(255,255,255),(0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            # print(ball.velocity)
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                movingRight = True
            if event.key == K_LEFT:
                movingLeft = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                movingRight = False
            if event.key == K_LEFT:
                movingLeft = False

    surf = pygame.transform.scale(display,windowSize)
    screen.blit(surf,(0,0))

    pygame.display.update()
    
    clk.tick(60)
pygame.quit()