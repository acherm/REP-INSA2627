# Reproducibility of computational experiments (INSA 2627)

* Introduction/motivation
  - slides: [https://docs.google.com/presentation/d/1J9oXuKFe3xGdVTWqjr8nEd1Dr5DtdevEjVYAOT_TJ10/edit?usp=sharing](https://docs.google.com/presentation/d/1J9oXuKFe3xGdVTWqjr8nEd1Dr5DtdevEjVYAOT_TJ10/edit?usp=sharing)
  - context: computational science; scientific methods in industry; automated SE; continuous SE/DevOps; software/AI eating the world (data+software+challenges) 
  - terminologies (reproductibility; repeatability; replicability; frictionless reproducibility)
  - initiatives (reproducible builds; software heritage; open source; open data; paperswithcode; etc.)
  - historical examples (reproducibility crisis)
  - some examples (climate models)
  - reproducibility and science
  - reproducibility in IT and outside IT 
  - replicability in science
  - replicability in IT and outside IT
  - take away: (frictionless) reproducibility is key to innovation! 
  - perspective: need to master automated software engineering and variability

* Lab session #1 [https://docs.google.com/presentation/d/1es2htp1XlILsvFiTITykZN0glBkey0T9f05i5OX4Kbk/edit?usp=sharing](https://docs.google.com/presentation/d/1es2htp1XlILsvFiTITykZN0glBkey0T9f05i5OX4Kbk/edit?usp=sharing)
  - instructions: [tp1-associativity-2627.md](tp1-associativity-2627.md) (complements the slides)

* Lab session #2 aka Reproducibility
  - instructions: [tp2-reproducibility-2627.md](tp2-reproducibility-2627.md)

* Reproducibilty foundations (methods, tools, techniques)
  - slides: https://docs.google.com/presentation/d/1eYXHFeSKa2SA8hQyvBB_Z0OY4ufakst5lVNMZzyuvLI/edit?usp=sharing
  - Reproducibility mindset
  - Open source software and tools
  - Master your computing environment
  - Explore the variants space
  - Threats to validity
  - Automate everything
  - Test and doubt about the quality of your software
    
* Lab session #3 aka Replicability, Variability and Consensus
https://docs.google.com/document/d/1jYBh6aIoE9DpiRwvES2tSn7TLTfyHYMJhWkkkFKEH0I/edit?usp=sharing


* Lab session #4 Towards reproducing and replicating results (of one of the papers below)


* Lab sessions #5 Instructions to report on reproducing and replicating results


## Papers to reproduce and replicate (choose 1 out of N)

Fill in your group (names) and the paper you choose in the shared sheet: https://docs.google.com/spreadsheets/d/160cPwKkVkRtip8unoTdfX5O5G8a-Ux7EOa_dr3UxVk8/edit?usp=sharing

* **Gzip beats BERT**
  - Zhiying Jiang, Matthew Yang, Mikhail Tsirlin, Raphael Tang, Yiqin Dai, Jimmy Lin. 2023. "Low-Resource" Text Classification: A Parameter-Free Classification Method with Compressors. In Findings of the Association for Computational Linguistics: ACL 2023, Toronto, Canada, pp. 6810–6828. https://doi.org/10.18653/v1/2023.findings-acl.426
  - code: https://github.com/bazingagin/npc_gzip
  - critique: Ken Schutte. 2023. Bad numbers in the "gzip beats BERT" paper? Blog post, 17 July 2023. https://kenschutte.com/gzip-knn-paper/
  - TL;DR: The paper classifies text with no training and no GPU, using gzip compression distances and a k-nearest-neighbour vote, and reports accuracy on par with BERT on several datasets. Schutte re-ran the released code and showed that the way accuracy is computed inflates these numbers.

* **Nix: reproducible builds at scale**
  - Julien Malka, Stefano Zacchiroli, Théo Zimmermann. 2025. Does Functional Package Management Enable Reproducible Builds at Scale? Yes. In Proceedings of the 22nd IEEE/ACM International Conference on Mining Software Repositories (MSR 2025), Ottawa, Canada, pp. 775–787. https://doi.org/10.1109/MSR66628.2025.00115
  - preprint: https://arxiv.org/abs/2501.15919
  - artifacts: https://gitlab.telecom-paris.fr/julien.malka/does-functional-package-management-enable-reproducible-builds-at-scale
  - data: https://doi.org/10.5281/zenodo.14736078 · https://doi.org/10.5281/zenodo.14728623
  - TL;DR: The authors rebuilt 709,816 Nix packages from 17 nixpkgs snapshots (2017–2023) and compared each rebuild bit-for-bit with the official binaries. They found 69–91% of builds reproducible, classified the causes of the failures, and released their build pipeline, data and logs.

* **The car-wash test**
  - Mathieu Acher. 2026. Le test du lave-auto : les LLMs ont-ils vraiment du sens commun ? [The car-wash test: do LLMs really have common sense?] Blog post (in French), 26 May 2026. https://blog.mathieuacher.com/LLMCarWashCommonSense/
  - scripts, raw LLM answers and judge verdicts: https://github.com/acherm/laveauto-llm
  - TL;DR: The study asks 8 LLMs, 120 times each and in two French wordings, "I want to wash my car, the car wash is 150 m away: walk or drive?", and an LLM judge scores every answer on two separate criteria. A simple rewording flips some models by about 58 points, in either direction.

* **Toby, The Oracle By Yosha**
  - Yosha Iglesias. 2026. Toby – The Oracle By Yosha. Open-source engine (AGPL) and method page (docs/METHOD.md), announced 10 October 2026. https://github.com/Yosha87/Toby (commit d3b9302)
  - TL;DR: Toby predicts human chess moves by combining Maia-3, a network trained to imitate human players, with a Leela search and a rule using 3–4 constants. Its author claims it is the best human-move predictor "for all levels and all time controls", tested with pre-registered protocols on test games that are not public.

* **Risk and confidence of configuration sampling**
  - Kallistos Weis, Martina Maggio, Norbert Siegmund, Sven Apel. 2026. Evaluating Risk and Confidence in Performance Bounds of Configuration Sampling Strategies. Proceedings of the ACM on Software Engineering 3, FSE (FSE 2026), Article FSE140, pp. 3162–3185. https://doi.org/10.1145/3808147
  - preprint: https://www.se.cs.uni-saarland.de/publications/docs/WMS+26.pdf
  - artifact (notebooks and data): https://doi.org/10.5281/zenodo.19682296
  - TL;DR: The paper asks how sure you can be that a sample of configurations contains the worst (or best) performing one: it defines an a posteriori risk and confidence, and compares 5 sampling strategies on 7 configurable systems (7z, LLVM, BerkeleyDB…) whose configurations were all measured. Recursive statistical search (SRS) gives the tightest guarantees, and solver-based sampling the least reliable ones.

## Resources

  * École Jeunes Chercheuses et Jeunes Chercheurs en Programmation https://gpl-ejcp.github.io/ejcp2023 
  * Frictionless reproducibility and deep variability https://hal.science/hal-04601752
  * Teaching Reproducibility and Embracing Variability: From Floating-Point Experiments to Replicating Research Mathieu Acher, Arnaud Gotlieb, Helge Spieker, Gauthier Le Bartz Lyan https://hal.science/hal-05190848v1
  * 2024 ACM Conference on Reproducibility and Replicability https://acm-rep.github.io/2024/ 
  - Practical strategies for teaching reproducibility.
By Fraida Fund, Stephanie Lieggi, Kate Keahey, Cormac Flanagan, Marc Richardson,  Haryadi Gunawi and Sarah Cohen Boulakia
  * https://forum.recherche-reproductible.fr/
  * MOOC REPRODUCIBLE RESEARCH II (Arnaud Legrand, Konrad Hinsen, C Pouzat, Matthieu Simonin, etc.)
  * https://alexnuttinck.dev/posts/1-the-reproducibility-crisis/ The Reproducibility Crisis by Alexandre Nuttinck


