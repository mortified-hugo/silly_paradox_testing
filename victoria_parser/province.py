from victoria_parser.pop import Pop


def create_further_lists(input_list: list):
    new_list = []
    index = 0
    item = ' '
    while item == '' or item[-1] != '}':
        try:
            item = input_list.pop(index)
            if item == '' or item[-1] == "=":
                new_list.append(item)
                inner_list = create_further_lists(input_list)
                new_list.append(inner_list)
            else:
                new_list.append(item)
        except IndexError:
            break

    return new_list


def recursive_list_to_dict(recursive_list):
    # TODO: Eliminate unecessary lists
    new_dict = {}
    for index, item in enumerate(recursive_list):
        structure = item.split("=")
        if structure[0] in new_dict.keys():
            if structure[-1] == '':
                take_list = recursive_list.pop(index + 1)
                new_dict[structure[0]].append(recursive_list_to_dict(take_list))
            else:
                new_dict[structure[0]].append(structure[-1])
        else:
            if structure[-1] == '':
                take_list = recursive_list.pop(index + 1)
                new_dict[structure[0]] = [recursive_list_to_dict(take_list)]
            else:
                new_dict[structure[0]] = [structure[-1]]
    return new_dict


class Province:
    types_of_pops = ["aristocrats", "capitalists", "artisans", "bureaucrats", "clergymen", "clerks",
                     "officers", "craftsmen", "farmers", "labourers", "slaves", "soldiers"]

    def __init__(self, data, number):
        self.number = number
        self.province_info = data[self.number][0]
        try:
            self.tag = self.province_info["owner"][0]
        except KeyError:
            self.tag = ''
        self.name = self.province_info["name"][0]
        self.pops = []
        for type_of_pops in self.types_of_pops:
            try:
                self.pops.append(Pop(self.province_info[type_of_pops], type_of_pops))
            except KeyError:
                continue
        all_pops = [pop.size for pop in self.pops]
        self.population = sum(all_pops)


class Provinces:
    def __init__(self, province):
        list_of_equals = [item.strip() for item in province.split("\n")]
        for index, item in enumerate(list_of_equals):
            if item == "{":
                list_of_equals.pop(index)
                #list_of_equals[index - 1] += item
            else:
                continue
        new_list = create_further_lists(list_of_equals)
        data = recursive_list_to_dict(new_list)
        self._aslist = new_list
        self._data = data
        self.provinces = []
        for key in data:
            self.provinces.append(Province(data, key))

    def calculate_world_population(self):
        population = []
        for province in self.provinces:
            province_population = province.population
            population.append(province_population)
        return sum(population) * 4

    def calculate_country_population(self, tag):
        total_country_population = []
        for province in self.provinces:
            if province.tag == f'"{tag}"':
                total_country_population.append(province.population)
            else:
                continue
        return sum(total_country_population) * 4

    def append(self, more_provinces):
        self.provinces += more_provinces.provinces


def get_world_data(province):
    world = Provinces(province)
    return world


def main():
    pass


if __name__ == '__main__':
    main()

