
%!trace_rule {"It ought to be that Jones goes to assist his neighbors."}
&obligatory{jones_goes}.

%!trace_rule {"It ought to be that if Jones goes, then he tells them he is coming."}
&obligatory{jones_tells} :- jones_goes.

%!trace_rule {"It ought to be that if Jones must go and there is no evidence that he is not coming, then he tells them he is coming."}
&obligatory{jones_tells} :- &non_violated_obligation{jones_goes}.

%!trace_rule {"If Jones does not go, then he ought not tell them he is coming."}
&obligatory{-jones_tells} :- -jones_goes.

%!trace_rule {"If Jones must not go and there is no evidence he is coming, then he ought not tell them he is coming."}
&obligatory{-jones_tells} :- &non_violated_obligation{-jones_goes}.

% Either Jones goes or he doesn’t.
{ jones_goes; -jones_goes }.

% Either Jones tells or he doesn’t.
{ jones_tells; -jones_tells }.

violated_obligation(X) :- &violated_obligation{X}.

%!trace {"The obligation of % was violated.", X} &violated_obligation{X}.
%!trace {"Jones goes."} jones_goes.
%!trace {"Jones does not go."} -jones_goes.
%!trace {"Jones tells he is coming."} jones_tells.
%!trace {"Jones does not tell he is coming."} -jones_tells.

%!show_trace &violated_obligation{X}.
%!show_trace &obligatory{X}.
