
% C4 (CTD and Defeasible Obligations) ((18) ∪ (3) ∪ {s,f})

%!trace_rule {"There must be no fence, unless a permission is granted"}
&default_prohibition{fence}.

%!trace_rule {"It must be a white fence, if the prohibition of a fence is violated"}
&obligatory{white_fence} :- &violated_prohibition{fence}.

%!trace_rule {"There may be a fence, if the cottage is by the sea"}
&permitted{fence} :- sea.

%!trace_rule {"A white fence is a fence"}
fence :- white_fence.

%!trace_rule {"It is obligatory a fence, if it is obligatory a white fence"}
&obligatory{fence} :- &obligatory{white_fence}.

% The cottage is by the sea.
sea.

% There is a fence.
fence.

%!show_trace &obligatory{X}.
%!show_trace &permitted{X}.
%!show_trace &forbidden{X}.
%!show_trace &omissible{X}.

%!trace {"There is a fence"} fence.
%!trace {"The cottage is by the sea"} sea.
%!trace {"There is a white fence"} white.
%!trace {"A fence is permitted"} &permitted{fence}.
