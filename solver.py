#TODO: report total press count?

import itertools as it

from collections import Counter, deque
from enum import Enum, auto
from typing import Callable, Iterable, Iterator, MutableMapping, NamedTuple, Self


class Color(Enum):
    GRAY = auto()
    RED = auto()
    BLACK = auto()
    GREEN = auto()
    YELLOW = auto()
    PURPLE = auto()
    WHITE = auto()
    BLUE = auto()
    ORANGE = auto()
    PINK = auto()


class Position(NamedTuple):
    """Represents a position in the grid."""

    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Position(self.x + other.x, self.y + other.y)

    def valid(self) -> bool:
        return -1 <= self.x <= 1 and -1 <= self.y <= 1


CENTER = Position(0, 0)

type Goal = set[tuple[Position, Color]]
"""Mapping from positions to goal colors. Almost always the corners in a single color."""

type GridState = tuple[Color, ...]
"""Hashable grid tuple for testing previous states."""

GRID_POSITIONS = [Position(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)]
"""All grid positions, in the order they are stored in the grid array."""


# 3x3 grid of colors, -1, 0, 1 indexes
class Grid(MutableMapping[Position, Color]):
    def __init__(self, colors: list[Color]) -> None:
        """Initializes a grid with the given colors."""
        if len(colors) != 9:
            raise ValueError("Grid must have exactly 9 colors")
        self.colors = colors

    colors: list[Color]

    def hashable_state(self) -> GridState:
        """Returns a hashable representation of the grid."""
        return tuple(self.colors)

    def display(self) -> str:
        """Returns a string representation of the grid."""
        return "\n".join(
            " ".join(self[Position(x, y)].name for x in (-1, 0, 1)) for y in (-1, 0, 1)
        )

    def _index(self, position: Position) -> int:
        return ((position.y + 1) * 3) + position.x + 1

    def __getitem__(self, position: Position) -> Color:
        return self.colors[self._index(position)]

    def __setitem__(self, position: Position, color: Color) -> None:
        self.colors[self._index(position)] = color

    def __delitem__(self, position: Position) -> None:
        self.colors[self._index(position)] = Color.GRAY

    def __iter__(self) -> Iterator[Position]:
        return iter(GRID_POSITIONS)

    def __len__(self) -> int:
        return 9

    # this was considerably slower than using a filtered list comprehension with items()!
    # def color_positions(self, color: Color) -> Iterable[Position]:
    #     """Returns the positions of the given color in the grid."""
    #     for i, c in enumerate(self.colors):
    #         if c == color:
    #             yield GRID_POSITIONS[i]

    def copy(self) -> Self:
        """Returns a copy of the grid."""
        return Grid(list(self.colors))

    def swap(self, pos1: Position, pos2: Position) -> Self | None:
        """Return a cloned grid iff the swap results in a new state."""
        idx1 = self._index(pos1)
        idx2 = self._index(pos2)
        if idx1 == idx2:
            return None

        a, b = self.colors[idx1], self.colors[idx2]
        if a == b:
            return None

        clone = self.copy()
        clone.colors[idx1], clone.colors[idx2] = b, a
        return clone

    def meets_goal(self, goal: Goal) -> bool:
        return all(self[pos] == color for pos, color in goal)


type Behavior = Callable[[Position, Grid], None]

COLOR_BEHAVIORS = dict[Color, Behavior]()
"""This dictionary dispatches the grid updated behavior for each color."""

COLOR_BEHAVIORS[Color.GRAY] = lambda position, grid: None


def purple(position: Position, grid: Grid) -> Grid | None:
    """Drops down one, swapping with the color below."""

    # no change if on bottom row
    if position.y == 1:
        return None

    new_position = Position(position.x, position.y + 1)
    return grid.swap(position, new_position)


COLOR_BEHAVIORS[Color.PURPLE] = purple


def yellow(position: Position, grid: Grid) -> Grid | None:
    """Moves up one, swapping with the color above."""

    # no change if on top row
    if position.y == -1:
        return None

    new_position = Position(position.x, position.y - 1)
    return grid.swap(position, new_position)


COLOR_BEHAVIORS[Color.YELLOW] = yellow


def red(position: Position, grid: Grid) -> Grid | None:
    """When any red is pressed, all whites turn black, and all blacks turn red."""
    # TODO: do blues behave as white or black here if one of them is in the center?

    whites = [pos for pos, color in grid.items() if color == Color.WHITE]
    blacks = [pos for pos, color in grid.items() if color == Color.BLACK]
    if not whites and not blacks:
        return None

    new_grid = grid.copy()
    for white in whites:
        new_grid[white] = Color.BLACK
    for black in blacks:
        new_grid[black] = Color.RED
    return new_grid


COLOR_BEHAVIORS[Color.RED] = red


def green(position: Position, grid: Grid) -> Grid | None:
    """Swaps with opposite corner or edge. Does nothing in the center."""
    if position == CENTER:
        return None

    new_position = Position(-position.x, -position.y)
    return grid.swap(position, new_position)


COLOR_BEHAVIORS[Color.GREEN] = green


def black(position: Position, grid: Grid) -> Grid | None:
    """Rotates the row to the right."""
    row = [grid[Position(x, position.y)] for x in (1, -1, 0)]
    if all(c == Color.BLACK for c in row):
        return None

    new_grid = grid.copy()
    for i, color in enumerate(row, start=-1):
        new_grid[Position(i, position.y)] = color

    return new_grid


COLOR_BEHAVIORS[Color.BLACK] = black

ADJACENTS = [
    Position(0, 1),  # down
    Position(1, 0),  # right
    Position(0, -1),  # up
    Position(-1, 0),  # left
]


def neighbors(position: Position) -> Iterable[Position]:
    """Returns the positions of the adjacent neighbors in the grid."""
    return (p for adj in ADJACENTS if (p := position + adj).valid())


def white(position: Position, grid: Grid) -> Grid | None:
    """Turns blank and turns adjacent blanks to the position's color.

    Using the position is necessary because when blue triggers this, it should be blue.
    """
    color = grid[position]
    new_grid = grid.copy()

    # blank out this position
    del new_grid[position]  
    for neighbor in neighbors(position):
        if grid[neighbor] == color:
            del new_grid[neighbor]

    return new_grid


COLOR_BEHAVIORS[Color.WHITE] = white


def blue(position: Position, grid: Grid) -> Grid | None:
    center_color = grid[CENTER]

    # base case: copying blue is no-op
    if center_color == Color.BLUE:
        return None

    # do the behavior for the center color
    return COLOR_BEHAVIORS[center_color](position, grid)


COLOR_BEHAVIORS[Color.BLUE] = blue


def orange(position: Position, grid: Grid) -> Grid | None:
    """Changes the color to the most common neighbor color."""
    neighbor_counts = Counter(grid[p] for p in neighbors(position))

    most_common = neighbor_counts.most_common(2)
    my_color = grid[position]

    # if there is no most common color, or if the top two are tied, return None
    if len(most_common) < 2 or most_common[0][1] != most_common[1][1]:
        color = most_common[0][0]
    else:
        return None

    # if the most common color is blank or my color, return None -- no change
    if color == Color.GRAY or color == my_color:
        return None

    new_grid = grid.copy()
    new_grid[position] = color
    return new_grid


COLOR_BEHAVIORS[Color.ORANGE] = orange


CYCLE_POSITIONS = [
    Position(0, -1),  # N
    Position(1, -1),  # NE
    Position(1, 0),  # E
    Position(1, 1),  # SE
    Position(0, 1),  # S
    Position(-1, 1),  # SW
    Position(-1, 0),  # W
    Position(-1, -1),  # NW
]


def cycle(position: Position) -> Iterable[Position]:
    return (p for adj in CYCLE_POSITIONS if (p := position + adj).valid())


def pink(position: Position, grid: Grid) -> Grid | None:
    """Cycles the colors clockwise around the position."""

    to_cycle = [grid[p] for p in cycle(position)]
    # all colors to rotate are the same, so no change
    if all(c == to_cycle[0] for c in to_cycle):
        return None

    new_grid = grid.copy()
    to_cycle.insert(0, to_cycle.pop())  # rotate the list clockwise
    for i, pos in enumerate(cycle(position)):
        new_grid[pos] = to_cycle[i]

    return new_grid


COLOR_BEHAVIORS[Color.PINK] = pink


class Play(NamedTuple):
    previous: "Play"
    press: Position
    depth: int = 0

    def next(self, position: Position) -> "Play":
        """Returns a new Play with the given position pressed."""
        return Play(self, position, self.depth + 1)


class State(NamedTuple):
    grid: Grid
    play: Play | None


def press(
    position: Position,
    grid: Grid,
) -> Grid | None:
    """Returns a grid updated by the play, or None if no change was made."""
    behavior = COLOR_BEHAVIORS[grid[position]]
    return behavior(position, grid)


def solve(
    grid: Grid,
    goal: Goal,
    max_depth: int = 10,
) -> tuple[Play, Grid] | None:
    """Finds a Play linked list that solves the grid to the goal."""

    if grid.meets_goal(goal):
        raise ValueError("Grid already meets goal")

    # initialize the queue with the starting state
    queue = deque()
    played_states = {grid.hashable_state()}  # max size: 9! (~362k, not accounting for color changes)
    queue.append(State(grid, None))

    while queue:
        grid, last_play = queue.popleft()

        for pos in GRID_POSITIONS:
            play = last_play.next(pos) if last_play else Play(None, pos)

            new_grid = press(pos, grid)
            if new_grid is None:
                continue

            # immediately return if the new grid meets the goal!
            if new_grid.meets_goal(goal):
                return play, new_grid

            hs = new_grid.hashable_state()
            if hs in played_states:
                # cycle or shorter path already played
                continue

            played_states.add(hs)

            # if we've reached the max depth, skip this state
            if play.depth >= max_depth:
                continue

            # enqueue state for exploration
            queue.append(State(new_grid, play))


def playthrough(play: Play, grid: Grid) -> Iterable[tuple[Position, Grid]]:
    """Returns the grid after playing through the given play."""

    plays = list[Position]()
    while play:
        plays.append(play.press)
        play = play.previous

    for p in reversed(plays):
        grid = press(p, grid)
        yield p, grid


CORNERS = {Position(x, y) for x, y in it.product((-1, 1), repeat=2)}


def corners(color: Color) -> Goal:
    """Returns the goal for the given color."""
    return {(pos, color) for pos in CORNERS}


if __name__ == "__main__":
    starting_state_str = input(
        "Enter the starting state (9 colors, space-separated, top/middle/bottom row): "
    ).upper()
    starting_state = [Color[color] for color in starting_state_str.split()]
    starting_grid = Grid(starting_state)

    counts = Counter(c for c in starting_grid.colors if c != Color.GRAY)
    default_goal = counts.most_common(1)[0][0]

    goal_color_str = input(f"Enter the goal color[s] (default: {default_goal.name}): ").upper()
    if " " in goal_color_str:
        corner_colors = [Color[gc] for gc in goal_color_str.split()]
        goal = set(zip(
            (Position(-1, -1), Position(1, -1), Position(-1, 1), Position(1, 1)),
            corner_colors
        ))
    else:
        goal_color = Color[goal_color_str] if goal_color_str else default_goal
        goal = corners(goal_color)

    max_depth = int(input("Enter the maximum depth (default 10): ") or 10)

    print()  # line break

    solution = solve(starting_grid, goal, max_depth)
    if solution:
        play, final_grid = solution
        print(f"Solution found ({play.depth + 1} moves):")
        for position, grid in playthrough(play, starting_grid):
            print(f"Play: {position}, Grid:\n{grid.display()}\n")
            input()
    else:
        print("No solution found.")
