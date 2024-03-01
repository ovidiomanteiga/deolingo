
# Deolingo: Deontic logic in ASP with Clingo

Deolingo is a tool for reasoning about Deontic Logic based in Answer Set Programming.
The tool is implemented in Python and uses Clingo as the ASP solver.

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
- `--outf=3`: Remove all Clingo output. Use in conjunction with `--translate` to output the translated program only.

The `deolingo` command supports most of the options of the Clingo command. 
You can use the `--help` option to see the available options.


### Library

To use Deolingo as a library, you can import the `deolingo` module and use the `deolingo.solve` function.

```python
import deolingo

program = """
    % Your Deontic Equilibrium Logic program here
    % Example: It is permitted to park if there is no evidence that it is forbidden to park.
    &pm{park} :- not &fb{park}.
"""

solutions = deolingo.solve(program)

print(solutions)
```

The `deolingo.solve` function returns a string with the output of the ASP solver.



## Examples

You can find examples of Deontic Equilibrium Logic programs in the [examples](deolingo/examples) directory.
See example from [example 2](deolingo/examples/preliminary/example2.lp)
```
% I must normally work (it is obligatory that I work if it is not explicitly omissible).
&ob{work} :- not &om{work}.

% On weekends, I have an explicit permission not to work.
&om{work} :- weekend.

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
Answer: ['ob(work)', 'ob_v(work)', 'pm_i(work)', '-om(work)', 'om_d(work)', 'ob_nf(work)', 'ob_d(work)', '-work', '-weekend']
SATISFIABLE
```

The output shows that the program is satisfiable and there is an answer set whose atoms mean:

- `ob(work)`: It is obligatory that I work.
  - `-om(work)`: It is not explicitly omissible that I work. Equivalent to `ob(work)`.
  - `ob_d(work)`: It is obligatory by default to work. Because it is obligatory to work and there is no evidence that it is omissible.
- `ob_v(work)`: I violated the obligation to work.
- `ob_nf(work)`: I did not fulfill the obligation to work.
- `-work`: I did not work.
- `-weekend`: It is not a weekend.
- `pm_i(work)`: I have an implicit permission to work. Because there is no evidence that work is forbidden.
- `om_d(work)`: It is omissible by default to work, since it is obligatory to work; but it is not omissible to work.


## Tests

The examples are also used as tests for Deolingo.
You can run all the tests using the following command in the root directory of the project

```bash
$ python -m pytest
```


## Deontic theory atoms

Deolingo uses the following atoms to represent the deontic theory:

### Main atoms

- `&ob{p}`: It is **obligatory** that `p`. Equivalent to forbidden not `p`: `&fb{-p}`. Also known as mandatory, duty and required.
- `&fb{p}`: It is **forbidden** that `p`. Equivalent to obligatory not `p`: `&ob{-p}`. Also known as prohibited and impermissible.
- `&om{p}`: It is **omissible** that `p`. Equivalent to not explicitly obligatory: `-&ob{p}` (but this syntax is not allowed, see ["Syntax limitations"](#syntax-limitations) below).
- `&pm{p}`: It is **permitted** (or permissible) that `p`. Equivalent to not explicitly forbidden: `-&ob{p}` (but this syntax is not allowed, see ["Syntax limitations"](#syntax-limitations) below).
- `&op{p}`: It is **optional** that `p`. Equivalent to omissible and permissible. Cannot be neither obligatory nor forbidden.
- `&deo{p}`: `p` is a **deontic** atom. It can be obligatory, forbidden, omissible, permitted or optional.

Deolingo also reifies the truth of the deontic atoms to allow general rules requiring it.
It is represented by the _holds_ theory atom `&h{p}`, which is true if, and only if, the atom `p` is true.

### Violation and fulfillment atoms

- `&ob_v{p}`: The obligation of `p` is violated.
- `&ob_f{p}`: The obligation of `p` is fulfilled.
- `&ob_nf{p}`: The obligation of `p` is not fulfilled.
- `&ob_nv{p}`: The obligation of `p` is not violated.
- `&ob_u{p}`: The obligation of `p` is undetermined. It is neither violated nor fulfilled.
- `&fb_v{p}`: The prohibition of `p` is violated.
- `&fb_f{p}`: The prohibition of `p` is fulfilled.
- `&fb_nf{p}`: The prohibition of `p` is not fulfilled.
- `&fb_nv{p}`: The prohibition of `p` is not violated.
- `&fb_u{p}`: The prohibition of `p` is undetermined. It is neither violated nor fulfilled.

### Implicit atoms and defaults

- `&ob_d{p}`: It is obligatory by **default** that `p`.
  If there is no evidence of not `p` being permitted, it is obligatory by default that `p`.
- `&fb_d{p}`: It is forbidden by **default** that `p`.
  If there is no evidence of not `p` being omissible, it is forbidden by default that `p`.
- `&om_d{p}`: It is omissible by **default** that `p`.
  If there is no evidence of `p` being obligatory, it is omissible by default that `p`.
- `&pm_d{p}`: It is permitted by **default** that `p`.
  If there is no evidence of `p` being forbidden, it is permitted by default that `p`.
- `&om_i{p}`: It is omissible **implicitly** that `p`. Requires default omissibility.
  Equivalent to not obligatory (default negation): there is no evidence of obligation: `not &ob{p}.`
- `&pm_i{p}`: It is permitted **implicitly** that `p`. Requires default permissibility.
  Equivalent to not obligatory (default negation): there is no evidence of prohibition: `not &fb{p}.`.


### Syntax limitations

- `-&ob{p}` explicit negation of theory atoms is not allowed by Clingo.
  Use the corresponding negative deontic atom instead, in this case `&om{p}`.
- `not &ob{p} :- conditions...` default negation of theory atoms is not allowed in the head of a rule by Clingo.
  If default negation of a theory atom is needed in the head, it can be obtained by the following constraint:
  - `:- not &ob{p}, conditions...`

Deolingo version 1 only supports simple terms in the deontic theory atoms, like atoms, their explicit negations and variables.
In future versions of Deolingo, the support for complex terms will be added as per the DELX paper;
for example: `&ob{p & q}.` meaning that it is obligatory that `p` and `q`.


## License

Deolingo is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

