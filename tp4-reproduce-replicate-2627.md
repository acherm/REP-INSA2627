# Lab session #4: Towards reproducing and replicating results (REP 2026-2027)

You have chosen one paper (see the [README](README.md)). The goal now is to:

1. **reproduce** some results of the original paper
2. **define a protocol** for a variation of the original study (replication): what to vary
   and how, the hypothesis, and the expected results. **The protocol will be validated in the upcoming
   weeks.**

## (Step 1) Read and analyze the paper

Understand the context, domain and scope first: read the abstract, introduction and conclusion to
get the objectives, hypotheses, methods and key findings. Review the related work the
authors cite... If references seem/are missing, search for them (e.g. Google Scholar,
https://scholar.google.fr/) with the key terms of the paper.

**Questions to check your understanding** (they help you verify that you "get" the
paper; they are not an exam: answer them briefly, in your own words):

* What is the main research question or hypothesis? Why is it significant in its field?
* Which gap in existing knowledge does it address? Which prior work does it build upon or
  differ from?
* What are the primary objectives? Are there secondary or exploratory questions?

## (Step 2) Identify what reproducibility and replicability require

* **Data**: are the datasets available and accessible? It includes pre-processing steps,
  transformations and selection criteria.
* **Methods and code**: experimental setup, algorithms, statistical analyses, software
  versions, linked code repositories, dependencies and environment requirements...
* **Results and metrics**: how results are measured and reported: key metrics, thresholds
  and statistical tests.
* A reproducibility statement or checklist (appendix, supplementary material) may exist.
  Note any missing component (proprietary code, inaccessible data).

**Questions to check your understanding** (they help you verify that you "get" the
paper; they are not an exam: answer them briefly, in your own words):

* Which data, materials or inputs are required? Are they openly available? If not, what
  is the impact on the reproducibility effort?
* Which methods and algorithms are used? Standard or customized? Are parameter settings
  given?
* Which tools, libraries and environments are needed? Are dependencies documented, with
  versions and configurations?
* Which material resources are needed to reproduce the results (e.g. GPU, computing time,
  storage, API credits for commercial models, paid or restricted-access data)? Do you have
  access to them? If not, which subset of the results can you realistically reproduce?
  **Report this ASAP and discuss it with Mathieu Acher**, do not wait for the end of the
  session.

**List** every ambiguity or vague description (unclear method or parameter), and every
potential variability factor (random seeds, data randomness, subjective decisions in data
processing or analysis).

## (Step 3) Reproduce

Goal: obtain the original results as closely as possible, with the same data, methods and
analyses, using the original code and data when available.

* **Data**: get the original datasets (repository or authors)... check that format and
  contents match the paper. Re-apply exactly the same pre-processing.
* **Environment**: set up the environment of the study (languages, libraries, versions).
  If unspecified, choose versions consistent with the date of the study and **record your
  choices**. Use **Docker and automated scripts** for a reproducible environment. Note
  environment settings, random seeds and hardware requirements that may influence the
  output (note: it will be useful for the replication effort).
* **Compare** your results with the paper, focusing on the key metrics and statistical
  results supporting the main claims.
* **Document deviations**: are they random, or linked to the environment, or missing
  parameters, or other variations? Describe the challenges you faced (unclear code,
  undocumented parameters, data inconsistencies) and how to overcome them.

**Conclude: is it reproducible?** Do you confirm the original results, to what degree, and
which factors explain the differences?

## (Step 4) Design the replication protocol

Goal: test robustness and generalizability by introducing controlled variations and
checking whether the findings still hold.

Sources of variability to examine:

* **Data sensitivity**: do findings depend on dataset size, distribution, feature types?
  Would other datasets generalize?
* **Methodological adjustments**: model parameters, feature selection, random seeds…
* **Environment**: hardware, software, library dependencies.

Threats to replicability, examples: **randomness** (set or vary seeds), **sampling bias** (vary
sample groups), **parameter sensitivity** (vary parameter values).

**Document all possible variations:**

* the variability factors;
* for each factor, its possible values (e.g. True/False), and why it is worth considering;
* the logical constraints across factors.
=> elaborate a feature model in UVL leveraging the UVL-studio (as in lab session 3)

**Formulate a hypothesis for each variation**, e.g. *"The original results are robust to
parameter variations in model X settings."* State the expected results and the limits of
deviation that would indicate fragility of the original findings.

## Deliverables (end of session)

* short answers to the questions of Steps 1 and 2 (including the resources needed), and the lists of ambiguities and variability
  factors
* the reproduction: Docker setup and scripts, reproduced results compared with the
  paper, documented deviations and challenges, and your conclusion on reproducibility;
* the replication protocol: variability factors (values, rationale, constraints, feature model),
  hypotheses and expected results.
