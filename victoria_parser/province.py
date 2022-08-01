from victoria_parser.pop import Pop


def create_further_lists(input_list: list, index: int):
    new_list = []
    while index < len(input_list):
        item = input_list.pop(index)
        if item[-1] == "{":
            new_list.append(item)
            inner_list = create_further_lists(input_list, index)
            new_list.append(inner_list)
        elif item[-1] != "}":
            new_list.append(item)
        else:
            break

    return new_list


def recursive_list_to_dict(recursive_list):
    # TODO: Eliminate unecessary lists
    new_dict = {}
    for index, item in enumerate(recursive_list):
        if type(item) is str:
            structure = item.split("=")
            if structure[0] in new_dict.keys():
                if structure[-1] == '{':
                    new_dict[structure[0]].append(recursive_list_to_dict(recursive_list[index + 1]))
                else:
                    new_dict[structure[0]].append(structure[-1])
            else:
                if structure[-1] == '{':
                    new_dict[structure[0]] = [recursive_list_to_dict(recursive_list[index + 1])]
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

    def get_total_population(self):
        all_pops = [pop.size for pop in self.pops]
        return sum(all_pops)


class Provinces:
    # TODO: Move reading statement up
    def __init__(self, province):
        list_of_equals = [item.strip() for item in province.split("\n")]
        for index, item in enumerate(list_of_equals):
            if item == "{":
                item = list_of_equals.pop(index)
                list_of_equals[index - 1] += item
            else:
                continue
        new_list = list_of_equals
        new_list = create_further_lists(new_list, 0)
        data = recursive_list_to_dict(new_list)
        self._aslist = new_list
        self._data = data
        self.provinces = []
        for key in data:
            self.provinces.append(Province(data, key))


def calculate_world_population(province):
    world = Provinces(province)
    population = []
    for province in world.provinces:
        province_population = province.get_total_population()
        population.append(province_population)
    return sum(population) * 4


def main():
    pass


if __name__ == '__main__':
    main()

