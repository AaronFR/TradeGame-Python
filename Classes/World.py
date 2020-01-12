from Classes.Building import Building
import math
from Utility.Content_package import Content_package


class World:
    content_package = Content_package("")

    def __init__(self, utilities, date, towns, traders):
        self.utilities = utilities

        self.date = date
        self.towns = towns
        self.traders = traders

        self.player = traders[0]
        self.player.current_town = self.get_current_town(self.player)

    def time_tick(self, days):
        """
        Calculated daily
        """
        for day in range(0, days):
            self.economic_calculations()
            self.date += 1

    def economic_calculations(self):
        """
        Calculates all global economic activity for towns and buildings
        """
        for town in self.towns:
            town.update()

            for building in town.holdings:
                building.update()

    def get_current_town(self, entity):
        """
        This my be necessary to keep as a last resort but for large numbers of
        towns the efficient anwser would be to update the town variable of the 
        trader to that town
        """
        for town in self.towns:
            if (
                town.position[0] == entity.position[0] and
                town.position[1] == entity.position[1]
            ):
                return town

        return None

    def get_town_object_from_name(self, town_name):
        """Currently Unused
        """
        for town in self.towns:
            if town_name == town.name:
                return town

    def calculate_distance(self, entity, chosen_town):
        x_difference = entity.position[0] - chosen_town.position[0]
        y_difference = entity.position[1] - chosen_town.position[1]

        return round((x_difference ** 2 + y_difference ** 2) ** (1/2), 2)

    def travel_listing(self):
        print_string = (
            f'Current Location: {self.player.current_town.name}'
            '\nDestinations: \n'
        )

        for town in self.towns:
            if list(town.position) != self.player.position:
                print_result = round(
                        (self.calculate_distance(self.player, town) * 100), 3
                )

                print_string += (
                    "    "
                    f"{town.name}"
                    f" {print_result}"
                    ' Kilometers\n'
                )

        self.utilities.print_text(print_string)

        action = self.utilities.ask_action('Where to?: ')
        return action

    def travel(self, destination=None):
        if destination is None:
            destination = self.travel_listing()

        for town in self.towns:
            if town.name == destination:
                selected_town = town
                distance = self.calculate_distance(self.player, town)
                days_taken = math.ceil(distance)

                self.time_tick(days_taken)
                self.player.position = list(selected_town.position)
                self.player.current_town = selected_town

                print("     Current Location:", self.player.current_town.name)
                print("     Journey took:", days_taken, "days")

    def trade(self):
        prices = self.player.current_town.calculate_prices()

        goods_price_readout_string = (
            f'\nFood:   {prices[0]}, per Crate'
            f'\nGoods:  {prices[1]}, per Crate'
            f'\nWallet: {round(self.player.wallet, 2)}\n'
        )

        self.utilities.print_text(goods_price_readout_string)
        action = self.utilities.ask_action('What would you like to trade... ')

        i = None
        if action == 'food':
            i = 0

        if action == 'goods':
            i = 1

        if i is not None:
            print('1 unit for ',  prices[i])
            print(
                '5 units for ',
                self.player.current_town.cummulative_price(5, i)
            )
            try:
                buy = int(
                    input(
                        'How much you trading? (negative for sell): '
                        )
                )
            except ValueError:
                buy = 0
            
            bill = self.player.current_town.cummulative_price(buy, i)
            transaction_allowed = True

            if bill > self.player.wallet:
                print("Hey! You don't have enough money!")
                transaction_allowed = False
            if buy > self.player.current_town.inventory[i]:
                if self.player.current_town.inventory[i] >= 0:
                    print("The town doesn't even have that much stock")
                    print("Town Stock", self.player.current_town.inventory[i])
                    print("Transaction Quantity", buy)
                    transaction_allowed = False
            if buy > self.player.cargo_capacity_remaining():
                print("You don't have that much space for that cargo")
                transaction_allowed = False
            if buy < -self.player.inventory[i]:
                print("You don't have that much commodity to sell")
                transaction_allowed = False

            if transaction_allowed:
                if (
                    buy > self.player.current_town.inventory[i] and
                    self.player.current_town.inventory[i] < 0
                ):
                    if buy < 0:
                        print("much obliged")
                    if buy > 0:
                        print("Fine ...You Bastard")

                self.player.current_town.inventory[i] -= buy
                self.player.wallet -= bill
                self.player.inventory[i] += buy

    def build(self):
        print(f"Construction Options in {self.player.current_town.name}:")
        print("     Farm: 5000 credits, 3 goods")
        print("     prod: 1 food")

        action = input('What would you like to build... ')

        if action == "farm":
            Building.build(
                'farm',
                self.player.current_town,
                [0, 0],
                self.player
            )

        self.player.property_property_owner()