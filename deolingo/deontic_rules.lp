
% Deontic axiom D for DELX
:- _deolingo_obligatory(X), _deolingo_forbidden(X), not _deolingo_holds(X), not _deolingo_holds(-X).

% Deontic operator rules

% Violation
_deolingo_violated(X) :- _deolingo_violated_obligation(X).
_deolingo_violated(X) :- _deolingo_violated_prohibition(X).

% Fulfillment
_deolingo_fulfilled(X) :- _deolingo_fulfilled_obligation(X).
_deolingo_fulfilled(X) :- _deolingo_fulfilled_prohibition(X).

% Obligation/prohibition equivalence
_deolingo_obligatory(X) :- _deolingo_forbidden(-X).
_deolingo_forbidden(-X) :- _deolingo_obligatory(X).
_deolingo_forbidden(X)  :- _deolingo_obligatory(-X).
_deolingo_obligatory(-X) :- _deolingo_forbidden(X).
-_deolingo_obligatory(X) :- -_deolingo_forbidden(-X).
-_deolingo_forbidden(-X) :- -_deolingo_obligatory(X).
-_deolingo_forbidden(X)  :- -_deolingo_obligatory(-X).
-_deolingo_obligatory(-X) :- -_deolingo_forbidden(X).

% Implicit permission
_deolingo_permitted_implicitly(X) :- not _deolingo_forbidden(X), _deolingo_deontic(X).
not _deolingo_forbidden(X) :- _deolingo_permitted_implicitly(X).

% Implicit omission
_deolingo_omissible_implicitly(X) :- not _deolingo_obligatory(X), _deolingo_deontic(X).
not _deolingo_obligatory(X) :- _deolingo_omissible_implicitly(X).

% Permissible and omissible
_deolingo_omissible(X) :- -_deolingo_obligatory(X).
-_deolingo_obligatory(X) :- _deolingo_omissible(X).
_deolingo_permitted(X) :- -_deolingo_forbidden(X).
-_deolingo_forbidden(X) :- _deolingo_permitted(X).
-_deolingo_omissible(X) :- _deolingo_obligatory(X).
_deolingo_obligatory(X) :- -_deolingo_omissible(X).
-_deolingo_permitted(X) :- _deolingo_forbidden(X).
_deolingo_forbidden(X) :- -_deolingo_permitted(X).

% Optional
_deolingo_optional(X) :- _deolingo_omissible(X), _deolingo_permitted(X).
_deolingo_omissible(X) :- _deolingo_optional(X).
_deolingo_permitted(X) :- _deolingo_optional(X).

% Permitted by default
_deolingo_permitted_by_default(X) :- not not _deolingo_forbidden(X); _deolingo_deontic(X).
_deolingo_permitted_by_default(X) :- _deolingo_permitted(X); _deolingo_deontic(X).
_deolingo_permitted(X) :- not _deolingo_forbidden(X), _deolingo_permitted_by_default(X).

% Omissible by default
_deolingo_omissible_by_default(X) :- not not _deolingo_obligatory(X); _deolingo_deontic(X).
_deolingo_omissible_by_default(X) :- _deolingo_omissible(X); _deolingo_deontic(X).
_deolingo_omissible(X) :- not _deolingo_obligatory(X), _deolingo_omissible_by_default(X).

% Obligation violation
_deolingo_violated_obligation(X) :- _deolingo_obligatory(X), _deolingo_holds(-X).
_deolingo_obligatory(X) :- _deolingo_violated_obligation(X).
_deolingo_holds(-X) :- _deolingo_violated_obligation(X).

% Fulfilled obligation
_deolingo_fulfilled_obligation(X) :- _deolingo_obligatory(X), _deolingo_holds(X).
_deolingo_obligatory(X) :- _deolingo_fulfilled_obligation(X).
_deolingo_holds(X) :- _deolingo_fulfilled_obligation(X).

% Non-fulfilled obligation
_deolingo_non_fulfilled_obligation(X) :- _deolingo_obligatory(X), not _deolingo_holds(X).
_deolingo_obligatory(X) :- _deolingo_non_fulfilled_obligation(X).
not _deolingo_holds(X) :- _deolingo_non_fulfilled_obligation(X).

% Non-violated obligation
_deolingo_non_violated_obligation(X) :- _deolingo_obligatory(X), not _deolingo_holds(-X).
_deolingo_obligatory(X) :- _deolingo_non_violated_obligation(X).
not _deolingo_holds(-X) :- _deolingo_non_violated_obligation(X).

% Undetermined obligation
_deolingo_undetermined_obligation(X) :- _deolingo_obligatory(X), not _deolingo_holds(X), not _deolingo_holds(-X).
_deolingo_obligatory(X) :- _deolingo_undetermined_obligation(X).
not _deolingo_holds(X) :- _deolingo_undetermined_obligation(X).
not _deolingo_holds(-X) :- _deolingo_undetermined_obligation(X).

% Default obligation
_deolingo_default_obligation(X) :- not not _deolingo_permitted(-X); _deolingo_deontic(X).
_deolingo_default_obligation(X) :- _deolingo_obligatory(X); _deolingo_deontic(X).
_deolingo_obligatory(X) :- not _deolingo_permitted(-X), _deolingo_default_obligation(X).

% Violated prohibition
_deolingo_violated_prohibition(X) :- _deolingo_forbidden(X), _deolingo_holds(X).
_deolingo_forbidden(X) :- _deolingo_violated_prohibition(X).
_deolingo_holds(X) :- _deolingo_violated_prohibition(X).

% Fulfilled prohibition
_deolingo_fulfilled_prohibition(X) :- _deolingo_forbidden(X), _deolingo_holds(-X).
_deolingo_forbidden(X) :- _deolingo_fulfilled_prohibition(X).
_deolingo_holds(-X) :- _deolingo_fulfilled_prohibition(X).

% Non-fulfilled prohibition
_deolingo_non_fulfilled_prohibition(X) :- _deolingo_forbidden(X), not _deolingo_holds(-X).
_deolingo_forbidden(X) :- _deolingo_non_fulfilled_prohibition(X).
not _deolingo_holds(-X) :- _deolingo_non_fulfilled_prohibition(X).

% Non-violated prohibition
_deolingo_non_violated_prohibition(X) :- _deolingo_forbidden(X), not _deolingo_holds(X).
_deolingo_forbidden(X) :- _deolingo_non_violated_prohibition(X).
not _deolingo_holds(X) :- _deolingo_non_violated_prohibition(X).

% Undetermined prohibition
_deolingo_undetermined_prohibition(X) :- _deolingo_forbidden(X), not _deolingo_holds(X), not _deolingo_holds(-X).
_deolingo_forbidden(X) :- _deolingo_undetermined_prohibition(X).
not _deolingo_holds(X) :- _deolingo_undetermined_prohibition(X).
not _deolingo_holds(-X) :- _deolingo_undetermined_prohibition(X).

% Default prohibition
_deolingo_default_prohibition(X) :- not not _deolingo_permitted(X); _deolingo_deontic(X).
_deolingo_default_prohibition(X) :- _deolingo_forbidden(X); _deolingo_deontic(X).
_deolingo_forbidden(X) :- not _deolingo_permitted(X), _deolingo_default_prohibition(X).

% Deontic
_deolingo_deontic(X) :- _deolingo_obligatory(X).
_deolingo_deontic(X) :- _deolingo_obligatory(-X).
_deolingo_deontic(X) :- _deolingo_forbidden(X).
_deolingo_deontic(X) :- _deolingo_forbidden(-X).
