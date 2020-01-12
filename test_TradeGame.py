"""
You have a stellaris like bug, where an item can be bought and sold and bought
and sold. The sell price will be higher than the buy due to supply and demand,
leading to infinite profit, however I'll leave it for now as an exploit,
to make money quickly
"""

import trade_game as game
from World import World
from Trader import Trader
from Town import Town
from Building import Building

import io


class Test_class:
    def setup_class(self):
        self.town1 = Town('Los Mantos', (-2, 0), 500, [10, 10], 'Coastal', [])
        self.town2 = Town('Kallac', (1, 1), 500, [10, 10], 'Karst', [])
        self.town3 = Town('Vinas', (2, -2), 500, [10, 10], 'Hilly', [])
        self.towns = [self.town1, self.town2, self.town3]

        self.player = Trader("The player", [1, 1], [0, 0], 15000, [], [])
        self.traders = [self.player]

        self.world = World(0, self.towns, self.traders)

    def test_journeys_take_time(self, monkeypatch):
        game.current_town = self.town2

        initial = self.world.date
        monkeypatch.setattr('sys.stdin', io.StringIO('Los Mantos'))
        self.world.travel()

        final = self.world.date
        assert final > initial
        assert final == initial + 4

    def test_basic_economics_town_consumption(self):
        case_study_town = self.towns[2]

        self.world.time_tick(1)

        assert case_study_town.consumption[0] > 0
        assert case_study_town.consumption[1] > 0

    def test_basic_economics_town_production(self):
        case_study_town = self.towns[0]
        self.world.time_tick(1)

        assert case_study_town.production[0] > 0
        assert case_study_town.production[1] > 0

    def test_economics_supply_vs_demand(self):
        case_study_town = self.towns[2]

        case_study_town.inventory = [50, 50]
        case_study_town.update()
        consumption_in_plenty = case_study_town.consumption.copy()

        case_study_town.inventory = [3, 3].copy()
        case_study_town.update()
        consumption_in_poverty = case_study_town.consumption.copy()

        assert consumption_in_plenty[0] > consumption_in_poverty[0]

    def test_economics_properties_affect_production(self):
        case_study_town = self.towns[0]

        self.world.time_tick(1)
        production_with_properties = case_study_town.production

        case_study_town.properties = ""
        self.world.time_tick(1)
        production_without_properties = case_study_town.production
        case_study_town.properties = "Coastal"

        assert production_with_properties > production_without_properties

    # build menu

    def test_building_placed(self):
        case_study_town = self.towns[0]
        test_farm = Building("farm", case_study_town, [0, 0], self.player)
        case_study_town.holdings.append(test_farm)
        case_study_town.holdings = [test_farm]

        assert test_farm in case_study_town.holdings

    def test_building_buffed_by_town_properties(self):
        town_buffed = self.towns[0]
        town_norm = self.towns[2]
        town_dampened = self.towns[1]

        arb = 10

        farm_buffed = Building("farm", town_buffed, [0, arb], self.player)
        farm_norm = Building("farm", town_norm, [0, arb], self.player)
        farm_dampened = Building("farm", town_dampened, [0, arb], self.player)

        farm_buffed.calculate_production()
        farm_norm.calculate_production()
        farm_dampened.calculate_production()

        print(farm_buffed.city.properties)
        print(farm_norm.city.properties)
        print(farm_dampened.city.properties)

        farm_rich = farm_buffed.production[0]
        farm_standard = farm_norm.production[0]
        farm_poor = farm_dampened.production[0]

        assert farm_rich > farm_standard
        assert farm_standard > farm_poor
