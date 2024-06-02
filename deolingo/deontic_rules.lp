
% Deontic weak axiom D for DELX
:- deolingo_obligatory(X), deolingo_forbidden(X), not deolingo_holds(X), not deolingo_holds(-X).

% Violation
deolingo_violated(X) :- deolingo_violated_obligation(X).
deolingo_violated(X) :- deolingo_violated_prohibition(X).

% Fulfillment
deolingo_fulfilled(X) :- deolingo_fulfilled_obligation(X).
deolingo_fulfilled(X) :- deolingo_fulfilled_prohibition(X).

% Obligation/prohibition equivalence
deolingo_obligatory(X) :- deolingo_forbidden(-X).
deolingo_forbidden(X)  :- deolingo_obligatory(-X).
-deolingo_obligatory(X) :- -deolingo_forbidden(-X).
-deolingo_forbidden(X)  :- -deolingo_obligatory(-X).

% Implicit permission
deolingo_permitted_implicitly(X) :- not deolingo_forbidden(X), deolingo_deontic(X).
not deolingo_forbidden(X) :- deolingo_permitted_implicitly(X).

% Implicit omission
deolingo_omissible_implicitly(X) :- not deolingo_obligatory(X), deolingo_deontic(X).
not deolingo_obligatory(X) :- deolingo_omissible_implicitly(X).

% Permissible and omissible
deolingo_omissible(X) :- -deolingo_obligatory(X).
-deolingo_obligatory(X) :- deolingo_omissible(X).
deolingo_permitted(X) :- -deolingo_forbidden(X).
-deolingo_forbidden(X) :- deolingo_permitted(X).
-deolingo_omissible(X) :- deolingo_obligatory(X).
deolingo_obligatory(X) :- -deolingo_omissible(X).
-deolingo_permitted(X) :- deolingo_forbidden(X).
deolingo_forbidden(X) :- -deolingo_permitted(X).

% Optional
deolingo_optional(X) :- deolingo_omissible(X), deolingo_permitted(X).
deolingo_omissible(X) :- deolingo_optional(X).
deolingo_permitted(X) :- deolingo_optional(X).

% Permitted by default
deolingo_permitted_by_default(X) :- not not deolingo_forbidden(X); deolingo_deontic(X).
deolingo_permitted_by_default(X) :- deolingo_permitted(X); deolingo_deontic(X).
deolingo_permitted(X) :- not deolingo_forbidden(X), deolingo_permitted_by_default(X).

% Omissible by default
deolingo_omissible_by_default(X) :- not not deolingo_obligatory(X); deolingo_deontic(X).
deolingo_omissible_by_default(X) :- deolingo_omissible(X); deolingo_deontic(X).
deolingo_omissible(X) :- not deolingo_obligatory(X), deolingo_omissible_by_default(X).

% Obligation violation
deolingo_violated_obligation(X) :- deolingo_obligatory(X), deolingo_holds(-X).
deolingo_obligatory(X) :- deolingo_violated_obligation(X).
deolingo_holds(-X) :- deolingo_violated_obligation(X).

% Fulfilled obligation
deolingo_fulfilled_obligation(X) :- deolingo_obligatory(X), deolingo_holds(X).
deolingo_obligatory(X) :- deolingo_fulfilled_obligation(X).
deolingo_holds(X) :- deolingo_fulfilled_obligation(X).

% Non-fulfilled obligation
deolingo_non_fulfilled_obligation(X) :- deolingo_obligatory(X), not deolingo_holds(X).
deolingo_obligatory(X) :- deolingo_non_fulfilled_obligation(X).
not deolingo_holds(X) :- deolingo_non_fulfilled_obligation(X).

% Non-violated obligation
deolingo_non_violated_obligation(X) :- deolingo_obligatory(X), not deolingo_holds(-X).
deolingo_obligatory(X) :- deolingo_non_violated_obligation(X).
not deolingo_holds(-X) :- deolingo_non_violated_obligation(X).

% Undetermined obligation
deolingo_undetermined_obligation(X) :- deolingo_obligatory(X), not deolingo_holds(X), not deolingo_holds(-X).
deolingo_obligatory(X) :- deolingo_undetermined_obligation(X).
not deolingo_holds(X) :- deolingo_undetermined_obligation(X).
not deolingo_holds(-X) :- deolingo_undetermined_obligation(X).

% Default obligation
deolingo_default_obligation(X) :- not not deolingo_permitted(-X); deolingo_deontic(X).
deolingo_default_obligation(X) :- deolingo_obligatory(X); deolingo_deontic(X).
deolingo_obligatory(X) :- not deolingo_permitted(-X), deolingo_default_obligation(X).

% Violated prohibition
deolingo_violated_prohibition(X) :- deolingo_forbidden(X), deolingo_holds(X).
deolingo_forbidden(X) :- deolingo_violated_prohibition(X).
deolingo_holds(X) :- deolingo_violated_prohibition(X).

% Fulfilled prohibition
deolingo_fulfilled_prohibition(X) :- deolingo_forbidden(X), deolingo_holds(-X).
deolingo_forbidden(X) :- deolingo_fulfilled_prohibition(X).
deolingo_holds(-X) :- deolingo_fulfilled_prohibition(X).

% Non-fulfilled prohibition
deolingo_non_fulfilled_prohibition(X) :- deolingo_forbidden(X), not deolingo_holds(-X).
deolingo_forbidden(X) :- deolingo_non_fulfilled_prohibition(X).
not deolingo_holds(-X) :- deolingo_non_fulfilled_prohibition(X).

% Non-violated prohibition
deolingo_non_violated_prohibition(X) :- deolingo_forbidden(X), not deolingo_holds(X).
deolingo_forbidden(X) :- deolingo_non_violated_prohibition(X).
not deolingo_holds(X) :- deolingo_non_violated_prohibition(X).

% Undetermined prohibition
deolingo_undetermined_prohibition(X) :- deolingo_forbidden(X), not deolingo_holds(X), not deolingo_holds(-X).
deolingo_forbidden(X) :- deolingo_undetermined_prohibition(X).
not deolingo_holds(X) :- deolingo_undetermined_prohibition(X).
not deolingo_holds(-X) :- deolingo_undetermined_prohibition(X).

% Default prohibition
deolingo_default_prohibition(X) :- not not deolingo_permitted(X); deolingo_deontic(X).
deolingo_default_prohibition(X) :- deolingo_forbidden(X); deolingo_deontic(X).
deolingo_forbidden(X) :- not deolingo_permitted(X), deolingo_default_prohibition(X).

% Deontic
deolingo_deontic(X) :- deolingo_obligatory(X).
deolingo_deontic(X) :- deolingo_forbidden(X).
