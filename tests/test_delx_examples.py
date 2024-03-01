
from deolingo.facade import run_deolingo, read_example


def test_delx_example_1_1():
    # Arrange
    example = read_example("delx/example1.1.lp")
    expected_answer_set = {'ob(-f)', 'fb(f)', 'pm_i(w)', 'om_i(w)', 'om_i(f)', '-om(-f)', '-pm(f)', 'pm_d(f)',
                           'ob_nf(-f)', 'ob_nv(-f)', 'ob_u(-f)', 'fb_nf(f)', 'fb_nv(f)', 'fb_u(f)', 'fb_d(f)'}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_delx_example_1_2():
    # Arrange
    example = read_example("delx/example1.2.lp")
    expected_answer_set = {'ob(-f)', 'fb(f)', 'pm_i(w)', 'om_i(w)', 'om_i(f)', '-om(-f)', '-pm(f)', 'pm_d(f)',
                           'ob_nf(-f)', 'ob_nv(-f)', 'ob_u(-f)', 'fb_nf(f)', 'fb_nv(f)', 'fb_u(f)', 'fb_d(f)'}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_delx_example_2():
    # Arrange
    example = read_example("delx/example2.lp")
    expected_answer_set = {'ob(-f)', 'fb(f)', 'pm_i(pay)', 'pm_i(w)', 'om_i(f)', 'om_i(pay)', 'om_i(w)', '-om(-f)',
                           '-pm(f)', 'pm_d(f)', 'ob_nf(-f)', 'ob_nv(-f)', 'ob_u(-f)', 'fb_nf(f)', 'fb_nv(f)',
                           'fb_u(f)', 'fb_d(f)'}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_delx_example_3():
    # Arrange
    example = read_example("delx/example3.lp")
    expected_answer_set = {'f', 'ob(-f)', 'ob(w)', 'ob(f)', 'ob(pay)', 'fb(-w)', 'fb(f)', 'fb(-f)', 'fb(-pay)',
                           'ob_v(-f)', 'viol(f)', 'viol(-f)', 'fb_v(f)', 'ob_f(f)', 'ful(-f)', 'ful(f)', 'fb_f(-f)',
                           'pm_i(pay)', 'pm_i(w)', '-om(w)', '-om(-f)', '-om(f)', '-om(pay)', '-pm(f)', '-pm(-w)',
                           '-pm(-f)', '-pm(-pay)', 'pm_d(f)', 'om_d(f)', 'om_d(w)', 'om_d(pay)', 'ob_nf(w)',
                           'ob_nf(-f)', 'ob_nf(pay)', 'ob_nv(w)', 'ob_nv(f)', 'ob_nv(pay)', 'ob_u(w)', 'ob_u(pay)',
                           'ob_d(f)', 'ob_d(w)', 'ob_d(pay)', 'fb_nf(f)', 'fb_nf(-w)', 'fb_nf(-pay)', 'fb_nv(-w)',
                           'fb_nv(-f)', 'fb_nv(-pay)', 'fb_u(-w)', 'fb_u(-pay)', 'fb_d(f)'}
    # Act
    actual_answer_sets = run_deolingo(example[1])
    # Assert
    assert len(actual_answer_sets) == 1
    actual_answer_set = set(actual_answer_sets[0])
    assert actual_answer_set.issuperset(expected_answer_set)


def test_delx_example_4():
    # Arrange
    example = read_example("delx/example4.lp")
    expected_answer_set = {'fb(f)', 'ob(-f)', 'pm_i(w)', 'om_i(w)', 'om_i(f)', '-om(-f)', '-pm(f)', 'pm_d(f)',
                           'ob_nf(-f)', 'ob_nv(-f)', 'ob_u(-f)', 'fb_nf(f)', 'fb_nv(f)', 'fb_u(f)', 'fb_d(f)'}
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
    expected_answer_set = {'f', 'ob(-f)', 'ob(w)', 'ob(f)', 'fb(-w)', 'fb(f)', 'fb(-f)', 'ob_v(-f)', 'viol(f)',
                           'viol(-f)', 'fb_v(f)', 'ob_f(f)', 'ful(-f)', 'ful(f)', 'fb_f(-f)', 'pm_i(w)', '-om(w)',
                           '-om(-f)', '-om(f)', '-pm(f)', '-pm(-w)', '-pm(-f)', 'pm_d(f)', 'om_d(f)', 'om_d(w)',
                           'ob_nf(w)', 'ob_nf(-f)', 'ob_nv(w)', 'ob_nv(f)', 'ob_u(w)', 'ob_d(f)', 'ob_d(w)', 'fb_nf(f)',
                           'fb_nf(-w)', 'fb_nv(-w)', 'fb_nv(-f)', 'fb_u(-w)', 'fb_d(f)'}
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
        # Model 1
        {'ob(-f)', 'ob(-m)', '-f', 'fb(m)', 'fb(f)', 'ob_f(-f)', 'ful(f)', 'ful(-f)', 'fb_f(f)', 'pm_i(w)', 'om_i(m)',
         'om_i(f)', 'om_i(w)', '-om(-f)', '-om(-m)', '-pm(m)', '-pm(f)', 'pm_d(f)', 'pm_d(m)', 'ob_nf(-m)', 'ob_nv(-f)',
         'ob_nv(-m)', 'ob_u(-m)', 'fb_nf(m)', 'fb_nv(m)', 'fb_nv(f)', 'fb_u(m)', 'fb_d(f)', 'fb_d(m)'},
        # Model 2
        {'f', 'ob(-f)', 'ob(w)', 'ob(m)', 'ob(f)', 'fb(-m)', 'fb(-w)', 'fb(f)', 'fb(-f)', 'ob_v(-f)', 'viol(f)',
         'viol(-f)', 'fb_v(f)', 'ob_f(f)', 'ful(f)', 'ful(-f)', 'fb_f(-f)', 'pm_i(m)', 'pm_i(w)', '-om(m)', '-om(w)',
         '-om(-f)', '-om(f)', '-pm(f)', '-pm(-w)', '-pm(-m)', '-pm(-f)', 'pm_d(f)', 'om_d(w)', 'om_d(f)', 'om_d(m)',
         'ob_nf(m)', 'ob_nf(w)', 'ob_nf(-f)', 'ob_nv(m)', 'ob_nv(w)', 'ob_nv(f)', 'ob_u(m)', 'ob_u(w)', 'ob_d(w)',
         'ob_d(f)', 'ob_d(m)', 'fb_nf(f)', 'fb_nf(-w)', 'fb_nf(-m)', 'fb_nv(-w)', 'fb_nv(-m)', 'fb_nv(-f)', 'fb_u(-w)',
         'fb_u(-m)', 'fb_d(f)'}
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
        # Model 1
        {'ob(-f)', 'ob(-m)', '-f', 'fb(m)', 'fb(f)', 'ob_f(-f)', 'ful(f)', 'ful(-f)', 'fb_f(f)', 'pm_i(w)', 'om_i(m)',
         'om_i(w)', 'om_i(f)', '-om(-f)', '-om(-m)', '-pm(m)', '-pm(f)', 'pm_d(f)', 'pm_d(m)', 'ob_nf(-m)', 'ob_nv(-f)',
         'ob_nv(-m)', 'ob_u(-m)', 'fb_nf(m)', 'fb_nv(m)', 'fb_nv(f)', 'fb_u(m)', 'fb_d(f)', 'fb_d(m)'},
        # Model 2
        {'f', 'ob(-f)', 'ob(w)', 'ob(m)', 'ob(f)', 'fb(-m)', 'fb(-w)', 'fb(f)', 'fb(-f)', 'ob_v(-f)', 'viol(f)',
         'viol(-f)', 'fb_v(f)', 'ob_f(f)', 'ful(f)', 'ful(-f)', 'fb_f(-f)', 'pm_i(m)', 'pm_i(w)', '-om(m)', '-om(w)',
         '-om(-f)', '-om(f)', '-pm(f)', '-pm(-w)', '-pm(-m)', '-pm(-f)', 'pm_d(f)', 'om_d(f)', 'om_d(w)', 'om_d(m)',
         'ob_nf(m)', 'ob_nf(w)', 'ob_nf(-f)', 'ob_nv(m)', 'ob_nv(w)', 'ob_nv(f)', 'ob_u(m)', 'ob_u(w)', 'ob_d(f)',
         'ob_d(w)', 'ob_d(m)', 'fb_nf(f)', 'fb_nf(-w)', 'fb_nf(-m)', 'fb_nv(-w)', 'fb_nv(-m)', 'fb_nv(-f)', 'fb_u(-w)',
         'fb_u(-m)', 'fb_d(f)'}
    ]
    # Act
    actual_answer_sets = run_deolingo(example[1], all_models=True)
    # Assert
    assert len(actual_answer_sets) == 2
    actual_answer_set_0 = set(actual_answer_sets[0])
    actual_answer_set_1 = set(actual_answer_sets[1])
    assert actual_answer_set_0.issuperset(expected_answer_sets[0])
    assert actual_answer_set_1.issuperset(expected_answer_sets[1])
