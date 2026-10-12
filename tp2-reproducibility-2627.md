# Lab session #2 — Reproducibility with git, Docker and GitHub Actions

You work in the same pair as in lab #1, and you start from the repository you created there
(associativity + banking). The idea is to concretely practice git, Docker and GitHub Actions
(or GitLab CI).

I'm not giving a complete course on these technologies (I assume you know them a bit), but
I'm giving concrete explanations and pointers so that you can do it by yourself. And I'm
obviously here to help!

Take as much time as needed to install the tools and get comfortable with them: it matters
for the rest of the REP course and for your future as an engineer.

* **Mandatory core**: Parts 1 to 5. **Bonus**: Parts 6 and 7.
* If you don't finish the core during the session, finish it before lab #3: lab #3 starts
  from a repository whose GitHub Actions workflow works.
* **AI** is allowed from this lab on (Part 4 is even about LLMs). If you use an AI assistant,
  say so in your README: which tool and model, and what you used it for.

## Part 1 — Reproducible?

* Create a git repository on GitHub (or GitLab) and push your code for both problems, if you
  haven't done it in lab #1.
* Refactor your code so that anyone can run it and automatically get your answers, written
  to two files:
  * `answer_associativity.txt`: how often (x+y)+z == x+(y+z)?
  * `answer_banking.txt`: how much money after 50 years?
* Write instructions in a `README.md`, as precise as possible, to reproduce your results,
  including the answers someone is supposed to get. If your answer changes from one run to
  the next, say what counts as "the same result".
* Share your repository: add its URL to your group's row in the shared sheet
  https://docs.google.com/spreadsheets/d/1Ell7cEijcauAl2xoc3Ht-dJb53WOjd-6uLhXlUGUFoo/edit?usp=sharing
* Try to reproduce another group's results with their repository and README only. Take the
  group just after yours in the sheet (the last group takes the first one).
* Report the difficulties you run into as GitHub issues on their repository.
* (consensus) Do you get the answers announced in their README? Are they equal to your own
  answers? Give possible reasons for any discrepancy.

## Part 2 — Docker

Back to *your* repository.

"It works on my machine" is sometimes a fallacy.

Docker (https://docs.docker.com) is a platform to package, distribute and run applications in
isolated environments called containers, which can be deployed and run consistently on any
system. Docker holds the *promise* of providing an environment that is the same on every
machine: the hope is that you can move your application from one machine to another, be it
your laptop, a server or a cloud provider. In this lab, you use Docker to create an isolated
environment where your programs compute both answers, hopefully the same way on every machine.

Some basic terminology:

* A **Dockerfile** is a configuration file containing the instructions to build a Docker
  image. It typically specifies the base image, the working directory, the dependencies, and
  the commands needed to set up and run your application. It's a recipe that tells Docker how
  to create an environment for your code to run.
* A **Docker image** is a snapshot of an environment built from a Dockerfile. It contains
  everything needed to run the application: operating system, code, dependencies. An image is
  immutable: it doesn't change once created.
* A **Docker container** is a running *instance* of an image. The image is the blueprint, the
  container is where the application actually runs, in an isolated environment. Containers
  are lightweight and fast because they share the host operating system's kernel, unlike
  virtual machines.

Your goal: write a Dockerfile such that running a container computes both answers.

### 1. Choose a base image

Pick a base image that matches your programming language, for example `python:3.14-slim`
(Python), `node:24` (Node.js) or `gcc:15` (C).

```dockerfile
FROM python:3.14-slim
```

Question: why would `gcc:latest` be a bad idea in a reproducibility course? And
`python:3.14-slim` itself is rebuilt regularly: look up what an image *digest* is.

### 2. Set the working directory

```dockerfile
WORKDIR /app
```

### 3. Copy your code

```dockerfile
COPY . /app
```

### 4. Install dependencies

* Python: list the required packages in a `requirements.txt` file
  (uv, https://github.com/astral-sh/uv, is an alternative to pip).

  ```dockerfile
  RUN pip install -r requirements.txt
  ```
* C: the `gcc` image already contains the compiler. Install other system libraries with
  `apt-get` if you need them.

### 5. Build and run your programs

```dockerfile
# Python
CMD ["python", "associativity.py"]
```

```dockerfile
# C
RUN gcc -o associativity associativity.c
CMD ["./associativity"]
```

Your container must compute **both** answers. The simplest way is a small script
(e.g. `run.sh`) that runs both programs, used as the `CMD`.

### Build the image and run a container

```bash
docker build -t rep-lab2 .
docker run --rm rep-lab2
```

### Get the answer files out of the container

Files written inside a container disappear with it. To get `answer_associativity.txt` and
`answer_banking.txt` on your machine, use a bind mount
(https://docs.docker.com/engine/storage/bind-mounts/):

```bash
docker run --rm -v "$(pwd)":/out rep-lab2
```

The current folder of your machine (`$(pwd)`, or `${PWD}` in Windows PowerShell) is mounted as
`/out` inside the container, so your programs must write their answer files into `/out`.
Make the output folder a parameter or an environment variable rather than hard-coding it.
On Linux, add `--user "$(id -u):$(id -g)"` so that the files don't belong to root.

Final step: push to git, and update your README with the instructions to reproduce your
results with Docker.

## Part 3 — Automate with GitHub Actions (and Docker)

Write a workflow (`.github/workflows/<name>.yml`) that, on every push, builds your Docker
image, runs the container, and pushes `answer_associativity.txt` and `answer_banking.txt`
to your repository.

* You don't need to write your own action: a workflow whose steps run `docker build` and
  `docker run` is enough. Start from https://docs.github.com/en/actions/get-started/quickstart
  (if you're curious, you can also package your code as a Docker container action:
  https://docs.github.com/en/actions/sharing-automations/creating-actions/creating-a-docker-container-action).
* To push from a workflow, see
  https://github.com/actions/checkout?tab=readme-ov-file#push-a-commit-using-the-built-in-token
  (or https://github.com/ad-m/github-push-action).
* By default, the workflow's token can only read your repository, and `git push` fails with a
  403 error. Grant write access in your workflow:

  ```yaml
  permissions:
    contents: write
  ```
* If the answers didn't change since the last run, `git commit` has nothing to commit and
  fails: handle this case.

Update your README: the answer files in the repository are now produced by GitHub Actions.

## Part 4 — What about LLMs?

Choose an LLM (Mistral, ChatGPT, Gemini, DeepSeek, etc.) and ask it to address both
problems (associativity and banking) in a programming language other than the one(s) you used.

Make this work reproducible: the generated code must run with Docker (and/or Nix) and through
GitHub Actions. Save the results in `answer_associativity_llm.txt` and `answer_banking_llm.txt`.

Share your prompts, the details of the LLM (which model and version, when, through which
interface) and the full answers, including any back-and-forth with the LLM, in
`LLM_associativity.md` and `LLM_banking.md`. The LLM may not answer the specific question
(you then have to guide it), or may add incorrect claims to the code: comment on it.

How do the LLM's answers compare with those of your hand-written programs from lab #1?

## Part 5 — Nix instead of Docker

Your goal: make your programs runnable in a pinned Nix environment (`shell.nix`), as an
alternative to Docker, and add the instructions to reproduce your results with Nix to your
README.

### Why Nix?

* **Reproducible**: everyone gets the **same** tool versions, whatever the quirks of their OS.
* **Declarative**: you **describe** what you need (Python, NumPy, …) in a file, and Nix builds
  or fetches exactly that.
* **Isolated**: tools live in the **Nix store** (`/nix/store`), not in your system's global
  site-packages, so projects don't step on each other.
* **Shareable**: commit one small file to your repository, and others get the exact same
  environment. Nix is also "compatible" with Docker.

A few Nix concepts. **Packages** are prebuilt recipes (e.g. Python 3.11 or NumPy) that Nix can
fetch or build reproducibly. The **Nix store** is a read-only cache where those packages live,
apart from the rest of your system. A **development shell** (created with `mkShell`) is a
temporary environment where your declared tools are on the PATH, perfect for project work.
**Pinning** means choosing a specific snapshot of the package catalog so that, six months from
now, you still get the same versions. When you see a hash in a Nix expression, treat it as a
safety check: it ensures you fetch exactly the content you intended, not "something close".

Install Nix: https://nixos.org/download/

### Try Nix without committing anything

```bash
# 1) Fire up a shell with just Python 3.11 (temporary)
nix-shell -p python311

# 2) Add something else, e.g. git
nix-shell -p python311 git
```

When the shell opens, you have those tools. Exit, and your system is unchanged.

### Make it declarative (shareable with your teammate)

Put a file named `shell.nix` at the root of your repository:

```nix
# shell.nix (simple, no pinning yet)
{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  packages = [
    pkgs.python311
  ];
}
```

Now anyone can run:

```bash
nix-shell          # drops into the declared environment
python --version
```

This already gives you a stable way to **declare** your tools. But `<nixpkgs>` is taken from
your `NIX_PATH` and follows the evolution of the package catalog: different machines (or
future you) may get different versions. Pinning, below, fixes this.

### Add Python packages with pip

If you manage Python dependencies with `pip`, you typically use a local virtualenv:

```nix
# shell.nix (with a local venv populated by pip)
{ pkgs ? import <nixpkgs> {} }:
let
  py = pkgs.python311;
in
pkgs.mkShell {
  packages = [ py pkgs.python311Packages.venvShellHook ];
  venvDir = ".venv";

  postVenvCreation = ''
    python -m pip install --upgrade pip
    if [ -f requirements.txt ]; then
      PIP_DISABLE_PIP_VERSION_CHECK=1 python -m pip install -r requirements.txt
    fi
  '';

  postShellHook = ''
    echo "Python: $(python --version)"
  '';
}
```

Usage:

```bash
nix-shell              # creates/uses .venv and installs requirements
python src/your_app.py
```

You can swap pip for uv later. The examples are for Python, but the same principles apply to
other languages and tools (compilers, build tools, package managers, etc.).

### Only now: pin the package catalog

**Why**: without pinning, `<nixpkgs>` changes over time. If your teammate tries the project
next semester, they may get a slightly different Python or different system libraries.
Pinning freezes the catalog so that everyone gets the same thing.

**How**: replace `<nixpkgs>` with a fixed snapshot.

1. Create `nixpkgs-pin.nix`:

   ```nix
   # nixpkgs-pin.nix — picks a specific snapshot of nixpkgs
   let
     rev = "<COMMIT>";     # a nixpkgs commit, e.g. the head of the nixos-26.05 branch
     sha256 = "<SHA256>";  # safety checksum, see step 3
   in
   import (builtins.fetchTarball {
     url = "https://github.com/NixOS/nixpkgs/archive/${rev}.tar.gz";
     inherit sha256;
   })
   ```

2. Use the pin in `shell.nix`:

   ```nix
   # shell.nix (same as before, but pinned)
   let
     pkgs = import ./nixpkgs-pin.nix {};
     py = pkgs.python311;
   in
   pkgs.mkShell {
     packages = [ py pkgs.python311Packages.venvShellHook ];
     venvDir = ".venv";
     postVenvCreation = ''
       python -m pip install --upgrade pip
       if [ -f requirements.txt ]; then
         PIP_DISABLE_PIP_VERSION_CHECK=1 python -m pip install -r requirements.txt
       fi
     '';
   }
   ```

3. Get the `sha256`:

   ```bash
   nix-prefetch-url --unpack https://github.com/NixOS/nixpkgs/archive/<COMMIT>.tar.gz
   ```

   prints the value to paste. If you put a wrong hash instead, Nix stops with a hash mismatch:
   paste the value after `got:`, not the other one (that's the hash you wrote).

### Where this sits vs Docker

* **Nix dev shell**: fast and lightweight, great for development and CI steps; no daemon, no
  images to rebuild.
* **Docker**: still the mainstream for deployable runtime images. Many teams use *both*: Nix
  for development/CI reproducibility, Docker for deployment.

### To go further later

* Replace pip with **uv** (same `shell.nix` shape).
* Move to **Nix flakes** once you're comfortable: a nicer CLI and a lock file, but optional.

## Part 6 (bonus) — GitHub Actions with Nix

Same as Part 3, but with Nix instead of Docker
(see for instance https://github.com/cachix/install-nix-action).

## Part 7 (bonus) — Reproducing and replicating a talk

Sylvie Boldo's talk at the Collège de France (the banking problem comes from it):
https://www.college-de-france.fr/fr/agenda/seminaire/semantiques-mecanisees-quand-la-machine-raisonne-sur-ses-langages/arithmetique-des-ordinateurs-et-sa-formalisation
(also look at the slides/PDF of the talk).

**Reproduce** a subset of what is said in the talk (figures, tables, etc.):

* push the code to your repository;
* use Docker and GitHub Actions (or GitLab CI) to produce an `answer_boldo.pdf`.

**Replicate** (change programming language, compiler flags or versions, etc.):

* push the code to your repository;
* use Docker and GitHub Actions (or GitLab CI) to produce an `answer_repl_boldo.pdf`;
* is it consistent with the original claims of the talk?

## Outcomes

Before lab #3, your repository contains:

* the code for both problems, and a README with the instructions to reproduce your results,
  including the expected answers;
* a Dockerfile, and a GitHub Actions workflow that computes and pushes
  `answer_associativity.txt` and `answer_banking.txt`;
* the LLM files of Part 4;
* a pinned `shell.nix` to reproduce your results with Nix (Part 5).

And you have opened issues on the repository of the group you reproduced.
