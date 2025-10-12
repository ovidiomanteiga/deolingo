import unittest

from deolingo.examples import ExampleReader
from deolingo.solver import DeolingoSolver


class DeolingoRegressionTestCase(unittest.TestCase):

    @staticmethod
    def get_sut(all_models=True):
        return DeolingoSolver(all_models=all_models)

    def test_issue_10_error_1(self):
        """Test for the 1st error on issue https://github.com/ovidiomanteiga/deolingo/issues/10"""
        # Arrange
        example = """
            &obligatory{c} :- not &obligatory{m}.
            &obligatory{s}.
        """
        expected_answer_set = {'&obligatory{s}', '&obligatory{c}'}
        # Act
        actual_answer_sets = self.get_sut().solve(example)
        # Assert
        assert len(actual_answer_sets) == 1
        actual_answer_set = set(actual_answer_sets[0])
        assert actual_answer_set == expected_answer_set

    def test_issue_10_error_2(self):
        """Test for 2nd error on issue https://github.com/ovidiomanteiga/deolingo/issues/10"""
        # Arrange
        example = """
            &obligatory{c} :- not &obligatory{m}.
            &obligatory{m} :- not &obligatory{c}.
        """
        expected_answer_set_0 = {'&obligatory{m}'}
        expected_answer_set_1 = {'&obligatory{c}'}
        # Act
        actual_answer_sets = self.get_sut().solve(example)
        print(actual_answer_sets)
        # Assert
        assert len(actual_answer_sets) == 2
        assert set(actual_answer_sets[0]) == expected_answer_set_0
        assert set(actual_answer_sets[1]) == expected_answer_set_1


class DeolingoRegressionOptimizedTestCase(DeolingoRegressionTestCase):

    @staticmethod
    def get_sut(all_models=True):
        return DeolingoSolver(all_models=all_models, optimize=True)
