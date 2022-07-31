from pathlib import Path

import nbformat
from click.testing import CliRunner
from nbformat.notebooknode import NotebookNode
from pytest import fixture

from nb_move_imports import reorder_imoprt_statements
from nb_move_imports.main import IMPORT_CELL_TAG, main


@fixture
def unsorted_nb(shared_datadir: Path) -> NotebookNode:
    nb_path = shared_datadir / "unsorted_nb.ipynb"
    return nbformat.read(nb_path, as_version=4)


def test_convertion(unsorted_nb: NotebookNode) -> None:
    sorted_nb = reorder_imoprt_statements(unsorted_nb)
    import_cell, *code_cells = sorted_nb["cells"]

    # check that all imoprt statements has been removed
    for c in code_cells:
        assert "import" not in c["source"]

    # check that the import statements are in the first cell
    assert "import sys" in import_cell["source"]

    # check that the first cell has been tagged
    assert IMPORT_CELL_TAG in import_cell["metadata"]["tags"]


def test_cli(shared_datadir: Path, tmpdir: Path) -> None:
    runner = CliRunner()

    # define paths
    input_path = str(shared_datadir / "unsorted_nb.ipynb")
    output_path = str(tmpdir / "sorted_nb.ipynb")

    # run cli
    result = runner.invoke(main, [input_path, output_path])

    # read in sorted notebook
    sorted_nb = nbformat.read(output_path, as_version=4)
    import_cell, *code_cells = sorted_nb["cells"]

    # check that all imoprt statements has been removed
    for c in code_cells:
        assert "import" not in c["source"]

    # check that the import statements are in the first cell
    assert "import sys" in import_cell["source"]
    assert result.exit_code == 0
