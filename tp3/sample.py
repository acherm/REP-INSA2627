"""Sample configurations of a feature model (UVL file) into a CSV file.

    python sample.py fm/experiment.uvl --size 30 --seed 1 -o configs/sample.csv
    python sample.py fm/experiment.uvl --size 30 --seed 1 --include configs/*.csvconf -o configs/sample.csv
    python sample.py fm/experiment.uvl --pairwise -o configs/pairwise.csv        (optional)

Random sampling is uniform among the valid configurations. Same model + same seed =>
same sample: run it twice and compare.
--pairwise: instead, every pair of values of two different factors appears at least once.
--include: configurations of your own, one file each, one line `Feature,True` per selected
feature (e.g. your three programs); features not listed are not selected, parents of a
selected feature are added; each file must be a valid configuration of the model.

Output: one row per configuration. Columns: config_id, origin_of_config, then one column
per variation point of the model: a group (alternative, or, [n..m]), named after its
parent, whose value is the selected children joined by '+'; or an optional feature whose
presence no group tells (True/False).

Requires flamapy (Python >= 3.11): pip install flamapy==2.6.0
"""
import argparse
import csv
import os
import random
import subprocess
import sys
import tempfile
from pathlib import Path

# flamapy's random sampling also depends on the iteration order of Python sets, which
# changes at every run unless PYTHONHASHSEED is fixed: same --seed, different samples.
# Fix it by re-running this script with PYTHONHASHSEED=0.
if os.environ.get("PYTHONHASHSEED") != "0":
    sys.exit(subprocess.call([sys.executable, *sys.argv],
                             env={**os.environ, "PYTHONHASHSEED": "0"}))

from flamapy.interfaces.python import FLAMAFeatureModel
from flamapy.metamodels.fm_metamodel.transformations import UVLReader


def variation_points(model):
    """One column per variation point: (name, children) for a group, (name, None) for an
    optional feature whose presence no group of at least one child already tells."""
    points = []

    def visit(feature):
        for rel in feature.get_relations():
            if rel.is_group():
                points.append((feature.name, [c.name for c in rel.children]))
            elif rel.is_optional():
                child = rel.children[0]
                if not any(r.is_group() and r.card_min >= 1 for r in child.get_relations()):
                    points.append((child.name, None))
            for child in rel.children:
                visit(child)

    visit(model.root)
    names = [name for name, _ in points]       # two columns with the same name: suffix
    return [(name if names[:i].count(name) == 0 else f"{name}_{names[:i].count(name) + 1}",
             children) for i, (name, children) in enumerate(points)]


def to_row(points, selected):
    """A configuration (set of selected feature names) -> one CSV row."""
    row = {}
    for name, children in points:
        if children is None:
            row[name] = name in selected
        else:
            row[name] = "+".join(c for c in children if c in selected)
    return row


def read_csvconf(path, model):
    """Selected features of a .csvconf file, plus their ancestors."""
    selected = {line.split(",")[0].strip() for line in path.read_text().splitlines()
                if line.strip().endswith("True")}
    for name in list(selected):
        feature = model.get_feature_by_name(name)
        if feature is None:
            sys.exit(f"{path}: unknown feature {name}")
        while feature.get_parent() is not None:
            feature = feature.get_parent()
            selected.add(feature.name)
    return selected


def is_valid(fm, selected):
    """Is this selection, with every other feature deselected, a valid configuration?"""
    with tempfile.NamedTemporaryFile("w", suffix=".csvconf", delete=False) as f:
        f.write("".join(f"{name},True\n" for name in sorted(selected)))
    try:
        return fm.satisfiable_configuration(f.name, full_configuration=True)
    finally:
        os.unlink(f.name)


def main():
    p = argparse.ArgumentParser(description="Sample configurations of a UVL feature model.")
    p.add_argument("model", help="the .uvl file")
    p.add_argument("--size", type=int, default=30, help="number of random configurations")
    p.add_argument("--seed", type=int, default=1, help="seed of the random sampling")
    p.add_argument("--pairwise", action="store_true", help="pairwise sample instead of random")
    p.add_argument("--include", nargs="*", default=[], help=".csvconf files to add")
    p.add_argument("-o", "--output", default="configs/sample.csv")
    args = p.parse_args()

    fm = FLAMAFeatureModel(args.model)
    model = UVLReader(args.model).transform()
    points = variation_points(model)
    print(f"{args.model}: {fm.configurations_number()} valid configurations, "
          f"dead features: {fm.dead_features()}")

    rows = []
    for path in map(Path, args.include):
        selected = read_csvconf(path, model)
        if not is_valid(fm, selected):
            sys.exit(f"{path}: not a valid configuration of {args.model} "
                     f"(features not listed are not selected)")
        rows.append({"config_id": path.stem, "origin_of_config": "anchor",
                     **to_row(points, selected)})

    if args.pairwise:
        sample = [{n for n, v in c.elements.items() if v} for c in fm.t_wise_sampling(t=2)]
        prefix, origin = "pw", "pairwise"
    else:
        random.seed(args.seed)
        sample = [{n for n, v in c.items() if v} for c in fm.sampling(args.size)]
        prefix, origin = "r", "random"
    for i, selected in enumerate(sample, start=1):
        rows.append({"config_id": f"{prefix}{i:02d}", "origin_of_config": origin,
                     **to_row(points, selected)})

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {out}: {len(args.include)} included + {len(sample)} {origin} "
          f"= {len(rows)} configurations")


if __name__ == "__main__":
    main()
