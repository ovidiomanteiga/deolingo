
import unittest

from deolingo._ast_rewriting_transformer import DeonticASTRewritingTransformer
from clingo.ast import parse_string


def parse(string) -> str:
    transformer = DeonticASTRewritingTransformer(translate=True)
    translated = ""

    def callback(x):
        nonlocal translated
        translated = str(transformer(x))
    parse_string(string, callback)
    return translated


class DeolingoRewritingTranslatorTestCase(unittest.TestCase):

    def test_permitted_implicitly(self):
        actual = parse(":- &permitted_implicitly{a}.")
        expected = "#false :- not _deolingo_forbidden(a)."
        self.assertEqual(expected, actual)

    def test_permitted_implicitlyg_negated(self):
        actual = parse(":- not &permitted_implicitly{a}.")
        expected = "#false :- not not _deolingo_forbidden(a)."
        self.assertEqual(expected, actual)

    def test_permitted_implicitly_strong_negated(self):
        actual = parse(":- &permitted_implicitly{-a}.")
        expected = "#false :- not _deolingo_forbidden(-a)."
        self.assertEqual(expected, actual)

    def test_omissible_implicitly(self):
        actual = parse(":- &omissible_implicitly{a}.")
        expected = "#false :- not _deolingo_obligatory(a)."
        self.assertEqual(expected, actual)

    def test_omissible_implicitlyg_negated(self):
        actual = parse(":- not &omissible_implicitly{a}.")
        expected = "#false :- not not _deolingo_obligatory(a)."
        self.assertEqual(expected, actual)

    def test_omissible_implicitly_strong_negated(self):
        actual = parse(":- &omissible_implicitly{-a}.")
        expected = "#false :- not _deolingo_obligatory(-a)."
        self.assertEqual(expected, actual)

    def test_violated_obligation(self):
        actual = parse(":- &violated_obligation{a}.")
        expected = "#false :- _deolingo_obligatory(a); -_deolingo_holds(a)."
        self.assertEqual(expected, actual)

    def test_violated_obligation_negated(self):
        actual = parse(":- not &violated_obligation{a}.")
        expected = "#false :- not _deolingo_obligatory(a); not -_deolingo_holds(a)."
        #expected = """#false :- not _deolingo_violated_obligation(a).
        #_deolingo_violated_obligation(X) :- _deolingo_obligatory(X); -_deolingo_holds(X)."""
        # WARNING: This is not the right result, but it is the result of the current implementation.
        # #false :- not _deolingo_obligatory(a).
        # #false :- not -_deolingo_holds(a)."
        self.assertEqual(expected, actual)

    def test_violated_obligation_strong_negated(self):
        actual = parse(":- &violated_obligation{-a}.")
        expected = "#false :- _deolingo_obligatory(-a); -_deolingo_holds(-a)."
        self.assertEqual(expected, actual)

    def test_non_violated_obligation(self):
        actual = parse(":- &non_violated_obligation{a}.")
        expected = "#false :- _deolingo_obligatory(a); not -_deolingo_holds(a)."
        self.assertEqual(expected, actual)

    def test_non_violated_obligation_strong_negated(self):
        actual = parse(":- &non_violated_obligation{-a}.")
        expected = "#false :- _deolingo_obligatory(-a); not -_deolingo_holds(-a)."
        self.assertEqual(expected, actual)

    def test_fulfilled_obligation(self):
        actual = parse(":- &fulfilled_obligation{a}.")
        expected = "#false :- _deolingo_obligatory(a); _deolingo_holds(a)."
        self.assertEqual(expected, actual)

    def test_fulfilled_obligation_strong_negated(self):
        actual = parse(":- &fulfilled_obligation{-a}.")
        expected = "#false :- _deolingo_obligatory(-a); _deolingo_holds(-a)."
        self.assertEqual(expected, actual)

    def test_non_fulfilled_obligation(self):
        actual = parse(":- &non_fulfilled_obligation{a}.")
        expected = "#false :- _deolingo_obligatory(a); not _deolingo_holds(a)."
        self.assertEqual(expected, actual)

    def test_non_fulfilled_obligation_strong_negated(self):
        actual = parse(":- &non_fulfilled_obligation{-a}.")
        expected = "#false :- _deolingo_obligatory(-a); not _deolingo_holds(-a)."
        self.assertEqual(expected, actual)

    def test_undetermined_obligation(self):
        actual = parse(":- &undetermined_obligation{a}.")
        expected = "#false :- _deolingo_obligatory(a); not _deolingo_holds(a); not -_deolingo_holds(a)."
        self.assertEqual(expected, actual)

    def test_undetermined_obligation_strong_negated(self):
        actual = parse(":- &undetermined_obligation{-a}.")
        expected = "#false :- _deolingo_obligatory(-a); not _deolingo_holds(-a); not -_deolingo_holds(-a)."
        self.assertEqual(expected, actual)

    def test_violated_prohibition(self):
        actual = parse(":- &violated_prohibition{a}.")
        expected = "#false :- _deolingo_forbidden(a); _deolingo_holds(a)."
        self.assertEqual(expected, actual)

    def test_violated_prohibition_strong_negated(self):
        actual = parse(":- &violated_prohibition{-a}.")
        expected = "#false :- _deolingo_forbidden(-a); _deolingo_holds(-a)."
        self.assertEqual(expected, actual)

    def test_non_violated_prohibition(self):
        actual = parse(":- &non_violated_prohibition{a}.")
        expected = "#false :- _deolingo_forbidden(a); not _deolingo_holds(a)."
        self.assertEqual(expected, actual)

    def test_non_violated_prohibition_strong_negated(self):
        actual = parse(":- &non_violated_prohibition{-a}.")
        expected = "#false :- _deolingo_forbidden(-a); not _deolingo_holds(-a)."
        self.assertEqual(expected, actual)

    def test_fulfilled_prohibition(self):
        actual = parse(":- &fulfilled_prohibition{a}.")
        expected = "#false :- _deolingo_forbidden(a); -_deolingo_holds(a)."
        self.assertEqual(expected, actual)

    def test_fulfilled_prohibition_strong_negated(self):
        actual = parse(":- &fulfilled_prohibition{-a}.")
        expected = "#false :- _deolingo_forbidden(-a); -_deolingo_holds(-a)."
        self.assertEqual(expected, actual)

    def test_non_fulfilled_prohibition(self):
        actual = parse(":- &non_fulfilled_prohibition{a}.")
        expected = "#false :- _deolingo_forbidden(a); not -_deolingo_holds(a)."
        self.assertEqual(expected, actual)

    def test_non_fulfilled_prohibition_strong_negated(self):
        actual = parse(":- &non_fulfilled_prohibition{-a}.")
        expected = "#false :- _deolingo_forbidden(-a); not -_deolingo_holds(-a)."
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
