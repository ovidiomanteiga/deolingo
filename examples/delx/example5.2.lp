% C5 (Constitutive Norms) (2nd example)
% (i) There must be no fence (f).
&ob{-f}.
% (ii) If there is a fence, it must be a white (w) fence.
&ob{w} :- f.
% If white fence, then fence.
f :- w.
% No white fence if not fence.
-w :- -f.
% Obligatory fence if non violated white fence.
&ob{f} :- &ob{w}, not -w.
% Forbidden white if non violated fence.
&fb{w} :- &fb{f}, not f.
% There is a fence.
f.