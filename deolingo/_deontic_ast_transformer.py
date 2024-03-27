
import copy

from clingo import ast as ast
from clingo.ast import Transformer
from clingox.ast import theory_term_to_term

from deolingo._deontic_atom import DeonticAtoms


class MultipleRuleException(Exception):
    def __init__(self, rules, line=None):
        self.rules = rules
        self.line = line


def _symbolic_atom(location, name, terms):
    return ast.SymbolicAtom(ast.Function(location, name, terms, False))


def _symbolic_literal(location, sign, atom_name, terms):
    return ast.Literal(location, sign, _symbolic_atom(location, atom_name, terms))


class DeonticASTTransformer(Transformer):

    def __init__(self, translate=False):
        super().__init__()
        self.deontic_atoms = set()
        self.translate = translate
        self.translated_program = ""
        self._last_literal_sign = None
        self._head_theory_atoms_sequence = []
        self._body_theory_atoms_sequence = []
        self._in_body = False
        self._in_head = False
        self._in_rule = False

    def visit_Comment(self, comment):
        self._add_to_translation(comment.location, comment)
        return comment

    def visit_Rule(self, rule):
        self._in_rule = True
        self._in_head = True
        self._head_theory_atoms_sequence = []
        self._body_theory_atoms_sequence = []
        multi_rule = None
        new_head = self.visit(rule.head)
        multi_rule, new_head = self._process_theory_atoms_in_head(multi_rule, new_head, rule)
        self._in_head = False
        self._in_body = True
        new_body = self.visit_sequence(rule.body)
        new_body = self._filter_out_theory_atoms_and_literals_of_theory_atoms(new_body)
        new_body.extend(map(lambda x: x['atom'], self._body_theory_atoms_sequence))
        self._in_body = False
        assert new_head is not None
        assert new_body is not None
        if multi_rule is not None:
            for r in multi_rule:
                r.body.extend(new_body)
            raise MultipleRuleException(multi_rule, rule.location)
        new_rule = ast.Rule(rule.location, new_head, new_body)
        self._add_to_translation(rule.location, new_rule)
        return new_rule

    def visit_Literal(self, literal):
        if literal.atom.ast_type == ast.ASTType.TheoryAtom:
            self._last_literal_sign = literal.sign
        self.visit(literal.atom)
        return literal

    def visit_TheoryAtom(self, atom):
        if atom.term.name == "show":
            self._map_show_atom(atom)
        if self._in_head:
            iterable, literals = self._map_deontic_atom_with_sequence(atom)
            if not iterable:
                return atom
            conditional_literals = [ast.ConditionalLiteral(atom.term.location, lit['atom'], lit['condition'])
                                    for lit in literals]
            self._head_theory_atoms_sequence.extend(conditional_literals)
        elif self._in_body:
            iterable, literals = self._map_deontic_atom_with_sequence(atom)
            if not iterable:
                return atom
            self._body_theory_atoms_sequence.extend(literals)
        return atom

    def _process_theory_atoms_in_head(self, multi_rule, new_head, rule):
        if new_head.ast_type == ast.ASTType.Disjunction or new_head.ast_type == ast.ASTType.TheoryAtom:
            new_head_elements = self._filter_out_theory_atoms_and_literals_of_theory_atoms(
                new_head.elements) if new_head.ast_type == ast.ASTType.Disjunction else []
            if len(self._head_theory_atoms_sequence) == 1 and len(self._head_theory_atoms_sequence[0].condition) > 0:
                new_rule = ast.Rule(rule.location, self._head_theory_atoms_sequence[0].literal,
                                    self._head_theory_atoms_sequence[0].condition)
                new_rule_2 = copy.deepcopy(new_rule)
                ob_nv_atom_name = DeonticAtoms.NON_VIOLATED_OBLIGATION.value.prefixed()
                ob_nv_term = self._head_theory_atoms_sequence[0].condition[0].atom.symbol
                symbolic_atom = _symbolic_atom(rule.location, ob_nv_atom_name, [ob_nv_term])
                new_rule_2.body = [ast.Literal(rule.location, ast.Sign.NoSign, symbolic_atom)]
                multi_rule = [new_rule, new_rule_2]
            else:
                new_head_elements.extend(self._head_theory_atoms_sequence)
                new_head = ast.Disjunction(new_head.location, new_head_elements)
        return multi_rule, new_head

    def _add_to_translation(self, location, statement):
        if self.translate:
            if location is not None:
                self.translated_program += f"\n% Source line: {location.begin.line}\n"
            self.translated_program += str(statement) + "\n"

    def _map_deontic_atom_with_sequence(self, atom):
        if len(atom.elements) < 1:
            raise Exception(f"Empty deontic atom '{atom}'")
        deontic_atom = DeonticAtoms.with_name(atom.term.name)
        if deontic_atom is None:
            raise Exception(f"Deontic atom '{atom.term}' not found")
        new_name = deontic_atom.value.prefixed()
        new_terms = [{'term': theory_term_to_term(the_term.terms[0]), 'condition': the_term.condition}
                     for the_term in atom.elements]
        sign = self._last_literal_sign if self._last_literal_sign is not None else ast.Sign.NoSign
        location = atom.term.location
        new_atoms = [{'atom': _symbolic_literal(location, sign, new_name, [term['term']]),
                      'condition': term['condition']} for term in new_terms]
        deontic_term = new_terms[0]['term']
        if deontic_term.ast_type != ast.ASTType.Variable:
            dt_name = str(deontic_term)
            dt_is_negated = dt_name.startswith("-")
            dt_name = dt_name[1:] if dt_is_negated else dt_name
            self.deontic_atoms.add(dt_name)
        return True, new_atoms

    def _map_show_atom(self, atom):
        show_atoms = set()
        for e in atom.elements:
            da = DeonticAtoms.with_name(str(e.terms[0]))
            if da is not None:
                show_atoms.add(da.value.prefixed())
        show_rules = []
        for sa in show_atoms:
            show_rules.append(ast.ShowSignature(atom.location, sa, 1, 1))
        raise MultipleRuleException(show_rules, atom.location)

    def _filter_out_theory_atoms_and_literals_of_theory_atoms(self, elements):
        return [e for e in elements if e.ast_type != ast.ASTType.TheoryAtom and
                (e.ast_type != ast.ASTType.Literal or e.atom.ast_type != ast.ASTType.TheoryAtom)]
