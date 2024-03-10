% C5 (Constitutive Norms)
% (i) There must be no fence (f).
&obligatory{-f}.
% (ii) If there is a fence, it must be a white (w) fence.
&obligatory{w} :- f.
% (iii) If the cottage is by the sea (s), there must be a fence.
&obligatory{f} :- s.
% If it is obligatory a white fence, then it is obligatory a fence.
&obligatory{f} :- &obligatory{w}.
% No white fence if not fence.
-w :- -f.
% Not forbidden a white fence if not forbidden a fence.
&forbidden{w} :- &forbidden{f}.
% There is a fence.
f.
% The fence is white.
%w.