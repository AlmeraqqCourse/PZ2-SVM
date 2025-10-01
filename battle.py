import random
from effects import EffectSystem

class TurnOrder:
    """Итератор для определения порядка ходов"""
    
    def __init__(self, party, boss):
        self.party = party
        self.boss = boss
        self.current_turn = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        # Собираем всех участников боя
        all_combatants = self.party + [self.boss]
        alive_combatants = [c for c in all_combatants if c.is_alive]
        
        if not alive_combatants:
            raise StopIteration
        
        # Сортируем по ловкости для определения порядка ходов
        alive_combatants.sort(key=lambda x: x.agility, reverse=True)
        
        if self.current_turn >= len(alive_combatants):
            self.current_turn = 0
        
        next_combatant = alive_combatants[self.current_turn]
        self.current_turn += 1
        
        return next_combatant

class Battle:
    """Класс управления боем"""
    
    def __init__(self, party, boss):
        self.party = party
        self.boss = boss
        self.turn_order = TurnOrder(party, boss)
        self.round = 1
    
    def start_battle(self):
        """Запускает бой"""
        print("\n" + "="*50)
        print("🚨 НАЧИНАЕТСЯ БОЙ! 🚨")
        print("="*50)
        
        while any(member.is_alive for member in self.party) and self.boss.is_alive:
            print(f"\n--- Раунд {self.round} ---")
            
            for combatant in self.turn_order:
                if not combatant.is_alive:
                    continue
                
                if combatant == self.boss:
                    self._boss_turn()
                else:
                    self._player_turn(combatant)
                
                # Проверяем конец боя
                if not self.boss.is_alive or not any(member.is_alive for member in self.party):
                    break
            
            self._end_round()
            self.round += 1
        
        self._end_battle()
    
    def _player_turn(self, player):
        """Ход игрока"""
        print(f"\n🎯 Ход {player.name}:")
        print(f"HP: {player.hp}/{player.max_hp} | MP: {player.mp}/{player.max_mp}")
        
        # Показываем доступные действия
        actions = ["1. Базовая атака", "2. Использовать навык"]
        if any(item.type == "consumable" for item in player.inventory):
            actions.append("3. Использовать предмет")
        
        print(" | ".join(actions))
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            self._basic_attack(player)
        elif choice == "2":
            self._use_skill(player)
        elif choice == "3" and "3. Использовать предмет" in actions:
            self._use_item(player)
        else:
            print("❌ Неверный выбор! Пропуск хода.")
    
    def _basic_attack(self, player):
        """Базовая атака игрока"""
        damage = player.basic_attack(self.boss)
        actual_damage = EffectSystem.calculate_damage_with_effects(player, self.boss, damage)
        self.boss.hp -= actual_damage
    
    def _use_skill(self, player):
        """Использование навыка игроком"""
        print("\nДоступные навыки:")
        for i, skill in enumerate(player.skills, 1):
            cooldown_info = f" [КД: {player.cooldowns.get(skill['name'], 0)}]" if skill['name'] in player.cooldowns else ""
            print(f"{i}. {skill['name']} (Мана: {skill['mp_cost']}){cooldown_info}")
        
        try:
            choice = int(input("Выберите навык: ")) - 1
            if 0 <= choice < len(player.skills):
                skill = player.skills[choice]
                player.use_skill(skill["name"], self.boss, self.party)
            else:
                print("❌ Неверный выбор!")
        except ValueError:
            print("❌ Введите число!")
    
    def _use_item(self, player):
        """Использование предмета"""
        consumables = [item for item in player.inventory if item.type == "consumable"]
        if not consumables:
            print("❌ Нет расходуемых предметов!")
            return
        
        print("\nДоступные предметы:")
        for i, item in enumerate(consumables, 1):
            print(f"{i}. {item.name}")
        
        try:
            choice = int(input("Выберите предмет: ")) - 1
            if 0 <= choice < len(consumables):
                item = consumables[choice]
                if item.use(player):
                    player.inventory.remove(item)
            else:
                print("❌ Неверный выбор!")
        except ValueError:
            print("❌ Введите число!")
    
    def _boss_turn(self):
        """Ход босса"""
        print(f"\n👹 Ход {self.boss.name}:")
        alive_party = [member for member in self.party if member.is_alive]
        self.boss.take_turn(alive_party)
    
    def _end_round(self):
        """Завершение раунда"""
        # Обновляем кулдауны и эффекты
        for member in self.party:
            if member.is_alive:
                member.update_cooldowns()
                EffectSystem.apply_effects(member)
        
        EffectSystem.apply_effects(self.boss)
        
        # Показываем статус
        print(f"\n📊 Статус после раунда {self.round}:")
        for member in self.party:
            status = "💚" if member.is_alive else "💀"
            print(f"{status} {member.name}: HP {member.hp}/{member.max_hp}")
        print(f"👹 {self.boss.name}: HP {self.boss.hp}/{self.boss.max_hp}")
    
    def _end_battle(self):
        """Завершение боя"""
        print("\n" + "="*50)
        if not self.boss.is_alive:
            print("🎉 ПОБЕДА! Босс повержен!")
            print("💎 Герои получают сокровища и славу!")
        else:
            print("💀 ПОРАЖЕНИЕ... Босс оказался сильнее.")
        print("="*50)