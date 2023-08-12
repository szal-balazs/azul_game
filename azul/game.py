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


class Wall:
    def __init__(self):
        self.wall = self.make_wall()

    @staticmethod
    def make_wall():
        ordered_tile_types = [
            TileType.BLUE,
            TileType.YELLOW,
            TileType.RED,
            TileType.BLACK,
            TileType.WHITE
        ]

        wall = [[ordered_tile_types[(-i + j) % 5] for j in range(5)] for i in range(5)]
        null_line = ["None" for _ in range(5)]
        wall.insert(0, null_line)
        return wall

    def can_put_in(self, tile_type, line_no):
        return tile_type in self.wall[line_no]

    def counting_points(self, line_no, column_no):
        points = 1

        def count_tiles(start, step, is_row):
            point = 0
            x = start + step
            while x in range(1, 6) if is_row else x in range(5):
                if self.wall[x][column_no] == "Tile" if is_row else self.wall[line_no][x] == "Tile":
                    point += 1
                    x += step
                else:
                    break
            return point

        points += count_tiles(line_no, 1, True) + count_tiles(line_no, -1, True) + \
                  count_tiles(column_no, 1, False) + count_tiles(column_no, -1, False)

        return points

    def put_tile_in(self, tile_type, line_no):
        column_no = self.wall[line_no].index(tile_type)
        self.wall[line_no][column_no] = "Tile"
        return self.counting_points(line_no, column_no)

    def any_hor_is_full(self):
        return any([all(("Tile" == self.wall[i][j]) for j in range(5)) for i in range(1, 6)])

    def hor_is_full(self):
        return [all(("Tile" == self.wall[i][j]) for j in range(5)) for i in range(1, 6)].count(True) * 2

    def vert_is_full(self):
        return [all(("Tile" == self.wall[j][i]) for j in range(1, 6)) for i in range(5)].count(True) * 7

    def all_same_color(self):
        ordered_tile_types = [
            TileType.BLUE,
            TileType.YELLOW,
            TileType.RED,
            TileType.BLACK,
            TileType.WHITE
        ]

        return [any(ordered_tile_types[i] in x for x in self.wall) for i in range(5)].count(False) * 10

    def score_wall(self):
        points = 0
        points += self.hor_is_full()
        print(self.hor_is_full())
        points += self.vert_is_full()
        print(self.vert_is_full())
        points += self.all_same_color()
        print(self.all_same_color())
        return points


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
        return sum(self.counter.values()) \
            # + (1 if self.starting_player_marker else 0)

    def is_empty(self):
        return self.size() == 0


class Line(collections.deque):
    def __init__(self, value):
        super().__init__(self, value)
        self._maxlen = value
        self.tile_type = None

    def is_full(self):
        return len(self) == self.maxlen

    def can_accept(self, tile_type):
        a = not self.is_full()
        b = self.tile_type is None or self.tile_type is tile_type
        return a and b

    def accept_tile(self, tile_type):
        if self.can_accept(tile_type):
            self.append(tile_type)
            self.tile_type = tile_type


class Floor:
    def __init__(self):
        self.floor = []

    def __len__(self):
        return len(self.floor)

    def accept_tile(self, tile):
        self.floor.append(tile)

    def score(self):
        score = 0
        for x in range(1, len(self.floor) + 1):
            if x <= 2:
                score += 1
            elif 2 < x < 6:
                score += 2
            else:
                score += 3
        return score


class Board:
    def __init__(self):
        self.lines = [Line(i) for i in range(6)]
        self.wall = Wall()
        self.floor = Floor()


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

    def draw(self, how_many):
        split = min(how_many, len(self.bag))
        head, self.bag = self.bag[:split], self.bag[split + 1:]
        return head

    def refill(self, tiles):
        random.shuffle(tiles)
        self.bag = tiles


class Lid:
    def __init__(self):
        self.lid = []

    def __len__(self):
        return len(self.lid)

    def is_empty(self):
        return len(self) == 0

    def accept_tile(self, tile_type):
        return self.lid.append(tile_type)

    def take_out_tiles(self):
        tiles = [tile for tile in self.lid]
        self.lid.clear()
        return tiles


class Game:
    def __init__(self, players):
        self.logger = utils.get_logger('Game')
        self.bag = Bag()
        self.lid = Lid()
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
            print(f"Bag : {len(self.bag)}")
            print(f"Lid : {len(self.lid)}")

            self.factories = Game.offer(self.bag, self.lid)
            self.center = Center()

            self.play_turns()
            self.logger.info(f'Round {current_round} is over')
            print()

            if self.is_end_of_game(current_round):
                for p in self.players:
                    wall_points = p.player.board.wall.score_wall()
                    p.player.score += wall_points
                    print(f"{p.player.name} got {wall_points} points from the wall.")
                # for player in sorted(self.players, key=lambda p: p.player.score, reverse=True):
                #     print(player.player.name, player.player.score)
                winner = ""
                winner_score = 0
                winner_full_hor_score = 0
                for p in self.players:
                    print(f"{p.player.name}: {p.player.score}\n"
                          f"And has {int(p.player.board.wall.hor_is_full() / 2)} full horizontal lines")
                    if winner_score < p.player.score:
                        winner = p.player.name
                        winner_score = p.player.score
                        winner_full_hor_score = p.player.board.wall.hor_is_full()
                    elif winner_score == p.player.score:
                        if winner_full_hor_score < p.player.board.wall.hor_is_full():
                            winner = p.player.name
                        elif winner_full_hor_score == p.player.board.wall.hor_is_full():
                            winner += " & " + p.player.name

                self.logger.info(f'End of the game. The winner is: {winner}')
                return

    def play_turns(self):
        for turn, current_player in enumerate(
                itertools.dropwhile(
                    lambda p: p is not self.starting_player,
                    itertools.cycle(self.players)
                )
        ):

            if self.is_round_over():
                for p in self.players:
                    for line in p.player.board.lines:
                        if line.is_full() and line.maxlen != 0:
                            p.player.score += p.player.board.wall.put_tile_in(line.tile_type, line.maxlen)
                            print(f'{p.player.name} put a {line.tile_type} to the wall, line no {line.maxlen} '
                                  f'Score {p.player.score}')
                            self.lid.lid += [line[i] for i in range(line.maxlen - 1)]
                            line.clear()
                            line.tile_type = None
                    self.lid.lid += p.player.board.floor.floor
                    floor_score = min(p.player.score, p.player.board.floor.score())
                    p.player.score -= floor_score
                    print(f"{p.player.name} had {len(p.player.board.floor)} tile(s) in the floor."
                          f" -{floor_score} points")
                    p.player.board.floor.floor.clear()
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

        # line = player.board.lines[move.line_no] if move.line_no != "floor" else "floor"
        # if line != "floor":
        #     if line.tile_type is None:
        #         line.tile_type = move.tile_type
        #     line.count += no_taken

    def refill_bag(self):
        self.bag.refill(self.lid.take_out_tiles())

    @staticmethod
    def offer(bag, lid):
        offer = []
        for _ in range(5):
            if len(bag) >= 4:
                offer += [Factory(bag.draw(4))]
            else:
                tiles = bag.draw(len(bag))
                bag.refill(lid.take_out_tiles())
                tiles += bag.draw(4 - len(bag))
                if not tiles:
                    tiles = []
                offer += [Factory(tiles)]
        return offer

    def is_round_over(self):
        return all([f.is_empty() for f in self.factories]) and self.center.is_empty()

    def is_end_of_game(self, rounds):
        any_full_wall_line = any([p.player.board.wall.any_hor_is_full() for p in self.players])
        if any_full_wall_line is True:
            print("Full wall line")
        return (self.bag.is_empty() and self.lid.is_empty()) or any_full_wall_line or rounds > 50
