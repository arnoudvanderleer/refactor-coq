# Refactor Coq

This repository contains two scripts for refactoring coq code, using `.glob` files generated by Dune.

## Usage

The first script, `generate.py` searches a directory and its subdirectories for definitions, lemmas and proofs that need to be converted to `snake_case`. This can of course be adapted to your own use case. It takes 3 (optional) arguments: the search directory, the project root and the "glob root", for example:
```bash
$ ./generate.py ./generate.py UniMath/CategoryTheory/Limits/ ../coq/
```
This searches the directory `../coq/UniMath/CategoryTheroy/Limits` for definitions that still need updating. The default argument for the glob root is `_build/default`, so the script will look for the corresponding glob files in `../coq/_build/default/UniMath/CategoryTheory/Limits/`. If your glob files are located elsewhere (for example, next to your files or in another directory), you need to supply their root directory as a third argument.

`generate.py` generates a file called `changes.txt`. Every line in this file lists the namespace of an identifier that needs changing, its new name and its old name. Of course, this file can also be generated manually. A line in this file looks like:
```
UniMath.CategoryTheory.Limits.Cats.Limits postcomp_with_lim_arrow postcompWithLimArrow
```

The second script, `substitute.py` takes the substitutions listed in `changes.txt` and applies them to all files in a directory (and its subdirectories). Its arguments are very similar to those of `generate.py`:
```bash
$ ./substitute.py UniMath ../coq/
```
This will perform all the substitutions listed in `changes.txt` in all files under `../coq/UniMath/` (again, using `_build/default` as the glob root).
