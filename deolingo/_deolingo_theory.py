
from deolingo._deontic_atom import DeonticAtoms as Deo


_DEOLINGO_THEORY = f"""
#theory deolingo {{
    deontic_term {{
        - : 4, unary;
        && : 3, binary, left;
        || : 2, binary, left;
        | : 1, binary, left
    }};
    show_term {{ / : 1, binary, left }};
    &{Deo.OBLIGATORY.value.name}/0 : deontic_term, any;
    &{Deo.FORBIDDEN.value.name}/0 : deontic_term, any;
    &{Deo.OMISSIBLE.value.name}/0 : deontic_term, any;
    &{Deo.PERMITTED.value.name}/0 : deontic_term, any;
    &{Deo.OPTIONAL.value.name}/0 : deontic_term, any;
    &{Deo.PERMITTED_BY_DEFAULT.value.name}/0 : deontic_term, any;
    &{Deo.OMISSIBLE_BY_DEFAULT.value.name}/0 : deontic_term, any;
    &{Deo.HOLDS.value.name}/0 : deontic_term, any;
    &{Deo.DEONTIC.value.name}/0 : deontic_term, any;
    &{Deo.PERMITTED_IMPLICITLY.value.name}/0 : deontic_term, any;
    &{Deo.OMISSIBLE_IMPLICITLY.value.name}/0 : deontic_term, any;
    &{Deo.VIOLATED.value.name}/0 : deontic_term, any;
    &{Deo.FULFILLED.value.name}/0 : deontic_term, any;
    &{Deo.VIOLATED_OBLIGATION.value.name}/0 : deontic_term, any;
    &{Deo.FULFILLED_OBLIGATION.value.name}/0 : deontic_term, any;
    &{Deo.NON_VIOLATED_OBLIGATION.value.name}/0 : deontic_term, any;
    &{Deo.NON_FULFILLED_OBLIGATION.value.name}/0 : deontic_term, any;
    &{Deo.UNDETERMINED_OBLIGATION.value.name}/0 : deontic_term, any;
    &{Deo.DEFAULT_OBLIGATION.value.name}/0 : deontic_term, any;
    &{Deo.VIOLATED_PROHIBITION.value.name}/0 : deontic_term, any;
    &{Deo.FULFILLED_PROHIBITION.value.name}/0 : deontic_term, any;
    &{Deo.NON_VIOLATED_PROHIBITION.value.name}/0 : deontic_term, any;
    &{Deo.NON_FULFILLED_PROHIBITION.value.name}/0 : deontic_term, any;
    &{Deo.UNDETERMINED_PROHIBITION.value.name}/0 : deontic_term, any;
    &{Deo.DEFAULT_PROHIBITION.value.name}/0 : deontic_term, any;
    &show/0 : show_term, directive
}}.
"""


_DEOLINGO_RESTRICTED_THEORY = f"""
#theory deolingo_restricted {{
    deontic_term {{
        - : 4, unary;
        && : 3, binary, left;
        || : 2, binary, left;
        | : 1, binary, left
    }};
    show_term {{ / : 1, binary, left }};
    &{Deo.OBLIGATORY.value.name}/0 : deontic_term, any;
    &{Deo.FORBIDDEN.value.name}/0 : deontic_term, any;
    &{Deo.OMISSIBLE.value.name}/0 : deontic_term, any;
    &{Deo.PERMITTED.value.name}/0 : deontic_term, any;
    &{Deo.OPTIONAL.value.name}/0 : deontic_term, any;
    &{Deo.PERMITTED_BY_DEFAULT.value.name}/0 : deontic_term, head;
    &{Deo.OMISSIBLE_BY_DEFAULT.value.name}/0 : deontic_term, head;
    &{Deo.HOLDS.value.name}/0 : deontic_term, any;
    &{Deo.DEONTIC.value.name}/0 : deontic_term, any;
    &{Deo.PERMITTED_IMPLICITLY.value.name}/0 : deontic_term, body;
    &{Deo.OMISSIBLE_IMPLICITLY.value.name}/0 : deontic_term, body;
    &{Deo.VIOLATED.value.name}/0 : deontic_term, body;
    &{Deo.FULFILLED.value.name}/0 : deontic_term, body;
    &{Deo.VIOLATED_OBLIGATION.value.name}/0 : deontic_term, body;
    &{Deo.FULFILLED_OBLIGATION.value.name}/0 : deontic_term, body;
    &{Deo.NON_VIOLATED_OBLIGATION.value.name}/0 : deontic_term, body;
    &{Deo.NON_FULFILLED_OBLIGATION.value.name}/0 : deontic_term, body;
    &{Deo.UNDETERMINED_OBLIGATION.value.name}/0 : deontic_term, body;
    &{Deo.DEFAULT_OBLIGATION.value.name}/0 : deontic_term, head;
    &{Deo.VIOLATED_PROHIBITION.value.name}/0 : deontic_term, body;
    &{Deo.FULFILLED_PROHIBITION.value.name}/0 : deontic_term, body;
    &{Deo.NON_VIOLATED_PROHIBITION.value.name}/0 : deontic_term, body;
    &{Deo.NON_FULFILLED_PROHIBITION.value.name}/0 : deontic_term, body;
    &{Deo.UNDETERMINED_PROHIBITION.value.name}/0 : deontic_term, body;
    &{Deo.DEFAULT_PROHIBITION.value.name}/0 : deontic_term, head;
    &show/0 : show_term, directive
}}.
"""
