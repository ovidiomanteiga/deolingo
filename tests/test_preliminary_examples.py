
from deolingo.facade import run_deolingo, read_example


def test_preliminary_example_1():
    # Arrange
    example = read_example("preliminary/example1.lp")
    expected_answer_set = {"park", "pm_i(park)", "om_i(park)"}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_preliminary_example_2():
    # Arrange
    example = read_example("preliminary/example2.lp")
    expected_answer_set = {'ob(work)', 'fb(-work)', 'ob_v(work)', 'viol(-work)', 'viol(work)', 'fb_v(-work)',
                           'pm_i(work)', '-om(work)', '-pm(-work)', 'om_d(work)', 'ob_nf(work)', 'ob_d(work)',
                           'fb_nf(-work)', '-work', '-weekend'}
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
    expected_answer_set = {'walk', 'ob(walk_right)', 'ob(-walk)', 'ob(walk)', 'walk_right', 'fb(walk)',
                           'fb(-walk_right)', 'fb(-walk)', 'ob_v(-walk)', 'viol(walk)', 'viol(-walk)', 'fb_v(walk)',
                           'ob_f(walk_right)', 'ob_f(walk)', 'ful(-walk_right)', 'ful(-walk)', 'ful(walk_right)',
                           'ful(walk)', 'fb_f(-walk_right)', 'fb_f(-walk)', 'pm_i(walk_right)', '-om(walk_right)',
                           '-om(walk)', '-om(-walk)', '-pm(walk)', '-pm(-walk_right)', '-pm(-walk)', 'pm_d(walk)',
                           'om_d(walk_right)', 'om_d(walk)', 'ob_nf(-walk)', 'ob_nv(walk_right)', 'ob_nv(walk)',
                           'ob_d(walk_right)', 'ob_d(walk)', 'fb_nf(walk)', 'fb_nv(-walk_right)', 'fb_nv(-walk)',
                           'fb_d(walk)'}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_preliminary_example_5():
    # Arrange
    example = read_example("preliminary/example5.lp")
    expected_answer_set = {'pm(fence)', 'fence', 'sea', '-fb(fence)', '-ob(-fence)', 'pm_i(white)', 'pm_i(fence)',
                           'om_i(white)', 'om_i(fence)', 'om(-fence)', 'pm_d(fence)', 'fb_d(fence)'}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)
