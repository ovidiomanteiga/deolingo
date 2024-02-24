
from clingo import ast as ast
from clingo.ast import Transformer
from clingox.ast import theory_term_to_term

from _deontic_atom import DeonticAtoms


class DeonticTransformer(Transformer):

    def __init__(self):
        super().__init__()
        self.deontic_atoms = set()

    def map_deontic_atom(self, atom, as_literal=False):
        deontic_atom = DeonticAtoms.with_name(atom.term.name)
        if deontic_atom is not None:
            deontic_atom = deontic_atom.value
            new_name = deontic_atom.prefixed()
            if len(atom.elements) == 1:
                new_name = ("-" if deontic_atom.is_negated else "") + new_name
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
        return atom

    def visit_Rule(self, rule):
        new_head = rule.head
        if rule.head is not None:
            if rule.head.ast_type == ast.ASTType.TheoryAtom:
                new_head = self.map_deontic_atom(rule.head, as_literal=True)
            new_head = self(new_head)
        new_body = rule.body
        if rule.body is not None:
            new_body = self.visit_sequence(rule.body)
        return ast.Rule(rule.location, new_head, new_body)

    def visit_TheoryAtom(self, atom):
        return self.map_deontic_atom(atom)
