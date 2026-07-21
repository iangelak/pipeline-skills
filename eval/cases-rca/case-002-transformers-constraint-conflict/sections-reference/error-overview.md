The fromager bootstrap for the `rhaiis` cpu-ubi9 collection failed during dependency resolution when attempting to resolve the `transformers` package. A requirement for `transformers>=5.6.0` conflicts with the pipeline constraint `transformers<5`, making resolution impossible:

```error
L6713: 05:19:16 ERROR Unable to resolve requirement specifier transformers>=5.6.0 with constraint transformers<5 using PyPI resolver (searching at https://pypi.org/simple): found no match for transformers>=5.6.0 using PyPI resolver (searching at https://pypi.org/simple), searching for sdists, ignoring pre-release versions
```

A separate resolution of `transformers>=4.38.0` (from `xgrammar-0.2.3`) succeeded earlier, resolving to `transformers-4.57.6` within the `transformers<5` constraint. The conflicting `transformers>=5.6.0` specifier originates from `vllm-0.24.0+rhaiv.1`.
