class Item:
    """Базовый класс предмета"""
    
    def __init__(self, name, description, item_type):
        self.name = name
        self.description = description
        self.type = item_type
    
    def use(self, target):
        pass

class HealthPotion(Item):
    """Зелье здоровья"""
    
    def __init__(self):
        super().__init__(
            "Зелье здоровья",
            "Восстанавливает 50 HP",
            "consumable"
        )
    
    def use(self, target):
        heal_amount = 50
        target.hp = min(target.max_hp, target.hp + heal_amount)
        print(f"🧪 {target.name} использует Зелье здоровья! +{heal_amount} HP")
        return True

class ManaPotion(Item):
    """Зелье маны"""
    
    def __init__(self):
        super().__init__(
            "Зелье маны", 
            "Восстанавливает 30 MP",
            "consumable"
        )
    
    def use(self, target):
        mana_amount = 30
        target.mp = min(target.max_mp, target.mp + mana_amount)
        print(f"🔵 {target.name} использует Зелье маны! +{mana_amount} MP")
        return True

class Inventory:
    """Инвентарь персонажа"""
    
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        self.items.append(item)
    
    def remove_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                return item
        return None
    
    def get_items(self):
        return [f"{item.name}: {item.description}" for item in self.items]