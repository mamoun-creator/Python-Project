# Mamoun Mohamed
# 21/11/2024
# Dungeon Explorer Adventure Game.

import random
import time

class GameCharacter:
    """Base class for characters in the game."""
    def __init__(self, name, health, strength):
        """
        Initialize a game character.
        
        Args:
            name (str): Character's name
            health (int): Starting health points
            strength (int): Character's strength level
        """
        self.name = name
        self.health = health
        self.max_health = health
        self.strength = strength
        self.inventory = []
    
    def is_alive(self):
        """
        Check if character is alive.
        
        Returns:
            bool: True if health > 0, False otherwise
        """
        return self.health > 0
    
    def take_damage(self, damage):
        """
        Reduce character's health.
        
        Args:
            damage (int): Amount of damage to inflict
        """
        self.health = max(0, self.health - damage)
    
    def heal(self, amount):
        """
        Restore character's health.
        
        Args:
            amount (int): Health points to restore
        """
        self.health = min(self.max_health, self.health + amount)
    
    def add_to_inventory(self, item):
        """
        Add item to character's inventory.
        
        Args:
            item (str): Item to add
        """
        self.inventory.append(item)

class Player(GameCharacter):
    """Player-specific character class."""
    def __init__(self, name):
        """
        Initialize player with default stats.
        
        Args:
            name (str): Player's character name
        """
        super().__init__(name, health=100, strength=10)
        self.experience = 0
        self.level = 1
    
    def gain_experience(self, xp):
        """
        Increase player's experience and level.
        
        Args:
            xp (int): Experience points gained
        """
        self.experience += xp
        if self.experience >= 100 * self.level:
            self.level_up()
    
    def level_up(self):
        """Increase player's stats when leveling up."""
        self.level += 1
        self.max_health += 20
        self.health = self.max_health
        self.strength += 5
        print(f"🎉 {self.name} leveled up to Level {self.level}!")

class Enemy(GameCharacter):
    """Enemy character class."""
    def __init__(self, name, health, strength, loot):
        """
        Initialize enemy with specific attributes.
        
        Args:
            name (str): Enemy name
            health (int): Enemy health points
            strength (int): Enemy strength
            loot (list): Possible items to drop
        """
        super().__init__(name, health, strength)
        self.loot = loot

class GameWorld:
    """Manages game world and interactions."""
    def __init__(self, player):
        """
        Initialize game world.
        
        Args:
            player (Player): Player character
        """
        self.player = player
        self.current_location = "Village"
        self.locations = {
            "Village": ["Forest", "Cave", "Mountain"],
            "Forest": ["Village", "Ancient Ruins"],
            "Cave": ["Village", "Underground Cavern"],
            "Mountain": ["Village", "Peak"],
            "Ancient Ruins": ["Forest"],
            "Underground Cavern": ["Cave"],
            "Peak": ["Mountain"]
        }
        self.enemies = {
            "Forest": Enemy("Forest Goblin", 30, 5, ["Rusty Dagger"]),
            "Cave": Enemy("Cave Troll", 50, 8, ["Stone Hammer"]),
            "Mountain": Enemy("Mountain Golem", 70, 12, ["Enchanted Gem"]),
            "Underground Cavern": Enemy("Shadow Creature", 40, 7, ["Dark Crystal"]),
            "Ancient Ruins": Enemy("Ancient Guardian", 60, 10, ["Mysterious Scroll"])
        }
    
    def explore(self):
        """Manage player exploration and encounters."""
        print(f"\n🌍 You are currently in {self.current_location}")
        print("Possible destinations:", ", ".join(self.locations[self.current_location]))
        
        choice = input("Where would you like to go? ").capitalize()
        
        if choice in self.locations[self.current_location]:
            self.current_location = choice
            print(f"🚶 Traveling to {self.current_location}...")
            time.sleep(1)
            
            # Random encounter chance
            if random.random() < 0.6 and self.current_location in self.enemies:
                self.battle(self.enemies[self.current_location])
        else:
            print("❌ You cannot travel there from this location.")
    
    def battle(self, enemy):
        """
        Manage combat between player and enemy.
        
        Args:
            enemy (Enemy): Enemy to fight
        """
        print(f"\n⚔️ Encountered {enemy.name}!")
        
        while self.player.is_alive() and enemy.is_alive():
            print(f"\n{self.player.name}: {self.player.health} HP")
            print(f"{enemy.name}: {enemy.health} HP")
            
            action = input("Do you want to (A)ttack or (R)un? ").lower()
            
            if action == 'a':
                # Player attack
                damage = random.randint(1, self.player.strength)
                enemy.take_damage(damage)
                print(f"You deal {damage} damage to {enemy.name}")
                
                # Enemy counterattack
                if enemy.is_alive():
                    enemy_damage = random.randint(1, enemy.strength)
                    self.player.take_damage(enemy_damage)
                    print(f"{enemy.name} deals {enemy_damage} damage to you")
            elif action == 'r':
                if random.random() < 0.5:
                    print("🏃 Successfully escaped!")
                    break
                else:
                    print("❌ Failed to escape!")
                    enemy_damage = random.randint(1, enemy.strength)
                    self.player.take_damage(enemy_damage)
                    print(f"{enemy.name} deals {enemy_damage} damage to you")
            
            # Check battle outcome
            if not enemy.is_alive():
                print(f"🏆 You defeated {enemy.name}!")
                loot = random.choice(enemy.loot)
                self.player.add_to_inventory(loot)
                self.player.gain_experience(random.randint(10, 50))
                print(f"🎁 Found: {loot}")
            
            if not self.player.is_alive():
                print("☠️ Game Over! You were defeated.")
                exit()

def main():
    """Main game loop."""
    print("🏰 Welcome to Dungeon Explorer!")
    player_name = input("Enter your character's name: ")
    player = Player(player_name)
    world = GameWorld(player)
    
    while True:
        print("\n--- Game Menu ---")
        print("1. Explore")
        print("2. View Character Stats")
        print("3. View Inventory")
        print("4. Quit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            world.explore()
        elif choice == '2':
            print(f"\n🧙 {player.name}'s Stats:")
            print(f"Level: {player.level}")
            print(f"Health: {player.health}/{player.max_health}")
            print(f"Strength: {player.strength}")
            print(f"Experience: {player.experience}")
        elif choice == '3':
            print("\n🎒 Inventory:")
            print(player.inventory if player.inventory else "Empty")
        elif choice == '4':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
