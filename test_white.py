from solver import Color, Position, press, neighbors
from test_solve import create_grid


def test__neighbors():
    assert set(neighbors(Position(0, 0))) == {
        Position(0, -1), Position(-1, 0), Position(0, 1), Position(1, 0),
    }

def test__white():
    grid = create_grid(
        (Color.WHITE, Color.WHITE, Color.WHITE),
        (Color.YELLOW, Color.WHITE, Color.BLACK),
        (Color.BLUE, Color.BLUE, Color.BLUE),
    )

    tl = press(Position(-1, -1), grid)
    assert tl.colors == [
        Color.GRAY, Color.GRAY, Color.WHITE,
        Color.YELLOW, Color.WHITE, Color.BLACK,
        Color.BLUE, Color.BLUE, Color.BLUE,
    ]

    tm = press(Position(0, -1), grid)
    assert tm.colors == [
        Color.GRAY, Color.GRAY, Color.GRAY,
        Color.YELLOW, Color.GRAY, Color.BLACK,
        Color.BLUE, Color.BLUE, Color.BLUE,
    ]

    c = press(Position(0, 0), grid)
    assert c.colors == [
        Color.WHITE, Color.GRAY, Color.WHITE,
        Color.YELLOW, Color.GRAY, Color.BLACK,
        Color.BLUE, Color.BLUE, Color.BLUE,
    ]

def test__blue_white():
    grid = create_grid(
        (Color.WHITE, Color.WHITE, Color.WHITE),
        (Color.YELLOW, Color.WHITE, Color.BLACK),
        (Color.BLUE, Color.BLUE, Color.BLUE),
    )

    mb = press(Position(0, 1), grid)
    assert mb.colors == [
        Color.WHITE, Color.WHITE, Color.WHITE,
        Color.YELLOW, Color.WHITE, Color.BLACK,
        Color.GRAY, Color.GRAY, Color.GRAY,
    ]