
#program always.

fluent(q). % inertial fluents: [q]uarantine
% (A) If [p]ositive then maintain [q]uarantine until [n]egative
&maintain_default_obligation(n){q} :- deolingo_holds(p).
% (B) If [p]ositive and [q]uarantine then [r]eport before [n]egative
&achieve_default_obligation(n){r} :- deolingo_holds(p), deolingo_holds(q).
% (C) if violated oblig. of [q]uarantine then forbid [r]eport
&forbidden{r} :- &violated_obligation{q}.

deolingo_holds(-P) :- -deolingo_holds(P).
-deolingo_holds(P) :- deolingo_holds(-P).
p :- deolingo_holds(p).
q :- deolingo_holds(q).
r :- deolingo_holds(r).
n :- deolingo_holds(n).
le :- deolingo_holds(le).
-p :- deolingo_holds(-p).
-q :- deolingo_holds(-q).
-r :- deolingo_holds(-r).
-n :- deolingo_holds(-n).
-le :- deolingo_holds(-le).


#program dynamic.
% Inertia for fluents
deolingo_holds(F) :- fluent(F), 'deolingo_holds(F), not -deolingo_holds(F).
-deolingo_holds(F) :- fluent(F), -'deolingo_holds(F), not deolingo_holds(F).
