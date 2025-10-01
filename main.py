import random
from game_data import GameData
from battle import Battle
from mixins import GameSessionManager, LoggingMixin

class WarcraftRPG(LoggingMixin):
    """Главный класс игры"""
    
    def __init__(self):
        super().__init__()
        self.party = []
        self.boss = None
    
    def start_game(self):
        """Запускает игру"""
        with GameSessionManager():
            self._show_intro()
            self._setup_game()
            self._show_boss_intro()
            self._start_battle()
            self._show_ending()
    
    def _show_intro(self):
        """Показывает вступление"""
        print(GameData.get_intro_story())
        input("\nНажмите Enter чтобы продолжить...")
    
    def _setup_game(self):
        """Настраивает игру"""
        print("\n🧙‍♂️ Формирование группы героев...")
        self.party = GameData.create_party()
        GameData.setup_initial_items(self.party)
        
        print("\n✅ Ваша группа:")
        for member in self.party:
            print(f"  - {member}")
            print(f"    Навыки: {', '.join(skill['name'] for skill in member.skills)}")
        
        input("\nНажмите Enter чтобы продолжить...")
    
    def _show_boss_intro(self):
        """Показывает вступление к бою с боссом"""
        print(GameData.get_boss_intro())
        input("\nНажмите Enter чтобы начать бой...")
    
    def _start_battle(self):
        """Начинает бой"""
        self.boss = GameData.create_boss()
        battle = Battle(self.party, self.boss)
        battle.start_battle()
    
    def _show_ending(self):
        """Показывает завершение игры"""
        if any(member.is_alive for member in self.party) and not self.boss.is_alive:
            ending = """
🎉 ЭПИЛОГ: ПОБЕДА ДОБРА!

С последним вздохом Арканиса, темная энергия рассеивается...
Портал Бездны закрывается, и мир Азерота спасен!

Короли и королевы всех королевств чествуют героев.
Ваши имена будут воспеты в песнях и легендах на века!

Спасибо за игру! Азерот в безопасности... пока что.
            """
        else:
            ending = """
💀 ЭПИЛОГ: ТРИУМФ ТЬМЫ...

С падением героев, ничто не может остановить Арканиса.
Темная магия поглощает Азерот, превращая его в царство Бездны.

Надежда угасла, свет погас...
Мир погружается в вечную тьму.

Игра окончена. Может быть, в другой раз удача будет на вашей стороне...
            """
        
        print(ending)
        self.log_event("Игра завершена")

if __name__ == "__main__":
    random.seed(42)  # Для повторяемости результатов
    game = WarcraftRPG()
    game.start_game()