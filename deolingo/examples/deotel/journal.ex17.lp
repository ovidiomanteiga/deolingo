
#program always.
% (D) if violated oblig. to [q]uarantine , pay a [f]ine before end of [m]onth
&achieve_default_obligation(m){f} :- &forbidden{r}, deolingo_holds(r).

#program initial. 
&tel{
    deolingo_holds(q) ;> &true ;> deolingo_holds(p) ;> &true ;> 
    deolingo_holds(n) & deolingo_holds(-q) & deolingo_holds(r) ;> &true ;> deolingo_holds(m) 
}.
