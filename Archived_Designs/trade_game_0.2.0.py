from World import World
from Trader import Trader
from Town import Town

from Utilities import Utilities


utilities = Utilities()

player = Trader(utilities, "The player", [1, 1], [0, 0], 1000, [], [])
dummy_player = Trader(utilities, "Dumb", [1, 1], [0, 0], 0, [], [])
town1 = Town(utilities, 'Los Mantos', (-2, 0), 500, [10, 10], 'Coastal', [])
town2 = Town(utilities, 'Kallac', (1, 1), 500, [10, 10], 'Karst', [])
town3 = Town(utilities, 'Vinas', (2, -2), 500, [10, 10], 'Hilly', [])

towns = [town1, town2, town3]
traders = [player, dummy_player]

world = World(utilities, 0, towns, traders)

run_game = True

input_action = None


def main_interface():
    player_town = world.player.current_town

    building_unlocked = False
    if player.wallet >= 5000 or "property_owner" in player.properties:
        building_unlocked = True
    sensible = 0

    try:
        if __name__ == '__main__':
            action = input('>: ')
        else:
            action = input_action
    except Exception:
        print("(Unintelligible)")

    if action == 'description':
        player_town.describe()
        sensible = 1
    if action == 'check':
        player.describe()
        sensible = 1
    if action == 'trade':
        world.trade()
        sensible = 1
    if action == 'travel':
        world.travel()
        sensible = 1
    if action == 'build' and building_unlocked:
        world.build()
        sensible = 1
    if action == 'interact':
        player_town.holdings[0].interact(player)
        sensible = 1

    if action == 'exit game':
        global run_game
        run_game = False
    else:
        if sensible == 0:
            print('What?')


def main_gameplay_loop():
    print('The following options are available: description, trade, travel and check. When finished just type "exit game" ')

    # regex this
    global run_game
    while run_game:
        main_interface()


if __name__ == '__main__':
    main_gameplay_loop()
