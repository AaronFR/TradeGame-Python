from Classes.World import World
from Classes.Trader import Trader
from Classes.Town import Town

from Utility.Utilities import Utilities
# from Gui import Gui


class Game_interface:

    def __init__(self, utilities):
        self.utilities = utilities

        player = Trader(utilities, "The player", [1, 1], [0, 0], 1000, [], [])
        dummy_player = Trader(utilities, "Dumb", [1, 1], [0, 0], 0, [], [])
        town1 = Town(utilities, 'Los Mantos', (-2, 0), 500, [10, 10], 'Coastal', [])
        town2 = Town(utilities, 'Kallac', (1, 1), 500, [10, 10], 'Karst', [])
        town3 = Town(utilities, 'Vinas', (2, -2), 500, [10, 10], 'Hilly', [])

        towns = [town1, town2, town3]
        traders = [player, dummy_player]

        self.world = World(utilities, 0, towns, traders)

        self.run_game = True
        self.input_action = None

        opening_text = (
            'The following options are available: '
            'description, trade, travel and check. '
            'When finished just type "exit game"'
        )
        if utilities.run_through_terminal:
            print(opening_text)
        else:
            utilities.text_package = opening_text

    def main_interface(self):
        player_town = self.world.player.current_town

        building_unlocked = False
        if (
            self.world.player.wallet >= 5000 or
            "property_owner" in self.world.player.properties
        ):
            building_unlocked = True
        sensible = 0

        try:
            if __name__ == '__main__':
                action = input('>: ')
            else:
                action = self.utilities.ask_action('')
        except Exception as e:
            print("(Unintelligible)")
            print(e)

        if action == 'description':
            player_town.describe()
            sensible = 1
        if action == 'check':
            self.world.player.describe()
            sensible = 1
        if action == 'trade':
            self.world.trade()
            sensible = 1
        if action == 'travel':
            self.world.travel()
            sensible = 1
        if action == 'build' and building_unlocked:
            self.world.build()
            sensible = 1
        if action == 'interact':
            player_town.holdings[0].interact(self.world.player)
            sensible = 1

        if action == 'exit game':
            self.run_game = False
        else:
            if sensible == 0:
                print('What?')

    def main_gameplay_loop(self):
        # regex this
        while self.run_game:
            self.main_interface()


if __name__ == '__main__':
    utilities = Utilities()
    utilities.run_through_terminal = True

    game_interface = Game_interface(utilities)
    game_interface.main_gameplay_loop()
