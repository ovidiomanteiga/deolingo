
#program always.
% (B ’) If [p] and non - violated obligation of [q] uarantine then [r] eport before [n]egative
&achieve_default_obligation(n){r} :- deolingo_holds(p), &obligatory{q}, not -deolingo_holds(q).

#program initial.

&tel{
    deolingo_holds(p) ;> & true ;> deolingo_holds(r) ;> & true ;> 
    deolingo_holds(n) ;> & true
}.
