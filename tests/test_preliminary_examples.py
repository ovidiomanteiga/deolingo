
import unittest

from deolingo.examples import ExampleReader
from deolingo.solver import DeolingoSolver


class DeolingoPreliminaryExamplesTestCase(unittest.TestCase):

    @staticmethod
    def get_sut():
        return DeolingoSolver()

    def test_preliminary_example_1(self):
        # Arrange
        example = ExampleReader().read_example("preliminary/example1.lp")
        expected_answer_set = {"park"}
        # Act
        actual_answer_sets = self.get_sut().solve(example.contents)
        # Assert
        assert len(actual_answer_sets) == 1
        actual_answer_set = set(actual_answer_sets[0])
        assert actual_answer_set == expected_answer_set
    
    def test_preliminary_example_2(self):
        # Arrange
        example = ExampleReader().read_example("preliminary/example2.lp")
        expected_answer_set = {'&obligatory{work}', '-work', '-weekend'}
        # Act
        actual_answer_sets = self.get_sut().solve(example.contents)
        # Assert
        assert len(actual_answer_sets) == 1
        actual_answer_set = set(actual_answer_sets[0])
        assert actual_answer_set == expected_answer_set
    
    def test_preliminary_example_3(self):
        # Arrange
        example = ExampleReader().read_example("preliminary/example3.lp")
        # Act
        actual_answer_sets = self.get_sut().solve(example.contents)
        # Assert
        assert actual_answer_sets == []

    def test_preliminary_example_4(self):
        # Arrange
        example = ExampleReader().read_example("preliminary/example4.lp")
        expected_answer_set = {'walk', '&obligatory{walk_right}', '&obligatory{walk}', 'walk_right', '&forbidden{walk}'}
        # Act
        actual_answer_sets = self.get_sut().solve(example.contents)
        print(actual_answer_sets)
        # Assert
        assert len(actual_answer_sets) == 1
        actual_answer_set = set(actual_answer_sets[0])
        assert actual_answer_set == expected_answer_set
    
    def test_preliminary_example_5(self):
        # Arrange
        example = ExampleReader().read_example("preliminary/example5.lp")
        expected_answer_set = {'&permitted{fence}', 'fence', 'sea'}
        # Act
        actual_answer_sets = self.get_sut().solve(example.contents)
        # Assert
        assert len(actual_answer_sets) == 1
        actual_answer_set = set(actual_answer_sets[0])
        assert actual_answer_set == expected_answer_set


class DeolingoPreliminaryExamplesOptimizedTestCase(DeolingoPreliminaryExamplesTestCase):

    @staticmethod
    def get_sut():
        return DeolingoSolver(optimize=True)
