# Vaccination Registry — Search Structures Compared

A command-line registry of patients and their vaccines, implemented six times with different search structures (from a linear scan to an AVL tree) and benchmarked to compare their time complexity in practice.

*Individual project. Course: Algorithms and Data Structures, University of Coimbra, 2022/23 (weekly assignments 4.1 to 4.4, graded by the Mooshak online judge).*

## The problem

The program reads commands from standard input, one per line:

| Command | Effect |
|---|---|
| `ACRESCENTA <patient> <vaccine> <date>` | Creates the patient, adds the vaccine, or updates its expiry date |
| `CONSULTA <patient>` | Shows the patient's vaccines in alphabetical order |
| `LISTAGEM` | Lists every patient (ascending) with their vaccines |
| `APAGA` | Deletes all records |
| `FIM` | Ends the input |

The program's messages are in Portuguese (`NOVO UTENTE CRIADO`, `VACINA ATUALIZADA`, `NAO ENCONTRADO`, ...).

## Implementations

| File | Structure | Search | Insert |
|---|---|---|---|
| [a_linear_search.py](solutions/a_linear_search.py) | Sorted list, linear search | O(n) | O(n) |
| [b_binary_search_iterative.py](solutions/b_binary_search_iterative.py) | Sorted list, iterative binary search | O(log n) | O(n) |
| [c_binary_search_recursive.py](solutions/c_binary_search_recursive.py) | Sorted list, recursive binary search | O(log n) | O(n) |
| [d_bst_iterative.py](solutions/d_bst_iterative.py) | Binary search tree, iterative | O(log n) average, O(n) worst | same |
| [e_bst_recursive.py](solutions/e_bst_recursive.py) | Binary search tree, recursive | O(log n) average, O(n) worst | same |
| [f_avl_tree.py](solutions/f_avl_tree.py) | AVL tree (self-balancing) | O(log n) | O(log n) |

Each patient holds a second structure of the same kind with their vaccines, so vaccine lookups use the same method.

## Results

Total time in seconds to run N commands, from the reports in [reports/](reports/) (Portuguese).

**Scenario 1:** 10% insertions, 90% searches

| N | Linear | Binary (iter.) | Binary (rec.) | BST (iter.) | BST (rec.) | AVL |
|---:|---:|---:|---:|---:|---:|---:|
| 20,000 | 0.44 | 0.35 | 0.40 | 0.08 | 0.13 | 0.13 |
| 40,000 | 1.78 | 0.41 | 0.49 | 0.17 | 0.25 | 0.26 |
| 60,000 | 4.82 | 0.85 | 0.80 | 0.26 | 0.38 | 0.41 |
| 80,000 | 11.18 | 1.30 | 1.38 | 0.36 | 0.54 | 0.55 |
| 100,000 | 25.02 | 1.56 | 2.06 | 0.48 | 0.75 | 0.71 |

**Scenario 2:** 90% insertions, 10% searches

| N | Linear | Binary (iter.) | Binary (rec.) | BST (iter.) | BST (rec.) | AVL |
|---:|---:|---:|---:|---:|---:|---:|
| 20,000 | 2.60 | 0.81 | 0.84 | 0.13 | 0.19 | 0.17 |
| 40,000 | 13.84 | 0.99 | 0.94 | 0.26 | 0.42 | 0.43 |
| 60,000 | 24.62 | 1.24 | 1.30 | 0.39 | 0.66 | 0.69 |
| 80,000 | 32.97 | 1.59 | 1.57 | 0.52 | 0.92 | 0.90 |
| 100,000 | 43.11 | 1.68 | 1.75 | 0.65 | 1.30 | 1.14 |

- The linear version's time grows much faster than the others': at 100,000 commands it is 12 to 66 times slower.
- The trees beat the sorted lists, because inserting into the middle of a Python list copies part of it.
- The iterative BST was the fastest. The keys were random, which keeps a plain BST close to balanced, so the AVL tree's rotations add cost without a benefit here.

## How to run

```bash
python solutions/f_avl_tree.py < examples/input.txt
```

Any of the six solutions takes the same input. The scripts in [benchmarks/](benchmarks/) generate random commands for both scenarios and print the timings. They take several minutes, because the tree benchmarks average 100 runs.

## Known limitations

These issues were found in a later review. The code is kept as submitted. Re-tested against the assignment's examples and 300 random command sequences, B, C and F gave the expected output every time.

- **A (linear):** patient numbers are compared as text, so `120` is listed before `45`. Vaccines are matched by substring (`covid` also matches `covid19`). A leftover debug `print` outputs the whole list at the end.
- **D (iterative BST):** updating the date of an existing vaccine can insert a duplicate instead, and the new date is written to the wrong node.
- **D and E (BSTs):** `LISTAGEM` on an empty registry crashes.
- **Benchmarks:**
  - The timings include printing every result, which the assignment asked to exclude.
  - Patient numbers are drawn from 1 to 20,000, so the structures never hold more than 20,000 patients.
  - The BST and AVL timings are averages of 100 runs, while the list versions were timed once.
  - The benchmark script for binary search was not kept.
