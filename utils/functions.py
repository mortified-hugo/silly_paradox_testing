from time import time


def avg(list_of_numbers: list):
    return sum(list_of_numbers)/len(list_of_numbers)


def timer(func):
    def timed_func():
        start = time()
        func()
        end = time()
        print(f"Run in {round(end - start, 2)} seconds")
    return timed_func
