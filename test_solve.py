
from solver import Color, Grid, Position, playthrough, solve

def test__purple():
    start = [
        Color.BLANK, Color.PURPLE, Color.BLANK,
        Color.BLANK, Color.PINK, Color.BLANK,
        Color.PURPLE, Color.PURPLE, Color.PURPLE,
    ]
    goal = [
        (Position(-1, -1), Color.PURPLE),
        (Position(1, -1), Color.PURPLE),
        (Position(1, 1), Color.PURPLE),
        (Position(-1, 1), Color.PURPLE),
    ]
    grid = Grid(start)

    actual = solve(grid, goal, max_depth=5)

    assert actual is not None, "No solution found"

    # play, final_grid = actual
    # for position, grid in playthrough(play, grid):
    #     print(f"Play: {position}, Grid:\n{grid.display()}\n")

    # pytest.fail()
