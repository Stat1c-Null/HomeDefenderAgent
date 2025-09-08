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
current_time = py.time.get_ticks()

aliveZombies = []
deadZombies = []

zombiesKilled = 0
zombiesCleaned = 0

zombieGoalX,zombieGoalY = dis_width / 2, dis_height / 2

patrolPoints = [(zombieGoalX - 100, zombieGoalY - 100),
                (zombieGoalX + 100, zombieGoalY - 100),
                (zombieGoalX + 100, zombieGoalY + 100),
                (zombieGoalX - 100, zombieGoalY + 100)]
patrolIndex = 0

class Zombie:
    def __init__(self,xpos, ypos, radius, speed, targetX, targetY):
        self.xpos = xpos
        self.ypos = ypos
        self.radius = radius
        self.speed = speed
        self.targetX = targetX
        self.targetY = targetY
        self.isDead = False

    #Draw Zombie on the Screen
    def draw(self):
        py.draw.circle(dis, red, (self.xpos, self.ypos), self.radius)

    #Move zombie towards the goal
    def move(self):
        if not self.isDead:
            if self.xpos < self.targetX:
                self.xpos += self.speed
            elif self.xpos > self.targetX:
                self.xpos -= self.speed
            if self.ypos < self.targetY:
                self.ypos += self.speed
            elif self.ypos > self.targetY:
                self.ypos -= self.speed

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
        global patrolIndex
        targetX, targetY = patrolPoints[patrolIndex]
        #Ones Agent reaches patrol point, move to next point
        if abs(self.xpos - targetX) < 5 and abs(self.ypos - targetY) < 5:
            patrolIndex = (patrolIndex + 1) % len(patrolPoints)
        else:
            #Move horizontally or vertically towards target
            if self.xpos < targetX:
                self.xpos += self.speed
            elif self.xpos > targetX:
                self.xpos -= self.speed
            if self.ypos < targetY:
                self.ypos += self.speed
            elif self.ypos > targetY:
                self.ypos -= self.speed

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
    global aliveZombies, current_time
    
    action_time = None
    spawn_delya = 3000
    if action_time is None:
        action_time = current_time + 3000

    if action_time is not None and current_time >= action_time:
        xpos = random.randint(0, dis_width)
        ypos = random.randint(0, dis_height)
        new_zombie = Zombie(xpos, ypos, 7, 2, zombieGoalX, zombieGoalY)
        aliveZombies.append(new_zombie)
        action_time = current_time + spawn_delya
 
agent = Agent(xpos=300, ypos=400, radius=10, speed=5, health=100)
zombie = Zombie(xpos=200, ypos=300, radius=7, speed=2, targetX=zombieGoalX, targetY=zombieGoalY)
 
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
        #Draw target
        py.draw.rect(dis, black, (zombieGoalX, zombieGoalY, 30, 30))
        #Draw Score
        zombiesKilledScore(0)
        zombiesCleanedScore(0)

        #Agent Logic
        agent.patrol()

        #Zombie Logic
        zombie.move()

        #Update display
        py.display.update() 
        clock.tick(30)
 
    py.quit()
    quit()
 
 
gameLoop()
