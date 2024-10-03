# Base Item class
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
        return f"{self.name} ({self.rarity}): {self.description}"


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
        return f"{self.name} is used, dealing {attack_power} damage"


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


if __name__ == "__main__":
    belthronding = Weapon(name='Belthronding', rarity='legendary', damage=5000, type='bow')
    print(belthronding.pick_up('Beleg'))
    print(belthronding.equip())
    print(belthronding.use())

    broken_pot_lid = Shield(name='wooden lid', description='A lid made of wood, useful in cooking. No one will choose it willingly for a shield', defense=5, broken=True)
    print(broken_pot_lid.pick_up('Beleg'))
    print(broken_pot_lid.equip())
    print(broken_pot_lid.use())
    print(broken_pot_lid.throw_away())
    print(broken_pot_lid.use())

    attack_potion = Potion.from_ability(name='atk potion temp', owner='Beleg', type='attack')
    print(attack_potion.use())
    print(attack_potion.use())

    print(isinstance(belthronding, Item))
    print(isinstance(broken_pot_lid, Shield))
    print(isinstance(attack_potion, Weapon))