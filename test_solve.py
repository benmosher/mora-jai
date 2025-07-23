import pytest
from solver import Color, Grid, Position, corners, playthrough, solve

type Row = tuple[Color, Color, Color]
type InputGrid = tuple[Row, Row, Row]


def create_grid(top: Row, middle: Row, bottom: Row) -> Grid:
    """Helper function to create a Grid from a tuple of rows."""
    return Grid([color for row in (top, middle, bottom) for color in row], None)


def test__corners():
    goal = corners(Color.PURPLE)
    assert goal == {
        (Position(-1, -1), Color.PURPLE),
        (Position(1, -1), Color.PURPLE),
        (Position(1, 1), Color.PURPLE),
        (Position(-1, 1), Color.PURPLE),
    }


def test__purple():
    grid = create_grid(
        (Color.GRAY, Color.PURPLE, Color.GRAY),
        (Color.GRAY, Color.PINK, Color.GRAY),
        (Color.PURPLE, Color.PURPLE, Color.PURPLE),
    )
    goal = corners(Color.PURPLE)
    actual = solve(grid, goal, max_depth=5)

    assert actual is not None, "No solution found"


def test__trading_post():
    grid = create_grid(
        (Color.PINK, Color.GRAY, Color.GRAY),
        (Color.GRAY, Color.YELLOW, Color.YELLOW),
        (Color.GRAY, Color.YELLOW, Color.YELLOW),
    )

    goal = corners(Color.YELLOW)
    actual = solve(grid, goal, max_depth=10)

    assert actual is not None, "No solution found"

def test__fenn():
    grid = create_grid(
        (Color.GRAY, Color.GREEN, Color.GRAY),
        (Color.ORANGE, Color.RED, Color.ORANGE),
        (Color.WHITE, Color.GREEN, Color.BLACK),
    )

    goal = corners(Color.RED)
    actual = solve(grid, goal, max_depth=30)

    assert actual is not None, "No solution found"


def test__sanctum_arch_aries():
    grid = create_grid(
        (Color.BLACK, Color.YELLOW, Color.GRAY),
        (Color.YELLOW, Color.GREEN, Color.YELLOW),
        (Color.GRAY, Color.YELLOW, Color.BLACK),
    )

    goal = corners(Color.YELLOW)
    actual = solve(grid, goal, max_depth=10)

    assert actual is not None, "No solution found"


def test__rough_draft_white():
    grid = create_grid(
        (Color.WHITE, Color.WHITE, Color.WHITE),
        (Color.YELLOW, Color.WHITE, Color.BLACK),
        (Color.BLUE, Color.BLUE, Color.BLUE),
    )

    goal = corners(Color.BLUE)
    actual = solve(grid, goal, max_depth=30)

    assert actual is not None, "No solution found"

def test__rough_draft_red():
    # red white yellow blue green blue blue yellow blue (goal: red)
    grid = create_grid(
        (Color.RED, Color.WHITE, Color.YELLOW),
        (Color.BLUE, Color.GREEN, Color.BLUE),
        (Color.BLUE, Color.YELLOW, Color.BLUE),
    )

    goal = corners(Color.RED)
    actual = solve(grid, goal, max_depth=50)

    assert actual is not None, "No solution found"