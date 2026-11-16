# Tablerito

A kanban-style task board: one board with lists and cards, with attachments. It is the sample
app of the Infrastructure and Cloud-Native course, and it has problems on purpose: finding them is
the activity of session 2.

Python with Flask. The tools are in `mise.toml`, and [uv](https://docs.astral.sh/uv/) manages the
dependencies, with `pyproject.toml` and `uv.lock`: there is no need to set up a virtual environment
by hand.

## Running it

With [mise](https://mise.jdx.dev), which installs Python and uv, the commands are the same on
Windows, Mac and Linux:

```bash
mise install
mise run dev
```

`mise install` is only needed the first time; it asks whether you trust the repo's `mise.toml`.
Tablerito takes a few seconds to start. Then open http://localhost:8080.

Without mise, uv is enough: it downloads Python if you don't have a suitable one (3.12 or newer).
To install it on Mac or Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then, in a new terminal:

```bash
uv run python -m tablerito
```

## Tests

```bash
mise run test
```

Without mise, `uv run pytest`.
