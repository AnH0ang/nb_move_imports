from pathlib import Path

import nbformat
from click.testing import CliRunner
from nbformat.notebooknode import NotebookNode
from pytest import fixture

from nb_move_imports import reorder_imoprt_statements
from nb_move_imports.main import IGNORE_CELL_TAG, IMPORT_CELL_TAG, main


@fixture
def unsorted_nb(shared_datadir: Path) -> NotebookNode:
    nb_path = shared_datadir / "unsorted_nb.ipynb"
    return nbformat.read(nb_path, as_version=4)


def test_convertion(unsorted_nb: NotebookNode) -> None:
    sorted_nb = reorder_imoprt_statements(unsorted_nb)
    import_cell, *code_cells = sorted_nb["cells"]

    # check that all imoprt statements has been removed
    for c in code_cells:
        if IGNORE_CELL_TAG not in c["metadata"].get("tags", []):
            assert "import" not in c["source"]
        else:
            assert "import" in c["source"]

    # check that the import statements are in the first cell
    assert "import sys" in import_cell["source"]

    # check that the first cell has been tagged
    assert IMPORT_CELL_TAG in import_cell["metadata"]["tags"]


def test_cli(shared_datadir: Path, tmpdir: Path) -> None:
    runner = CliRunner()

    # define paths
    path = str(shared_datadir / "unsorted_nb.ipynb")

    # run cli
    result = runner.invoke(main, [path])
    assert result.exit_code == 0

    # read in sorted notebook
    sorted_nb = nbformat.read(path, as_version=4)
    test_convertion(sorted_nb)
