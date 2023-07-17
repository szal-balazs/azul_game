import random

tile_types = {"yellow": 20,
              "red": 20,
              "blue": 20,
              "white": 20,
              "black": 20
              }


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
        self.floor = []
        self.first_sample_line = []
        self.second_sample_line = []
        self.third_sample_line = []
        self.fourth_sample_line = []
        self.fifth_sample_line = []

    def take_from_man(self, manufacturer):
        answer = input("Which color would you like to take ?\n")
        while answer not in manufacturer.offer:
            answer = input("Please enter a color that the manufacturer has !\n")
        for i in range(manufacturer.offer.count(answer)):
            manufacturer.offer.remove(answer)
            self.hand.append(answer)

    def put_in_sample_line(self):
        sample_line = {
            "first": self.first_sample_line,
            "second": self.second_sample_line,
            "third": self.third_sample_line,
            "fourth": self.fourth_sample_line,
            "fifth": self.fifth_sample_line,
        }
        answer = input("Which sample line you want to put your tile ?\n")
        while answer not in sample_line.keys():
            answer = input("Please enter a valid line !\n")
        while len(sample_line[answer]) >= list(sample_line.keys()).index(answer) + 1:
            answer = input("You cant put down any more tile in that line !\n")
        color = input("Which color would you like to put down ?\n")
        while color not in self.hand:
            color = input("Please enter a color that you have !\n")

        tile_counter = 0
        while len(sample_line[answer]) < list(sample_line.keys()).index(answer) + 1 \
                and color in self.hand:
            self.hand.remove(color)
            sample_line[answer].append(color)
            tile_counter += 1

        print(f"You put down {tile_counter} {color} tile to the {answer} line")


manufacturer1 = Manufacturer()
manufacturer1.make_offer(tile_types)

print(f" Offer : {manufacturer1}")

player = Player()
player.take_from_man(manufacturer1)

print(tile_types)
print(f" Offer : {manufacturer1}")
print(f" Hand : {player.hand}")

player.put_in_sample_line()
print(player.hand)
