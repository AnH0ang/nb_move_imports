# nb_move_imports

------------------------------

Move import statements in jupyter notebook to the first cell

## Use nb_move_imports

To run the script on a specific jupyter notebook run:

```console
nb_move_imports path/to/notebook.ipynb
```

## Precommit Hook

Add this section to your `pre-commit-config.yaml` so that the nb_move_imports script is executed before each commit with pre-commit.

```yaml
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: 0.2.0
  hooks:
    - id: nb_move_imports
      name: nb_move_imports
```
