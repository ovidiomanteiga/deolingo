
from deolingo.lib import solve, read_example


def test_preliminary_example_1():
    # Arrange
    example = read_example("preliminary/example1.lp")
    expected_answer_set = {"park"}
    # Act
    actual_answer_sets = solve(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_preliminary_example_2():
    # Arrange
    example = read_example("preliminary/example2.lp")
    expected_answer_set = {'&obligatory{work}', '-work', '-weekend'}
    # Act
    actual_answer_sets = solve(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_preliminary_example_3():
    # Arrange
    example = read_example("preliminary/example3.lp")
    # Act
    actual_answer_sets = solve(example[1])
    # Assert
    assert actual_answer_sets == []


def test_preliminary_example_4():
    # Arrange
    example = read_example("preliminary/example4.lp")
    expected_answer_set = {'walk', '&obligatory{walk_right}', '&obligatory{walk}', 'walk_right', '&forbidden{walk}'}
    # Act
    actual_answer_sets = solve(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_preliminary_example_5():
    # Arrange
    example = read_example("preliminary/example5.lp")
    expected_answer_set = {'&permitted{fence}', 'fence', 'sea'}
    # Act
    actual_answer_sets = solve(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)
