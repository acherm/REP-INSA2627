# Lab session #3 — Replicability and Variability (REP 2026-2027)

Same pair, same GitHub repository as in labs #1 and #2. 
Finish lab #2 before starting this lab session (the Nix part is not "mandatory" though).
AI is allowed: declare the usage in your README (tool, model,
what for, what you checked) throughout your experiments.

There is not necessarily a consensus across groups' answers to "how often does
`(x+y)+z == x+(y+z)` hold?". 
And beyond associativity, we are interested by other mathematical property.
Moreover, why some factors have such an effect is unclear.
Let's investigate why, systematically.

## Part 1 — Three programs, one list of variability factors

* **List all possible factors that can have an effect on the computed answer** (we have already done that informally on the whiteboard), starting
  from your program (lab #1, in language L1), the one an LLM generated in lab #2 (in
  language L2), and the programs of your colleagues:
  * revisit what you have done, each decision and detail that may or may not have an effect on the result
  * be inspired by what LLMs have implemented: if an LLM's solution differs from yours, it is
    certainly due to some variability...
  * be creative ;)

  A **comparison matrix** helps: one row per program, one column per factor, and in each
  cell the choice the program makes. For example, starting with the number of repetitions:

  | Program | repetitions | … | result |
  |---|---|---|---|
  | yours, in L1 (lab #1) | 1,000 or 10,000 | | 92 |
  | LLM, in L2 (lab #2) | 1,000,000 | | 42 |
  | LLM, in L1 (new) | 10,000 | | 13 |

note that for a given program, many possible values can be tried out of a variability factor (e.g., for repetitions, you have tried with 1,000 but perhaps with other values as well...). Hence, in a cell documenting a variability factor, we can document a range of possible values 

* Ask an LLM again to generate a program quantifying how often the associativity holds,
  this time in L1, the language of your original program (keep the prompt, the model and
  the answer). You now have **three programs**. Add the third one to the matrix and update
  the list of factors. What can it tell you that the first two cannot?

The list is never finished: update it every time this lab reveals a new factor.

## Part 2 — One factor, one branch: the property checked

Associativity of `+` is one property among others: associativity of `*`, distributivity
(`x * (y + z) == x * y + x * z`), `x * (1 / x) == 1`…

**Create a git branch that produces a variation of your code checking another mathematical property than associativity.
Using GitHub Actions, show that the answer is indeed different.** Add the property to your
list of variability factors. The rest of the lab investigates it systematically, with the others!

## Part 3 — Exploring all factors? Variability mechanisms

A limitation of prior experiments (one branch per variability factor) is that:

* we certainly consider a subset of factors (not all) since it's manual and time-consuming;
* we study only one factor at a time (not the combination of factors).

We will write a procedure to automatically explore all variability factors and their
combinations, on the three programs. And yes, we will write a program that generates
other programs. There are several ways to make a program vary: try each of the four below,
on one piece of variability. Small examples in Python:
https://github.com/acherm/REP-INSA2627/tree/main/toy

### 3.1 Runtime parameters

The factor is a variable of the program, and a loop over its values explores every
combination within a single execution (`parameterized.py`).

*Exercise*: in one execution of your program, try different numbers of repetitions, from
100 to 1,000,000. What happens to the answer?

### 3.2 Command-line interface (CLI)

The program reads the values of the factors from its arguments when it starts, and prints
its answer together with the values it actually used (`cli.py`). In Python, with
`argparse`:

```python
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--repetitions", type=int, default=1000)
args = parser.parse_args()
percentage = check_property(args.repetitions)
print(json.dumps({"repetitions": args.repetitions, "percentage": percentage}))
```

```bash
$ python assoc.py --repetitions=10000
{"repetitions": 10000, "percentage": 82.33}
```

In C, loop over `argv`: `sscanf(argv[i], "--repetitions=%d", &repetitions);` (Java:
`args`, JavaScript: `process.argv`, or a library). Then a script calls the programs once
per combination of values, in bash (`bash_cli.sh`):

```bash
for r in 100 1000 10000; do
  python assoc.py --repetitions=$r
  ./assoc --repetitions=$r        # same arguments for a compiled program
done
```

or in Python, which also reads the answers back:

```python
import json, subprocess, sys

out = subprocess.run([sys.executable, "assoc.py", "--repetitions=1000"],
                     capture_output=True, text=True).stdout
answer = json.loads(out)          # {"repetitions": 1000, "percentage": ...}
```

*Exercise*: make the generation of random numbers configurable from the command line,
with the same arguments for your three programs, and write a script that calls them on
combinations of values. Same arguments, same answer?

### 3.3 Template-based generation

The code becomes a template with holes `{{ … }}`; a generator fills the holes with the
values of the factors and writes one program per combination
(`property_template.py.jinja`, `jinja_call.py`). With Jinja2 (`pip install Jinja2`), a
template `assoc.py.jinja`:

```python
import random

def check_property(repetitions):
    holds = 0
    for _ in range(repetitions):
        x, y, z = random.random(), random.random(), random.random()
        if {{ lhs }} == {{ rhs }}:
            holds += 1
    return 100 * holds / repetitions

print(check_property({{ repetitions }}))
```

and the generator `generate.py`, which writes each variant, then runs it:

```python
import subprocess
import sys
from pathlib import Path
from jinja2 import Template

template = Template(Path("assoc.py.jinja").read_text())
properties = {"assoc_add": ("(x + y) + z", "x + (y + z)"),
              "assoc_mul": ("(x * y) * z", "x * (y * z)")}
Path("generated").mkdir(exist_ok=True)
for name, (lhs, rhs) in properties.items():
    path = Path(f"generated/{name}.py")
    path.write_text(template.render(lhs=lhs, rhs=rhs, repetitions=10000))
    result = subprocess.run([sys.executable, path], capture_output=True, text=True)
    print(name, result.stdout.strip())
```

A hole can hold any piece of code: an expression, a type (`{{ type }} x, y, z;` in C), an
import… For a compiled language, compile each generated file before running it
(`gcc -O2 -o generated/assoc_add generated/assoc_add.c`). Run each variant in its own
process, as above, not with `exec()` as `jinja_call.py` does. In Python, `float` is a
double; single precision is `numpy.float32`.

*Exercise*: investigate the property systematically: write a template of your program in
which the property checked (Part 2) and the type of the numbers (float vs double) are
holes; generate all the variants and run them.

### 3.4 The computing environment

The program does not change; the interpreter, the compiler, the libraries or the operating
system around it do. Two ways, seen in lab #2. A build argument in a Dockerfile:

```dockerfile
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim
COPY assoc.py .
CMD ["python", "assoc.py"]
```

```bash
docker build --build-arg PYTHON_VERSION=3.10 -t assoc:3.10 . && docker run --rm assoc:3.10
```

(for C: `FROM gcc:${GCC_VERSION}`). Or a matrix of GitHub Actions jobs, one job per value:

```yaml
jobs:
  run:
    runs-on: ubuntu-24.04
    strategy:
      matrix:
        python-version: ["3.10", "3.14"]
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: ${{ matrix.python-version }}
      - run: python assoc.py
```

*Exercise*: run your programs with two versions of their interpreter or compiler, or in
any other variation of the computing environment you can think of. Same answer?

### 3.5 Comparison of approaches

Here is an informal comparison of approaches:

| | CLI | Template | Runtime parameters | Computing environment |
|---|---|---|---|---|
| Execution | Run with arguments from the command line | Generate new code and run it | Single execution explores multiple combinations | Build or pick an environment, run the program in it |
| Code flexibility | Fixed code, dynamic behavior via arguments | Code generation based on templates (at compile time) | Fixed code, dynamic behavior via input combinations | Fixed code, the environment around it changes |
| Complexity | Simple to implement, but may require additional scripting for multiple runs | More complex due to code generation | Medium complexity, automated exploration | Dockerfile or workflow; one build or job per environment |
| Use case | When multiple runs with different inputs are needed | When code structure needs to change with each variation | When exploring multiple input combinations in a single run | When the factor is outside the program |
| Need for additional scripting | Often requires a separate script to automate multiple configurations | No need for additional scripting, automation built into code generation | No need for additional scripts, explores all combinations automatically | Build arguments, or a matrix of jobs |
| Examples of use | Quickly testing different inputs at runtime | Automatically generating versions of a program | Systematically testing multiple combinations without user intervention | Same program, several interpreter or compiler versions |
| Pros | Easy to use, no code regeneration | Flexible for generating different structures | Automates exploration, no repeated runs needed | Reaches what no in-code mechanism can |
| Cons | Requires additional scripting for automated multiple runs | Complexity of managing templates and generated files | Requires careful design for large-scale factor combinations | Slow and costly: images, CI minutes |

All have pros and cons. For the rest of the work, choose, for each factor of your list,
the mechanism that varies it.

## Part 4 — Modelling variability factors

Whatever the mechanism, there is a need to:

* model the possible values of variability factors;
* explore all combinations of factors; if it's too much, use a sampling (i.e. a subset);
* store results in a tabular format, e.g. a CSV file (columns = variability factors + answer).

**Properly list and document all variability factors, including possible values and
constraints across variability factors, as a feature model.** Write it in UVL Studio,
https://blog.mathieuacher.com/uvl-studio/ (in the browser, nothing to install): the example
*Sandwich (start here)* and the *UVL cheat sheet* tab show the notation, and the slides
https://github.com/acherm/REP-INSA2627/blob/main/feature-models-uvl/slides.pdf sum up its
syntax and semantics. Then:

* how many configurations? Count by hand, then compare with the *Analysis* tab;
* express your three programs, as they were, as configurations of the model
  (*Configurator* tab); if one cannot be expressed, the model is incomplete;
* save the model (*Save .uvl*) in your repository.

## Part 5 — Sampling

**You cannot run every configuration: produce a random sample of them, reproducibly.**
Sampling produces data, so it is a script, versioned and run by GitHub Actions, never a
notebook cell. Use `sample.py`
(https://github.com/acherm/REP-INSA2627/blob/main/tp3/sample.py; Python ≥ 3.11 and
`pip install flamapy==2.6.0`):

```bash
python sample.py fm/experiment.uvl --size 30 --seed 1 --include configs/*.csvconf -o configs/sample.csv
```

It writes one row per configuration, one column per factor. `--include` adds
configurations of your own, such as your three programs (one file each, one line
`Feature,True` per selected feature). Choose the size of the sample and justify it. Same
command, same sample: check it. (Optional: `--pairwise`, compared with a random sample of
the same size.)

## Part 6 — Serializing results

**Write a script that derives the variant of each row of the sample, runs it, and stores
its result in a CSV file: one row per run, columns = variability factors + answer.**
Deriving a variant combines your mechanisms: pick the program, fill the template, compile
if needed, call it with the right arguments, in the right environment. The answer is
random: run every configuration several times. Each row must hold what is needed to re-run
it, and to know where it ran.

## Part 7 — GitHub Actions

Write a GitHub Actions workflow that produces the results automatically: it samples,
derives and runs the variants, and stores the CSV in the repository. Its matrix of jobs
covers the factors of the computing environment (3.4), e.g. language versions, or CPU
architectures with the runners `ubuntu-24.04` and `ubuntu-24.04-arm`. Re-run the workflow
on the same commit: same results?

## Part 8 — Analyzing results

Using the CSV file of the results:

* describe to what extent variability factors impact the result and answer;
* recommend values of variability factors to have a stable result;
* explain the answers you and the LLM got in labs #1 and #2;
* correlation is not causation: which of the effects you found can you explain
  *causally*? What would you have to run to show it? Run it.

Hint: apply interpretable machine learning (e.g. a decision tree) to systematize the
analysis.

Write the text and conclusions in a Jupyter notebook (https://jupyter.org), which reads
the CSV and never produces data. Install: `pip install jupyterlab pandas matplotlib
scikit-learn`, then `jupyter lab` (it opens in your browser); or open the `.ipynb` file in
VS Code (Jupyter extension) and select, as kernel, the Python where you installed them.
Before each commit: *Restart Kernel and Run All Cells*.

## Lab report

Your GitHub repository, containing:

* the code to run all the experiments (programs, templates, scripts, Dockerfiles, GitHub
  Actions);
* the feature model (`.uvl`), the sample, and the CSV of results produced by GitHub Actions;
* a Jupyter notebook detailing the experiments (comparison matrix, variability factors,
  analysis of results, recommendations) and answering the questions;
* a README.md explaining the architecture of the repository, how to reproduce the results,
  and the AI usage statement.
