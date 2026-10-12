# Lab session #1 — How often (x+y)+z == x+(y+z)?

* **Format**: in class, in pairs. Keep the same pair for labs #2 and #3.
* **AI-free**: no ChatGPT, Copilot, etc. today, and don't search the web for the
  answer. The programs are short. The point is to *find out for yourself*, and your
  hand-written programs are the human baseline for the LLM experiment of lab #2.
* **Not graded**, but **keep your code**: lab #2 starts from it.

## What to do

1. **Is (x+y)+z == x+(y+z)?**
   Choose any language, compiler/interpreter, library, computing environment or machine
   (Java, Rust, Scratch, SageMath, a spreadsheet…). Is it true? Always?

2. **How often (x+y)+z == x+(y+z)?**
   Write a program that prints a **percentage**.
   The question is *deliberately* under-specified ("x, y, z: number"), so you will have to make
   choices. Make them, and write each one down: they are part of your result.

3. **Is your result reproducible?**
   Run your program again, on another machine if you can. Do you get the same result?

4. **The banking problem: do the same.**
   *"My banker proposed this investment to me: you give me e ≈ 2.71828… The following year,
   I take 1 euro as a fee and multiply by 1. The next year, I take 1 euro as a fee and
   multiply by 2. The next year, I take 1 euro as a fee and multiply by 3. […] After n years,
   I take 1 euro as a fee and multiply by n. To retrieve my money, there is a 1 euro fee.
   In 50 years, for my retirement, how much money will I have?"*
   Write a program that answers this question, write down your choices, and check whether your
   result is reproducible.

5. **Report** in the shared sheet
   https://docs.google.com/spreadsheets/d/1Ell7cEijcauAl2xoc3Ht-dJb53WOjd-6uLhXlUGUFoo/edit?usp=sharing
   your answer to each problem, along with whatever another group would need to get the same
   answer. 

6. **If you have time**: build another variant (another language, compiler/interpreter,
   library, environment or machine) and report it too.

## Class discussion

We look at the sheet together:
- Do the groups agree? If not, why not?
- Could another group get your answer from what you reported alone? What was missing?

## Outcomes

Push your code for both problems to a git repository (GitHub or GitLab), with a short README
that lists your choices. **Lab #2 starts from this repository.**

## To go further (optional)

- **Contribute** a new variant (a new language, compiler or flags, ideally with a Dockerfile
  or Nix file) as a pull request to
  https://github.com/FAMILIAR-project/reproducibility-associativity
- **Sylvie Boldo's talk** at the Collège de France, which the banking example comes from:
  https://www.college-de-france.fr/fr/agenda/seminaire/semantiques-mecanisees-quand-la-machine-raisonne-sur-ses-langages/arithmetique-des-ordinateurs-et-sa-formalisation
  (reproducing and replicating it is a bonus of lab #2).
