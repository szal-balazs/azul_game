import unittest
import game

# ---------- wall test dummy's

full_row_wall = game.Wall()
for i in range(5):
    full_row_wall.wall[1][i] = "Tile"

full_column_wall = game.Wall()
for i in range(1, 6):
    full_column_wall.wall[i][0] = "Tile"

full_color_wall = game.Wall()
for i in range(1, 6):
    j = full_color_wall.wall[i].index(game.TileType.BLUE)
    full_color_wall.wall[i][j] = "Tile"

starting_wall = game.Wall()

# ---------- line test dummy's

null_line = game.Line(0)

empty_line = game.Line(5)

some_in_line = game.Line(5)
for _ in range(3):
    some_in_line.accept_tile(game.TileType.BLUE)

full_line = game.Line(5)
for _ in range(5):
    full_line.accept_tile(game.TileType.BLUE)

# ----------  floor test dummy's

empty_floor = game.Floor()

two_in_floor = game.Floor()
for _ in range(2):
    two_in_floor.accept_tile(game.TileType.BLUE)

five_in_floor = game.Floor()
for _ in range(5):
    five_in_floor.accept_tile(game.TileType.BLUE)

seven_in_floor = game.Floor()
for _ in range(7):
    seven_in_floor.accept_tile(game.TileType.BLUE)


class MyTestCase(unittest.TestCase):

    def test_wall_can_put_in(self):
        self.assertEqual(full_row_wall.can_put_in(game.TileType.BLUE, 1), False)
        self.assertEqual(full_column_wall.can_put_in(game.TileType.BLUE, 2), True)
        self.assertEqual(full_color_wall.can_put_in(game.TileType.BLUE, 2), False)
        self.assertEqual(starting_wall.can_put_in(game.TileType.BLUE, 2), True)

    def test_wall_put_tile_in(self):
        self.assertEqual(full_row_wall.put_tile_in(game.TileType.YELLOW, 2), 2)
        self.assertEqual(full_column_wall.put_tile_in(game.TileType.YELLOW, 1), 2)
        self.assertEqual(full_color_wall.put_tile_in(game.TileType.YELLOW, 1), 4)
        self.assertEqual(starting_wall.put_tile_in(game.TileType.YELLOW, 1), 1)

    def test_wall_any_row_is_full(self):
        self.assertEqual(full_row_wall.any_row_is_full(), True)
        self.assertEqual(full_column_wall.any_row_is_full(), False)
        self.assertEqual(full_color_wall.any_row_is_full(), False)
        self.assertEqual(starting_wall.any_row_is_full(), False)

    def test_wall_row_is_full(self):
        self.assertEqual(full_row_wall.row_is_full(), 2)
        self.assertEqual(full_column_wall.row_is_full(), 0)
        self.assertEqual(full_color_wall.row_is_full(), 0)
        self.assertEqual(starting_wall.row_is_full(), 0)

    def test_wall_column_is_full(self):
        self.assertEqual(full_row_wall.column_is_full(), 0)
        self.assertEqual(full_column_wall.column_is_full(), 7)
        self.assertEqual(full_color_wall.column_is_full(), 0)
        self.assertEqual(starting_wall.column_is_full(), 0)

    def test_wall_color_is_full(self):
        self.assertEqual(full_row_wall.color_is_full(), 0)
        self.assertEqual(full_column_wall.color_is_full(), 0)
        self.assertEqual(full_color_wall.color_is_full(), 10)
        self.assertEqual(starting_wall.color_is_full(), 0)

    def test_wall_score_wall(self):
        self.assertEqual(full_row_wall.score_wall(), 2)
        self.assertEqual(full_column_wall.score_wall(), 7)
        self.assertEqual(full_color_wall.score_wall(), 10)
        self.assertEqual(starting_wall.score_wall(), 0)

    def test_lines_is_full(self):
        self.assertEqual(empty_line.is_full(), False)
        self.assertEqual(some_in_line.is_full(), False)
        self.assertEqual(full_line.is_full(), True)

    def test_lines_is_unfinished(self):
        self.assertEqual(empty_line.is_unfinished(), False)
        self.assertEqual(some_in_line.is_unfinished(), True)
        self.assertEqual(full_line.is_unfinished(), False)

    def test_lines_type(self):
        self.assertEqual(empty_line.tile_type, None)
        self.assertEqual(some_in_line.tile_type, game.TileType.BLUE)
        self.assertEqual(some_in_line.tile_type, game.TileType.BLUE)

    def test_lines_can_accept(self):
        self.assertEqual(null_line.can_accept(game.TileType.YELLOW), False)
        self.assertEqual(empty_line.can_accept(game.TileType.YELLOW), True)
        self.assertEqual(some_in_line.can_accept(game.TileType.BLUE), True)
        self.assertEqual(some_in_line.can_accept(game.TileType.YELLOW), False)
        self.assertEqual(full_line.can_accept(game.TileType.YELLOW), False)

    def test_floor_score(self):
        self.assertEqual(empty_floor.score(), 0)
        self.assertEqual(two_in_floor.score(), 2)
        self.assertEqual(five_in_floor.score(), 8)
        self.assertEqual(seven_in_floor.score(), 14)


if __name__ == '__main__':
    unittest.main()
