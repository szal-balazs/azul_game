import copy
import enum
import collections
import itertools
import random

from azul import utils


class TileType(enum.Enum):
    BLACK = 1
    BLUE = 2
    RED = 3
    WHITE = 4
    YELLOW = 5


def grid():
    ordered_tile_types = [
        TileType.BLUE,
        TileType.YELLOW,
        TileType.RED,
        TileType.BLACK,
        TileType.WHITE
    ]

    g = [[ordered_tile_types[(-i + j) % 5] for j in range(5)] for i in range(5)]
    return g


class Factory:
    def __init__(self, tiles):
        self.counter = collections.Counter(tiles)

    def take(self, tile_type):
        no_taken = self.counter.pop(tile_type)
        rest = copy.deepcopy(self.counter)
        self.counter.clear()
        return no_taken, rest

    def size(self):
        return sum(self.counter.values())

    def is_empty(self):
        return self.size() == 0


class Center:
    def __init__(self):
        self.starting_player_marker = True
        self.counter = collections.Counter()

    def add(self, tiles):
        self.counter = self.counter + tiles

    def take(self, tile_type):
        self.starting_player_marker = False
        return self.counter.pop(tile_type)

    def size(self):
        return sum(self.counter.values()) + (1 if self.starting_player_marker else 0)

    def is_empty(self):
        return self.size() == 0


class Line:
    def __init__(self):
        self.tile_type = None
        self.count = 0


class Board:
    def __init__(self):
        self.lines = [Line() for _ in range(6)]
        self.lines[0] = None
        self.floor = []
        self.wall = [[None for _ in range(5)] for _ in range(6)]
        self.wall[0] = None


class Player:
    def __init__(self, player):
        self.player = player
        self.board = Board()
        self.score = 0


class Move:
    def __init__(self, factory_idx, tile_type, line_no):
        self.factory_idx = factory_idx
        self.tile_type = tile_type
        self.line_no = line_no


class Update:
    def __init__(self, player_name, move):
        self.player_name = player_name
        self.move = move


class Bag:
    def __init__(self):
        bag = [20 * [tile_type] for tile_type in TileType]
        bag = list(itertools.chain.from_iterable(bag))
        random.shuffle(bag)
        self.bag = bag

    def __len__(self):
        return len(self.bag)

    def is_empty(self):
        return len(self) == 0

    def draw(self):
        split = min(4, len(self.bag))
        head, self.bag = self.bag[:split], self.bag[split + 1:]
        return head


class Game:
    def __init__(self, players):
        self.logger = utils.get_logger('Game')
        self.bag = Bag()
        self.factories = None
        self.center = None
        self.players = [Player(p) for p in players]
        self.starting_player = random.choice(self.players)

    def play(self):
        self.logger.info("Let's go!")
        print()

        self.play_rounds()

    def play_rounds(self):
        current_round = 0
        while True:
            current_round += 1

            self.logger.info(f'- - - - - Round {current_round} - - - - -')
            print()

            self.factories = Game.offer(self.bag)
            self.center = Center()

            self.play_turns()
            self.logger.info(f'Round {current_round} is over')
            print()

            if self.is_end_of_game():
                self.logger.info(f'End of the game. The winner is: {"unimplemented"}')
                return

    def play_turns(self):
        for turn, current_player in enumerate(
                itertools.dropwhile(
                    lambda p: p is not self.starting_player,
                    itertools.cycle(self.players)
                )
        ):
            if self.is_round_over():
                break

            if turn % len(self.players) == 0:
                self.logger.info(f'- - - - - {turn // len(self.players) + 1} - - - - -')
                print()

            self.logger.info(f"It's {current_player.player.name}'s turn")

            move = current_player.player.take_turn(self.factories, self.center)
            self.process_move(current_player, move)
            print()

            update = Update(current_player.player.name, move)
            for p in self.players:
                p.player.process_update(update)

            print()

    def process_move(self, player, move):
        if move.factory_idx == 5:
            if self.center.starting_player_marker:
                self.starting_player = player
            no_taken = self.center.take(move.tile_type)
        else:
            no_taken, rest = self.factories[move.factory_idx].take(move.tile_type)
            self.center.add(rest)

        line = player.board.lines[move.line_no]
        if line.tile_type is None:
            line.tile_type = move.tile_type
        line.count += no_taken

    @staticmethod
    def offer(bag):
        return [Factory(bag.draw()) for _ in range(5)]

    def is_round_over(self):
        return all([f.is_empty() for f in self.factories]) and self.center.is_empty()

    def is_end_of_game(self):
        # TODO: Implement me
        return self.bag.is_empty()
