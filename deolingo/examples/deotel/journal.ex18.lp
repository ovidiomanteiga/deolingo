
#program always. 
% (E) If [le] lockdown ends , cancel maintain [q]uarantine and achieve [r]eport
&cancel_maintain_default_obligation(n){q} :- deolingo_holds(le). 
&cancel_achieve_default_obligation(n){r} :- deolingo_holds(le). 

#program initial. 
&tel{
    deolingo_holds(p) ;> deolingo_holds(q) ;> deolingo_holds(p) ;> &true ;>
    deolingo_holds(le) ;> deolingo_holds(-q) ;> &true 
}.
