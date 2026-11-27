"""Build the project notebook from analysis.py and run it, so the two can never disagree.

analysis.py is written in the "percent" cell format: `# %%` starts a code cell and
`# %% [markdown]` a text cell, so it still runs as a plain script. This converts it to a
notebook, shows each saved figure under the cell that draws it, executes the notebook from
top to bottom, and saves it with its outputs.

    python make_notebook.py                     # rebuilds the one .ipynb in this folder
    python make_notebook.py my_notebook.ipynb   # or name it

Needs the same data as analysis.py, plus: pip install jupytext nbclient ipykernel
"""
import pathlib
import re
import sys

import jupytext
import nbformat
from nbclient import NotebookClient

HERE = pathlib.Path(__file__).resolve().parent
SAVEFIG = re.compile(r"""savefig\(\s*f?["']([^"']+?\.png)["']""")


def figure_paths(code: str) -> list[str]:
    paths = []
    for p in SAVEFIG.findall(code):
        p = p.replace("{FIG}", "figures").replace("{OUT}/", "").replace("{OUT}", ".")
        paths.append(p.removeprefix("./"))
    return paths


def build(target: pathlib.Path) -> None:
    nb = jupytext.read(HERE / "analysis.py", fmt="py:percent")
    cells = [nbformat.v4.new_code_cell("from IPython.display import Image, display  # shows the saved figures inline")]
    for cell in nb.cells:
        if cell.cell_type == "code" and not cell.source.strip():
            continue
        cell.metadata = {}
        cells.append(cell)
        if cell.cell_type == "code":
            for p in figure_paths(cell.source):
                cells.append(nbformat.v4.new_code_cell(f'display(Image(filename="{p}"))'))
    out = nbformat.v4.new_notebook(cells=cells)
    out.metadata = {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
                    "language_info": {"name": "python"}}
    # Markdown first so the title is the first thing a reader sees
    if len(cells) > 1 and cells[1].cell_type == "markdown":
        cells[0], cells[1] = cells[1], cells[0]
    NotebookClient(out, timeout=3600, kernel_name="python3",
                   resources={"metadata": {"path": str(HERE)}}).execute()
    nbformat.write(out, target)
    print(f"Wrote {target.name}: {len(out.cells)} cells, executed top to bottom")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = HERE / sys.argv[1]
    else:
        found = sorted(HERE.glob("*.ipynb"))
        if len(found) != 1:
            sys.exit("Name the notebook to build: python make_notebook.py <name>.ipynb")
        target = found[0]
    build(target)
