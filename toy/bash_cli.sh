#!/bin/bash
# Call the CLI program (cli.py) once per combination of values.
PYTHON="${PYTHON:-python3}"

run() {
    echo "Running: $PYTHON cli.py --operation1='$1' --operation2='$2' --repetitions=$3"
    "$PYTHON" cli.py --operation1="$1" --operation2="$2" --repetitions="$3"
}

run "(x + y) + z" "x + (y + z)" 1000
run "x + y"       "y + x"       500
run "(x - y) - z" "x - (y - z)" 1000
run "x * (y / z)" "(x * y) / z" 700
