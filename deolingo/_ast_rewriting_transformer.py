
import copy

from clingo import ast as ast

from deolingo._ast_transformer import DeonticASTTransformer, _symbolic_atom, _positive_literal, \
    _negative_literal
from deolingo._deontic_atom import DeonticAtoms


class DeonticASTRewritingTransformer(DeonticASTTransformer):

    # <editor-fold desc="Initialization">

    def __init__(self, translate=False):
        super().__init__(translate=translate)
        self._derivation_rules_to_be_added = set()

    # </editor-fold>

    # <editor-fold desc="Getters/Setters">

    @property
    def derivation_rules_to_be_added(self):
        return self._derivation_rules_to_be_added

    # </editor-fold>

    # <editor-fold desc="clingo.ast.Transformer override">

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
            rewritten_literals = self._rewrite_literals(literals)
            conditional_literals = [ast.ConditionalLiteral(atom.term.location, lit['term'], lit['condition'])
                                    if has_valid_condition(lit) else lit['term']
                                    for lit in rewritten_literals]
            self._body_theory_atoms_sequence.extend(conditional_literals)
        return atom

    # </editor-fold>

    # <editor-fold desc="Private methods">

    def _rewrite_literals(self, literals):
        new_literals = []
        for lit in literals:
            new_term = lit['term']
            new_condition = lit['condition'] if 'condition' in lit else None
            if new_term.atom.symbol.name in [DeonticAtoms.VIOLATED_OBLIGATION.value.prefixed(),
                                             DeonticAtoms.FULFILLED_OBLIGATION.value.prefixed(),
                                             DeonticAtoms.NON_VIOLATED_OBLIGATION.value.prefixed(),
                                             DeonticAtoms.NON_FULFILLED_OBLIGATION.value.prefixed(),
                                             DeonticAtoms.UNDETERMINED_OBLIGATION.value.prefixed()]:
                if new_term.sign == ast.Sign.Negation:
                    new_literals.append(lit)
                    self._derivation_rules_to_be_added.add(new_term.atom.symbol.name)
                    continue
                is_fulfillment = new_term.atom.symbol.name in [DeonticAtoms.FULFILLED_OBLIGATION.value.prefixed(),
                                                               DeonticAtoms.NON_FULFILLED_OBLIGATION.value.prefixed()]
                is_negated = new_term.atom.symbol.name in [DeonticAtoms.NON_VIOLATED_OBLIGATION.value.prefixed(),
                                                           DeonticAtoms.NON_FULFILLED_OBLIGATION.value.prefixed()]
                is_undetermined = new_term.atom.symbol.name == DeonticAtoms.UNDETERMINED_OBLIGATION.value.prefixed()
                new_term_2 = copy.deepcopy(new_term)
                new_term_3 = copy.deepcopy(new_term)
                new_term.atom.symbol.name = DeonticAtoms.OBLIGATORY.value.prefixed()
                new_term_2.atom.symbol.name = DeonticAtoms.HOLDS.value.prefixed()
                new_term_3.atom.symbol.name = DeonticAtoms.HOLDS.value.prefixed()
                new_literals.append({'term': new_term, 'condition': new_condition})
                if is_negated or is_undetermined:
                    new_term_2.sign = ast.Sign.Negation
                    new_term_3.sign = ast.Sign.Negation
                if not is_fulfillment and not is_undetermined:
                    self._negate_deontic_atom_content(new_term_2)
                new_literals.append({'term': new_term_2, 'condition': new_condition})
                if is_undetermined:
                    self._negate_deontic_atom_content(new_term_3)
                    new_literals.append({'term': new_term_3, 'condition': new_condition})
            elif new_term.atom.symbol.name in [DeonticAtoms.VIOLATED_PROHIBITION.value.prefixed(),
                                               DeonticAtoms.FULFILLED_PROHIBITION.value.prefixed(),
                                               DeonticAtoms.NON_VIOLATED_PROHIBITION.value.prefixed(),
                                               DeonticAtoms.NON_FULFILLED_PROHIBITION.value.prefixed(),
                                               DeonticAtoms.UNDETERMINED_PROHIBITION.value.prefixed()]:
                if new_term.sign == ast.Sign.Negation:
                    new_literals.append(lit)
                    self._derivation_rules_to_be_added.add(new_term.atom.symbol.name)
                    continue
                is_fulfillment = new_term.atom.symbol.name in [DeonticAtoms.FULFILLED_PROHIBITION.value.prefixed(),
                                                               DeonticAtoms.NON_FULFILLED_PROHIBITION.value.prefixed()]
                is_negated = new_term.atom.symbol.name in [DeonticAtoms.NON_VIOLATED_PROHIBITION.value.prefixed(),
                                                           DeonticAtoms.NON_FULFILLED_PROHIBITION.value.prefixed()]
                new_term_2 = copy.deepcopy(new_term)
                new_term.atom.symbol.name = DeonticAtoms.FORBIDDEN.value.prefixed()
                new_term_2.atom.symbol.name = DeonticAtoms.HOLDS.value.prefixed()
                new_literals.append({'term': new_term, 'condition': new_condition})
                if is_negated:
                    new_term_2.sign = ast.Sign.Negation
                if is_fulfillment:
                    self._negate_deontic_atom_content(new_term_2)
                new_literals.append({'term': new_term_2, 'condition': new_condition})
            elif new_term.atom.symbol.name in [DeonticAtoms.PERMITTED_IMPLICITLY.value.prefixed()]:
                new_term.atom.symbol.name = DeonticAtoms.FORBIDDEN.value.prefixed()
                new_term.sign = ast.Sign.Negation if new_term.sign == ast.Sign.NoSign else ast.Sign.DoubleNegation
                new_literals.append({'term': new_term, 'condition': new_condition})
            elif new_term.atom.symbol.name in [DeonticAtoms.OMISSIBLE_IMPLICITLY.value.prefixed()]:
                new_term.atom.symbol.name = DeonticAtoms.OBLIGATORY.value.prefixed()
                new_term.sign = ast.Sign.Negation if new_term.sign == ast.Sign.NoSign else ast.Sign.DoubleNegation
                new_literals.append({'term': new_term, 'condition': new_condition})
            else:
                new_literals.append(lit)
        return new_literals

    def _process_theory_atoms_in_head(self, multi_rule, new_head, rule):
        if (new_head.ast_type == ast.ASTType.Disjunction or new_head.ast_type == ast.ASTType.TheoryAtom) and \
               not self._is_telingo_atom(new_head):
            new_head_elements = self._filter_out_theory_atoms_and_literals_of_theory_atoms(
                new_head.elements) if new_head.ast_type == ast.ASTType.Disjunction else []
            if self._deontic_conditional is not None:
                new_rule = ast.Rule(rule.location,
                                    self._deontic_conditional.term,
                                    [self._deontic_conditional.condition])
                new_rule_2 = copy.deepcopy(new_rule)
                ob_atom_name = DeonticAtoms.OBLIGATORY.value.prefixed()
                nh_atom_name = DeonticAtoms.HOLDS.value.prefixed()
                conditional_term = self._deontic_conditional.condition.atom.symbol
                nh_conditional_term = copy.deepcopy(conditional_term)
                negative = "-"
                if str(nh_conditional_term).startswith("-"):
                    negative = ""
                    nh_conditional_term = nh_conditional_term.argument
                ob_atom = _symbolic_atom(rule.location, ob_atom_name, [conditional_term])
                nh_atom = _symbolic_atom(rule.location, negative + nh_atom_name, [nh_conditional_term])
                new_rule_2.body = [_positive_literal(rule.location, ob_atom),
                                   _negative_literal(rule.location, nh_atom)]
                multi_rule = [new_rule, new_rule_2]
            else:
                new_head_elements.extend(self._head_theory_atoms_sequence)
                new_head = ast.Disjunction(new_head.location, new_head_elements)
        return multi_rule, new_head

    def _negate_deontic_atom_content(self, deontic_atom):
        if deontic_atom.atom.symbol.ast_type == ast.ASTType.Function:
            if deontic_atom.atom.symbol.arguments[0].ast_type == ast.ASTType.UnaryOperation:
                deontic_atom.atom.symbol.arguments[0] = deontic_atom.atom.symbol.arguments[0].argument
            else:
                arg0 = deontic_atom.atom.symbol.arguments[0]
                deontic_atom.atom.symbol.arguments[0] = \
                    ast.UnaryOperation(deontic_atom.location, ast.UnaryOperator.Minus, arg0)
        else:
            deontic_atom.atom.symbol.name = "-" + deontic_atom.atom.symbol.name

    # </editor-fold>
