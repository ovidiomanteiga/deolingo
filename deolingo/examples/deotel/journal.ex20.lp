
#program always.

d :- deolingo_holds(d).
g :- deolingo_holds(g).
-d :- deolingo_holds(-d).
-g :- deolingo_holds(-g).

% (1) You should not tell the secret to [r] Reagan
&forbidden{r}. 
% (2) You should not tell the secret to [g] Gorbachev
&forbidden{g}. 
% (3) If you tell [g], you should tell [r] by a [d]eadline
&achieve_default_obligation(d){r} :- deolingo_holds(g).
% (4) If you tell [r], you should tell [g] by a [d]eadline 
&achieve_default_obligation(d){g} :- deolingo_holds(r).

#program initial . 
&tel { 
    deolingo_holds(r) ;> &true ;> &true ;> deolingo_holds(g) ;>
    &true ;> deolingo_holds(r) ;> &true
}.