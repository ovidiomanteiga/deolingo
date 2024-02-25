
from deolingo.facade import run_deolingo, read_example


def test_delx_example_1_1():
    # Arrange
    example = read_example("delx/example1.1.lp")
    expected_answer_set = {'fb(f)', 'imp_perm(w)'}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_delx_example_1_2():
    # Arrange
    example = read_example("delx/example1.2.lp")
    expected_answer_set = {'fb(f)', 'imp_perm(w)'}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_delx_example_2():
    # Arrange
    example = read_example("delx/example2.lp")
    expected_answer_set = {'fb(f)', 'imp_perm(pay)', 'imp_perm(w)'}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_delx_example_3():
    # Arrange
    example = read_example("delx/example3.lp")
    expected_answer_set = {'f', 'ob(w)', 'ob(f)', 'ob(pay)', 'fb(f)', 'violated(f)', 'violated(-f)',
                           'fulfilled(-f)', 'fulfilled(f)', 'imp_perm(pay)', 'imp_perm(w)'}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_delx_example_4():
    # Arrange
    example = read_example("delx/example4.lp")
    expected_answer_set = {'fb(f)', 'imp_perm(w)'}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_delx_example_5_1():
    # Arrange
    example = read_example("delx/example5.1.lp")
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert actual_answer_sets == []


def test_delx_example_5_2():
    # Arrange
    example = read_example("delx/example5.2.lp")
    expected_answer_set = {'f', 'ob(w)', 'ob(f)', 'fb(f)', 'violated(f)',
                           'violated(-f)', 'fulfilled(-f)', 'fulfilled(f)', 'imp_perm(w)'}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_delx_example_6_1():
    # Arrange
    example = read_example("delx/example6.1.lp")
    expected_answer_sets = [
        {'-f', 'fb(m)', 'fb(f)', 'fulfilled(f)', 'fulfilled(-f)', 'imp_perm(w)'},
        {'f', 'ob(w)', 'ob(m)', 'ob(f)', 'fb(f)', 'violated(-f)', 'violated(f)',
            'fulfilled(f)', 'fulfilled(-f)', 'imp_perm(m)', 'imp_perm(w)'}
    ]
    # Act
    actual_answer_sets = run_deolingo(example[1], all_models=True)
    # Assert
    assert len(actual_answer_sets) == 2
    actual_answer_set_0 = set(actual_answer_sets[0])
    actual_answer_set_1 = set(actual_answer_sets[1])
    assert actual_answer_set_0.issuperset(expected_answer_sets[0])
    assert actual_answer_set_1.issuperset(expected_answer_sets[1])


def test_delx_example_6_2():
    # Arrange
    example = read_example("delx/example6.2.lp")
    expected_answer_sets = [
        {'-f', 'fb(m)', 'fb(f)', 'fulfilled(f)', 'fulfilled(-f)', 'imp_perm(w)'},
        {'f', 'ob(w)', 'ob(m)', 'ob(f)', 'fb(f)', 'violated(-f)', 'violated(f)',
         'fulfilled(f)', 'fulfilled(-f)', 'imp_perm(w)', 'imp_perm(m)'}
    ]
    # Act
    actual_answer_sets = run_deolingo(example[1], all_models=True)
    # Assert
    assert len(actual_answer_sets) == 2
    actual_answer_set_0 = set(actual_answer_sets[0])
    actual_answer_set_1 = set(actual_answer_sets[1])
    assert actual_answer_set_0.issuperset(expected_answer_sets[0])
    assert actual_answer_set_1.issuperset(expected_answer_sets[1])
