
from deolingo.facade import run_deolingo, read_example


def test_preliminary_example_1():
    # Arrange
    example = read_example("preliminary/example1.lp")
    expected_answer_set = {"park", "imp_perm(park)"}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_preliminary_example_2():
    # Arrange
    example = read_example("preliminary/example2.lp")
    expected_answer_set = {'ob(work)', 'violated(work)', 'imp_perm(park)', 'imp_perm(work)', '-work', '-weekend'}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_preliminary_example_3():
    # Arrange
    example = read_example("preliminary/example3.lp")
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert actual_answer_sets == []


def test_preliminary_example_4():
    # Arrange
    example = read_example("preliminary/example4.lp")
    expected_answer_set = {'walk', 'ob(walk_right)', 'ob(walk)', 'walk_right', 'fb(walk)',
                           'fb(-walk)', 'violated(walk)', 'violated(-walk)', 'fulfilled(-walk)',
                           'fulfilled(-walk_right)', 'fulfilled(walk)', 'fulfilled(walk_right)',
                           'imp_perm(work)', 'imp_perm(park)', 'imp_perm(walk_right)', 'imp_perm(fight)'}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_preliminary_example_5():
    # Arrange
    example = read_example("preliminary/example5.lp")
    expected_answer_set = {'-fb(fence)', 'fence', 'sea', 'imp_perm(work)', 'imp_perm(fight)', 'imp_perm(walk)',
                           'imp_perm(fence)', 'imp_perm(park)', 'imp_perm(white)', 'imp_perm(walk_right)'}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)
