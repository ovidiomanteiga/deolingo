% Contrary to Duty (CTD)
% I must not walk in the street
% If I walk in the street, I must walk on the right side of the street
&forbidden{walk}.
&obligatory{walk_right} :- walk.
walk :- walk_right.
&obligatory{walk} :- &obligatory{walk_right}.
walk.
walk_right.