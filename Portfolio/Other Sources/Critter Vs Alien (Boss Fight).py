import random
import sys

class Critter(object):
    """A Virtual pet"""
    def __init__(self, name, health, max_health):
        self.name = name
        self.health = health
        self.max_health = max_health
    def birth(self):
        print("\n" + self.name, "has been born!")
        print("'Hi. I'm", self.name + "!'")
        print("'I have been born!'")
        input()
    def blast_damage(self):
        dodge_chance = random.randint(1,8)
        if dodge_chance == 8:
            print(self.name, "dodged the blast and took no damage!")
            print(self.name, "has", self.health, "HP remaining!")
        else:
            damage_output = random.randint(19,21)
            self.health -= damage_output
            if self.health < 0:
                self.health = 0
            print(self.name, "took", damage_output, "damage from the blast!")
            print(self.name, "has", self.health, "HP remaining!")
            if self.health == 0:
                input()
                print(self.name, "collapsed to the ground!")
                print("'Uhhh, I don't feel so good.'")
                print(self.name, "became unconscious!")
                input()
                print("The alien laughs maniacally!")
                print("Mwahahaha!")
                print("You lost the battle!")
    def lifesteal_damage(self):
        dodge_chance = random.randint(1,8)
        if dodge_chance == 8:
            print(self.name, "dodged the lifesteal and took no damage!")
            print(self.name, "has", self.health, "HP remaining!")
        else:
            damage_output = random.randint(14,16)
            self.health -= damage_output
            if self.health < 0:
                self.health = 0
            alien1.health += damage_output
            if alien1.health > alien1.max_health:
                alien1.health = alien1.max_health
            print(self.name, "took", damage_output, "damage from the lifesteal!")
            print(self.name, "has", self.health, "HP remaining!")
            if self.health == 0:
                input()
                print(self.name, "collapsed to the ground!")
                print("'Uhhh, I don't feel so good.'")
                print(self.name, "became unconscious!")
                input()
                print("The alien laughs maniacally!")
                print("Mwahahaha!")
                print("You lost the battle!")
            else:
                print("The alien recovered", damage_output, "HP and now has", alien1.health, "HP remaining!")
    def multishot_damage(self):
        shots_hit = random.randint(0,3)
        if shots_hit == 0:
            print(self.name, "dodged the multi-shot and took no damage!")
            print(self.name, "has", self.health, "HP remaining!")
        else:
            damage_output = random.randint(11,13)
            self.health -= (shots_hit * damage_output)
            if self.health < 0:
                self.health = 0
            print(self.name, "got hit by the multi-shot", shots_hit, "times!")
            print(self.name, "took", shots_hit * damage_output, "damage from the multi-shot!")
            print(self.name, "has", self.health, "HP remaining!")
            if self.health == 0:
                input()
                print(self.name, "collapsed to the ground!")
                print("'Uhhh, I don't feel so good.'")
                print(self.name, "became unconscious!")
                input()
                print("The alien laughs maniacally!")
                print("Mwahahaha!")
                print("You lost the battle!")
    def hyper_laser_damage(self):
        dodge_chance = random.randint(1,10)
        if dodge_chance == 10:
            print("Surprisingly,", self.name, "dodged the hyper-laser and took no damage!")
            print(self.name, "has", self.health, "HP remaining!")
        else:
            damage_output = random.randint(49,51)
            self.health -= damage_output
            if self.health < 0:
                self.health = 0
            print("Ouch!", self.name, "took", damage_output, "damage from the hyper-laser!")
            print(self.name, "has", self.health, "HP remaining!")
            if self.health == 0:
                input()
                print(self.name, "collapsed to the ground!")
                print("'Uhhh, I don't feel so good.'")
                print(self.name, "became unconscious!")
                input()
                print("The alien laughs maniacally!")
                print("Mwahahaha!")
                print("You lost the battle!")
    def electric_shock_damage(self):
        damage_output = random.randint(9,11)
        self.health -= damage_output
        if self.health < 0:
            self.health = 0
        print(self.name, "took", damage_output, "damage from the electric shock!")
        print(self.name, "has", self.health, "HP remaining!")
        if self.health == 0:
            input()
            print(self.name, "collapsed to the ground!")
            print("'Uhhh, I don't feel so good.'")
            print(self.name, "became unconscious!")
            input()
            print("The alien laughs maniacally!")
            print("Mwahahaha!")
            print("You lost the battle!")
    def scratch(self, alien):
            print("\n" + self.name, "used scratch!")
            alien.scratch_damage()
    def bite(self, alien):
        print("\n" + self.name, "used bite!")
        alien.bite_damage()
    def tail_attack(self, alien):
        print("\n" + self.name, "used tail attack!")
        alien.tail_attack_damage()
    def recover(self):
        self.health += 40
        if self.health > self.max_health:
            self.health = self.max_health
        print("\n" + self.name, "used recover!")
        print(self.name, "recovered 40 HP")
        print(self.name, "has", self.health, "health remaining!")
    def critter_stampede(self, alien):
        input("\n" + self.name + " unleashed their ultimate ability, critter stampede! \nMultiple critter friends rush towards the alien foe!")
        alien.critter_stampede_damage()
    def get_name(self):
        return self.name

class Alien(object):
    """A Killer"""
    def __init__(self, health, max_health):
        self.health = health
        self.max_health = max_health
        print("The alien has been created and wants to destroy the newborn", crit1.get_name() + "!")
        print("The alien has", self.health, "HP!")
        print(crit1.get_name(), "has", crit1.health, "HP!")
        print(crit1.get_name(), "must defeat the alien to win!")
        input()
    def blast(self, crit):
            print("The alien used blast!")
            crit.blast_damage()
    def lifesteal(self, crit):
        print("The alien used lifesteal!")
        crit.lifesteal_damage()
    def multishot(self, crit):
        print("The alien used multi-shot!")
        crit.multishot_damage()
    def hyper_laser(self, crit):
        input("The alien used hyper-laser! \nThe hyper-laser heads straight towards " + crit1.get_name() + " at full speed!")
        crit.hyper_laser_damage()
    def electric_shock(self, crit):
        print("The alien used electric shock!")
        crit.electric_shock_damage()
    def scratch_damage(self):
        dodge_chance = random.randint(1,7)
        if dodge_chance == 7:
            print("The alien dodged the scratch and took no damage!")
            print("The alien has", self.health, "HP remaining!")
        else:
            damage_output = random.randint(16,18)
            self.health -= damage_output
            if self.health < 0:
                self.health = 0
            print("The alien took", damage_output, "damage from the scratch!")
            print("The alien has", self.health, "HP remaining!")
            if self.health == 0:
                input()
                print("The alien collapses to the ground!")
                print("The alien is dead!")
                input()
                print(crit1.get_name(), "joyfully does the default fortnite dance!")
                print("'HOORAY!'")
                print("You won the battle!")
    def bite_damage(self):
        dodge_chance = random.randint(1,3)
        if dodge_chance == 3:
            print("The alien dodged the bite and took no damage!")
            print("The alien has", self.health, "HP remaining!")
        else:
            damage_output = random.randint(29,31)
            self.health -= damage_output
            if self.health < 0:
                self.health = 0
            crit1.health += 5
            if crit1.health > crit1.max_health:
            	crit1.health = crit1.max_health
            print("The alien took", damage_output, "damage from the bite!")
            print("The alien has", self.health, "HP remaining!")
            if self.health == 0:
                input()
                print("The alien collapses to the ground!")
                print("The alien is dead!")
                input()
                print(crit1.get_name(), "joyfully does the default fortnite dance!")
                print("'HOORAY!'")
                print("You won the battle!")
            else:
            	print(crit1.get_name(), "recovered 5 HP and now has", crit1.health, "HP remaining!")
    def tail_attack_damage(self):
        dodge_chance = random.randint(1,7)
        if dodge_chance == 7:
            print("The alien dodged the tail attack and took no damage!")
            print("The alien has", self.health, "HP remaining!")
        else:
            crit_chance = random.randint(1,3)
            if crit_chance == 3:
                damage_output = random.randint(39,41)
                self.health -= damage_output
                if self.health < 0:
                    self.health = 0
                print("A critical hit! The alien took", damage_output, "damage from the tail attack!")
                print("The alien has", self.health, "HP remaining!")
                if self.health == 0:
                    input()
                    print("The alien collapses to the ground!")
                    print("The alien is dead!")
                    input()
                    print(crit1.get_name(), "joyfully does the default fortnite dance!")
                    print("'HOORAY!'")
                    print("You won the battle!")
            else:
                damage_output = random.randint(9,11)
                self.health -= damage_output
                if self.health < 0:
                    self.health = 0
                print("The alien took", damage_output, "damage from the tail attack!")
                print("The alien has", self.health, "HP remaining!")
                if self.health == 0:
                    input()
                    print("The alien collapses to the ground!")
                    print("The alien is dead!")
                    input()
                    print(crit1.get_name(), "joyfully does the default fortnite dance!")
                    print("'HOORAY!'")
                    print("You won the battle!")
    def critter_stampede_damage(self):
        dodge_chance = random.randint(1,10)
        if dodge_chance == 10:
            print("Surprisingly, the alien dodged the critter stampede and took no damage!")
            print("The alien has", self.health, "HP remaining!")
        else:
            damage_output = random.randint(99,101)
            self.health -= damage_output
            if self.health < 0:
                self.health = 0
            print("OOF! The alien took", damage_output, "damage from the critter stampede!")
            print("The alien has", self.health, "HP remaining!")
            if self.health == 0:
                input()
                print("The alien collapses to the ground!")
                print("The alien is dead!")
                input()
                print(crit1.get_name(), "joyfully does the default fortnite dance!")
                print("'HOORAY!'")
                print("You won the battle!")
        
# main

def start_combat():
    recover_cooldown = 3
    critter_stampede_cooldown = 6
    hyper_laser_charge_time = 0
    learn = input("Would you like to learn the alien's moveset before we begin? (Yes/No): ")
    while learn != "Yes" and learn != "yes" and learn != "No" and learn != "no":
        learn = input("Just enter yes or no... (Yes/No): ")
    if learn == "Yes" or learn == "yes":
        print("\n1. Blast - deals ~20 damage. \n2. Lifesteal - deals ~15 damage, but heals the alien for that much damage. \n3. Multi-shot - can hit up to 3 times, with each hit dealing ~12 damage. \n4. Hyper-laser - deals ~50 damage, but requires 3 turns to charge up. \n5. Electric Shot - deals ~10 damage, but is undodgeable, and may stun for 1 turn.")
        input()
        print("Let the battle begin!")
        input()
    elif learn == "No" or learn == "no":
        print("\nLet the battle begin!")
        input()
    while True:
        recover_cooldown -= 1
        if recover_cooldown < 0:
            recover_cooldown = 0
        critter_stampede_cooldown -= 1
        if critter_stampede_cooldown < 0:
            critter_stampede_cooldown = 0
        print("1. Scratch - deals ~17 damage. \n2. Bite - deals ~30 damage, heals for 5 HP but has more likely chances of being dodged. \n3. Tail Attack - deals ~10 damage, but has a chance of doing ~30 extra damage. \n4. Recover - heals for 40 HP, and requires a cooldown of 3 turns. \n5. Critter Stampede - deals ~100 damage, and requires a cooldown of 6 turns.\n")
        print(crit1.get_name(), "HP:", crit1.health, "\nAlien HP:", alien1.health, "\nRecover Cooldown:", recover_cooldown, "\nCritter Stampede Cooldown:", critter_stampede_cooldown)
        choice = input("\nPlease enter the number of which move " + crit1.get_name() + " should use (1-5): ")
        while choice != "1" and choice != "2" and choice != "3" and choice != "4" and choice != "5":
            choice = input("Please enter a valid choice! (1-5): ")
        while choice == "4" and recover_cooldown != 0:
                choice = input("\n" + crit1.get_name() + " still needs to wait " + str(recover_cooldown) + " more turns to use recover!\nPlease enter a different number of your choice (1-5): ")
                while choice != "1" and choice != "2" and choice != "3" and choice != "4" and choice != "5":
                    choice = input("Please enter a valid choice!: ")
                while choice == "5" and critter_stampede_cooldown != 0:
                    choice = input("\n" + crit1.get_name() + " still needs to wait " + str(critter_stampede_cooldown) + " more turns to use critter stampede!\nPlease enter a different number of your choice (1-5): ")
                    while choice != "1" and choice != "2" and choice != "3" and choice != "4" and choice != "5":
                        choice = input("Please enter a valid choice! (1-5): ")
                    if choice == "5" and critter_stampede_cooldown == 0:
                        critter_stampede_cooldown = 6
                        crit1.critter_stampede(alien1)
                        input()
                        if alien1.health == 0:
                            break
        if choice == "4" and recover_cooldown == 0:
            recover_cooldown = 3
            crit1.recover()
            input()
        while choice == "5" and critter_stampede_cooldown != 0:
            choice = input("\n" + crit1.get_name() + " still needs to wait " + str(critter_stampede_cooldown) + " more turns to use critter stampede!\nPlease enter a different number of your choice (1-5): ")
            while choice != "1" and choice != "2" and choice != "3" and choice != "4" and choice != "5":
                choice = input("Please enter a valid choice!: ")
            while choice == "4" and recover_cooldown != 0:
                choice = input("\n" + crit1.get_name() + " still needs to wait " + str(recover_cooldown) + " more turns to use recover!\nPlease enter a different number of your choice (1-5): ")
                while choice != "1" and choice != "2" and choice != "3" and choice != "4" and choice != "5":
                    choice = input("Please enter a valid choice! (1-5): ")
            if choice == "4" and recover_cooldown == 0:
                recover_cooldown = 3
                crit1.recover()
                input()
        if choice == "5" and critter_stampede_cooldown == 0:
            critter_stampede_cooldown = 6
            crit1.critter_stampede(alien1)
            input()
            if alien1.health == 0:
                break
        if choice == "1":
            crit1.scratch(alien1)
            input()
            if alien1.health == 0:
                break
        if choice == "2":
            crit1.bite(alien1)
            input()
            if alien1.health == 0:
                break
        if choice == "3":
            crit1.tail_attack(alien1)
            input()
            if alien1.health == 0:
                break
        alien_choice = random.randint(1,5)
        if hyper_laser_charge_time == 2 or hyper_laser_charge_time == 1:
            hyper_laser_charge_time -= 1
            if hyper_laser_charge_time == 0:
                alien1.hyper_laser(crit1)
                input()
                if crit1.health == 0:
                	break
            else:
                print("The alien continues charging up it's hyper-laser for 1 more turn!")
                input()
        else:
            if alien_choice == 1:
                alien1.blast(crit1)
                input()
                if crit1.health == 0:
                    break
            if alien_choice == 2:
                alien1.lifesteal(crit1)
                input()
                if crit1.health == 0:
                    break
            if alien_choice == 3:
                alien1.multishot(crit1)
                input()
                if crit1.health == 0:
                    break
            if alien_choice == 4:
                hyper_laser_charge_time = 2
                print("The alien begins to charge up it's hyper-laser for 2 turns!")
                input()
            if alien_choice == 5:
                alien1.electric_shock(crit1)
                input()
                if crit1.health == 0:
                    break
                else:
                    stun_chance = random.randint(1,3)
                    if stun_chance == 3:
                        print(crit1.get_name(), "became stunned from the electric shock!", crit1.get_name(), "cannot fight this turn!")
                        input()
                        alien_choice = random.randint(1,4)
                        if alien_choice == 1:
                            alien1.blast(crit1)
                            input()
                            if crit1.health == 0:
                                break
                        if alien_choice == 2:
                            alien1.lifesteal(crit1)
                            input()
                            if crit1.health == 0:
                                break
                        if alien_choice == 3:
                            alien1.multishot(crit1)
                            input()
                            if crit1.health == 0:
                                break
                        if alien_choice == 4:
                            hyper_laser_charge_time = 2
                            print("The alien begins to charge up it's hyper-laser for 2 turns!")
                            input()
                            
print("Welcome to the 'Critter Vs Alien (Boss Fight)' program!")
input()
print("A critter is just about to be born!")
crit1_name = input("Please enter a name for the critter: ")
while crit1_name == "" or crit1_name[0] == " ":
    if crit1_name == "":
        crit1_name = input("\nAhem... You need to enter a name for the critter: ")
    elif crit1_name[0] == " ":
        crit1_name = input("\nPlease enter a name (without a space at the beginning) for the critter: ")
crit1 = Critter(crit1_name, 0, 0)
crit1.birth()

print("An alien is about to be created!")
alien1_difficulty = input("Please enter the difficulty for this alien (Easy/Normal/Hard/Insane/Impossible): ")

while alien1_difficulty != "Easy" and alien1_difficulty != "easy" and alien1_difficulty != "Normal" and alien1_difficulty != "normal" and alien1_difficulty != "Hard" and alien1_difficulty != "hard" and alien1_difficulty != "Insane" and alien1_difficulty != "insane" and alien1_difficulty != "Impossible" and alien1_difficulty != "impossible":
    alien1_difficulty = input("\nAhem... \nPlease enter a VALID difficulty for this alien (Easy/Normal/Hard/Insane/Impossible): ")

if alien1_difficulty == "Easy" or alien1_difficulty == "easy":
    print("\nYou have selected easy mode!")
    input()
    crit1 = Critter(crit1_name, 150, 150)
    alien1 = Alien(200, 200)
    start_combat()
elif alien1_difficulty == "Normal" or alien1_difficulty == "normal":
    print("\nYou have selected normal mode!")
    input()
    crit1 = Critter(crit1_name, 145, 145)
    alien1 = Alien(350, 350)
    start_combat()
elif alien1_difficulty == "Hard" or alien1_difficulty == "hard":
    print("\nYou have selected hard mode!")
    input()
    crit1 = Critter(crit1_name, 140, 140)
    alien1 = Alien(500, 500)
    start_combat()
elif alien1_difficulty == "Insane" or alien1_difficulty == "insane":
    print("\nYou have selected insane mode!")
    input()
    crit1 = Critter(crit1_name, 135, 135)
    alien1 = Alien(650, 650)
    start_combat()
elif alien1_difficulty == "Impossible" or alien1_difficulty == "impossible":
    print("\nYou have selected impossible mode!")
    input()
    crit1 = Critter(crit1_name, 130, 130)
    alien1 = Alien(800, 800)
    start_combat()

print("Thank you for using the 'Critter Vs Alien (Boss Fight)' program!")
input("Press the enter key once more to exit the program.")
exit()
