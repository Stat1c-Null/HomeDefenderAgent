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
projectiles = []

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
        if not self.isDead:
            py.draw.circle(dis, red, (self.xpos, self.ypos), self.radius)
        else:  
            py.draw.circle(dis, black, (self.xpos, self.ypos), self.radius)

    #Move zombie towards the goal
    def move(self):
        if not self.isDead:
            self.xpos, self.ypos = moveToGoal(self.xpos, self.ypos, self.targetX, self.targetY, self.speed)

class Agent:
    def __init__(self, xpos, ypos, radius, speed, health, visionRange):
        self.xpos = xpos
        self.ypos = ypos
        self.radius = radius
        self.speed = speed
        self.health = health
        self.visionRange = visionRange
        self.target = None
        self.patrolCounter = 0  # Counter to manage patrol timing

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
            if patrolIndex == len(patrolPoints) - 1:
                self.patrolCounter += 1
        else:
            #Move horizontally or vertically towards target
            self.xpos, self.ypos = moveToGoal(self.xpos, self.ypos, targetX, targetY, self.speed)

        #Change direction of patroling after 2 complete cycles
        if self.patrolCounter == 2:
            patrolPoints.reverse()
            self.patrolCounter = 0
    #Scan area around agent for alive zombies
    def scanForZombies(self, aliveZombies):
        for zombie in aliveZombies:
            distance = ((self.xpos - zombie.xpos) ** 2 + (self.ypos - zombie.ypos) ** 2) ** 0.5
            if distance <= self.visionRange and not zombie.isDead:
                print("Zombie Spotted and Shot!")
                self.target = zombie
                self.shoot(self.target)
                
                #return zombie

    #Move towards dead zombie
    def moveToZombie(self, zombieX, zombieY):
        self.xpos, self.ypos = moveToGoal(self.xpos, self.ypos, zombieX, zombieY, self.speed)

    #Shoot zombie
    def shoot(self, target):
        # Spawn a projectile towards the target zombie
        projectile = Projectile(self.xpos, self.ypos, target)
        projectiles.append(projectile)

    #Burn zombie
    def burn(self, deadZombie):
        print("Zombie Burned!")
        deadZombies.remove(deadZombie)

class Projectile:
    def __init__(self, xpos, ypos, target, speed=10, radius=4):
        self.xpos = xpos
        self.ypos = ypos
        self.target = target
        self.speed = speed
        self.radius = radius
        self.active = True

    def move(self):
        if not self.active:
            return
        # If target is already dead, deactivate projectile
        if self.target.isDead:
            self.active = False
            return
        self.xpos, self.ypos = moveToGoal(self.xpos, self.ypos, self.target.xpos, self.target.ypos, self.speed)
        # Check for collision with target
        distance = ((self.xpos - self.target.xpos) ** 2 + (self.ypos - self.target.ypos) ** 2) ** 0.5
        if distance <= self.radius + self.target.radius:
            self.active = False
            self.target.isDead = True
            if self.target in aliveZombies:
                aliveZombies.remove(self.target)
                deadZombies.append(self.target)
            global zombiesKilled
            zombiesKilled += 1

    def draw(self):
        if self.active:
            py.draw.circle(dis, yellow, (int(self.xpos), int(self.ypos)), self.radius)

# Move entity towards a goal position
def moveToGoal(xpos, ypos, targetX, targetY, speed):
    if xpos < targetX:
        xpos += speed
    elif xpos > targetX:
        xpos -= speed
    if ypos < targetY:
        ypos += speed
    elif ypos > targetY:
        ypos -= speed
    return xpos, ypos
 
def zombiesKilledScore(killed):
    value = font_style.render("Zombies Killed: " + str(killed), True, yellow)
    dis.blit(value, [0, 0])
    
def zombiesCleanedScore(cleaned):
    mesg = font_style.render("Zombies Cleaned: " + str(cleaned), True, blue)
    dis.blit(mesg, [dis_width / 3, 0])

# Spawn a new zombie at a random edge of the screen
def spawnZombies():
    global aliveZombies
    randomizer = random.random()

    #Randomly choose side of the screen to spawn zombie
    if randomizer < 0.25:
        xpos = random.randint(-100, 0)
        ypos = random.randint(0, dis_height)
    elif randomizer < 0.5:
        xpos = random.randint(dis_width, dis_width + 100)
        ypos = random.randint(0, dis_height)
    elif randomizer < 0.75:
        xpos = random.randint(0, dis_width)
        ypos = random.randint(-100, 0)
    else:
        xpos = random.randint(0, dis_width)
        ypos = random.randint(dis_height, dis_height + 100)

    new_zombie = Zombie(xpos, ypos, 7, 2, zombieGoalX, zombieGoalY)
    aliveZombies.append(new_zombie)
 
agent = Agent(xpos=300, ypos=400, radius=10, speed=5, health=100, visionRange=110)

def gameLoop():
    global zombiesCleaned
    game_over = False
    current_time = py.time.get_ticks()
    action_time = current_time + 5000
    burn_delay = 1000
    burn_time = 0
    burning = False
 
    while not game_over:
        for event in py.event.get():
            if event.type == py.QUIT:
                game_over = True

        current_time = py.time.get_ticks()
        #Fill background with a color
        dis.fill(brown)

        #Draw and move Zombies
        for zombie in aliveZombies:
            zombie.draw()
            zombie.move()
        for deadZombie in deadZombies:
            deadZombie.draw()

        # Draw and move Projectiles
        for projectile in projectiles[:]:
            projectile.move()
            projectile.draw()
            if not projectile.active:
                projectiles.remove(projectile)

        #Draw target
        py.draw.rect(dis, black, (zombieGoalX, zombieGoalY, 30, 30))
        #Draw Score
        zombiesKilledScore(zombiesKilled)
        zombiesCleanedScore(zombiesCleaned)

        #Draw Agent
        agent.draw()

        #Agent Logic
        if len(deadZombies) == 0:
            agent.patrol()
            agent.scanForZombies(aliveZombies)
        else:
            agent.target = deadZombies[0]
            agent.moveToZombie(agent.target.xpos, agent.target.ypos)
            #Check if agent is close enough to burn the dead zombie
            if(abs(agent.xpos - agent.target.xpos) < 5 and abs(agent.ypos - agent.target.ypos) < 5) and burning == False:
                #Apply artificial delay for burning action
                burn_time = current_time + burn_delay
                burning = True
            #Burn zombies
            if current_time >= burn_time and burning == True:
                agent.burn(agent.target)
                zombiesCleaned += 1
                burning = False

        #Spawn Zombies
        if current_time >= action_time:
            spawnZombies()
            action_time = current_time + random.randint(1000,5000)

        #Update display
        py.display.update() 
        clock.tick(30)
 
    py.quit()
    quit()
 
 
gameLoop()
