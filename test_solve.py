import pytest
from solver import Color, Grid, Position, corners, playthrough, solve

def test__purple():
    start = [
        Color.BLANK, Color.PURPLE, Color.BLANK,
        Color.BLANK, Color.PINK, Color.BLANK,
        Color.PURPLE, Color.PURPLE, Color.PURPLE,
    ]
    goal = corners(Color.PURPLE)
    grid = Grid(start)

    actual = solve(grid, goal, max_depth=5)

    assert actual is not None, "No solution found"

    # play, final_grid = actual
    # for position, grid in playthrough(play, grid):
    #     print(f"Play: {position}, Grid:\n{grid.display()}\n")

    # pytest.fail()

def test__trading_post():
    start = [
        Color.PINK, Color.BLANK, Color.BLANK,
        Color.BLANK, Color.YELLOW, Color.YELLOW,
        Color.BLANK, Color.YELLOW, Color.YELLOW,
    ]

    goal = corners(Color.YELLOW)

    actual = solve(Grid(start), goal, max_depth=10)

    assert actual is not None, "No solution found"



def test__fenn():
    start = [
        Color.BLANK, Color.GREEN, Color.BLANK,
        Color.ORANGE, Color.RED, Color.ORANGE,
        Color.WHITE, Color.GREEN, Color.BLACK,
    ]

    goal = corners(Color.RED)

    actual = solve(Grid(start), goal, max_depth=20)

    assert actual is not None, "No solution found"


def test__sanctum_arch_aries():
    start = [
        Color.BLACK, Color.YELLOW, Color.BLANK,
        Color.YELLOW, Color.GREEN, Color.YELLOW,
        Color.BLANK, Color.YELLOW, Color.BLACK,
    ]

    goal = corners(Color.YELLOW)

    actual = solve(Grid(start), goal, max_depth=10)

    assert actual is not None, "No solution found"
