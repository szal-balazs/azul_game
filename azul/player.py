import itertools
import random

from azul import utils, game


class Player:
    def __init__(self, name):
        self.logger = utils.get_logger(name)
        self.name = name
        self.board = game.Board()
        self.score = 0
        self.lid = []

    def select_line(self, tile_type):

        possible_lines = [self.board.line.maxlen for self.board.line in self.board.lines
                          if (self.board.line.can_accept(tile_type)
                              and self.board.wall.can_put_in(tile_type, self.board.line.maxlen))]
        return possible_lines

    def take_turn(self, factories, center):
        for idx, tile_source in enumerate(itertools.chain(factories, [center])):
            if not tile_source.is_empty():
                counter = tile_source.counter

                most_common = counter.most_common(1)
                if len(most_common) == 0:
                    continue

                tile_type, tile_cnt = most_common[0]

                factory_idx = idx

                line_no = random.choice(self.select_line(tile_type)) if self.select_line(tile_type) else "floor"

                for _ in range(tile_cnt):
                    if line_no != "floor":
                        self.board.lines[line_no].accept_tile(tile_type)
                        self.say_move(factory_idx, tile_type, tile_cnt, line_no)
                    else:
                        if len(self.board.floor.floor) < 7:
                            self.board.floor.accept_tile(tile_type)
                            self.say_move(factory_idx, tile_type, tile_cnt, "floor")
                        else:
                            self.lid.append(tile_type)
                            self.say_move(factory_idx, tile_type, tile_cnt, "lid")

                return game.Move(factory_idx, tile_type, line_no)

    def say_move(self, factory_idx, tile_type, tile_cnt, line_no):
        tile_source = 'the center' if factory_idx == 5 else f'factory {factory_idx} '
        self.logger.info(f"I'm taking {tile_cnt} {tile_type} tile(s) from {tile_source} "
                         f"and placing it/them on line {line_no}")

    def process_update(self, update):
        self.say_update(update)

    def say_update(self, update):
        player_name = update.player_name
        tile_type = update.move.tile_type
        factory_idx = update.move.factory_idx
        tile_source = 'the center' if factory_idx == 5 else f'factory {factory_idx} '
        line_no = update.move.line_no

        self.logger.info(f"{player_name} is taking {tile_type} tile(s) from {tile_source} "
                         f"and placing it/them on line {line_no}")


class SmarterPlayer:
    def __init__(self, name):
        self.logger = utils.get_logger(name)
        self.name = name
        self.board = game.Board()
        self.score = 0
        self.lid = []

    def select_line(self, tile_type):

        possible_lines = [self.board.line.maxlen for self.board.line in self.board.lines
                          if (self.board.line.can_accept(tile_type)
                              and self.board.wall.can_put_in(tile_type, self.board.line.maxlen))]
        return possible_lines

    def take_turn(self, factories, center):
        for idx, tile_source in enumerate(itertools.chain(factories, [center])):
            if not tile_source.is_empty():
                counter = tile_source.counter

                most_common = counter.most_common(1)
                if len(most_common) == 0:
                    continue

                tile_type, tile_cnt = most_common[0]

                factory_idx = idx

                line_no = random.choice(self.select_line(tile_type)) if self.select_line(tile_type) else "floor"

                for _ in range(tile_cnt):
                    if line_no != "floor":
                        self.board.lines[line_no].accept_tile(tile_type)
                        self.say_move(factory_idx, tile_type, tile_cnt, line_no)
                    else:
                        if len(self.board.floor.floor) < 7:
                            self.board.floor.accept_tile(tile_type)
                            self.say_move(factory_idx, tile_type, tile_cnt, "floor")
                        else:
                            self.lid.append(tile_type)
                            self.say_move(factory_idx, tile_type, tile_cnt, "lid")

                return game.Move(factory_idx, tile_type, line_no)

    def say_move(self, factory_idx, tile_type, tile_cnt, line_no):
        tile_source = 'the center' if factory_idx == 5 else f'factory {factory_idx} '
        self.logger.info(f"I'm taking {tile_cnt} {tile_type} tile(s) from {tile_source} "
                         f"and placing it/them on line {line_no}")

    def process_update(self, update):
        self.say_update(update)

    def say_update(self, update):
        player_name = update.player_name
        tile_type = update.move.tile_type
        factory_idx = update.move.factory_idx
        tile_source = 'the center' if factory_idx == 5 else f'factory {factory_idx} '
        line_no = update.move.line_no

        self.logger.info(f"{player_name} is taking {tile_type} tile(s) from {tile_source} "
                         f"and placing it/them on line {line_no}")
