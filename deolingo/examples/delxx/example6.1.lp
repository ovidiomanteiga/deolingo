
% C6 (Defeasible Deontic Detachment) (1st example: Π ∪ (21) ∪ {f ∨ ¬f})

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

%!trace_rule {"We must put a street mailbox if we put a fence"}
&obligatory{mailbox} :- fence.

%!trace_rule {"We must not put a street mailbox if we do not put a fence"}
&forbidden{mailbox} :- -fence.

% Fence or not fence.
1 {fence; -fence} 1.

%!trace {"There is a fence"} fence.
%!trace {"There is no fence"} -fence.

%!show_trace &obligatory{X}.
%!show_trace &forbidden{X}.
