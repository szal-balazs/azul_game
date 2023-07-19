import itertools
import random

from azul import utils, game


class Player:
    def __init__(self, name):
        self.logger = utils.get_logger(name)
        self.name = name

    def take_turn(self, factories, center):
        for idx, tile_source in enumerate(itertools.chain(factories, [center])):
            if not tile_source.is_empty():
                counter = tile_source.counter

                most_common = counter.most_common(1)
                if len(most_common) == 0:
                    continue

                tile_type, tile_cnt = most_common[0]

                factory_idx = idx
                line_no = random.randint(1, 5)

                self.say_move(factory_idx, tile_type, tile_cnt, line_no)

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
