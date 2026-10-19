# Small examples of variability mechanisms (lab #3)

The same toy program ("how often does a property hold for random x, y, z?") made to vary
in three ways:

| Files | Mechanism |
|---|---|
| `parameterized.py` | runtime parameters: a single execution loops over the values of the factors |
| `cli.py` + `bash_cli.sh` | command-line interface: the program reads the values from its arguments; a script calls it once per combination |
| `property_template.py.jinja` + `jinja_call.py` | template-based generation: Jinja2 fills the holes of a template and writes one program per combination (`pip install Jinja2`) |

Run them from this folder:

```bash
python3 parameterized.py
python3 cli.py --operation1='(x + y) + z' --operation2='x + (y + z)' --repetitions=1000
bash bash_cli.sh
python3 jinja_call.py
```

They are kept minimal on purpose: `cli.py` and `parameterized.py` evaluate the operations
with `eval()`, and `jinja_call.py` runs the generated code with `exec()` inside its own
process. Don't copy these two shortcuts into your experiments: see the lab #3 instructions.
