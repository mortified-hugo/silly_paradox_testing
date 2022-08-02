import re
from victoria_parser import get_world_data
from utils import timer


def read_vicky(file):
    with open(file, mode='r') as save_file:
        save_data = save_file.read()
        remove_junk = save_data.split('\n1=\n{')
        all_provinces = '1=\n{' + remove_junk[-1].split('\n3000=\n{')[0]
        return all_provinces


def read_eu4(file):
    with open(file, mode='r') as save_file:
        everything = save_file.read()
        losses = re.findall(r"members=.\n.+\n", everything)
        all_losses = []
        for event in losses:
            all_losses.append(re.findall(r'\d+', event))
        list_of_losses = []
        for event_losses in all_losses:
            for type_of_loss in event_losses:
                list_of_losses.append(int(type_of_loss))
        return sum(list_of_losses)


def read_by_factor(provinces, factor):
    partial = provinces.split(f"\n{factor + 1}=\n")
    provinces = f"{factor + 1}=\n" + partial[-1]
    world = get_world_data(partial[0])
    for n in range(2, round(2800/factor) + 1):
        n *= factor
        n += 1
        partial = provinces.split(f"\n{n}=\n")
        provinces = f"{n}=\n" + partial[-1]
        group_data = get_world_data(partial[0])
        world.append(group_data)

    return world

@timer
def main():
    data = read_vicky("input/GG.v2")
    provinces = data.split("\n2800=\n")[0]  # 2704
    world = read_by_factor(provinces, 25)
    world_population = world.calculate_world_population()
    russian_population = world.calculate_country_population('GER')
    percentage = round(russian_population/world_population, 2)
    print(f"There are {world_population} people in this world, "
          f"of those {russian_population} live in Germany, {percentage}% of the total")


if __name__ == '__main__':
    main()
