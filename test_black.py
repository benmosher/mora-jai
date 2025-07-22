from solver import Color, black, Position


def test__black():
    grid = {
        Position(-1, 0): Color.BLACK,
        Position(0, 0): Color.WHITE,
        Position(1, 0): Color.RED,
    }

    actual = black(Position(-1, 0), grid)

    assert actual == {
        Position(-1, 0): Color.RED,
        Position(0, 0): Color.BLACK,
        Position(1, 0): Color.WHITE,
    }
