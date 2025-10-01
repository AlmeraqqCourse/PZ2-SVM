import random  # ДОБАВИТЬ ЭТУ СТРОКУ

class EffectSystem:
    """Система управления эффектами"""
    
    @staticmethod
    def apply_effects(character):
        """Применяет эффекты к персонажу"""
        for effect in character.effects[:]:
            # Применяем эффекты
            if effect["name"] == "Замедление":
                character.agility -= effect.get("agility_reduction", 5)
            elif effect["name"] == "Боевой клич":
                character.strength += effect.get("strength_bonus", 5)
            
            # Уменьшаем длительность
            effect["duration"] -= 1
            if effect["duration"] <= 0:
                # Убираем эффекты при завершении
                if effect["name"] == "Замедление":
                    character.agility += effect.get("agility_reduction", 5)
                elif effect["name"] == "Боевой клич":
                    character.strength -= effect.get("strength_bonus", 5)
                
                character.effects.remove(effect)
                print(f"💨 Эффект {effect['name']} закончился у {character.name}")
    
    @staticmethod
    def calculate_damage_with_effects(attacker, target, base_damage):
        """Рассчитывает урон с учетом эффектов"""
        final_damage = base_damage
        
        # Эффекты атакующего
        for effect in attacker.effects:
            if effect["name"] == "Боевой клич":
                final_damage += effect.get("strength_bonus", 0)
        
        # Эффекты защиты цели
        for effect in target.effects:
            if effect["name"] == "Магический щит":
                final_damage = int(final_damage * 0.5)
            elif effect["name"] == "Щит":
                final_damage -= effect.get("defense_bonus", 0)
            elif effect["name"] == "Божественный щит" and effect.get("invulnerable", False):
                final_damage = 0
                print(f"✨ {target.name} защищен Божественным щитом!")
        
        return max(0, final_damage)