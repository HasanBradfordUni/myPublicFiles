import random
import time
import json
import os

"""
🕹️ Turn-Based RPG Battle Engine
A comprehensive text-based RPG featuring:
- Object-oriented character system with inheritance
- Dynamic inventory and item management
- Status effects and turn-based combat
- Enemy AI with decision-making
- Experience and leveling system
- Save/load functionality
- Modular design with clear separation of concerns
"""

# ═══════════════════════════════════════════════════════════════════════════════
# STATUS EFFECTS MODULE
# ═══════════════════════════════════════════════════════════════════════════════

class StatusEffect:
    """Base class for all status effects."""
    def __init__(self, name, duration, description=""):
        self.name = name
        self.duration = duration
        self.description = description
    
    def apply_effect(self, character):
        """Apply the effect to a character. Override in subclasses."""
        pass
    
    def on_expire(self, character):
        """Called when the effect expires. Override if needed."""
        pass

class Poison(StatusEffect):
    """Poison status effect that deals damage over time."""
    def __init__(self, duration, damage_per_turn=8):
        super().__init__("Poison", duration, f"Takes {damage_per_turn} damage per turn")
        self.damage_per_turn = damage_per_turn
    
    def apply_effect(self, character):
        character.hp = max(0, character.hp - self.damage_per_turn)
        return f"💚 {character.name} takes {self.damage_per_turn} poison damage!"

class Stun(StatusEffect):
    """Stun status effect that prevents actions."""
    def __init__(self, duration):
        super().__init__("Stun", duration, "Cannot perform actions")
    
    def apply_effect(self, character):
        return f"😵 {character.name} is stunned and cannot act!"

class Regeneration(StatusEffect):
    """Regeneration status effect that heals over time."""
    def __init__(self, duration, heal_per_turn=12):
        super().__init__("Regeneration", duration, f"Heals {heal_per_turn} HP per turn")
        self.heal_per_turn = heal_per_turn
    
    def apply_effect(self, character):
        old_hp = character.hp
        character.heal(self.heal_per_turn)
        healed = character.hp - old_hp
        return f"💚 {character.name} regenerates {healed} HP!"

class Strength(StatusEffect):
    """Strength buff that increases attack power."""
    def __init__(self, duration, attack_bonus=10):
        super().__init__("Strength", duration, f"+{attack_bonus} attack power")
        self.attack_bonus = attack_bonus
        self.applied = False
    
    def apply_effect(self, character):
        if not self.applied:
            character.attack += self.attack_bonus
            self.applied = True
            return f"💪 {character.name} feels stronger!"
        return None
    
    def on_expire(self, character):
        if self.applied:
            character.attack -= self.attack_bonus
            return f"💪 {character.name}'s strength boost fades."

class Shield(StatusEffect):
    """Shield buff that increases defense."""
    def __init__(self, duration, defense_bonus=8):
        super().__init__("Shield", duration, f"+{defense_bonus} defense")
        self.defense_bonus = defense_bonus
        self.applied = False
    
    def apply_effect(self, character):
        if not self.applied:
            character.defense += self.defense_bonus
            self.applied = True
            return f"🛡️ {character.name} is protected by a magical shield!"
        return None
    
    def on_expire(self, character):
        if self.applied:
            character.defense -= self.defense_bonus
            return f"🛡️ {character.name}'s shield dissolves."

# ═══════════════════════════════════════════════════════════════════════════════
# ITEM AND INVENTORY MODULE
# ═══════════════════════════════════════════════════════════════════════════════

class Item:
    """Base class for all items."""
    def __init__(self, name, description="", value=0):
        self.name = name
        self.description = description
        self.value = value
    
    def use(self, user, target=None):
        """Use the item. Override in subclasses."""
        return f"{user.name} uses {self.name}."
    
    def can_use_in_battle(self):
        """Whether this item can be used during battle."""
        return True

class HealthPotion(Item):
    """Restores health points."""
    def __init__(self, heal_amount=40):
        super().__init__("Health Potion", f"Restores {heal_amount} HP", 25)
        self.heal_amount = heal_amount
    
    def use(self, user, target=None):
        old_hp = user.hp
        user.heal(self.heal_amount)
        actual_heal = user.hp - old_hp
        return f"❤️ {user.name} drinks a Health Potion and recovers {actual_heal} HP!"

class ManaPotion(Item):
    """Restores mana points."""
    def __init__(self, mana_amount=30):
        super().__init__("Mana Potion", f"Restores {mana_amount} MP", 20)
        self.mana_amount = mana_amount
    
    def use(self, user, target=None):
        old_mp = user.mp
        user.restore_mp(self.mana_amount)
        actual_restore = user.mp - old_mp
        return f"💙 {user.name} drinks a Mana Potion and recovers {actual_restore} MP!"

class Antidote(Item):
    """Cures poison status effect."""
    def __init__(self):
        super().__init__("Antidote", "Cures poison status", 15)
    
    def use(self, user, target=None):
        removed = user.remove_status_effect(Poison)
        if removed:
            return f"🟢 {user.name} uses an Antidote and cures poison!"
        else:
            return f"🟢 {user.name} uses an Antidote, but wasn't poisoned."

class Bomb(Item):
    """Explosive item that damages enemies."""
    def __init__(self, damage=35):
        super().__init__("Bomb", f"Deals {damage} damage to enemy", 30)
        self.damage = damage
    
    def use(self, user, target):
        if target and target.is_alive():
            damage_dealt = target.take_damage(self.damage)
            return f"💥 {user.name} throws a bomb at {target.name} for {damage_dealt} damage!"
        return f"💥 {user.name} wastes a bomb on nothing!"

class StrengthPotion(Item):
    """Grants temporary strength boost."""
    def __init__(self, duration=5):
        super().__init__("Strength Potion", f"Increases attack for {duration} turns", 40)
        self.duration = duration
    
    def use(self, user, target=None):
        user.add_status_effect(Strength(self.duration))
        return f"💪 {user.name} drinks a Strength Potion and feels empowered!"

class ShieldPotion(Item):
    """Grants temporary defense boost."""
    def __init__(self, duration=4):
        super().__init__("Shield Potion", f"Increases defense for {duration} turns", 35)
        self.duration = duration
    
    def use(self, user, target=None):
        user.add_status_effect(Shield(self.duration))
        return f"🛡️ {user.name} drinks a Shield Potion and gains magical protection!"

class RegenerationElixir(Item):
    """Grants health regeneration over time."""
    def __init__(self, duration=6):
        super().__init__("Regeneration Elixir", f"Regenerates health for {duration} turns", 50)
        self.duration = duration
    
    def use(self, user, target=None):
        user.add_status_effect(Regeneration(self.duration))
        return f"💚 {user.name} drinks a Regeneration Elixir and begins to heal over time!"

class Weapon(Item):
    """Weapon that can be equipped to increase attack."""
    def __init__(self, name, attack_bonus, description=""):
        super().__init__(name, description, attack_bonus * 10)
        self.attack_bonus = attack_bonus
        self.equipped = False
    
    def can_use_in_battle(self):
        return False  # Weapons are equipped, not used
    
    def equip(self, character):
        """Equip this weapon to a character."""
        if character.equipped_weapon:
            character.unequip_weapon()
        character.equipped_weapon = self
        character.attack += self.attack_bonus
        self.equipped = True
        return f"⚔️ {character.name} equips {self.name}!"
    
    def unequip(self, character):
        """Unequip this weapon from a character."""
        if self.equipped:
            character.attack -= self.attack_bonus
            character.equipped_weapon = None
            self.equipped = False
            return f"⚔️ {character.name} unequips {self.name}."

class IronSword(Weapon):
    """Basic iron sword."""
    def __init__(self):
        super().__init__("Iron Sword", 15, "A sturdy iron blade (+15 attack)")

class SteelSword(Weapon):
    """Upgraded steel sword."""
    def __init__(self):
        super().__init__("Steel Sword", 25, "A sharp steel blade (+25 attack)")

class Inventory:
    """Manages character inventory."""
    def __init__(self, max_capacity=20):
        self.items = []
        self.max_capacity = max_capacity
    
    def add_item(self, item):
        """Add an item to inventory."""
        if len(self.items) < self.max_capacity:
            self.items.append(item)
            return True
        return False  # Inventory full
    
    def remove_item(self, item):
        """Remove an item from inventory."""
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def has_item(self, item_type):
        """Check if inventory contains item of specified type."""
        return any(isinstance(item, item_type) for item in self.items)
    
    def get_item(self, item_type):
        """Get first item of specified type."""
        for item in self.items:
            if isinstance(item, item_type):
                return item
        return None
    
    def get_usable_items(self):
        """Get all items that can be used in battle."""
        return [item for item in self.items if item.can_use_in_battle()]
    
    def get_weapons(self):
        """Get all weapons in inventory."""
        return [item for item in self.items if isinstance(item, Weapon)]
    
    def count_items(self):
        """Return count of each item type."""
        item_counts = {}
        for item in self.items:
            item_name = item.name
            item_counts[item_name] = item_counts.get(item_name, 0) + 1
        return item_counts

# ═══════════════════════════════════════════════════════════════════════════════
# CHARACTER MODULE
# ═══════════════════════════════════════════════════════════════════════════════

class Character:
    """Base character class with core stats and functionality."""
    def __init__(self, name, hp=100, mp=50, attack=20, defense=10, speed=10):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.base_attack = attack
        self.attack = attack
        self.base_defense = defense
        self.defense = defense
        self.speed = speed
        self.status_effects = []
        self.inventory = Inventory()
        self.equipped_weapon = None
        self.critical_chance = 0.1  # 10% chance for critical hits
    
    def take_damage(self, damage):
        """Apply damage to character after defense calculation."""
        # Critical hit check for attacker would be handled by battle system
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def heal(self, amount):
        """Heal the character up to max HP."""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def restore_mp(self, amount):
        """Restore mana points up to max MP."""
        self.mp = min(self.max_mp, self.mp + amount)
    
    def is_alive(self):
        """Check if character is alive."""
        return self.hp > 0
    
    def add_status_effect(self, effect):
        """Add a status effect, replacing existing effects of same type."""
        # Remove existing effects of same type
        self.status_effects = [e for e in self.status_effects if type(e) != type(effect)]
        self.status_effects.append(effect)
    
    def remove_status_effect(self, effect_type):
        """Remove all status effects of specified type."""
        removed = any(isinstance(e, effect_type) for e in self.status_effects)
        self.status_effects = [e for e in self.status_effects if not isinstance(e, effect_type)]
        return removed
    
    def has_status_effect(self, effect_type):
        """Check if character has specified status effect."""
        return any(isinstance(e, effect_type) for e in self.status_effects)
    
    def process_status_effects(self):
        """Process all active status effects and return messages."""
        messages = []
        effects_to_remove = []
        
        for effect in self.status_effects:
            # Apply effect
            message = effect.apply_effect(self)
            if message:
                messages.append(message)
            
            # Decrease duration
            effect.duration -= 1
            if effect.duration <= 0:
                effects_to_remove.append(effect)
        
        # Remove expired effects
        for effect in effects_to_remove:
            expire_message = effect.on_expire(self)
            if expire_message:
                messages.append(expire_message)
            self.status_effects.remove(effect)
        
        return messages
    
    def get_status_summary(self):
        """Get a summary of current status effects."""
        if not self.status_effects:
            return "None"
        return ", ".join([f"{e.name}({e.duration})" for e in self.status_effects])
    
    def use_item(self, item, target=None):
        """Use an item from inventory."""
        if item in self.inventory.items:
            result = item.use(self, target)
            self.inventory.remove_item(item)
            return result, True
        return f"{self.name} doesn't have {item.name}!", False
    
    def equip_weapon(self, weapon):
        """Equip a weapon from inventory."""
        if weapon in self.inventory.items:
            return weapon.equip(self)
        return f"{weapon.name} not in inventory!"
    
    def unequip_weapon(self):
        """Unequip current weapon."""
        if self.equipped_weapon:
            message = self.equipped_weapon.unequip(self)
            return message
        return f"{self.name} has no weapon equipped."

class Player(Character):
    """Player character with leveling and special abilities."""
    def __init__(self, name):
        super().__init__(name, hp=120, mp=60, attack=25, defense=12, speed=12)
        self.level = 1
        self.experience = 0
        self.experience_to_next = 100
        self.skill_points = 0
        
        # Starting inventory
        self.inventory.add_item(HealthPotion())
        self.inventory.add_item(HealthPotion())
        self.inventory.add_item(ManaPotion())
        self.inventory.add_item(Antidote())
        self.inventory.add_item(IronSword())
    
    def gain_experience(self, amount):
        """Gain experience and level up if threshold reached."""
        self.experience += amount
        messages = []
        
        while self.experience >= self.experience_to_next:
            self.experience -= self.experience_to_next
            old_level = self.level
            self.level_up()
            messages.append(f"🌟 {self.name} levels up! Level {old_level} → {self.level}")
            messages.append(f"💪 Stats increased! +{self.get_stat_gains()} to all stats")
        
        return messages
    
    def level_up(self):
        """Increase level and stats."""
        self.level += 1
        stat_gain = self.get_stat_gains()
        
        # Increase base stats
        self.max_hp += stat_gain * 8
        self.max_mp += stat_gain * 5
        self.base_attack += stat_gain * 2
        self.base_defense += stat_gain
        self.speed += 1
        
        # Update current stats (preserve temporary modifiers)
        current_attack_mod = self.attack - self.base_attack + stat_gain * 2
        current_defense_mod = self.defense - self.base_defense + stat_gain
        self.attack = self.base_attack + current_attack_mod
        self.defense = self.base_defense + current_defense_mod
        
        # Full heal on level up
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # Increase experience requirement
        self.experience_to_next = int(self.experience_to_next * 1.2)
        self.skill_points += 1
    
    def get_stat_gains(self):
        """Calculate stat gains per level."""
        return max(1, self.level // 3)
    
    def special_attack(self, target):
        """Perform special attack if enough MP."""
        mp_cost = 20
        if self.mp >= mp_cost:
            self.mp -= mp_cost
            base_damage = int(self.attack * 1.8)
            
            # Check for critical hit
            is_critical = random.random() < self.critical_chance * 2  # Double crit chance for special
            if is_critical:
                base_damage = int(base_damage * 1.5)
            
            damage_dealt = target.take_damage(base_damage)
            
            crit_text = " 💥 CRITICAL HIT!" if is_critical else ""
            return damage_dealt, f"✨ {self.name} unleashes a devastating special attack!{crit_text}"
        return 0, f"❌ {self.name} doesn't have enough MP for special attack! (Need {mp_cost} MP)"
    
    def focus(self):
        """Restore MP instead of attacking."""
        mp_restore = 15 + self.level
        old_mp = self.mp
        self.restore_mp(mp_restore)
        actual_restore = self.mp - old_mp
        return f"🧘 {self.name} focuses and restores {actual_restore} MP!"

class Enemy(Character):
    """Base enemy class with AI behavior."""
    def __init__(self, name, hp, mp, attack, defense, speed, exp_reward=50):
        super().__init__(name, hp, mp, attack, defense, speed)
        self.exp_reward = exp_reward
        self.ai_personality = "balanced"  # aggressive, defensive, balanced
        self.special_cooldown = 0
    
    def ai_action(self, target):
        """AI decision making for enemy actions."""
        # Reduce special cooldown
        if self.special_cooldown > 0:
            self.special_cooldown -= 1
        
        # Heal if HP is critically low
        if self.hp < self.max_hp * 0.25 and random.random() < 0.8:
            heal_amount = 20 + random.randint(5, 15)
            self.heal(heal_amount)
            return f"💚 {self.name} heals for {heal_amount} HP!", "heal"
        
        # Use special ability if available and conditions met
        if self.special_cooldown == 0 and self.mp >= self.get_special_cost():
            if self.should_use_special(target):
                return self.special_ability(target), "special"
        
        # Regular attack
        return self.basic_attack(target), "attack"
    
    def should_use_special(self, target):
        """Determine if enemy should use special ability."""
        if self.ai_personality == "aggressive":
            return random.random() < 0.6
        elif self.ai_personality == "defensive":
            return random.random() < 0.3 and self.hp < self.max_hp * 0.6
        else:  # balanced
            return random.random() < 0.4
    
    def basic_attack(self, target):
        """Perform basic attack."""
        is_critical = random.random() < self.critical_chance
        damage = self.attack
        if is_critical:
            damage = int(damage * 1.5)
        
        damage_dealt = target.take_damage(damage)
        crit_text = " 💥 Critical hit!" if is_critical else ""
        return f"⚔️ {self.name} attacks {target.name} for {damage_dealt} damage!{crit_text}"
    
    def special_ability(self, target):
        """Override in subclasses."""
        return f"✨ {self.name} does something special!"
    
    def get_special_cost(self):
        """Get MP cost for special ability."""
        return 15

class Goblin(Enemy):
    """Agile goblin enemy with poison attacks."""
    def __init__(self):
        super().__init__("Goblin Warrior", hp=70, mp=40, attack=18, defense=8, speed=16, exp_reward=60)
        self.ai_personality = "aggressive"
        self.critical_chance = 0.15  # Higher crit chance
    
    def special_ability(self, target):
        """Poison dagger attack."""
        mp_cost = self.get_special_cost()
        self.mp -= mp_cost
        self.special_cooldown = 3
        
        base_damage = int(self.attack * 1.2)
        damage_dealt = target.take_damage(base_damage)
        target.add_status_effect(Poison(4, 6))
        
        return f"🗡️💚 {self.name} strikes with a poison dagger for {damage_dealt} damage and applies poison!"
    
    def get_special_cost(self):
        return 15

class Troll(Enemy):
    """Powerful troll enemy with devastating attacks."""
    def __init__(self):
        super().__init__("Mountain Troll", hp=180, mp=30, attack=35, defense=25, speed=6, exp_reward=100)
        self.ai_personality = "aggressive"
    
    def special_ability(self, target):
        """Devastating club smash."""
        mp_cost = self.get_special_cost()
        self.mp -= mp_cost
        self.special_cooldown = 4
        
        base_damage = int(self.attack * 2.2)
        damage_dealt = target.take_damage(base_damage)
        
        # Chance to stun
        if random.random() < 0.4:
            target.add_status_effect(Stun(2))
            return f"🔨💥 {self.name} delivers a crushing blow for {damage_dealt} damage and stuns {target.name}!"
        else:
            return f"🔨💥 {self.name} delivers a crushing blow for {damage_dealt} damage!"
    
    def get_special_cost(self):
        return 20

class DarkMage(Enemy):
    """Magical enemy with various spell attacks."""
    def __init__(self):
        super().__init__("Dark Mage", hp=90, mp=100, attack=22, defense=10, speed=14, exp_reward=120)
        self.ai_personality = "balanced"
        self.spell_list = ["fireball", "ice_shard", "dark_bolt", "shield"]
    
    def special_ability(self, target):
        """Cast a random spell."""
        mp_cost = self.get_special_cost()
        self.mp -= mp_cost
        self.special_cooldown = 2
        
        spell = random.choice(self.spell_list)
        
        if spell == "fireball":
            damage = int(self.attack * 1.6)
            damage_dealt = target.take_damage(damage)
            return f"🔥 {self.name} casts Fireball for {damage_dealt} damage!"
        
        elif spell == "ice_shard":
            damage = int(self.attack * 1.3)
            damage_dealt = target.take_damage(damage)
            target.add_status_effect(Stun(1))
            return f"❄️ {self.name} casts Ice Shard for {damage_dealt} damage and freezes {target.name}!"
        
        elif spell == "dark_bolt":
            damage = int(self.attack * 1.4)
            damage_dealt = target.take_damage(damage)
            target.add_status_effect(Poison(3, 5))
            return f"🌑 {self.name} casts Dark Bolt for {damage_dealt} damage and corrupts {target.name}!"
        
        elif spell == "shield":
            self.add_status_effect(Shield(5, 12))
            return f"🛡️ {self.name} casts Shield and gains magical protection!"
    
    def get_special_cost(self):
        return 25

class DragonWyrm(Enemy):
    """Powerful late-game boss enemy."""
    def __init__(self):
        super().__init__("Ancient Dragon Wyrm", hp=300, mp=150, attack=45, defense=30, speed=10, exp_reward=500)
        self.ai_personality = "balanced"
        self.breath_attacks = ["fire", "ice", "poison"]
        self.enraged = False
    
    def special_ability(self, target):
        """Dragon breath attacks."""
        mp_cost = self.get_special_cost()
        self.mp -= mp_cost
        self.special_cooldown = 3
        
        # Become enraged when below 50% HP
        if self.hp < self.max_hp * 0.5 and not self.enraged:
            self.enraged = True
            self.attack += 10
            self.critical_chance += 0.1
        
        breath_type = random.choice(self.breath_attacks)
        
        if breath_type == "fire":
            damage = int(self.attack * 1.8)
            damage_dealt = target.take_damage(damage)
            return f"🔥🐉 {self.name} breathes scorching fire for {damage_dealt} damage!"
        
        elif breath_type == "ice":
            damage = int(self.attack * 1.5)
            damage_dealt = target.take_damage(damage)
            target.add_status_effect(Stun(2))
            return f"❄️🐉 {self.name} breathes freezing ice for {damage_dealt} damage and freezes {target.name}!"
        
        elif breath_type == "poison":
            damage = int(self.attack * 1.3)
            damage_dealt = target.take_damage(damage)
            target.add_status_effect(Poison(5, 10))
            return f"💚🐉 {self.name} breathes toxic poison for {damage_dealt} damage and severely poisons {target.name}!"
    
    def get_special_cost(self):
        return 35

# ═══════════════════════════════════════════════════════════════════════════════
# BATTLE ENGINE MODULE
# ═══════════════════════════════════════════════════════════════════════════════

class Battle:
    """Battle management class handling turn-based combat."""
    def __init__(self, player, enemy, ui):
        self.player = player
        self.enemy = enemy
        self.ui = ui
        self.turn_count = 0
        self.battle_log = []
        self.player_wins = 0
        self.enemy_wins = 0
    
    def start_battle(self):
        """Main battle loop with proper turn order."""
        self.ui.display_battle_start(self.player, self.enemy)
        
        while self.player.is_alive() and self.enemy.is_alive():
            self.turn_count += 1
            self.ui.display_turn_info(self.turn_count, self.player, self.enemy)
            
            # Determine turn order by speed (with random factor for ties)
            player_initiative = self.player.speed + random.randint(1, 10)
            enemy_initiative = self.enemy.speed + random.randint(1, 10)
            
            if player_initiative >= enemy_initiative:
                # Player goes first
                if not self.player_turn():
                    break  # Player died or battle ended
                if self.enemy.is_alive():
                    if not self.enemy_turn():
                        break  # Enemy died or battle ended
            else:
                # Enemy goes first
                if not self.enemy_turn():
                    break  # Enemy died or battle ended
                if self.player.is_alive():
                    if not self.player_turn():
                        break  # Player died or battle ended
            
            # Process status effects at end of turn
            self.process_end_of_turn_effects()
            
            # Add dramatic pause between turns
            time.sleep(1)
        
        return self.end_battle()
    
    def player_turn(self):
        """Handle player's turn. Returns False if battle should end."""
        if self.is_stunned(self.player):
            self.ui.display_message("😵 You are stunned and skip your turn!")
            return True
        
        while True:  # Allow player to retry invalid actions
            action = self.ui.get_player_action(self.player)
            
            if action == "attack":
                self.handle_player_attack()
                break
            elif action == "special":
                if self.handle_player_special():
                    break
                # If special failed, let player choose again
            elif action == "item":
                if self.handle_item_use():
                    break
                # If item use failed, let player choose again
            elif action == "focus":
                self.handle_player_focus()
                break
            elif action == "run":
                if self.attempt_flee():
                    return False  # Battle ended by fleeing
                break
        
        return True
    
    def enemy_turn(self):
        """Handle enemy's turn. Returns False if battle should end."""
        if self.is_stunned(self.enemy):
            self.ui.display_message(f"😵 {self.enemy.name} is stunned and skips their turn!")
            return True
        
        action_result, action_type = self.enemy.ai_action(self.player)
        self.ui.display_message(action_result)
        
        return True
    
    def handle_player_attack(self):
        """Handle player basic attack."""
        is_critical = random.random() < self.player.critical_chance
        damage = self.player.attack
        
        if is_critical:
            damage = int(damage * 1.5)
        
        damage_dealt = self.enemy.take_damage(damage)
        crit_text = " 💥 CRITICAL HIT!" if is_critical else ""
        
        self.ui.display_message(f"⚔️ You attack {self.enemy.name} for {damage_dealt} damage!{crit_text}")
    
    def handle_player_special(self):
        """Handle player special attack. Returns True if successful."""
        damage_dealt, message = self.player.special_attack(self.enemy)
        self.ui.display_message(message)
        return damage_dealt > 0
    
    def handle_player_focus(self):
        """Handle player focus action."""
        message = self.player.focus()
        self.ui.display_message(message)
    
    def handle_item_use(self):
        """Handle player item usage. Returns True if successful."""
        usable_items = self.player.inventory.get_usable_items()
        
        if not usable_items:
            self.ui.display_message("❌ No usable items in inventory!")
            return False
        
        item = self.ui.select_item(usable_items)
        if not item:
            return False  # Player cancelled
        
        # Determine target based on item type
        target = self.enemy if isinstance(item, Bomb) else None
        message, success = self.player.use_item(item, target)
        self.ui.display_message(message)
        return success
    
    def attempt_flee(self):
        """Attempt to flee from battle."""
        flee_chance = 0.7 + (self.player.speed - self.enemy.speed) * 0.05
        flee_chance = max(0.1, min(0.9, flee_chance))  # Clamp between 10-90%
        
        if random.random() < flee_chance:
            self.ui.display_message(f"💨 You successfully flee from {self.enemy.name}!")
            return True
        else:
            self.ui.display_message(f"❌ You couldn't escape from {self.enemy.name}!")
            return False
    
    def is_stunned(self, character):
        """Check if character is stunned."""
        return character.has_status_effect(Stun)
    
    def process_end_of_turn_effects(self):
        """Process status effects for both characters at end of turn."""
        self.ui.display_message("\n--- Status Effects ---")
        
        # Process player status effects
        player_messages = self.player.process_status_effects()
        for message in player_messages:
            self.ui.display_message(message)
        
        # Process enemy status effects
        enemy_messages = self.enemy.process_status_effects()
        for message in enemy_messages:
            self.ui.display_message(message)
        
        if not player_messages and not enemy_messages:
            self.ui.display_message("No active status effects.")
    
    def end_battle(self):
        """Handle battle end and return result."""
        if self.player.is_alive() and self.enemy.is_alive():
            # Battle ended by fleeing
            return "fled"
        elif self.player.is_alive():
            # Player victory
            self.ui.display_victory(self.enemy)
            exp_messages = self.player.gain_experience(self.enemy.exp_reward)
            for message in exp_messages:
                self.ui.display_message(message)
            return "victory"
        else:
            # Player defeat
            self.ui.display_defeat()
            return "defeat"

# ═══════════════════════════════════════════════════════════════════════════════
# USER INTERFACE MODULE
# ═══════════════════════════════════════════════════════════════════════════════

class UI:
    """User interface class handling all text-based I/O."""
    def __init__(self):
        self.animation_delay = 0.8
        self.input_delay = 0.3
    
    def display_welcome(self):
        """Display welcome message with ASCII art."""
        self.clear_screen()
        welcome_art = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║      ⚔️  TURN-BASED RPG BATTLE ENGINE  ⚔️                      ║
║                                                                  ║
║               🏰 Adventure Awaits! 🏰                          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
        """
        print(welcome_art)
        time.sleep(self.animation_delay)
    
    def get_player_name(self):
        """Get player name with validation."""
        while True:
            name = input("\n🧙 Enter your hero's name: ").strip()
            if name and len(name) <= 20:
                return name
            elif len(name) > 20:
                print("❌ Name too long! Please use 20 characters or less.")
            else:
                return "Hero"  # Default name
    
    def display_battle_start(self, player, enemy):
        """Display battle start with dramatic flair."""
        print(f"\n{'='*60}")
        print(f"⚔️  {player.name} encounters a fearsome {enemy.name}! ⚔️")
        print(f"{'='*60}")
        
        # Display combatant stats
        print(f"\n🛡️  {player.name} (Level {player.level})")
        print(f"   HP: {player.hp}/{player.max_hp} | MP: {player.mp}/{player.max_mp}")
        print(f"   ATK: {player.attack} | DEF: {player.defense} | SPD: {player.speed}")
        
        print(f"\n👹 {enemy.name}")
        print(f"   HP: {enemy.hp}/{enemy.max_hp} | MP: {enemy.mp}/{enemy.max_mp}")
        print(f"   ATK: {enemy.attack} | DEF: {enemy.defense} | SPD: {enemy.speed}")
        
        print(f"\n{'='*60}")
        print("🎯 Battle begins!")
        time.sleep(self.animation_delay)
    
    def display_turn_info(self, turn_count, player, enemy):
        """Display turn information and character status."""
        print(f"\n{'─'*50}")
        print(f"🎲 Turn {turn_count}")
        print(f"{'─'*50}")
        
        # Player status
        hp_bar = self.create_health_bar(player.hp, player.max_hp, 20)
        mp_bar = self.create_mana_bar(player.mp, player.max_mp, 20)
        
        print(f"🛡️  {player.name}: {hp_bar} HP: {player.hp}/{player.max_hp}")
        print(f"     {mp_bar} MP: {player.mp}/{player.max_mp}")
        
        player_status = player.get_status_summary()
        if player_status != "None":
            print(f"     Status: {player_status}")
        
        # Enemy status
        enemy_hp_bar = self.create_health_bar(enemy.hp, enemy.max_hp, 20)
        print(f"👹 {enemy.name}: {enemy_hp_bar} HP: {enemy.hp}/{enemy.max_hp}")
        
        enemy_status = enemy.get_status_summary()
        if enemy_status != "None":
            print(f"     Status: {enemy_status}")
        
        print(f"{'─'*50}")
    
    def create_health_bar(self, current, maximum, length=20):
        """Create a visual health bar."""
        if maximum == 0:
            return "❌" * length
        
        filled_length = int(length * current / maximum)
        bar = "❤️" * filled_length + "🖤" * (length - filled_length)
        return f"[{bar}]"
    
    def create_mana_bar(self, current, maximum, length=20):
        """Create a visual mana bar."""
        if maximum == 0:
            return "❌" * length
        
        filled_length = int(length * current / maximum)
        bar = "💙" * filled_length + "⚫" * (length - filled_length)
        return f"[{bar}]"
    
    def get_player_action(self, player):
        """Get player action choice with detailed menu."""
        print("\n🎯 Choose your action:")
        print("1. ⚔️  Attack - Basic physical attack")
        print("2. ✨ Special Attack - Powerful attack (20 MP)")
        print("3. 🧰 Use Item - Use item from inventory")
        print("4. 🧘 Focus - Restore MP instead of attacking")
        print("5. 💨 Attempt to Flee - Try to escape battle")
        print("6. 📋 View Stats - Check detailed character info")
        
        while True:
            try:
                choice = input("\nEnter choice (1-6): ").strip()
                
                if choice == "1":
                    return "attack"
                elif choice == "2":
                    return "special"
                elif choice == "3":
                    return "item"
                elif choice == "4":
                    return "focus"
                elif choice == "5":
                    return "run"
                elif choice == "6":
                    self.display_character_details(player)
                    continue  # Show menu again
                else:
                    print("❌ Invalid choice! Please enter 1-6.")
                    
            except (ValueError, KeyboardInterrupt):
                print("❌ Invalid input! Please enter a number 1-6.")
    
    def display_character_details(self, character):
        """Display detailed character information."""
        print(f"\n📋 {character.name} - Detailed Stats")
        print(f"{'='*40}")
        print(f"Level: {getattr(character, 'level', 'N/A')}")
        print(f"Experience: {getattr(character, 'experience', 'N/A')}")
        print(f"HP: {character.hp}/{character.max_hp}")
        print(f"MP: {character.mp}/{character.max_mp}")
        print(f"Attack: {character.attack}")
        print(f"Defense: {character.defense}")
        print(f"Speed: {character.speed}")
        print(f"Critical Chance: {character.critical_chance*100:.1f}%")
        
        if hasattr(character, 'equipped_weapon') and character.equipped_weapon:
            print(f"Weapon: {character.equipped_weapon.name}")
        
        print(f"Status Effects: {character.get_status_summary()}")
        
        # Show inventory
        if hasattr(character, 'inventory'):
            item_counts = character.inventory.count_items()
            if item_counts:
                print(f"\n🧰 Inventory:")
                for item_name, count in item_counts.items():
                    print(f"  {item_name} x{count}")
            else:
                print(f"\n🧰 Inventory: Empty")
        
        input("\nPress Enter to continue...")
    
    def select_item(self, items):
        """Let player select an item from a list."""
        if not items:
            return None
        
        print(f"\n🧰 Available items:")
        for i, item in enumerate(items, 1):
            print(f"{i}. {item.name} - {item.description}")
        print("0. Cancel")
        
        while True:
            try:
                choice = int(input("Select item (number): "))
                if choice == 0:
                    return None
                elif 1 <= choice <= len(items):
                    return items[choice - 1]
                else:
                    print(f"❌ Invalid selection! Please enter 0-{len(items)}.")
            except ValueError:
                print("❌ Please enter a valid number!")
    
    def display_message(self, message):
        """Display a message with appropriate timing."""
        print(message)
        time.sleep(self.input_delay)
    
    def display_victory(self, enemy):
        """Display victory message with celebration."""
        victory_art = f"""
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
🎉                                          🎉
🎉          ⭐ VICTORY! ⭐                  🎉
🎉                                          🎉
🎉   You have defeated the {enemy.name}!   🎉
🎉                                          🎉
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
        """
        print(victory_art)
        print(f"\n💰 You gained {enemy.exp_reward} experience points!")
        time.sleep(self.animation_delay)
    
    def display_defeat(self):
        """Display defeat message."""
        defeat_art = """
💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
💀                                    💀
💀          💔 DEFEAT 💔              💀
💀                                    💀
💀     You have been vanquished!      💀
💀        Better luck next time!      💀
💀                                    💀
💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
        """
        print(defeat_art)
        time.sleep(self.animation_delay)
    
    def clear_screen(self):
        """Clear the screen (works on most systems)."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_yes_no_input(self, prompt):
        """Get yes/no input from user."""
        while True:
            response = input(f"{prompt} (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("❌ Please enter 'y' or 'n'.")

# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADER MODULE (OPTIONAL)
# ═══════════════════════════════════════════════════════════════════════════════

class DataLoader:
    """Optional class for loading game data from JSON files."""
    
    @staticmethod
    def save_player_data(player, filename="player_save.json"):
        """Save player data to JSON file."""
        try:
            player_data = {
                "name": player.name,
                "level": player.level,
                "experience": player.experience,
                "hp": player.hp,
                "max_hp": player.max_hp,
                "mp": player.mp,
                "max_mp": player.max_mp,
                "attack": player.attack,
                "defense": player.defense,
                "speed": player.speed,
                "inventory": [item.name for item in player.inventory.items]
            }
            
            with open(filename, 'w') as f:
                json.dump(player_data, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Error saving game: {e}")
            return False
    
    @staticmethod
    def load_player_data(filename="player_save.json"):
        """Load player data from JSON file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"❌ Error loading game: {e}")
            return None
    
    @staticmethod
    def create_item_from_name(item_name):
        """Create item instance from name string."""
        item_map = {
            "Health Potion": HealthPotion(),
            "Mana Potion": ManaPotion(),
            "Antidote": Antidote(),
            "Bomb": Bomb(),
            "Strength Potion": StrengthPotion(),
            "Shield Potion": ShieldPotion(),
            "Regeneration Elixir": RegenerationElixir(),
            "Iron Sword": IronSword(),
            "Steel Sword": SteelSword()
        }
        return item_map.get(item_name, HealthPotion())  # Default to health potion
# ═══════════════════════════════════════════════════════════════════════════════
# MAIN GAME MODULE
# ═══════════════════════════════════════════════════════════════════════════════

class Game:
    """Main game class managing overall game flow and logic."""
    def __init__(self):
        """Initialize the game."""
        self.ui = UI()
        self.data_loader = DataLoader()
        self.player = None
        self.current_stage = 1
        self.max_stages = 5
        self.game_mode = "campaign"  # or "survival"
        
    def start_game(self):
        """Main game entry point."""
        self.ui.display_welcome()
        
        # Check for save file
        if self.ui.get_yes_no_input("🗂️  Load saved game?"):
            if self.load_game():
                print("✅ Game loaded successfully!")
            else:
                print("❌ No save file found or load failed. Starting new game.")
                self.create_new_player()
        else:
            self.create_new_player()
        
        # Main game loop
        self.main_game_loop()
    
    def create_new_player(self):
        """Create a new player character."""
        name = self.ui.get_player_name()
        self.player = Player(name)
        print(f"\n🎭 Welcome, {self.player.name}! Your adventure begins...")
        time.sleep(1)
        
        # Tutorial battle
        if self.ui.get_yes_no_input("🎯 Would you like to fight a tutorial battle?"):
            self.tutorial_battle()
    
    def tutorial_battle(self):
        """Simple tutorial battle."""
        print("\n📚 Tutorial: Learn the basics of combat!")
        tutorial_goblin = Goblin()
        tutorial_goblin.hp = 30  # Weaker for tutorial
        tutorial_goblin.attack = 10
        
        battle = Battle(self.player, tutorial_goblin, self.ui)
        result = battle.start_battle()
        
        if result == "victory":
            print("🎓 Tutorial complete! You're ready for real battles.")
            # Give bonus items for completing tutorial
            self.player.inventory.add_item(HealthPotion())
            self.player.inventory.add_item(Bomb())
            print("🎁 You received bonus items for completing the tutorial!")
        
        time.sleep(2)
    
    def main_game_loop(self):
        """Main game loop with different modes."""
        while True:
            self.ui.clear_screen()
            print(f"\n🏰 {self.player.name}'s Adventure - Stage {self.current_stage}")
            print(f"{'='*50}")
            
            choice = self.get_main_menu_choice()
            
            if choice == "battle":
                result = self.stage_battle()
                if result == "victory":
                    self.current_stage += 1
                    if self.current_stage > self.max_stages:
                        self.victory_ending()
                        break
                elif result == "defeat":
                    self.defeat_ending()
                    break
            
            elif choice == "shop":
                self.visit_shop()
            
            elif choice == "inventory":
                self.manage_inventory()
            
            elif choice == "stats":
                self.ui.display_character_details(self.player)
            
            elif choice == "save":
                self.save_game()
            
            elif choice == "quit":
                if self.ui.get_yes_no_input("💾 Save before quitting?"):
                    self.save_game()
                print("👋 Thanks for playing!")
                break
    
    def get_main_menu_choice(self):
        """Display main menu and get player choice."""
        print("🎮 What would you like to do?")
        print("1. ⚔️  Enter Battle - Fight the next enemy")
        print("2. 🏪 Visit Shop - Buy items and equipment")
        print("3. 🧰 Manage Inventory - Use items and equip weapons")
        print("4. 📊 View Stats - Check character details")
        print("5. 💾 Save Game - Save your progress")
        print("6. 🚪 Quit Game - Exit the game")
        
        choice_map = {
            "1": "battle",
            "2": "shop", 
            "3": "inventory",
            "4": "stats",
            "5": "save",
            "6": "quit"
        }
        
        while True:
            choice = input("\nEnter choice (1-6): ").strip()
            if choice in choice_map:
                return choice_map[choice]
            print("❌ Invalid choice! Please enter 1-6.")
    
    def stage_battle(self):
        """Create and fight a stage-appropriate enemy."""
        enemy = self.create_stage_enemy()
        print(f"\n🎯 Stage {self.current_stage} Battle!")
        
        battle = Battle(self.player, enemy, self.ui)
        result = battle.start_battle()
        
        if result == "victory":
            # Bonus rewards for higher stages
            bonus_exp = self.current_stage * 10
            exp_messages = self.player.gain_experience(enemy.exp_reward + bonus_exp)
            for message in exp_messages:
                print(message)
            
            # Chance for bonus items
            if random.random() < 0.3:
                bonus_item = self.get_random_item()
                if self.player.inventory.add_item(bonus_item):
                    print(f"🎁 Bonus reward: You found a {bonus_item.name}!")
        
        input("\nPress Enter to continue...")
        return result
    
    def create_stage_enemy(self):
        """Create enemy appropriate for current stage."""
        if self.current_stage == 1:
            return random.choice([Goblin(), Goblin()])
        elif self.current_stage == 2:
            return random.choice([Goblin(), Troll()])
        elif self.current_stage == 3:
            return random.choice([Troll(), DarkMage()])
        elif self.current_stage == 4:
            return random.choice([DarkMage(), Troll()])
        else:  # Stage 5 and beyond - boss fights
            return DragonWyrm()
    
    def visit_shop(self):
        """Shop system for buying items."""
        print("\n🏪 Welcome to the Adventurer's Shop!")
        print("='*40")
        
        shop_items = [
            (HealthPotion(), 25),
            (ManaPotion(), 20),
            (Antidote(), 15),
            (Bomb(), 30),
            (StrengthPotion(), 40),
            (ShieldPotion(), 35),
            (RegenerationElixir(), 50),
            (SteelSword(), 250)
        ]
        
        player_gold = getattr(self.player, 'gold', 100 + self.current_stage * 50)
        print(f"💰 Your gold: {player_gold}")
        
        print("\n🛒 Items for sale:")
        for i, (item, price) in enumerate(shop_items, 1):
            print(f"{i}. {item.name} - {item.description} (💰 {price} gold)")
        print("0. Leave shop")
        
        while True:
            try:
                choice = int(input("\nWhat would you like to buy? (0 to leave): "))
                if choice == 0:
                    break
                elif 1 <= choice <= len(shop_items):
                    item, price = shop_items[choice - 1]
                    
                    if player_gold >= price:
                        if self.player.inventory.add_item(item):
                            player_gold -= price
                            print(f"✅ Purchased {item.name} for {price} gold!")
                        else:
                            print("❌ Inventory full! Can't buy more items.")
                    else:
                        print(f"❌ Not enough gold! Need {price} gold.")
                else:
                    print(f"❌ Invalid choice! Please enter 0-{len(shop_items)}.")
            except ValueError:
                print("❌ Please enter a valid number!")
        
        # Store gold back to player (simplified approach)
        self.player.gold = player_gold
    
    def manage_inventory(self):
        """Inventory management interface."""
        while True:
            print(f"\n🧰 {self.player.name}'s Inventory")
            print("="*40)
            
            # Show items
            item_counts = self.player.inventory.count_items()
            if not item_counts:
                print("📦 Inventory is empty!")
            else:
                for item_name, count in item_counts.items():
                    print(f"  {item_name} x{count}")
            
            print("\n🔧 Inventory Actions:")
            print("1. 💊 Use Item")
            print("2. ⚔️  Equip Weapon")
            print("3. 🗑️  Drop Item")
            print("4. 🔙 Return to Main Menu")
            
            choice = input("\nChoose action (1-4): ").strip()
            
            if choice == "1":
                self.use_inventory_item()
            elif choice == "2":
                self.equip_weapon_menu()
            elif choice == "3":
                self.drop_item_menu()
            elif choice == "4":
                break
            else:
                print("❌ Invalid choice! Please enter 1-4.")
    
    def use_inventory_item(self):
        """Use an item outside of battle."""
        usable_items = [item for item in self.player.inventory.items 
                       if not isinstance(item, (Weapon, Bomb))]
        
        if not usable_items:
            print("❌ No usable items in inventory!")
            return
        
        item = self.ui.select_item(usable_items)
        if item:
            message, success = self.player.use_item(item)
            print(message)
    
    def equip_weapon_menu(self):
        """Weapon equipment menu."""
        weapons = self.player.inventory.get_weapons()
        
        if not weapons:
            print("❌ No weapons in inventory!")
            return
        
        print(f"\n⚔️  Current weapon: {self.player.equipped_weapon.name if self.player.equipped_weapon else 'None'}")
        
        weapon = self.ui.select_item(weapons)
        if weapon:
            if not weapon.equipped:
                message = self.player.equip_weapon(weapon)
                print(message)
            else:
                print("❌ That weapon is already equipped!")
    
    def drop_item_menu(self):
        """Drop item menu."""
        if not self.player.inventory.items:
            print("❌ No items to drop!")
            return
        
        item = self.ui.select_item(self.player.inventory.items)
        if item:
            if self.ui.get_yes_no_input(f"🗑️  Really drop {item.name}?"):
                self.player.inventory.remove_item(item)
                print(f"🗑️  Dropped {item.name}.")
    
    def get_random_item(self):
        """Get a random item for rewards."""
        items = [
            HealthPotion(), ManaPotion(), Antidote(), Bomb(),
            StrengthPotion(), ShieldPotion(), RegenerationElixir()
        ]
        return random.choice(items)
    
    def save_game(self):
        """Save the current game state."""
        if self.data_loader.save_player_data(self.player):
            print("💾 Game saved successfully!")
        else:
            print("❌ Failed to save game!")
    
    def load_game(self):
        """Load a saved game."""
        data = self.data_loader.load_player_data()
        if data:
            # Recreate player from saved data
            self.player = Player(data["name"])
            self.player.level = data.get("level", 1)
            self.player.experience = data.get("experience", 0)
            self.player.hp = data.get("hp", 100)
            self.player.max_hp = data.get("max_hp", 100)
            self.player.mp = data.get("mp", 50)
            self.player.max_mp = data.get("max_mp", 50)
            self.player.attack = data.get("attack", 20)
            self.player.defense = data.get("defense", 10)
            self.player.speed = data.get("speed", 10)
            
            # Restore inventory
            self.player.inventory.items = []
            for item_name in data.get("inventory", []):
                item = self.data_loader.create_item_from_name(item_name)
                self.player.inventory.add_item(item)
            
            return True
        return False
    
    def victory_ending(self):
        """Display victory ending."""
        ending_art = """
🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆
🏆                                            🏆
🏆       🎉 CONGRATULATIONS! 🎉              🏆
🏆                                            🏆
🏆    You have conquered all challenges!      🏆
🏆         You are a true hero!               🏆
🏆                                            🏆
🏆        Final Level: {:<2}                   🏆
🏆        Total Experience: {:<6}             🏆
🏆                                            🏆
🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆
        """.format(self.player.level, self.player.experience)
        print(ending_art)
    
    def defeat_ending(self):
        """Display defeat ending."""
        print("""
💀 Your adventure ends here...
   But every hero's journey has setbacks!
   
   🌟 Try again and become stronger!
   🌟 Learn from your battles!
   🌟 Victory awaits the persistent!
        """)


# ═══════════════════════════════════════════════════════════════════════════════
# GAME ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main function to start the game."""
    try:
        print("🎮 Initializing Turn-Based RPG Battle Engine...")
        time.sleep(1)
        
        game = Game()
        game.start_game()
        
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please restart the game.")

if __name__ == "__main__":
    main()

"""
🎯 FEATURE SUMMARY:
═══════════════════

✅ Object-Oriented Design:
   - Inheritance hierarchy (Character → Player/Enemy)
   - Polymorphism in status effects and items
   - Composition with inventory and battle systems

✅ Complete Battle System:
   - Turn-based combat with initiative
   - Critical hits and damage calculation
   - Status effects with duration tracking
   - AI decision making for enemies

✅ Rich Character Progression:
   - Experience and leveling system
   - Stat increases on level up
   - Equipment system with weapons

✅ Comprehensive Inventory:
   - Multiple item types with unique effects
   - Weapons that modify stats
   - Inventory capacity management

✅ Advanced Status Effects:
   - Poison (damage over time)
   - Stun (prevent actions)
   - Regeneration (healing over time)
   - Buffs (temporary stat boosts)

✅ Polished User Interface:
   - ASCII art and visual health bars
   - Clear action menus and feedback
   - Animated text with timing delays

✅ Game Progression:
   - Multiple stages with increasing difficulty
   - Shop system for purchasing items
   - Save/load functionality

✅ Enemy Variety:
   - Different enemy types with unique abilities
   - Scaling difficulty and AI personalities
   - Boss battles with special mechanics

📊 Line Count: ~1500 lines (including comments and documentation)
🎨 Code Quality: Modular, documented, and maintainable
🎮 Playability: Full game experience from tutorial to ending
"""
    