import random


class Manufacturer:

    def __init__(self):
        self.offer = []

    def __str__(self):
        s = " ".join(map(str, self.offer))
        return s

    def make_offer(self, tile_pool):
        for i in range(4):
            if len(self.offer) < 4:
                available_tile = [key for key, value in tile_pool.items() if value > 0]
                chosen_tile = (random.choice(available_tile))
                self.offer.append(chosen_tile)
                tile_pool[chosen_tile] -= 1


class Player:

    def __init__(self):
        self.hand = []
        self.base_line = []
        self.first_sample_line = []
        self.second_sample_line = []
        self.third_sample_line = []
        self.fourth_sample_line = []
        self.fifth_sample_line = []

    @staticmethod
    def choose_man():
        man_answer = ""
        while man_answer not in range(1, 5):
            try:
                man_answer = int(input("Which manufacturer you wanna take from ?\n"
                                       "[1,2,3,4,5]\n"))
            except ValueError:
                print("Please enter a whole number.")
            else:
                return man_answer

    def take_from_man(self, manufacturer, table):
        answer = input("Which color would you like to take ?\n")
        while answer not in manufacturer.offer:
            answer = input("Please enter a color that the manufacturer has !\n")
        for i in range(manufacturer.offer.count(answer)):
            manufacturer.offer.remove(answer)
            self.hand.append(answer)
        for i in range(len(manufacturer.offer)):
            table.append(manufacturer.offer[0])
            del manufacturer.offer[0]

    def put_in_sample_line(self):
        sample_lines = {
            "first": self.first_sample_line,
            "second": self.second_sample_line,
            "third": self.third_sample_line,
            "fourth": self.fourth_sample_line,
            "fifth": self.fifth_sample_line,
        }

        def check_sample_lines(a_list):
            for key, value in sample_lines.items():
                if len(value) < list(sample_lines.keys()).index(key) + 1:
                    if not value or color in value:
                        a_list.append(key)

        color = self.hand[0]

        possible_places = ("sample", "base")
        possible_sample_lines = []
        check_sample_lines(possible_sample_lines)

        while possible_sample_lines:
            while self.hand:
                print(f" Your hand : {self.hand}")
                line_answer = input("Which line you want to put your tile ?\n"
                                    f"{possible_places}\n")
                while line_answer not in possible_places:
                    line_answer = input("Please enter a valid line !\n")
                if line_answer == "sample":
                    sample_answer = input("Which line you want to put your tile ?\n"
                                          f"{possible_sample_lines}\n")
                    while sample_answer not in possible_sample_lines:
                        sample_answer = input("Please enter a valid sample line !\n")

                    self.hand.remove(color)
                    sample_lines[sample_answer].append(color)

                    print(f"You put down a {color} tile to the {sample_answer} line")

                    possible_sample_lines = []
                    check_sample_lines(possible_sample_lines)
            else:
                break
        else:
            print("You have to put your remaining tile(s) to the base line. ")
            while not self.hand:
                self.base_line.append(self.hand[0])
                del self.hand[0]


def main():
    bag = {"yellow": 20,
           "red": 20,
           "blue": 20,
           "white": 20,
           "black": 20
           }

    table = []

    player = Player()

    manufacturer1 = Manufacturer()
    manufacturer2 = Manufacturer()
    manufacturer3 = Manufacturer()
    manufacturer4 = Manufacturer()
    manufacturer5 = Manufacturer()

    manufacturer1.make_offer(bag)
    manufacturer2.make_offer(bag)
    manufacturer3.make_offer(bag)
    manufacturer4.make_offer(bag)
    manufacturer5.make_offer(bag)

    print(f" Man. 1 offer : {manufacturer1}")
    print(f" Man. 2 offer : {manufacturer2}")
    print(f" Man. 3 offer : {manufacturer3}")
    print(f" Man. 4 offer : {manufacturer4}")
    print(f" Man. 5 offer : {manufacturer5}")

    man_table = {
        1: manufacturer1,
        2: manufacturer2,
        3: manufacturer3,
        4: manufacturer4,
        5: manufacturer5
    }

    chosen_man = man_table[player.choose_man()]
    player.take_from_man(chosen_man, table)
    print(f" Hand : {player.hand}")

    player.put_in_sample_line()


if __name__ == "__main__":
    main()
