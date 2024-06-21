
person(1..8).

&obligatory{goes(P)} :- person(P).

&obligatory{tells(P)} :- goes(P).

&obligatory{tells(P)} :- &non_violated_obligation{goes(P)}, person(P).

&obligatory{-tells(P)} :- -goes(P), person(P).

&obligatory{-tells(P)} :- &non_violated_obligation{-goes(P)}, person(P).

{ goes(P); -goes(P) } :- person(P).

{ tells(P); -tells(P) } :- person(P).

violated_obligation(X) :- &violated_obligation{X}.
