
#theory deolingo {
    deontic_term {
        - : 4, unary;
        && : 3, binary, left;
        || : 2, binary, left;
        | : 1, binary, left
    };
    show_term { / : 1, binary, left };
    &obligatory/0 : deontic_term, any;
    &forbidden/0 : deontic_term, any;
    &omissible/0 : deontic_term, any;
    &permitted/0 : deontic_term, any;
    &optional/0 : deontic_term, any;
    &permitted_by_default/0 : deontic_term, any;
    &omissible_by_default/0 : deontic_term, any;
    &holds/0 : deontic_term, any;
    &deontic/0 : deontic_term, any;
    &permitted_implicitly/0 : deontic_term, any;
    &omissible_implicitly/0 : deontic_term, any;
    &violated/0 : deontic_term, any;
    &fulfilled/0 : deontic_term, any;
    &violated_obligation/0 : deontic_term, any;
    &fulfilled_obligation/0 : deontic_term, any;
    &non_violated_obligation/0 : deontic_term, any;
    &non_fulfilled_obligation/0 : deontic_term, any;
    &undetermined_obligation/0 : deontic_term, any;
    &default_obligation/0 : deontic_term, any;
    &violated_prohibition/0 : deontic_term, any;
    &fulfilled_prohibition/0 : deontic_term, any;
    &non_violated_prohibition/0 : deontic_term, any;
    &non_fulfilled_prohibition/0 : deontic_term, any;
    &undetermined_prohibition/0 : deontic_term, any;
    &default_prohibition/0 : deontic_term, any;
    &show/0 : show_term, directive
}.
