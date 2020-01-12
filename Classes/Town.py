import math
from Utility.Economic_unit import Economic_unit


class Town(Economic_unit):
    def __init__(
        self,
        utilities,
        name,
        position,
        population,
        inventory,
        properties,
        holdings
    ):
        """
        Huge lesson here, holdings used to be
        holdings = []
        This however caused an operation on the holdings property, to be shared
        between all objects within the class

        So I think any assinging of a defualt value, will cause it to become
        global... somehow.
        """

        self.utilities = utilities
        
        self.name = name
        self.position = position
        self.population = population
        self.inventory = inventory
        self.properties = properties
        self.holdings = holdings

        self.production = [0, 0]
        self.consumption = [0, 0]

        self.max_price = 500

    def describe(self):
        print(self.name)
        print('Population:', self.population)
        print(self.properties)

    def update(self):
        """
        With a big enough number of possible town properties this should be
        made into a csv
        """
        for commodity in range(len(self.inventory)):
            commodity_quantity = self.inventory[commodity]

            modifier = self.exponential_scaling(commodity_quantity)

            self.consumption[commodity] = 1 * modifier
            self.inventory[commodity] -= self.consumption[commodity]

        modifier_list = self.modify_production_by_properties(self)
        self.production = [1 * modifier_list[0], 1 * modifier_list[1]]

        for commodity in range(len(self.inventory)):
            self.inventory[commodity] += self.production[commodity]

    def exponential_scaling(self, commodity_quantity):
        exponential_scale = (
            commodity_quantity / (self.population / 20)
        )
        if exponential_scale > 1:
            exponential_scale = 1

        return math.exp(exponential_scale)

    def calculate_prices(self, mock_inventory=None):
        prices = []
        if mock_inventory is None:
            inventory = self.inventory
        else:
            inventory = mock_inventory

        for commodity in inventory:
            multiplier = 1 / self.exponential_scaling(commodity)
            price = round(self.max_price * multiplier, 1)
            prices.append(price)

        return prices

    def cummulative_price(self, transaction_quantity, i):
        prices = self.calculate_prices()
        mock_inventory = list(self.inventory)

        cummulative_price = 0
        if transaction_quantity < 0:
            transaction_quantity = -transaction_quantity
            for delta in range(transaction_quantity):
                prices = self.calculate_prices(mock_inventory)
                mock_inventory[i] += 1
                cummulative_price -= prices[i]
        else:
            for delta in range(transaction_quantity):
                prices = self.calculate_prices(mock_inventory)
                mock_inventory[i] -= 1
                cummulative_price += prices[i]

        return cummulative_price
