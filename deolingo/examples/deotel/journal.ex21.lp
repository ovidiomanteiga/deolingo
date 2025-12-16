


#program always .

w :- deolingo_holds(w).
-w :- deolingo_holds(-w).
s :- deolingo_holds(s).
-s :- deolingo_holds(-s).

fluent(s).
% (G .1) If disaster [w] arning , must arrive at [s] helter before disaster [h] its
&achieve_default_obligation(h){s} :- deolingo_holds(w).
% (G .2) If disaster [w] arning , must stay at [s] helter until no disaster [-h]
&maintain_default_obligation(-h){s} :- deolingo_holds(w).
% (H) [q] arantine and [s] helter are not compatible
deolingo_holds(-q) :- deolingo_holds(s). % Being at shelter implies not in quarantine
deolingo_holds(-s) :- deolingo_holds(q). % Being in quarantine implies not at shelter
&forbidden{q} :- &obligatory{s}. % Obligation of [s] implies prohibition of [q]
&forbidden{s} :- &obligatory{q}. % Obligation of [q] implies prohibition of [s]
% (I) cancel maintaining [q] when the disaster [h]its and we must be at [s]
&cancel_maintain_default_obligation(n){q} :- deolingo_holds(h), &obligatory{s}.

#program initial .
&tel{
    deolingo_holds(p) ;> deolingo_holds(q) ;> & true ;> deolingo_holds(w) ;> deolingo_holds(s)
    ;> deolingo_holds(h) ;> & true ;> deolingo_holds(-h) ;> & true
}.
