
% C5 (Constitutive Norms) (1st example: Π ∪ (19) ∪ {f})

%!trace_rule {"There must be no fence"}
&forbidden{fence}.

%!trace_rule {"It must be a white fence, if the prohibition of a fence is violated"}
&obligatory{white_fence} :- &violated_prohibition{fence}.

%!trace_rule {"There must be a fence, if the cottage is by the sea"}
&obligatory{fence} :- sea.

%!trace_rule {"A white fence is a fence"}
fence :- white_fence.

%!trace_rule {"It is obligatory a fence, if it is obligatory a white fence"}
&obligatory{fence} :- &obligatory{white_fence}.

%!trace_rule {"No white fence if no fence"}
-white_fence :- -fence.

%!trace_rule {"A white fence is forbidden if a fence also is"}
&forbidden{white_fence} :- &forbidden{fence}.

% There is a fence.
fence.

% The fence is white.
white_fence.

%!show_trace &obligatory{X}.
%!show_trace &permitted{X}.
%!show_trace &forbidden{X}.
%!show_trace &omissible{X}.

%!trace {"There is a fence"} fence.
%!trace {"The cottage is by the sea"} sea.
%!trace {"There is a white fence"} white.
