#Critters vs Alien Game
import random
import pygame
from time import sleep

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

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
        super().__init__(name)
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
        super().__init__(name)
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
        super().__init__(name)
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
    def __init__(self,health,image_file):
        super(Alien, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((255,255,255))
        self.image = pygame.image.load(image_file)
        self.rect = self.surf.get_rect(center=(500,350,))
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
        super().__init__(health)
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

def choice():
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Please enter an integer between 1 & 5")
        menu(critter)
    return choice
    
def spawn_aliens(aliens):
    aliens = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    try:
        number_of_aliens = int(input("How many aliens would you like to spawn? "))
    except ValueError:
        print("Invalid number for aliens")
        number_of_aliens = int(input("How many aliens would you like to spawn? "))
    for num in range(number_of_aliens):
        alien = Alien(50)
        aliens.add(alien)
        all_sprites.add(alien)
    return aliens, all_sprites

def play_game(aliens,critter):
    pygame.init()

    win = pygame.display.set_mode((720, 480))
    pygame.display.set_caption("Critters vs Aliens")

    clock = pygame.time.Clock()
    
    critters = pygame.sprite.Group()

    background = Background('Background.png', [0,0])

    all_sprites.add(critter)
    all_sprites.add(background)
    critters.add(critter)

    run = True
    while run:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        win.fill((0,0,0))
        win.blit(background.image, background.rect)
        win.blit(critter.surf, critter.rect)
    
        for num in range(0,len(aliens)):
            critter.attack(aliens[num])
        for alien in aliens:
            win.blit(alien.surf, alien.rect)
            alien.blast(critter)
            
def game(selected_choice,critter):
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
                critter = Cat(name,'Cat.png')
            elif critter_type == "Horse":
                critter = Horse(name,'Horse.png')
            elif critter_type == "Hamster":
                critter = Hamster(name,'Hamster.png')
            else:
                print("Please enter a valid option")
                critter_type = input("Enter your choice: ")
            menu()
            selected_choice = choice()
            game(selected_choice,critter)
        elif selected_choice == 2:
            critter.talk()
            menu()
            selected_choice = choice()
            game(selected_choice,critter)
        elif selected_choice == 3:
            spawn_aliens(aliens)
            menu()
            selected_choice = choice()
            game(selected_choice,critter)                                  
        elif selected_choice == 4:
            play_game(aliens, critter)
            menu()
            selected_choice = choice()
            game(selected_choice,critter)
        elif selected_choice == 5:
            noexit = False
            break
        else:
            print("Please enter an integer between 1 & 5")
            menu()
            selected_choice = choice()
            game(selected_choice,critter)

#Main
critter = Critter("")
aliens = []
menu()
selected_choice = choice()
game(selected_choice,critter)
