from typing import List, Union, Protocol, runtime_checkable
from abc import ABC, abstractmethod

@runtime_checkable
class Usable(Protocol):
    def use(self) -> str: ...

class Item:
    def __init__(self, name, description='', rarity='common'):
        self.name = name
        self.description = description
        self.rarity = rarity
        self._ownership = ''

    def pick_up(self, character: str) -> str:
        self._ownership = character
        return f"{self.name} is now owned by {character}"

    def throw_away(self) -> str:
        self._ownership = ''
        return f"{self.name} is thrown away"

    def use(self) -> str:
        if not self._ownership:
            return ""
        return f"{self.name} is used"

    def __str__(self):
        base_str = f"{self.name} ({self.rarity}): {self.description}"
        if self.rarity == 'legendary':
            return f"**LEGENDARY**\n{'*' * 20}\n*  {self.name.upper()}  *\n{'*' * 20}\n{base_str}"
        return base_str

class Weapon(Item):
    def __init__(self, name, damage, type, description='', rarity='common'):
        super().__init__(name, description, rarity)
        self.damage = damage
        self.type = type
        self.is_equipped = False
        self.attack_modifier = 1.15 if rarity == 'legendary' else 1.0

    def equip(self):
        self.is_equipped = True
        return f"{self.name} is equipped by {self._ownership}"

    def use(self) -> str:
        if not self._ownership or not self.is_equipped:
            return ""
        attack_power = self.damage * self.attack_modifier
        return f"{self.attack_move()}\n{self.name} is used, dealing {attack_power} damage"

    @abstractmethod
    def attack_move(self) -> str:
        pass

class SingleHandedWeapon(Weapon):
    def attack_move(self) -> str:
        return f"{self._ownership} slashes with {self.name}"

class DoubleHandedWeapon(Weapon):
    def attack_move(self) -> str:
        return f"{self._ownership} spins {self.name}"

class Pike(Weapon):
    def attack_move(self) -> str:
        return f"{self._ownership} thrusts {self.name}"

class RangedWeapon(Weapon):
    def attack_move(self) -> str:
        return f"{self._ownership} shoots {self.name}"

class Shield(Item):
    def __init__(self, name, defense, description='', rarity='common', broken=False):
        super().__init__(name, description, rarity)
        self.defense = defense
        self.is_equipped = False
        self.broken = broken
        self.defense_modifier = 1.10 if rarity == 'legendary' else 1.0

    def equip(self):
        self.is_equipped = True
        return f"{self.name} is equipped by {self._ownership}"

    def use(self) -> str:
        if not self._ownership or not self.is_equipped:
            return ""
        defense_power = self.defense * self.defense_modifier * (0.5 if self.broken else 1.0)
        return f"{self.name} is used, blocking {defense_power} damage"

class Potion(Item):
    def __init__(self, name, type, value, effective_time, description='', rarity='common'):
        super().__init__(name, description, rarity)
        self.type = type
        self.value = value
        self.effective_time = effective_time
        self.is_empty = False

    @classmethod
    def from_ability(cls, name, owner, type):
        potion = cls(name, type, value=50, effective_time=30, rarity='common')
        potion._ownership = owner
        return potion

    def use(self) -> str:
        if not self._ownership or self.is_empty:
            return ""
        self.is_empty = True
        effect = f"{'restores' if self.type == 'HP' else 'increases'} {self.value}"
        duration = f"for {self.effective_time}s" if self.effective_time > 0 else ""
        return f"{self._ownership} used {self.name}, and {self.type} {effect} {duration}"

class Inventory:
    def __init__(self, owner=None):
        self.owner = owner
        self.items: List[Item] = []

    def add_item(self, item: Item):
        if isinstance(item, Item):
            self.items.append(item)
            item.pick_up(self.owner)

    def remove_item(self, item: Item):
        if item in self.items:
            self.items.remove(item)
            item.throw_away()

    def view(self, type=None, item=None):
        if item:
            return str(item)
        if type:
            return [str(item) for item in self.items if isinstance(item, eval(type.capitalize()))]
        return [str(item) for item in self.items]

    def __iter__(self):
        return iter(self.items)

    def __contains__(self, item):
        return item in self.items


if __name__ == "__main__":

    master_sword = SingleHandedWeapon("Master Sword", 300, "sword", rarity="legendary")
    muramasa = DoubleHandedWeapon("Muramasa", 580, "katana", rarity="legendary")
    gungnir = Pike("Gungnir", 290, "spear", rarity="legendary")
    belthronding = RangedWeapon("Belthronding", 500, "bow", rarity="legendary")
    hp_potion = Potion("HP Potion", "HP", 100, 0)
    broken_pot_lid = Shield("Broken Pot Lid", 5, broken=True)
    round_shield = Shield("Round Shield", 50)


    beleg_backpack = Inventory(owner="Beleg")

   
    for item in [belthronding, hp_potion, master_sword, broken_pot_lid, muramasa, gungnir, round_shield]:
        beleg_backpack.add_item(item)

    
    print("All items in inventory:")
    for item_str in beleg_backpack.view():
        print(item_str)

    print("\nShields in inventory:")
    for item_str in beleg_backpack.view(type="shield"):
        print(item_str)

  
    beleg_backpack.remove_item(broken_pot_lid)

   
    if master_sword in beleg_backpack:
        print("\nUsing Master Sword:")
        master_sword.equip()
        print(master_sword.use())

   
    print("\nWeapons in inventory:")
    for item in beleg_backpack:
        if isinstance(item, Weapon):
            print(beleg_backpack.view(item=item))