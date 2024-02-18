% C5 (Constitutive Norms)
% (i) There must be no fence (f).
&ob{-f}.
% (ii) If there is a fence, it must be a white (w) fence.
&ob{w} :- f.
% (iii) If the cottage is by the sea (s), there must be a fence.
&ob{f} :- s.
% If it is obligatory a white fence, then it is obligatory a fence.
&ob{f} :- &ob{w}.
% No white fence if not fence.
-w :- -f.
% Not forbidden a white fence if not forbidden a fence.
&fb{w} :- &fb{f}.
% There is a fence.
f.
% The fence is white.
%w.