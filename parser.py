import re
from victoria_parser import calculate_world_population
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


@timer
def main():
    data = read_vicky("input/empty_save.v2")
    provinces = data.split("\n2705=\n")[0]
    print(calculate_world_population(provinces))


if __name__ == '__main__':
    main()
