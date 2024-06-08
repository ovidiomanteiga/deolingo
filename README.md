
# Deolingo: Deontic logic in ASP with Clingo

Deolingo is a tool for reasoning about Deontic Logic based in Answer Set Programming.
The tool is implemented in Python and uses [Clingo](https://potassco.org/clingo) as the ASP solver.

Deolingo implements the theoretical foundation described in the paper 
[_"Deontic Equilibrium Logic with eXplicit negation"_](https://www.dc.fi.udc.es/~cabalar/DELX.pdf) 
by Pedro Cabalar, Agata Ciabatonni and Leendert van der Torre.

DELX extends Equilibrium Logic for normative reasoning. 
In contrast to modal approaches, DELX utilizes a normal form that restricts deontic
operators solely to atoms. The cited paper establishes that any theories in DELX can be reduced to ASP.

## Installation

To install Deolingo, you need to have Python 3.6 or later installed in your system.

You can install Deolingo using pip:

```bash
pip install git+https://github.com/ovidiomanteiga/deolingo.git@main
```

You might as well give Deolingo a try in the [Deolingo web page](https://deolingo.azurewebsites.net/),
which features a fancy web editor using the [Monaco editor](https://github.com/microsoft/monaco-editor).


## Usage

You can use Deolingo as a library in your Python code or as a command line tool.

### Command line tool

To use Deolingo as a command line tool, you can use the `deolingo` command.

```bash
$ deolingo [OPTIONS] FILES...
```

Where `FILES` are paths to the file containing the Deontic Equilibrium Logic programs.

The following options are available:

- `-h, --help`: Show this message and exit.
- `-v, --version`: Show the version and exit.
- `--translate`: Prints the translated deontic logic program to the standard output.
- `--ungrouped`: Prints the answer sets ungrouped
  (by default they are grouped by world: facts, obligations, prohibitions).
- `--explain`: Explain the resulting answer sets using [Xclingo](https://github.com/bramucas/xclingo2).
- `--benchmark`: Run multiple configured solver instances against all the examples and prints the stats.
- `--generate`: Generates a deontic logic program from the given input text in natural language using an LLM.
  - `--generator=gemini|gpt4all|openai|huggingfacehub`: In conjunction with the `--generate` option, 
    indicates the LLM provider.
- `--optimize`: Runs the solver with the optimization mode, which reduces grounding (CPU and memory footprint). 
  See details below.
- `--temporal`: Runs the deontic logic program with temporal reasoning using [Telingo](https://github.com/potassco/telingo).

The `deolingo` command supports most of the options of the Clingo command-line app. 
You can use the `--help` option to see the available options. See also Clingo documentation for more information on:
- https://github.com/potassco/clingo
- https://potassco.org/clingo


### Library

To use Deolingo as a library, you can import the `deolingo` module and use the `DeolingoSolver` class.
A DeolingoControl class is also provided to control the solver and the grounding process, 
which subclasses the [`clingo.Control` class](https://potassco.org/clingo/python-api/5.7/clingo/control.html),
providing the same interface.

```python
import deolingo

program = """
    % Your Deontic Equilibrium Logic program here
    % Example: It is permitted to park if there is no evidence that it is forbidden to park.
    &permitted{park} :- not &forbidden{park}.
"""

solutions = DeolingoSolver().solve(program, all_models=True, grouped=True)

print(solutions)
```

The `DeolingoSolver.solve` method returns a list of all the deontic answer sets as the output of the deontic ASP solver.



## Examples

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

```bash
$ deolingo deolingo/examples/preliminary/example1.lp
```

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


## Tests

The examples are also used as tests for Deolingo.
You can run all the tests using the following command in the root directory of the project.

```bash
$ python -m pytest
// OR SIMPLY
$ pytest
```

That command also runs all the unit tests in the `tests` directory.


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

### Restricted Deolingo theory definition

When running Deolingo in optimized mode, the following theory definition is used to restrict
the usage of some deontic theory atoms to either heads or bodies:

```
#theory deolingo_restricted {
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
    &permitted_by_default/0 : deontic_term, head;
    &omissible_by_default/0 : deontic_term, head;
    &holds/0 : deontic_term, any;
    &deontic/0 : deontic_term, any;
    &permitted_implicitly/0 : deontic_term, body;
    &omissible_implicitly/0 : deontic_term, body;
    &violated/0 : deontic_term, body;
    &fulfilled/0 : deontic_term, body;
    &violated_obligation/0 : deontic_term, body;
    &fulfilled_obligation/0 : deontic_term, body;
    &non_violated_obligation/0 : deontic_term, body;
    &non_fulfilled_obligation/0 : deontic_term, body;
    &undetermined_obligation/0 : deontic_term, body;
    &default_obligation/0 : deontic_term, head;
    &violated_prohibition/0 : deontic_term, body;
    &fulfilled_prohibition/0 : deontic_term, body;
    &non_violated_prohibition/0 : deontic_term, body;
    &non_fulfilled_prohibition/0 : deontic_term, body;
    &undetermined_prohibition/0 : deontic_term, body;
    &default_prohibition/0 : deontic_term, head;
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


### Syntax limitations

- `-&obligatory{p}` explicit negation of theory atoms is not allowed by Clingo syntax.
  Use the corresponding negative deontic atom instead, in this case `&omissible{p}`.
  And `&permitted{p}` is equivalent to `-&forbidden{p}`.
- `not &obligatory{p} :- conditions...` default negation of theory atoms is not allowed in the head of a rule by Clingo.
  Instead, the same result can be obtained by the following constraint:
  - `:- not not &obligatory{p}, conditions...`
- `&obligatory{p && q}.` conjunction operator is not allowed in the head of a rule.
  Use the corresponding deontic atom instead in two rules, in this case `&obligatory{p}. &obligatory{q}.`.
- `:- &obligatory{p || q}.` disjunction operator is not allowed in the body of a rule.
  Use the corresponding deontic atoms instead in two rules, in this case `:- &obligatory{p}. :- &obligatory{q}.`.
- `&obligatory{not p}.` default negation of theory atoms is not allowed.
  If this expression is needed, use the equivalences described in the DELX paper:
  - `&obligatory{not p}` is equivalent to `not &obligatory{p}`.
  - `&forbidden{not p}` is equivalent to `not not &permitted{p}`.
- `&obligatory{&obligatory{p}}` nested deontic atoms are not allowed by Clingo syntax.
  The deontic atoms are restricted to simple terms, variables, conditionals or sequences.
  If this expression is needed, use the equivalences described in the DELX paper:
  - `&obligatory{&obligatory{p}}` is equivalent to `&obligatory{p}`.
  - `&obligatory{&forbidden{p}}` is equivalent to `&forbidden{p}`.
  - `&forbidden{&obligatory{p}}` is equivalent to `&omissible{p}`.
  - `&forbidden{&forbidden{p}}` is equivalent to `&permitted{p}`.



## License

Deolingo is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
