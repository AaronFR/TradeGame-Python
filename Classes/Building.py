import re
from Utility.Economic_unit import Economic_unit


class Building(Economic_unit):
    base_production = 0.5
    base_consumption = [0, 0.1]
    base_maintenance = 100
    base_cost_to_build = 5000
    base_resources_to_build = [0, 3]

    def __repr__(self):
        return f"Building({self.utilities}, {self.type}, {self.city},"
        f"{self.inventory}, {self.owner})"

    @classmethod
    def build(cls, utilities, type, city, inventory, owner):
        if type == "farm":
            if (
                owner.inventory[1] >= cls.base_resources_to_build[1] and
                owner.wallet >= cls.base_cost_to_build
            ):
                owner.wallet -= cls.base_cost_to_build
                owner.inventory[0] -= cls.base_resources_to_build[1]
                print("Build Succesful")
                return cls(type, city, inventory, owner)
            else:
                print("Insufficient Resources")

    def __init__(self, utilities, type, city, inventory, owner):
        self.utilities = utilities
        
        self.type = type
        self.city = city

        self.inventory = inventory
        self.owner = owner

        self.production = [0, 0]
        self.consumption = [0, 0]

        self.city.holdings.append(self)
        owner.holdings.append(self)

    def update(self):
        self.calculate_production()

        self.inventory[0] += self.production[0]
        self.inventory[1] += self.production[1]

        self.inventory[0] -= self.consumption[0]
        self.inventory[1] -= self.consumption[1]

        self.owner.wallet -= self.base_maintenance
        print(f"maintance of {self.type} cost {self.base_maintenance}")
        print("inventory", self.inventory)

    def calculate_production(self):
        current_town = self.city

        modifier_list = self.modify_production_by_properties(current_town)

        if self.type == "farm":
            if self.inventory[1] >= self.base_consumption[1]:
                self.production[0] = self.base_production * modifier_list[0]
                self.consumption = self.base_consumption
            else:
                self.production[0] = 0
                self.consumption[1] = 0
                print(f"INSUFFICIENT RESOURCES")

    def interact(self, entity):
        print(f"{self.type} in {self.city.name}")
        print(f"Production: {self.production} per day")
        print(f"\nInventory: {self.inventory}")

        try:
            action = input('>: ')
        except TypeError:
            print("(Unintelligible)")

        if action == "transfer":
            print("How much to transfer? (negative for deposit)")
            print("e.g. 5 food")

            text_to_parse = input('>: ')

            number_regex = re.search("[-+]?[0-9]+", text_to_parse)
            string_regex = re.search("[a-z]+", text_to_parse)

            number = int(number_regex.group())
            if type(number) is None:
                number = 0
            selection = string_regex.group()

            i = None
            try:
                if selection == "food":
                    i = 0
                if selection == "goods":
                    i = 1
            except TypeError:
                print("?")

            if i is not None:
                if number > self.inventory[i]:
                    print("Insufficient stock for withdrawl")
                elif number > entity.cargo_capacity:
                    print(
                        "You have insufficient free space for that withdrawl"
                    )
                elif number < 0 and number < -entity.inventory[i]:
                    print("Insufficient stock for deposit")
                else:
                    self.inventory[i] -= number
                    print("Transferred!")
                    entity.inventory[i] += number
