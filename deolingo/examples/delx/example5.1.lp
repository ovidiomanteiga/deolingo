
% C5 (Constitutive Norms) (1st example: Π ∪ (19) ∪ {f})

% (i) There must be no fence (f).
&forbidden{f}.

% (ii) If there is a fence, it must be a white (w) fence.
&obligatory{w} :- f, &forbidden{f}.

% (iii) If the cottage is by the sea (s), there must be a fence.
&obligatory{f} :- s.

% A white fence is a fence.
f :- w.

% If it is obligatory a white fence, then it is obligatory a fence.
&obligatory{f} :- &obligatory{w}.

% No white fence if not fence.
-w :- -f.

% Forbidden a white fence if forbidden a fence.
&forbidden{w} :- &forbidden{f}.

% There is a fence.
f.

% The fence is white.
w.
