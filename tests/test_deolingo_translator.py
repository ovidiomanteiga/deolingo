
import unittest

import pytest

from deolingo._rewriting_translator import DeolingoRewritingTranslator
from deolingo._translator import DeolingoTranslator


class DeolingoTranslatorTestCase(unittest.TestCase):
    
    @staticmethod
    def get_sut(callback):
        return DeolingoTranslator(add_to_program_callback=callback, translate=True,
                           add_theory=False, add_deontic_rules=False)
    
    def parse(self, string) -> str:
        translated = ""

        def callback(x):
            nonlocal translated
            translated += str(x) + "\n"

        translator = self.get_sut(callback)
        translator.transform_source(string)
        return translated

    def test_rule(self):
        actual = self.parse("&obligatory{a} :- &forbidden{b}.")
        expected = "deolingo_obligatory(a) :- deolingo_forbidden(b).\n"
        self.assertEqual(expected, actual)

    def test_rule_with_negation(self):
        actual = self.parse("&omissible{a} :- not &forbidden{b}.")
        expected = "deolingo_omissible(a) :- not deolingo_forbidden(b).\n"
        self.assertEqual(expected, actual)

    def test_deontic_sequence_head(self):
        actual = self.parse("&obligatory{a; -b}.")
        expected = "deolingo_obligatory(a); deolingo_obligatory(-b).\n"
        self.assertEqual(expected, actual)

    def test_deontic_sequence_body(self):
        actual = self.parse(":- &obligatory{a; -b}.")
        expected = "#false :- deolingo_obligatory(a); deolingo_obligatory(-b).\n"
        self.assertEqual(expected, actual)

    def test_deontic_sequence_head_variable(self):
        actual = self.parse("&obligatory{a;X} :- p(X).")
        expected = "deolingo_obligatory(a); deolingo_obligatory(X) :- p(X).\n"
        self.assertEqual(expected, actual)

    def test_deontic_sequence_default_negation_body(self):
        actual = self.parse(":- not &obligatory{a; b}.")
        expected = "#false :- not deolingo_obligatory(a); not deolingo_obligatory(b).\n"
        self.assertEqual(expected, actual)

    def test_deontic_sequence_body_variable(self):
        actual = self.parse(":- &obligatory{X;b}, p(X).")
        expected = "#false :- p(X); deolingo_obligatory(X); deolingo_obligatory(b).\n"
        # TODO: preserve order of atoms!
        self.assertEqual(expected, actual)

    def test_deontic_sequence_with_conditions_head(self):
        actual = self.parse("&obligatory{a: b; -c: d}.")
        expected = "deolingo_obligatory(a): b; deolingo_obligatory(-c): d.\n"
        self.assertEqual(expected, actual)

    def test_deontic_sequence_with_conditions_body(self):
        actual = self.parse(":- &obligatory{a: b; -c: d}.")
        expected = "#false :- deolingo_obligatory(a): b; deolingo_obligatory(-c): d.\n"
        self.assertEqual(expected, actual)

    def test_deontic_conditional(self):
        actual = self.parse("&obligatory{a|b}.")
        expected = "deolingo_obligatory(a) :- b.\ndeolingo_obligatory(a) :- deolingo_non_violated_obligation(b).\n"
        self.assertEqual(expected, actual)

    def test_deontic_conditional_explicit_negation(self):
        actual = self.parse("&obligatory{-a | -b}.")
        expected = "deolingo_obligatory(-a) :- -b.\ndeolingo_obligatory(-a) :- deolingo_non_violated_obligation(-b).\n"
        self.assertEqual(expected, actual)

    def test_deontic_conditional_variable(self):
        actual = self.parse("&obligatory{X | a} :- p(X).")
        expected = "deolingo_obligatory(X) :- a; p(X).\ndeolingo_obligatory(X) :- deolingo_non_violated_obligation(a); p(X).\n"
        self.assertEqual(expected, actual)

    def test_disjunction_head(self):
        actual = self.parse("&obligatory{a || b}.")
        expected = "deolingo_obligatory(a); deolingo_obligatory(b).\n"
        self.assertEqual(expected, actual)

    def test_disjunction_body(self):
        with pytest.raises(Exception):
            self.parse(":- &obligatory{a || b}.")

    def test_conjunction_head(self):
        with pytest.raises(Exception):
            self.parse("&obligatory{a && b}.")

    def test_conjunction_body(self):
        actual = self.parse(":- &obligatory{a && b}.")
        expected = "#false :- deolingo_obligatory(a); deolingo_obligatory(b).\n"
        self.assertEqual(expected, actual)


class DeolingoRewritingTranslatorTestCase(unittest.TestCase):

    @staticmethod
    def get_sut(callback):
        return DeolingoRewritingTranslator(add_to_program_callback=callback, translate=True,
                                           add_theory=False, add_deontic_rules=False)


if __name__ == '__main__':
    unittest.main()
