class Trader:
    cargo_capacity = 5

    def __init__(
        self,
        utilities,
        name,
        position,
        inventory,
        wallet,
        properties,
        holdings
    ):

        self.utilities = utilities
        
        self.name = name
        self.position = position
        self.inventory = inventory
        self.wallet = wallet
        self.properties = properties
        self.holdings = holdings

        self.current_town = None

    def property_property_owner(self):
        if "property_owner" not in self.properties:
            self.properties.append("property_owner")

    def describe(self):
        print(self.name)
        print("Cash: ", self.wallet)
        print("Inventory: ")
        # would like to add a way of getting the prices bought average
        print("     Food: ", self.inventory[0])
        print("     Goods: ", self.inventory[1])
        print("\nProperties:", self.properties)
        print("Holdings: ")
        if len(self.holdings) == 0:
            print("     N/A")
        for holding in self.holdings:
            print(
                "     ",
                holding.city.name,
                holding.type,
                holding.inventory,
                "producing",
                holding.production,
                "per day"
            )

    def cargo_capacity_remaining(self):
        cargo_capacity_occupied = 0

        for cargo in self.inventory:
            cargo_capacity_occupied += cargo

        return self.cargo_capacity - cargo_capacity_occupied