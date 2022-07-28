import re
from glob import glob


def read_vicky(file):
    with open(file, mode='r') as save_file:
        all_losses = []
        for line in save_file:
            if re.match(r"\s+losses=.", line):
                all_losses.append(int(re.findall(r'\d+', line)[0]))
            else:
                pass

        return sum(all_losses)


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


def main():
    for file in glob("input/*.v2"):
        print(read_vicky(file))
    print(read_eu4("input/gamestate"))


if __name__ == '__main__':
    main()
