# MERGE: Guided Vision-Language Models for Multi-Actor Event Reasoning and Grounding in Human-Robot Interaction

This repository contains the implementation of **MERGE**, accepted at the **2026 IEEE International Conference on Robotics and Automation (ICRA 2026)**.

MERGE is a system for multi-actor event reasoning and grounding in human-robot interaction scenarios. It combines a lightweight perception pipeline with Vision-Language Models (VLMs) to identify actors and objects, track them over time, and structure interactions as actor-action-object relations. The system is designed to support temporally consistent situational grounding in dynamic group interactions involving humans and robots.

For details, please refer to the paper:

**MERGE: Guided Vision-Language Models for Multi-Actor Event Reasoning and Grounding in Human-Robot Interaction**
Joerg Deigmoeller, Nakul Agarwal, Stephan Hasler, Daniel Tanneberg, Anna Belardinelli, Reza Ghoddoosian, Chao Wang, Felix Ocker, Fan Zhang, Behzad Dariush, Michael Gienger  
Accepted at **ICRA 2026**  
[arXiv:2603.18988](https://arxiv.org/abs/2603.18988)

## Installation

We recommend using [`uv`](https://docs.astral.sh/uv/getting-started/installation) for installation and dependency management.

After installing `uv`, run the following commands from the project root:

```bash
uv venv
uv sync
```
## Dataset

Before running the experiments, download the **GROUND** dataset from:

https://usa.honda-ri.com/ground

Unpack the dataset and run the following script, pointing it to the extracted `GROUND-eval` folder:

```bash
bash scripts/copy_ground_eval.sh ~/ground/GROUND-eval
```

The script copies the required evaluation data into the expected `data/scene_*` directories.

## API Keys

To use GPT-based models, set your OpenAI API key:

```bash
export OPENAI_API_KEY="SECRET_KEY"
```

To use Gemini-based models, set your Gemini API key:

```bash
export GEMINI_API_KEY="SECRET_KEY"
```

## Evaluation

The main evaluation script can be used to reproduce the quantitative results reported in the paper:

```bash
uv run scripts/evaluate.py
```

The script evaluates the method outputs stored in the dataset directories:

```text
data/scene_*/runs
```

These folders contain the outputs produced by the different methods and baselines. The evaluation script compares these outputs against the corresponding annotations and reports the metrics used in the paper.

Different experiment configurations can be selected by editing the corresponding configuration section in:

[`scripts/evaluate.py`](./examples/evaluate.py#L312)

By default, the evaluation runs **MERGE with GPT-4o**.


## Experiments

To run the full MERGE pipeline, use:

```bash
uv run scripts/merge_full.py
```

To run the baseline experiments, use:

```bash
uv run scripts/baselines.py
```
## Citation

If you use this repository, the GROUND dataset, or the MERGE system in your research, please cite our paper:

```bibtex
@inproceedings{deigmoeller2026merge,
  title={MERGE: Guided Vision-Language Models for Multi-Actor Event Reasoning and Grounding in Human-Robot Interaction},
  author={Deigmoeller, Joerg and Agarwal, Nakul and Hasler, Stephan and Tanneberg, Daniel and Belardinelli, Anna and Ghoddoosian, Reza and Wang, Chao and Ocker, Felix and Zhang, Fan and Dariush, Behzad and Gienger, Michael},
  booktitle={Proceedings of the 2026 IEEE International Conference on Robotics and Automation (ICRA)},
  year={2026}
}
```

## License

This project is licensed under the **BSD 3-Clause License**.

Copyright (c) 2025, Honda Research Institute Europe GmbH.
All rights reserved.

See the [`LICENSE`](./LICENSE) file for the full license text.

SPDX-License-Identifier: BSD-3-Clause
