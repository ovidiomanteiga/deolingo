import logging

from clingo import ast as ast
from clingo.ast import Transformer
from clingox.ast import theory_term_to_term

from deolingo._deontic_atom import DeonticAtoms


class SkipException(Exception):
    pass


class DeonticASTTransformer(Transformer):

    def __init__(self, translate=False):
        super().__init__()
        self.deontic_atoms = set()
        self.translate = translate
        self.translated_program = ""
        self.show_atoms = set()

    def visit_Rule(self, rule):
        new_head = rule.head
        if rule.head is not None:
            if rule.head.ast_type == ast.ASTType.TheoryAtom:
                new_head = self._map_deontic_atom(rule.head, as_literal=True)
            new_head = self(new_head)
        new_body = rule.body
        if rule.body is not None:
            new_body = self.visit_sequence(rule.body)
        new_rule = ast.Rule(rule.location, new_head, new_body)
        self._add_to_translation(rule.location, new_rule)
        return new_rule

    def visit_TheoryAtom(self, atom):
        if atom.term.name == "show":
            self._map_show_atom(atom)
            raise SkipException()
        return self._map_deontic_atom(atom)

    def _add_to_translation(self, location, statement):
        if self.translate:
            self.translated_program += f"\n% Source line: {location.begin.line}\n"
            self.translated_program += str(statement) + "\n"

    def _map_deontic_atom(self, atom, as_literal=False):
        deontic_atom = DeonticAtoms.with_name(atom.term.name)
        if len(atom.elements) < 1 or deontic_atom is None:
            return atom
        if len(atom.elements) > 1:
            logging.log(logging.WARNING, "Deontic atom with more than one element,"
                                         "only the first one will be considered.")
        new_name = deontic_atom.value.prefixed()
        new_terms = [theory_term_to_term(tterm) for tterm in atom.elements[0].terms]
        new_atom = ast.SymbolicAtom(ast.Function(atom.term.location, new_name, new_terms, False))
        if as_literal:
            new_atom = ast.Literal(atom.term.location, ast.Sign.NoSign, new_atom)
        deontic_term = new_terms[0]
        if deontic_term.ast_type != ast.ASTType.Variable:
            dt_name = str(deontic_term)
            dt_is_negated = dt_name.startswith("-")
            dt_name = dt_name[1:] if dt_is_negated else dt_name
            self.deontic_atoms.add(dt_name)
        return new_atom

    def _map_show_atom(self, atom):
        for e in atom.elements:
            da = DeonticAtoms.with_name(str(e.terms[0]))
            if da is not None:
                self.show_atoms.add(da.value.prefixed() + "/1")
