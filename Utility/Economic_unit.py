class Economic_unit:

    @staticmethod
    def modify_production_by_properties(current_town):
        """
        Designed to reduce redundant code between town and building classes
        """
        modifier_list = [1, 1]
        if current_town.properties == "Coastal":
            modifier_list[0] *= 1.1
        if current_town.properties == "Karst":
            modifier_list[0] *= 0.7
            modifier_list[1] *= 1.2
        if current_town.properties == "Hilly":
            modifier_list[0] *= 0.9
            modifier_list[1] *= 1.1

        return modifier_list
