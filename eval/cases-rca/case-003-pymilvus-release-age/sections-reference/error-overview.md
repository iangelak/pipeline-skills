The fromager bootstrap for the `rhai-cpu-ubi9` collection failed across all four architectures while resolving the `pymilvus` dependency of `langchain-milvus==0.4.0`. The error manifests differently per architecture:

**x86_64** — candidates blocked by release-age cooldown:

```error
L31025: 08:31:56 ERROR Unable to resolve requirement specifier pymilvus<4.0,>=3.0.0 with constraint None using PyPI resolver (searching at https://pypi.org/simple): found 2 candidate(s) for pymilvus<4.0,>=3.0.0 but all were published within the last 3 days (release-age cooldown; oldest is 2 day(s) old)
```

**aarch64** — no source distribution available:

```error
L31028: 08:39:37 ERROR Unable to resolve requirement specifier pymilvus<4.0,>=3.0.0 with constraint None using PyPI resolver (searching at https://pypi.org/simple): found no match for pymilvus<4.0,>=3.0.0 using PyPI resolver (searching at https://pypi.org/simple), searching for sdists, ignoring pre-release versions
```

**s390x and ppc64le** — job logs exceeded the 4MB limit at ~85% bootstrap progress before the error was captured. Both jobs were at a similar stage of bootstrap and likely hit the same `pymilvus` resolution failure.
