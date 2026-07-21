The root cause is a dependency version constraint conflict. The `vllm-0.24.0+rhaiv.1` package requires `transformers>=5.6.0`, but the rhaiis cpu-ubi9 constraints file pins `transformers<5`. These are irreconcilable — no version of transformers can satisfy both `>=5.6.0` and `<5` simultaneously.

The constraint `transformers<5` was originally added (AIPCC-9443) to prevent pulling in transformers 5.x, but the recent vllm upgrade from 0.21.0 to 0.24.0 (AIPCC-27609) introduced the dependency on transformers 5.6+. The constraint was not updated as part of that merge.

Both affected jobs (`rhaiis-cpu-ubi9-aarch64` and `rhaiis-cpu-ubi9-x86_64`) fail identically. An earlier resolution of `transformers>=4.38.0` from `xgrammar-0.2.3` succeeded (resolving to 4.57.6 within the `<5` constraint), confirming the constraint is active.

The fix is to remove or update the `transformers<5` constraint in `collections/rhaiis/cpu-ubi9/constraints.txt` to allow transformers 5.6+.
