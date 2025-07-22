from collections import Counter
from solver import possible_colors, Color, goal_still_reachable

def test__red_black_white():
    colors = [Color.RED, Color.WHITE, Color.BLACK]

    assert possible_colors(colors) == {
        Color.RED: 3,
        Color.WHITE: 1,
        Color.BLACK: 2,
    }

def test__oranges():
    """Oranges can turn green, but not black or gray."""
    colors = [Color.ORANGE, Color.ORANGE, Color.GREEN, Color.GREEN, Color.GRAY, Color.GRAY, Color.BLACK]

    assert possible_colors(colors) == {
        Color.ORANGE: 2,
        Color.GREEN: 4,
        Color.GRAY: 2,
        Color.BLACK: 1,
    }

def test__counter_comparison():
    """Ensure that the Counter comparison works as expected."""
    colors = [Color.RED, Color.RED, Color.GREEN, Color.GREEN, Color.BLUE]

    possibles = possible_colors(colors)

    assert possibles == {
        Color.RED: 2,
        Color.GREEN: 2,
        Color.BLUE: 1,
    }

    goal = Counter([Color.RED, Color.RED, Color.GREEN, Color.GREEN])

    assert goal_still_reachable(possibles, goal), "Possible colors should include at least the counts in goal"

    goal = Counter([Color.RED, Color.RED, Color.RED, Color.RED])

    assert not goal_still_reachable(possibles, goal), "Possible colors should not include more reds than available"