
from deolingo.examples import ExampleReader
from deolingo.solver import DeolingoSolver


def test_delx_example_1_1():
    # Arrange
    example = ExampleReader().read_example("delx/example1.1.lp")
    expected_answer_set = {'&forbidden{f}'}
    # Act
    actual_answer_sets = DeolingoSolver().solve(example.contents)
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_delx_example_1_2():
    # Arrange
    example = ExampleReader().read_example("delx/example1.2.lp")
    expected_answer_set = {'&forbidden{f}'}
    # Act
    actual_answer_sets = DeolingoSolver().solve(example.contents)
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_delx_example_2():
    # Arrange
    example = ExampleReader().read_example("delx/example2.lp")
    expected_answer_set = {'&forbidden{f}'}
    # Act
    actual_answer_sets = DeolingoSolver().solve(example.contents)
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_delx_example_3():
    # Arrange
    example = ExampleReader().read_example("delx/example3.lp")
    expected_answer_set = {'f', '&obligatory{w}', '&obligatory{f}', '&obligatory{pay}', '&forbidden{f}'}
    # Act
    actual_answer_sets = DeolingoSolver().solve(example.contents)
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_delx_example_4():
    # Arrange
    example = ExampleReader().read_example("delx/example4.lp")
    expected_answer_set = {'&forbidden{f}'}
    # Act
    actual_answer_sets = DeolingoSolver().solve(example.contents)
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_delx_example_5_1():
    # Arrange
    example = ExampleReader().read_example("delx/example5.1.lp")
    # Act
    actual_answer_sets = DeolingoSolver().solve(example.contents)
    # Assert
    assert actual_answer_sets == []


def test_delx_example_5_2():
    # Arrange
    example = ExampleReader().read_example("delx/example5.2.lp")
    expected_answer_set = {'f', '&obligatory{w}', '&obligatory{f}', '&forbidden{f}'}
    # Act
    actual_answer_sets = DeolingoSolver().solve(example.contents)
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_delx_example_6_1():
    # Arrange
    example = ExampleReader().read_example("delx/example6.1.lp")
    expected_answer_sets = [
        # Model 1
        {'-f', '&forbidden{m}', '&forbidden{f}'},
        # Model 2
        {'f', '&obligatory{w}', '&obligatory{m}', '&obligatory{f}', '&forbidden{f}'}
    ]
    # Act
    actual_answer_sets = DeolingoSolver(all_models=True).solve(example.contents)
    # Assert
    assert len(actual_answer_sets) == 2
    actual_answer_set_0 = set(actual_answer_sets[0])
    actual_answer_set_1 = set(actual_answer_sets[1])
    assert actual_answer_set_0.issuperset(expected_answer_sets[0])
    assert actual_answer_set_1.issuperset(expected_answer_sets[1])


def test_delx_example_6_2():
    # Arrange
    example = ExampleReader().read_example("delx/example6.2.lp")
    expected_answer_sets = [
        # Model 1
        {'-f', '&forbidden{m}', '&forbidden{f}'},
        # Model 2
        {'f', '&obligatory{w}', '&obligatory{m}', '&obligatory{f}', '&forbidden{f}'}
    ]
    # Act
    actual_answer_sets = DeolingoSolver(all_models=True).solve(example.contents)
    # Assert
    assert len(actual_answer_sets) == 2
    actual_answer_set_0 = set(actual_answer_sets[0])
    actual_answer_set_1 = set(actual_answer_sets[1])
    assert actual_answer_set_0.issuperset(expected_answer_sets[0])
    assert actual_answer_set_1.issuperset(expected_answer_sets[1])
