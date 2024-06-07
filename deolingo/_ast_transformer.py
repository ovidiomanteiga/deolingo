
import copy

from clingo import ast as ast
from clingo.ast import Transformer
from clingox.ast import theory_term_to_term, theory_term_to_literal

from deolingo._deontic_atom import DeonticAtoms


class DeonticASTTransformer(Transformer):

    # <editor-fold desc="Initialization">

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
        self._deontic_conditional = None
        self._file = None

    # </editor-fold>

    # <editor-fold desc="clingo.ast.Transformer override">

    def visit_Comment(self, comment):
        if not comment.value.startswith("%!"):
            raise MultipleRuleException([])
        self._add_to_translation(comment.location, comment)
        return comment

    def visit_Rule(self, rule):
        self._in_rule = True
        self._in_head = True
        self._head_theory_atoms_sequence = []
        self._body_theory_atoms_sequence = []
        self._deontic_conditional = None
        multi_rule = None
        new_head = self.visit(rule.head)
        multi_rule, new_head = self._process_theory_atoms_in_head(multi_rule, new_head, rule)
        self._in_head = False
        self._in_body = True
        new_body = self.visit_sequence(rule.body)
        new_body = self._filter_out_theory_atoms_and_literals_of_theory_atoms(new_body)
        new_body.extend(self._body_theory_atoms_sequence)
        self._in_body = False
        assert new_head is not None
        assert new_body is not None
        if multi_rule is not None:
            for rule in multi_rule:
                rule.body.extend(new_body)
            raise MultipleRuleException(multi_rule, rule.location)
        new_rule = ast.Rule(rule.location, new_head, new_body)
        self._add_to_translation(rule.location, new_rule)
        return new_rule

    def visit_Literal(self, literal):
        self._last_literal_sign = None
        if literal.atom.ast_type == ast.ASTType.TheoryAtom:
            self._last_literal_sign = literal.sign
        self.visit(literal.atom)
        return literal

    def visit_TheoryAtom(self, atom):
        if atom.term.name == "tel":
            return atom
        if atom.term.name == "show":
            self._map_show_atom(atom)

        def has_valid_condition(lit):
            return 'condition' in lit and lit['condition'] is not None and \
                lit['condition'] != []
        if self._in_head:
            iterable, literals, deontic_conditional = self._map_deontic_atom_with_sequence(atom)
            if deontic_conditional is not None:
                self._deontic_conditional = deontic_conditional
            if not iterable:
                return atom
            conditional_literals = [ast.ConditionalLiteral(atom.term.location, lit['term'], lit['condition'] or [])
                                    for lit in literals]
            self._head_theory_atoms_sequence.extend(conditional_literals)
        elif self._in_body:
            iterable, literals, deontic_conditional = self._map_deontic_atom_with_sequence(atom)
            if deontic_conditional is not None:
                raise Exception(f"Deontic conditional '{deontic_conditional}' not allowed in body")
            if not iterable:
                return atom
            conditional_literals = [ast.ConditionalLiteral(atom.term.location, lit['term'], lit['condition'])
                                    if has_valid_condition(lit) else lit['term']
                                    for lit in literals]
            self._body_theory_atoms_sequence.extend(conditional_literals)
        return atom

    # </editor-fold>

    # <editor-fold desc="Private methods">

    def _is_telingo_atom(self, atom):
        return (atom.ast_type == ast.ASTType.TheoryAtom and \
                hasattr(atom, "term") and atom.term.name == "tel")


    def _process_theory_atoms_in_head(self, multi_rule, new_head, rule):
        if new_head.ast_type == ast.ASTType.Disjunction or new_head.ast_type == ast.ASTType.TheoryAtom and \
               not self._is_telingo_atom(new_head):
            new_head_elements = self._filter_out_theory_atoms_and_literals_of_theory_atoms(
                new_head.elements) if new_head.ast_type == ast.ASTType.Disjunction else []
            if self._deontic_conditional is not None:
                new_rule = ast.Rule(rule.location,
                                    self._deontic_conditional.term,
                                    [self._deontic_conditional.condition])
                new_rule_2 = copy.deepcopy(new_rule)
                ob_nv_atom_name = DeonticAtoms.NON_VIOLATED_OBLIGATION.value.prefixed()
                ob_nv_term = self._deontic_conditional.condition.atom.symbol
                ob_nv_atom = _symbolic_atom(rule.location, ob_nv_atom_name, [ob_nv_term])
                new_rule_2.body = [_positive_literal(rule.location, ob_nv_atom)]
                multi_rule = [new_rule, new_rule_2]
            else:
                new_head_elements.extend(self._head_theory_atoms_sequence)
                new_head = ast.Disjunction(new_head.location, new_head_elements)
        return multi_rule, new_head

    def _add_to_translation(self, location, statement):
        if self.translate:
            if location is not None:
                if self._file != location.end.filename:
                    self._file = location.end.filename
                    self.translated_program += f"\n% File: {location.end.filename}\n"
                self.translated_program += f"\n% Source line: {location.begin.line}\n"
            self.translated_program += str(statement) + "\n"

    def _map_deontic_atom_with_sequence(self, atom):
        if len(atom.elements) < 1:
            raise Exception(f"Empty deontic atom '{atom}'")
        deontic_atom = DeonticAtoms.with_name(atom.term.name)
        if deontic_atom is None:
            if atom.term.name == "tel":
                return True, [atom], None
            raise Exception(f"Deontic atom '{atom.term}' not found")
        deontic_conditional = _DeonticConditional.from_deontic_atom(atom)
        if deontic_conditional is not None:
            if deontic_conditional.symbolic_term.ast_type != ast.ASTType.Variable:
                dt_name = str(deontic_conditional.symbolic_term)
                dt_is_negated = dt_name.startswith("-")
                dt_name = dt_name[1:] if dt_is_negated else dt_name
                self.deontic_atoms.add(dt_name)
            return False, None, deontic_conditional
        new_name = deontic_atom.prefixed()
        sign = self._last_literal_sign if self._last_literal_sign is not None else ast.Sign.NoSign
        new_deontic_atoms = []

        def symbolize_terms(terms):
            new_terms = [theory_term_to_term(t) for t in terms]
            for t in new_terms:
                if t.ast_type != ast.ASTType.Variable:
                    new_deontic_atoms.append(t)
            return _symbolic_literal(atom.term.location, sign, new_name, new_terms)
        is_disjunction = _DeonticDisjunctionOrConjunction.transform_deontic_atom(atom, operator="||")
        if is_disjunction and self._in_body:
            raise Exception(f"Disjunction '{atom}' not allowed in body")
        is_conjunction = _DeonticDisjunctionOrConjunction.transform_deontic_atom(atom, operator="&&")
        if is_conjunction and self._in_head:
            raise Exception(f"Conjunction '{atom}' not allowed in head")
        new_atoms = [{'term': symbolize_terms(the_term.terms), 'condition': the_term.condition}
                     for the_term in atom.elements]
        for new_deontic_atom in new_deontic_atoms:
            if new_deontic_atom.ast_type != ast.ASTType.Variable:
                dt_name = str(new_deontic_atom)
                dt_is_negated = dt_name.startswith("-")
                dt_name = dt_name[1:] if dt_is_negated else dt_name
                self.deontic_atoms.add(dt_name)
        return True, new_atoms, None

    def _map_show_atom(self, atom):
        show_atoms = set()
        for element in atom.elements:
            deontic_atom = DeonticAtoms.with_name(str(element.terms[0]))
            if deontic_atom is not None:
                show_atoms.add(deontic_atom.prefixed())
        show_rules = []
        for sa in show_atoms:
            show_rules.append(ast.ShowSignature(atom.location, sa, 1, 1))
        raise MultipleRuleException(show_rules, atom.location)

    def _filter_out_theory_atoms_and_literals_of_theory_atoms(self, elements):
        return [element for element in elements
                if (element.ast_type != ast.ASTType.TheoryAtom and
                (element.ast_type != ast.ASTType.Literal or
                 element.atom.ast_type != ast.ASTType.TheoryAtom)) or
                (element.ast_type == ast.ASTType.TheoryAtom and element.term.name == "tel") or
                (element.ast_type == ast.ASTType.Literal and
                 element.atom.ast_type == ast.ASTType.TheoryAtom and
                 element.atom.term.name == "tel")
                ]

    # </editor-fold>


# <editor-fold desc="Exception classes">

class MultipleRuleException(Exception):
    def __init__(self, rules, line=None):
        self.rules = rules
        self.line = line

# </editor-fold>


# <editor-fold desc="Private classes">

class _DeonticConditional:

    def __init__(self, deontic_atom, term, condition, symbolic_term, string_repr=None):
        self.deontic_atom = deontic_atom
        self.term = term
        self.condition = condition
        self.string_repr = string_repr
        self.symbolic_term = symbolic_term

    @staticmethod
    def from_deontic_atom(atom):
        if len(atom.elements) < 1:
            return None
        deontic_atom = DeonticAtoms.with_name(atom.term.name)
        if deontic_atom is None:
            return None
        deontic_atom_prefixed = deontic_atom.prefixed()
        for element in atom.elements:
            is_conditional = len(element.terms) == 1 and \
                             element.terms[0].ast_type == ast.ASTType.TheoryUnparsedTerm and \
                             len(element.terms[0].elements) == 2 and \
                             element.terms[0].elements[0].ast_type == ast.ASTType.TheoryUnparsedTermElement and \
                             element.terms[0].elements[1].ast_type == ast.ASTType.TheoryUnparsedTermElement and \
                             element.terms[0].elements[1].operators[0] == "|"
            if is_conditional:
                lhs_operators = element.terms[0].elements[0].operators
                rhs_operators = element.terms[0].elements[1].operators
                lhs_negative = lhs_operators[0] == "-" if len(lhs_operators) > 0 else False
                rhs_negative = rhs_operators[1] == "-" if len(rhs_operators) > 1 else False
                symbolic_term = theory_term_to_term(element.terms[0].elements[0].term)
                if lhs_negative:
                    symbolic_term = ast.UnaryOperation(atom.location, ast.UnaryOperator.Minus, symbolic_term)
                term = _symbolic_literal(atom.location, ast.Sign.NoSign, deontic_atom_prefixed, [symbolic_term])
                condition = theory_term_to_literal(element.terms[0].elements[1].term)
                if rhs_negative:
                    rhs_term = theory_term_to_term(element.terms[0].elements[1].term)
                    rhs_atom = ast.SymbolicAtom(ast.UnaryOperation(atom.location, ast.UnaryOperator.Minus, rhs_term))
                    condition = _positive_literal(atom.location, rhs_atom)
                return _DeonticConditional(deontic_atom_prefixed, term, condition, symbolic_term, str(atom))
        return None

    def __str__(self):
        return self.string_repr


class _DeonticDisjunctionOrConjunction:

    @staticmethod
    def transform_deontic_atom(atom, operator="||"):
        if len(atom.elements) < 1:
            return None
        deontic_atom = DeonticAtoms.with_name(atom.term.name)
        if deontic_atom is None:
            return None
        new_elements = []
        contains_operation = False
        for element in atom.elements:
            is_operation = False
            for term in element.terms:
                if term.ast_type == ast.ASTType.TheoryUnparsedTerm and len(term.elements) > 1:
                    pass
                else:
                    continue
                is_operation = term.elements[0].ast_type == ast.ASTType.TheoryUnparsedTermElement and \
                               all(x.ast_type == ast.ASTType.TheoryUnparsedTermElement and x.operators[0] == operator
                                   for x in term.elements[1:])
                if is_operation:
                    for el in term.elements:
                        new_element_term = theory_term_to_term(el.term)
                        new_element = ast.TheoryAtomElement([new_element_term], [])
                        new_elements.append(new_element)
            contains_operation = contains_operation or is_operation
            if not is_operation:
                new_elements.append(element)
        atom.elements = new_elements
        return contains_operation

# </editor-fold>


# <editor-fold desc="Helper functions">

def _positive_literal(location, atom):
    return ast.Literal(location, ast.Sign.NoSign, atom)


def _negative_literal(location, atom):
    return ast.Literal(location, ast.Sign.Negation, atom)


def _symbolic_atom(location, name, terms):
    return ast.SymbolicAtom(ast.Function(location, name, terms, False))


def _symbolic_literal(location, sign, atom_name, terms):
    return ast.Literal(location, sign, _symbolic_atom(location, atom_name, terms))

# </editor-fold>
