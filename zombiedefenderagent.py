import pygame as py
import random

py.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
brown = (142, 58, 2)
 
dis_width = 800
dis_height = 500

dis = py.display.set_mode((dis_width, dis_height))
py.display.set_caption('Zombie Defender Agent')
 
clock = py.time.Clock()
font_style = py.font.SysFont("comicsansms", 25)

aliveZombies = []
deadZombies = []

zombiesKilled = 0
zombiesCleaned = 0

zombieGoalX,zombieGoalY = dis_width / 2, dis_height / 2

class Zombie:
    def __init__(self,xpos, ypos, radius, speed):
        self.xpos = xpos
        self.ypos = ypos
        self.radius = radius
        self.speed = speed
        self.isDead = False

    #Draw Zombie on the Screen
    def draw(self):
        py.draw.circle(dis, red, (self.xpos, self.ypos), self.radius)

    #Move zombie towards the goal
    def move(self):
        pass

class Agent:
    def __init__(self, xpos, ypos, radius, speed, health):
        self.xpos = xpos
        self.ypos = ypos
        self.radius = radius
        self.speed = speed
        self.health = health
        self.target = None

    #Draw agent on the screen
    def draw(self):
        py.draw.circle(dis, green, (self.xpos, self.ypos), self.radius)

    #Patrol the area
    def patrol(self):
        pass

    #Move towards dead zombie
    def moveToZombie(self, zombieX, zombieY):
        pass

    #Shoot zombie
    def shoot(self, target):
        pass

    #Burn zombie
    def burn(self, zombie):
        pass

 
def zombiesKilledScore(killed):
    value = font_style.render("Zombies Killed: " + str(killed), True, yellow)
    dis.blit(value, [0, 0])
     
def zombiesCleanedScore(cleaned):
    mesg = font_style.render("Zombies Cleaned: " + str(cleaned), True, blue)
    dis.blit(mesg, [dis_width / 3, 0])

def spawnZombies():
    pass
 
agent = Agent(xpos=300, ypos=400, radius=10, speed=6, health=100)
zombie = Zombie(xpos=200, ypos=300, radius=7, speed=3)
 
def gameLoop():
    game_over = False
 
    while not game_over:
        for event in py.event.get():
            if event.type == py.QUIT:
                game_over = True

        #Fill background with a color
        dis.fill(brown)

        #Draw Agent
        agent.draw()

        #Draw Zombies
        zombie.draw()
        
        #Draw Score
        zombiesKilledScore(0)
        zombiesCleanedScore(0)

        #Update display
        py.display.update() 
        clock.tick(30)
 
    py.quit()
    quit()
 
 
gameLoop()
