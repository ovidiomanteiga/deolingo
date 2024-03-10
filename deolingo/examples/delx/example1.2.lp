% C1 (Explicit versus Negative permission)
% (i) There must be no fence (f).
&obligatory{-f}.
% (ii) If there is a fence, it must be a white (w) fence.
&obligatory{w} :- f.
% (iii) If the cottage is by the sea (s), there must be a fence.
&obligatory{f} :- s.
% If it is obligatory a white fence, then it is obligatory a fence.
&obligatory{f} :- &obligatory{w}.
% (iv) If it is permitted (explicit), I build a fence around my cottage
%f :- &permitted{f}.
% (iv) If it is permitted (implicit), I build a fence around my cottage
f :- not &forbidden{f}.
