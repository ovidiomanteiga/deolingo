
% Contrary to Duty (CTD)
% I must not walk in the street
% If I walk in the street, I must walk on the right side of the street

&forbidden{walk}.
&obligatory{walk_right} :- walk.
walk :- walk_right.
&obligatory{walk} :- &obligatory{walk_right}.
walk.
walk_right.

%!trace {"% is forbidden",X} &forbidden{X}.
%!trace {"% is obligatory",X} &obligatory{X}.
%!show_trace walk.
%!show_trace walk_right.
%!show_trace &forbidden{X}.
%!show_trace &obligatory{X}.
