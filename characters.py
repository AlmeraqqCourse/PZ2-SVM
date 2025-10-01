import abc
import random  # ДОБАВИТЬ ЭТУ СТРОКУ
from descriptors import BoundedStat

class Human:
    """Базовый класс для всех существ"""
    hp = BoundedStat(0, 1000)
    mp = BoundedStat(0, 500)
    strength = BoundedStat(1, 100)
    agility = BoundedStat(1, 100)
    intellect = BoundedStat(1, 100)
    
    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        self.hp = 100
        self.mp = 50
        self.strength = 10
        self.agility = 10
        self.intellect = 10
        self.effects = []
        self.cooldowns = {}
    
    @property
    def is_alive(self):
        return self.hp > 0
    
    def __str__(self):
        return f"{self.name} (Ур. {self.level}) - HP: {self.hp}/{self.max_hp} MP: {self.mp}/{self.max_mp}"
    
    @property
    def max_hp(self):
        return 100 + (self.level - 1) * 20 + self.strength * 2
    
    @property
    def max_mp(self):
        return 50 + (self.level - 1) * 10 + self.intellect * 3

# ... остальной код characters.py без изменений ...


class Character(Human, abc.ABC):
    """Абстрактный класс персонажа"""
    
    def __init__(self, name, level=1):
        super().__init__(name, level)
        self.skills = []
        self.inventory = []
        self._setup_skills()
    
    @abc.abstractmethod
    def _setup_skills(self):
        pass
    
    @abc.abstractmethod
    def basic_attack(self, target):
        pass
    
    @abc.abstractmethod
    def use_skill(self, skill_name, target=None, party=None):
        pass
    
    def update_cooldowns(self):
        """Обновление кулдаунов навыков"""
        for skill in list(self.cooldowns.keys()):
            self.cooldowns[skill] -= 1
            if self.cooldowns[skill] <= 0:
                del self.cooldowns[skill]


class Warrior(Character):
    """Класс Воина"""
    
    def _setup_skills(self):
        self.skills = [
            {"name": "Удар героя", "mp_cost": 10, "cooldown": 0, "description": "Мощная атака с двойным уроном"},
            {"name": "Щит бури", "mp_cost": 20, "cooldown": 3, "description": "Защита и контратака"},
            {"name": "Боевой клич", "mp_cost": 15, "cooldown": 2, "description": "Увеличивает силу всей группы"}
        ]
        self.hp = 150
        self.strength = 20
        self.agility = 12
        self.intellect = 8
    
    def basic_attack(self, target):
        damage = self.strength + random.randint(1, 10)
        if random.random() < 0.1:  # 10% шанс крита
            damage *= 2
            print(f"⚡ КРИТИЧЕСКИЙ УРОН! {self.name} наносит {damage} урона!")
        else:
            print(f"⚔️ {self.name} атакует {target.name} и наносит {damage} урона")
        target.hp -= damage
        return damage
    
    def use_skill(self, skill_name, target=None, party=None):
        skill = next((s for s in self.skills if s["name"] == skill_name), None)
        if not skill:
            return False
        
        if skill_name in self.cooldowns:
            print(f"❌ Навык {skill_name} на перезарядке! Осталось: {self.cooldowns[skill_name]} ходов")
            return False
        
        if self.mp < skill["mp_cost"]:
            print(f"❌ Недостаточно маны для {skill_name}!")
            return False
        
        self.mp -= skill["mp_cost"]
        self.cooldowns[skill_name] = skill["cooldown"]
        
        if skill_name == "Удар героя":
            damage = self.strength * 2 + random.randint(5, 15)
            target.hp -= damage
            print(f"🔥 {self.name} использует Удар героя на {target.name}! Нанесено {damage} урона!")
        
        elif skill_name == "Щит бури":
            self.effects.append({"name": "Щит", "duration": 2, "defense_bonus": 10})
            print(f"🛡️ {self.name} активирует Щит бури! Защита увеличена!")
        
        elif skill_name == "Боевой клич":
            for member in party:
                if member.is_alive:
                    member.strength += 5
                    member.effects.append({"name": "Боевой клич", "duration": 3, "strength_bonus": 5})
            print(f"📢 {self.name} издает Боевой клич! Сила группы увеличена!")
        
        return True


class Mage(Character):
    """Класс Мага"""
    
    def _setup_skills(self):
        self.skills = [
            {"name": "Огненный шар", "mp_cost": 15, "cooldown": 0, "description": "Базовая магическая атака"},
            {"name": "Ледяная стрела", "mp_cost": 20, "cooldown": 1, "description": "Замедляет цель"},
            {"name": "Щит маны", "mp_cost": 25, "cooldown": 4, "description": "Создает магический щит"}
        ]
        self.hp = 80
        self.mp = 100
        self.strength = 6
        self.agility = 10
        self.intellect = 24
    
    def basic_attack(self, target):
        damage = self.intellect // 2 + random.randint(1, 5)
        print(f"🔮 {self.name} атакует магией {target.name} и наносит {damage} урона")
        target.hp -= damage
        return damage
    
    def use_skill(self, skill_name, target=None, party=None):
        skill = next((s for s in self.skills if s["name"] == skill_name), None)
        if not skill:
            return False
        
        if skill_name in self.cooldowns:
            print(f"❌ Навык {skill_name} на перезарядке!")
            return False
        
        if self.mp < skill["mp_cost"]:
            print(f"❌ Недостаточно маны!")
            return False
        
        self.mp -= skill["mp_cost"]
        self.cooldowns[skill_name] = skill["cooldown"]
        
        if skill_name == "Огненный шар":
            damage = self.intellect + random.randint(10, 20)
            target.hp -= damage
            print(f"🔥 {self.name} запускает Огненный шар в {target.name}! Нанесено {damage} урона!")
        
        elif skill_name == "Ледяная стрела":
            damage = self.intellect // 2 + random.randint(5, 15)
            target.hp -= damage
            target.effects.append({"name": "Замедление", "duration": 2, "agility_reduction": 5})
            print(f"❄️ {self.name} выпускает Ледяную стрелу! {target.name} замедлен!")
        
        elif skill_name == "Щит маны":
            self.effects.append({"name": "Магический щит", "duration": 3, "damage_reduction": 0.5})
            print(f"💫 {self.name} создает Магический щит! Получаемый урон уменьшен!")
        
        return True


class Healer(Character):
    """Класс Целителя"""
    
    def _setup_skills(self):
        self.skills = [
            {"name": "Исцеление", "mp_cost": 20, "cooldown": 0, "description": "Лечит союзника"},
            {"name": "Божественный щит", "mp_cost": 30, "cooldown": 4, "description": "Защищает союзника"},
            {"name": "Молитва", "mp_cost": 40, "cooldown": 3, "description": "Лечит всю группу"}
        ]
        self.hp = 90
        self.mp = 120
        self.strength = 8
        self.agility = 12
        self.intellect = 20
    
    def basic_attack(self, target):
        damage = self.intellect // 3 + random.randint(1, 8)
        print(f"✨ {self.name} атакует {target.name} и наносит {damage} урона")
        target.hp -= damage
        return damage
    
    def use_skill(self, skill_name, target=None, party=None):
        skill = next((s for s in self.skills if s["name"] == skill_name), None)
        if not skill:
            return False
        
        if skill_name in self.cooldowns:
            print(f"❌ Навык {skill_name} на перезарядке!")
            return False
        
        if self.mp < skill["mp_cost"]:
            print(f"❌ Недостаточно маны!")
            return False
        
        self.mp -= skill["mp_cost"]
        self.cooldowns[skill_name] = skill["cooldown"]
        
        if skill_name == "Исцеление":
            heal = self.intellect + random.randint(15, 25)
            target.hp = min(target.max_hp, target.hp + heal)
            print(f"💚 {self.name} исцеляет {target.name} на {heal} HP!")  # ИСПРАВИТЬ: heal вместо heel
        
        elif skill_name == "Божественный щит":
            target.effects.append({"name": "Божественный щит", "duration": 2, "invulnerable": True})
            print(f"🌟 {self.name} защищает {target.name} Божественным щитом!")
        
        elif skill_name == "Молитва":
            for member in party:
                if member.is_alive:
                    heal = self.intellect // 2 + random.randint(10, 20)
                    member.hp = min(member.max_hp, member.hp + heal)
            print(f"🙏 {self.name} читает Молитву! Вся группа исцелена!")
        
        return True