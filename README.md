## MERGE: Guided Vision-Language Models for Multi-actor Event Reasoning and Grounding in Human–Robot Interaction

### Installation

It is recommneded to use uv for the installation [uv installation guide](https://docs.astral.sh/uv/getting-started/installation).

Once, you have uv installed, run following commands form the root folder:

```bash
uv venv
uv sync
```

### Evaluation

You can switch between the different experiments editing following lines:
[./examples/evaluate.py](./examples/evaluate.py#L265). Default setting
is MERGE with GPT-4o.

```bash
uv run examples/evaluate.py
```

### Experiments

The required image files will be shared via Github once the repository is available.

To use GPT, you need to set
```bash
export OPENAI_API_KEY="53CRE7_KEY"
```

and for Gemini

```bash
export GEMINI_API_KEY="53CRE7_KEY"
```

After this you can run MERGE with:

```bash
uv run examples/merge_full.py
```

and the baseline exmaples with:

```bash
uv run examples/baselines.py
```