#Critters vs Alien Game
import random
import pygame
from time import sleep

class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        super(Projectile, self).__init__()
        self.surf = pygame.Surface((10, 20))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(center=(400,250,))

    def set_position(self,stepx,stepy):
        self.rect.x += stepx
        self.rect.y += stepy
   
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Text1(pygame.sprite.Sprite):
    def __init__(self, size, color, width, height):
        text = "Critter"
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Arial", size)
        self.textSurf = self.font.render(text, 1, color)
        self.image = pygame.Surface((width, height))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect(center=(400,215))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])

class Text2(pygame.sprite.Sprite):
    def __init__(self, size, color, width, height):
        text = "Alien"
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Arial", size)
        self.textSurf = self.font.render(text, 1, color)
        self.image = pygame.Surface((width, height))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect(center=(500,315))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])
         
class Critter(pygame.sprite.Sprite):
    """A virtual pet"""
    def __init__(self,name):
        super(Critter, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(center=(400,250,))
        print ("A new critter has been born")
        self.__name = name
        self.__type = "Basic"
        health_num = random.randint(5,50)
        self.health = health_num

    def talk(self):
        print("Hi. I'm an instance of "+self.__type+" class Critter, called", self.__name)

    def attack(self,alien):
        attack = 5
        print("The",self.__type,"critter attacks the alien")
        alien.deadOrAlive(attack,alien)
    
    def deadOrAlive(self,blast,crit):
        self.health -= blast
        print(crit.get_name()+": I have "+str(self.health)+" health left")
        if self.health <=0:
            self.die(crit)
            self.health = 0
        else:
            self.alive(crit)

    def alive(self,crit):
        print(crit.get_name()+": You can't kill me that easily!!")

    def die(self,crit):
        print("The critter", crit.get_name(), "has been killed")

    def get_name(self):
        return self.__name

    def get_health(self):
        return self.health

class Cat(Critter):
    def __init__(self,name,image_file):
        super(Cat, self).__init__(name)
        self.__name = name
        self.__type = "Cat"
        self.image = pygame.image.load(image_file)
        health_num = random.randint(10,100)
        self.health = health_num

    def talk(self):
       print("Hi. I'm an instance of "+self.__type+" class Critter, called", self.__name)

    def attack(self,alien):
        attack = 10
        print("The Cat attacks the alien")
        alien.deadOrAlive(attack,alien)

class Horse(Critter):
    def __init__(self,name,image_file):
        super(Horse, self).__init__(name)
        self.__name = name
        self.__type = "Horse"
        self.image = pygame.image.load(image_file)
        health_num = random.randint(20,200)
        self.health = health_num

    def talk(self):
       print("Hi. I'm an instance of "+self.__type+" class Critter, called", self.__name)

    def attack(self,alien):
        attack = 7
        print("The Horse attacks the alien")
        alien.deadOrAlive(attack,alien)

class Hamster(Critter):
    def __init__(self,name,image_file):
        super(Hamster, self).__init__(name)
        self.__name = name
        self.__type = "Hamster"
        self.image = pygame.image.load(image_file)
        health_num = random.randint(7,75)
        self.health = health_num

    def talk(self):
       print("Hi. I'm an instance of "+self.__type+" class Critter, called", self.__name)

    def attack(self,alien):
        attack = 7
        print("The Hamster attacks the alien")
        alien.deadOrAlive(attack,alien)
        
class Alien(pygame.sprite.Sprite):
    """A virtual alien"""
    def __init__(self,health,locationX):
        super(Alien, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(center=(locationX,350,))
        self.health = health
        self.__type = "Basic"
        print ("A new",self.__type,"alien has been spawned.")
        

    def blast(self,critter):
        blast = 5
        print("The",self.__type,"alien blasts the critter")
        critter.deadOrAlive(blast,critter)

    def deadOrAlive(self,attack,alien):
        self.health -= attack
        print(self.__type+" Alien: I have "+str(self.health)+" health left")
        if self.health <=0:
            self.die(alien)
            self.health = 0
        else:
            self.alive(alien)

    def alive(self,alien):
        print(self.__type+" Alien : You can't kill me that easily!!")

    def die(self,alien):
        print("The "+self.__type+" alien has been killed")

    def get_health(self):
        return self.health

class Klingon(Alien):
    def __init__(self,health,name):
        self.__name = name
        super().__init__(self, health)
        self.health = health
        self.__type = "Klingon"
        print("A new",self.__type,"alien",name,"has been spawned.")
        
    def blast(self,critter):
        blast = 10
        print("The Klingon "+self.__name+" blasts the critter")
        critter.deadOrAlive(blast,critter)

    def deadOrAlive(self,attack,alien):
        self.health -= attack
        print(self.__type+" Alien: I have "+str(self.health)+" health left")
        if self.health <=0:
            self.die(alien)
        else:
            self.alive(alien)

    def alive(self,alien):
        print(self.__type+" Alien: You can't kill me that easily!!")

    def die(self,alien):
        print("The "+self.__type+" alien "+self.__name+" has been killed")

    def get_name(self):
        return self.__name


def menu():
    print("""1. Create and name critter;
2. Listen to critter;
3. Spawn aliens;
4. Play game;
5. Exit program.""")

def Choice():
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Please enter an integer between 1 & 5")
        menu()
        selected_choice = Choice()
    return choice
    
def spawn_aliens(alien_nums):
    try:
        number_of_aliens = int(input("How many aliens would you like to spawn? "))
    except ValueError:
        print("Invalid number for aliens")
        number_of_aliens = int(input("How many aliens would you like to spawn? "))
    for num in range(number_of_aliens):
        alien_nums.append(num)
    return alien_nums

def play_game(alien_nums,name,critter_type):
    pygame.init()

    win = pygame.display.set_mode((720, 480))
    pygame.display.set_caption("Aliens vs Critters")

    clock = pygame.time.Clock()

    critters = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    aliens = pygame.sprite.Group()

    for item in alien_nums:
        locX = item * 50
        alien = Alien(50,locX)
        aliens.add(alien)
        all_sprites.add(alien)

    if critter_type == "Cat":
        critter = Cat(name,'Cat.png')
    elif critter_type == "Horse":
        critter = Horse(name,'Horse.png')
    elif critter_type == "Hamster":
        critter = Hamster(name,'Hamster.png')

    BackGround = Background('Background.png', [0,0])
    text1 = Text1(6,"white",20,10)
    text2 = Text2(6,"white",20,10)
    projectile = Projectile()
    bgX = 0
    bgX2 = BackGround.image.get_width()

    all_sprites.add(critter)
    all_sprites.add(BackGround)
    all_sprites.add(text1)
    all_sprites.add(text2)
    all_sprites.add(projectile)
    critters.add(critter)

    ax,ay=(400,250)
    bx,by=(500,350)
    dx, dy = (bx - ax, by - ay)
    stepx, stepy = (dx / 50., dy / 50.)

    run = True
    while run:
        bgX -= 1.4
        bgX2 -= 1.4

        win.blit(BackGround.image, (bgX, 0))
        win.blit(BackGround.image, (bgX2, 0))
        pygame.display.update()

        if bgX < BackGround.image.get_width() * -1:
            bgX = BackGround.image.get_width()
    
        if bgX2 < BackGround.image.get_width() * -1:
            bgX2 = BackGround.image.get_width()

        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        win.fill((0,0,0))
        win.blit(critter.surf, critter.rect)
        win.blit(projectile.surf, projectile.rect)
        win.blit(text1.image, text1.rect)
        win.blit(text2.image, text2.rect)
        for alien in aliens:
            win.blit(alien.surf, alien.rect)
        pygame.display.update()
        projectile.set_position(stepx, stepy)
        pygame.display.update()
            
    for alien in aliens:
        critter.attack(alien)
        alien.blast(critter)

    pygame.quit()
         
def game(selected_choice,name,critter_type):
    noexit = True
    while noexit:    
        if selected_choice == 1:
            name = input("Enter a name for your critter: ")
            print("Types of critters are:")
            print("Cat (10-100 health, 10 attack)")
            print("Horse (20-200 health, 7 attack)")
            print("Hamster (7-75 health, 12 attack)") 
            critter_type = input("Enter your choice: ")
            if critter_type == "Cat":
                print("Your critter is a Cat")
            elif critter_type == "Horse":
                print("Your critter is a Horse")
            elif critter_type == "Hamster":
                print("Your critter is a Hamster")
            else:
                print("Please enter a valid option")
                critter_type = input("Enter your choice: ")
            menu()
            selected_choice = Choice()
            game(selected_choice,name,critter_type)
            return name, critter_type
        elif selected_choice == 2:
            critter.talk()
            menu()
            selected_choice = Choice()
            game(selected_choice,name,critter_type)
        elif selected_choice == 3:
            spawn_aliens(alien_nums)
            menu()
            selected_choice = Choice()
            game(selected_choice,name,critter_type)                                  
        elif selected_choice == 4:
            play_game(alien_nums, name, critter_type)
            menu()
            selected_choice = Choice()
            game(selected_choice,name,critter_type)
        elif selected_choice == 5:
            noexit = False
            break
        else:
            print("Please enter an integer between 1 & 5")
            menu()
            selected_choice = Choice()
            game(selected_choice,name,critter_type)

#Main
name = ""
critter_type = "Basic"
alien_nums = []
menu()
selected_choice = Choice()
game(selected_choice,name,critter_type)
"""critter1 = Critter("Tom")
critter2 = Cat("Gabriel")

critter1.talk()
critter2.talk()

alien1 = Alien(5)

alien2 = Klingon(100,"Dave")

c_health1 = critter1.get_health()
c_health2 = critter2.get_health()
a_health1 = alien1.get_health()
a_health2 = alien2.get_health()
while c_health1 >= 0 or c_health2 >= 0 or a_health1 >= 0 or a_health2 >= 0:
    print("Aliens turn!")
    alien1.blast(critter1)
    alien2.blast(critter2)
    c_health1 = critter1.get_health()
    c_health2 = critter2.get_health()
    print(c_health1, c_health2)
    sleep(1)
    print("Critters turn!")
    critter1.attack(alien1)
    critter2.attack(alien2)
    a_health1 = alien1.get_health()
    a_health2 = alien2.get_health()
    print(a_health1, a_health2)
    sleep(1)
    if c_health1 <= 0:
        break
    if c_health2 <= 0:
        break
    if a_health1 <= 0:
        break
    if a_health2 <= 0:
        break"""
