
from enum import Enum

from langchain_community.llms import GPT4All
from langchain_openai.llms import OpenAI
from langchain_community.llms import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
import google.generativeai as genai
import os


class Generator(str, Enum):
    GEMINI = "gemini"
    GPT4ALL = "gpt4all"
    OPENAI = "openai"
    HUGGINGFACE = "hugging"


class DeonticProgramGenerator:

    def __init__(self, generator=Generator.GPT4ALL, llm=None):
        self._generator = generator
        self._llm = llm
        self._openai_api_key = os.getenv('OPENAI_API_KEY', None)
        self._gemini_api_key = os.getenv('GEMINI_API_KEY', None)

    def generate_program(self, natural_language_text):
        if self._generator == Generator.GEMINI and self._gemini_api_key is not None:
            print("Using Gemini for generation")
            return self._generate_program_gemini(natural_language_text, model_name=self._llm)
        else:
            return self._generate_program_langchain(natural_language_text, model=self._llm, model_path=self._llm)

    def _generate_program_langchain(self, natural_language_text, model="meta-llama/CodeLlama-70b-Instruct-hf",
                                    model_path="./deolingo/models/mistral-7b-instruct-v0.1.Q4_0.gguf"):
        if self._generator == Generator.OPENAI and self._openai_api_key is not None:
            print("Using OpenAI for generation")
            llm = OpenAI(model_name="gpt-3.5-turbo-16k", temperature=0, openai_api_key=self._openai_api_key)
        elif self._generator == Generator.HUGGINGFACE:
            print("Using HuggingFaceHub for generation")
            llm = HuggingFaceEndpoint(repo_id=model, timeout=240)
        else:
            print(f"Using local GPT4All model for generation: {model_path}")
            llm = GPT4All(model=model_path)
        prompt = PromptTemplate(input_variables=["preprompt", "text"], template=_long_prompt_template)
        chain = prompt | llm
        output = chain.invoke({
            "preprompt": _pre_prompt,
            "text": natural_language_text
        })
        return output

    def _generate_program_gemini(self, natural_language_text, model_name="gemini-1.5-flash-latest"):
        genai.configure(api_key=self._gemini_api_key)
        model = genai.GenerativeModel(model_name=model_name)
        response = model.generate_content([_short_prompt_template, natural_language_text])
        return response.candidates[0].content.parts[0].text


_long_prompt_template = """
{preprompt}

Write a deontic logic program in Clingo based on the following description:
{text}
"""

_short_prompt_template = """
You are a Clingo expert and a Deontic logic expert. 
Using the following theory atoms &obligatory{{}} and &forbidden{{}}.
Write a deontic logic program in Clingo based on the following description:
{text}
"""

_pre_prompt = """
Consider this docs and examples:

Deolingo is a tool for reasoning about Deontic Logic based in Answer Set Programming.
The tool is implemented in Python and uses [Clingo](https://potassco.org/clingo) as the ASP solver.

## Examples

Simple example:
```
    % Example: It is permitted to park if there is no evidence that it is forbidden to park.
    &permitted{park} :- not &forbidden{park}.
```n

You can find examples of Deontic Equilibrium Logic programs in the [examples](deolingo/examples) directory.
See example from [example 2](deolingo/examples/preliminary/example2.lp)
```
% I must normally work (it is obligatory that I work if it is not explicitly omissible).
&obligatory{work} :- not &omissible{work}.

% On weekends, I have an explicit permission not to work.
&omissible{work} :- weekend.

% It is not a weekend.
-weekend.

% I decided not to work.
-work.
````

Output from deolingo:

```
Answer: 1
FACTS: -work, -weekend
OBLIGATIONS: &obligatory{work}
PROHIBITIONS:
SATISFIABLE
```

The output shows that the program is satisfiable and there is an answer set whose atoms mean:

- FACTS:
  - `-work`: I did not work.
  - `-weekend`: It is not a weekend.
- OBLIGATIONS:
- `&obligatory{work}`: It is obligatory that I work.
  The obligation to work is violated, although that is not checked in any rule and it is excluded from the answer set.
- PROHIBITIONS:
  - Nothing remarkable in the _world_ of prohibitions.


```

## Deontic theory atoms

Deolingo uses the following atoms to represent the deontic theory:

### Main atoms

- `&obligatory{p}`: It is **obligatory** that `p`. Equivalent to forbidden not `p`: `&forbidden{-p}`. Also known as mandatory, duty and required.
- `&forbidden{p}`: It is **forbidden** that `p`. Equivalent to obligatory not `p`: `&obligatory{-p}`. Also known as prohibited and impermissible.
- `&omissible{p}`: It is **omissible** that `p`. Equivalent to not explicitly obligatory: `-&obligatory{p}` (but this syntax is not allowed, see ["Syntax limitations"](#syntax-limitations) below).
- `&permitted{p}`: It is **permitted** (or permissible) that `p`. Equivalent to not explicitly forbidden: `-&obligatory{p}` (but this syntax is not allowed, see ["Syntax limitations"](#syntax-limitations) below).
- `&optional{p}`: It is **optional** that `p`. Equivalent to omissible and permissible. Cannot be neither obligatory nor forbidden.
- `&deontic{p}`: `p` is a **deontic** atom. It can be obligatory, forbidden, omissible, permitted or optional.

Deolingo also reifies the truth of the deontic atoms to allow general rules requiring it.
It is represented by the _holds_ theory atom `&holds{p}`, which is true if, and only if, the atom `p` is true.

### Violation and fulfillment atoms

- `&violated_obligation{p}`: The obligation of `p` is violated.
- `&violated_prohibition{p}`: The obligation of `p` is fulfilled.
- `&non_fulfilled_obligation{p}`: The obligation of `p` is not fulfilled.
- `&non_violated_obligation{p}`: The obligation of `p` is not violated.
- `&undetermined_obligation{p}`: The obligation of `p` is undetermined. It is neither violated nor fulfilled.
- `&violated_prohibition{p}`: The prohibition of `p` is violated.
- `&fulfilled_prohibition{p}`: The prohibition of `p` is fulfilled.
- `&non_fulfilled_prohibition{p}`: The prohibition of `p` is not fulfilled.
- `&non_violated_prohibition{p}`: The prohibition of `p` is not violated.
- `&undetermined_prohibition{p}`: The prohibition of `p` is undetermined. It is neither violated nor fulfilled.


### Implicit atoms and defaults

- `&default_obligation{p}`: It is obligatory by **default** that `p`.
  If there is no evidence of not `p` being permitted, it is obligatory by default that `p`.
- `&default_prohibition{p}`: It is forbidden by **default** that `p`.
  If there is no evidence of not `p` being omissible, it is forbidden by default that `p`.
- `&om_d{p}`: It is omissible by **default** that `p`.
  If there is no evidence of `p` being obligatory, it is omissible by default that `p`.
- `&permitted_by_default{p}`: It is permitted by **default** that `p`.
  If there is no evidence of `p` being forbidden, it is permitted by default that `p`.
- `&omissible_implicitly{p}`: It is omissible **implicitly** that `p`. Requires default omissibility.
  Equivalent to not obligatory (default negation): there is no evidence of obligation: `not &obligatory{p}.`
- `&permitted_implicitly{p}`: It is permitted **implicitly** that `p`. Requires default permissibility.
  Equivalent to not obligatory (default negation): there is no evidence of prohibition: `not &forbidden{p}.`.

### Clingo theory definition for Deolingo
```
#theory deolingo {
    deontic_term {
        - : 4, unary;
        && : 3, binary, left;
        || : 2, binary, left;
        | : 1, binary, left
    };
    show_term { / : 1, binary, left };
    &obligatory/0 : deontic_term, any;
    &forbidden/0 : deontic_term, any;
    &omissible/0 : deontic_term, any;
    &permitted/0 : deontic_term, any;
    &optional/0 : deontic_term, any;
    &permitted_by_default/0 : deontic_term, any;
    &omissible_by_default/0 : deontic_term, any;
    &holds/0 : deontic_term, any;
    &deontic/0 : deontic_term, any;
    &permitted_implicitly/0 : deontic_term, any;
    &omissible_implicitly/0 : deontic_term, any;
    &violated/0 : deontic_term, any;
    &fulfilled/0 : deontic_term, any;
    &violated_obligation/0 : deontic_term, any;
    &fulfilled_obligation/0 : deontic_term, any;
    &non_violated_obligation/0 : deontic_term, any;
    &non_fulfilled_obligation/0 : deontic_term, any;
    &undetermined_obligation/0 : deontic_term, any;
    &default_obligation/0 : deontic_term, any;
    &violated_prohibition/0 : deontic_term, any;
    &fulfilled_prohibition/0 : deontic_term, any;
    &non_violated_prohibition/0 : deontic_term, any;
    &non_fulfilled_prohibition/0 : deontic_term, any;
    &undetermined_prohibition/0 : deontic_term, any;
    &default_prohibition/0 : deontic_term, any;
    &show/0 : show_term, directive
}.
```

### Deontic theory atoms syntax

Currently, Deolingo supports the following constructs inside the deontic theory atoms:
- Simple terms and their explicit negations. 
  For example, `&obligatory{p}.` and `&obligatory{-p}.`.
- Variables. For example, `&obligatory{X}.` and `&obligatory{-X}.`.
- Conditional literals: `:- &obligatory{p: q}.` is equivalent to `:- &obligatory{p} : q.`.
- Sequences of simple terms and variables with conditional literals.
  For example, `&obligatory{p; X}.`, meaning `&obligatory{p}; &obligatory{X}.`.
- Disjunctions in the **head** of rules: `&obligatory{p || q}.`, which is equivalent to `&obligatory{p; q}.`.
- Conjunctions in the **body** of rules: `:- &obligatory{p && q}.`, which is equivalent to `:- &obligatory{p; q}.`.
- Deontic conditional operator (in the **head** of rules): `&obligatory{p | q}.`, 
  meaning `&obligatory{p} :- q. &obligatory{p} :- &non_violated_obligation{q}.`, as described in the DELX paper.
"""

