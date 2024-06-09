
% C1 (Explicit versus Negative permission) (2nd example: Π ∪ (16))

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

%!trace_rule {"I build a fence around my cottage, if it is implicitly permitted"}
fence :- &permitted_implicitly{fence}.

%!show_trace &obligatory{X}.
%!show_trace &forbidden{X}.

%!trace {"There is a fence"} fence.
%!trace {"The cottage is by the sea"} sea.
%!trace {"There is a white fence"} white.
