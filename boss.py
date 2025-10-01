import abc
import random  # ДОБАВИТЬ ЭТУ СТРОКУ
from characters import Human

class BossStrategy(abc.ABC):
    """Абстрактная стратегия поведения босса"""
    
    @abc.abstractmethod
    def execute(self, boss, targets):
        pass

class AggressiveStrategy(BossStrategy):
    """Агрессивная стратегия - атакует самого слабого"""
    
    def execute(self, boss, targets):
        alive_targets = [t for t in targets if t.is_alive]
        if not alive_targets:
            return
        
        target = min(alive_targets, key=lambda x: x.hp)
        damage = boss.strength + random.randint(10, 20)
        target.hp -= damage
        print(f"👹 {boss.name} яростно атакует {target.name}! Нанесено {damage} урона!")

class AOEStrategy(BossStrategy):
    """Стратегия массовой атаки"""
    
    def execute(self, boss, targets):
        alive_targets = [t for t in targets if t.is_alive]
        if not alive_targets:
            return
        
        damage = boss.intellect + random.randint(5, 15)
        for target in alive_targets:
            target.hp -= damage
        print(f"💀 {boss.name} использует массовую атаку! Все получают {damage} урона!")

class DebuffStrategy(BossStrategy):
    """Стратегия наложения дебаффов"""
    
    def execute(self, boss, targets):
        alive_targets = [t for t in targets if t.is_alive]
        if not alive_targets:
            return
        
        target = random.choice(alive_targets)
        target.effects.append({"name": "Проклятие", "duration": 3, "strength_reduction": 8})
        print(f"☠️ {boss.name} проклинает {target.name}! Сила уменьшена!")

class Boss(Human):
    """Класс босса с меняющимися стратегиями"""
    
    def __init__(self, name, level=10):
        super().__init__(name, level)
        self.hp = 500
        self.mp = 200
        self.strength = 30
        self.agility = 15
        self.intellect = 25
        self.strategies = {
            "aggressive": AggressiveStrategy(),
            "aoe": AOEStrategy(),
            "debuff": DebuffStrategy()
        }
        self.current_strategy = "aggressive"
    
    def take_turn(self, targets):
        """Босс делает ход согласно текущей стратегии"""
        # Меняем стратегию в зависимости от HP
        hp_percent = self.hp / self.max_hp
        
        if hp_percent < 0.3:  # Фаза ярости
            self.current_strategy = "aggressive"
        elif hp_percent < 0.6:  # Фаза массовых атак
            self.current_strategy = "aoe"
        else:  # Фаза дебаффов
            self.current_strategy = "debuff"
        
        strategy = self.strategies[self.current_strategy]
        strategy.execute(self, targets)
    
    @property
    def max_hp(self):
        return 500 + (self.level - 10) * 50