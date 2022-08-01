from dataclasses import dataclass
from utils import avg


@dataclass
class Pop:
    def __init__(self, pop_dict, pop_type):
        self._asdict = pop_dict
        self.pop_type = pop_type
        self.size = 0
        for pop_info in self._asdict:
            self.size += int(pop_info["size"][0])
        self.literacy = round(avg([float(n["literacy"][0]) for n in self._asdict]), 2)




