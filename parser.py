import re
import json
import matplotlib.pyplot as plt
from listener import Listener
from victoria_parser import get_world_data
from utils import timer


def read_vicky(file):
    with open(file, mode='r') as save_file:
        date = save_file.read(12)[-6:]
        country = save_file.read(15)[-3:]

        save_data = save_file.read()

        remove_junk = save_data.split('\n1=\n{')
        all_provinces = '1=\n{' + remove_junk[-1].split('\n3000=\n{')[0]
        return all_provinces, date, country


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


def print_world_population(file):
    # TODO: Make it a list of several countries
    data, date, player_country = read_vicky(file)
    provinces = data.split("\n2800=\n")[0]  # 2704
    world = read_by_factor(provinces, 25)
    world_population = world.calculate_world_population()

    country_population = world.calculate_country_population(player_country)
    percentage = round(country_population/world_population, 2)

    return world_population, date, country_population, player_country, percentage


@timer
def main():
    try:
        with open("pop.json", mode="r") as file:
            population = json.load(file)
    except FileNotFoundError:
        population = {}
    # CHANGE YOUR SAVE_FILE HERE
    watch_file = Listener("C:/Users/Hugo/Documents/Paradox Interactive/Victoria II/HPM/save games/autosave.v2")
    while True:
        info = watch_file.run(print_world_population, watch_file.filename)
        if (info is not None) and (info[1] not in population.keys()):
            population[info[1]] = info[0]
            awnser = f"There were {info[0]} people in {info[1]}."
            awnser += f"\n{info[2]} lived in the player's country " \
                      f"({info[3]}), {info[4]}% of the total\n"
            print(awnser)
            with plt.ion():
                plt.plot(population.values())
            with open("pop.json", mode="w") as file:
                json.dump(population, file)
        else:
            plt.pause(1)


if __name__ == '__main__':
    main()
