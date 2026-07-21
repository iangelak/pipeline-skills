The failure was caused by a new upstream release of `langchain-milvus` that introduced an unresolvable dependency on the `pymilvus` 3.x series.

**Failure Chain**

1. The `rhai/cpu-ubi9` requirements file (`collections/rhai/cpu-ubi9/requirements/team-notebooks-images.txt`) lists `langchain-milvus` without a version pin.
2. `langchain-milvus==0.4.0` was released on PyPI on 2026-07-17 — just 3 days before this pipeline ran on 2026-07-20. Fromager resolved it as the latest version.
3. This release bumped the pymilvus requirement from `pymilvus<3.0,>=2.6.0` (in 0.3.3) to `pymilvus<4.0,>=3.0.0`, requiring the brand-new pymilvus 3.x major version series.
4. pymilvus 3.0.0 is currently the only 3.x release available on PyPI. It was published as a wheel-only package (`pymilvus-3.0.0-1-py3-none-any.whl`) with no source distribution (sdist).
5. The resolution failed for two distinct reasons depending on architecture:

**x86_64:** The resolver found 2 pymilvus candidates matching `>=3.0.0,<4.0` but all were published within the last 3 days, triggering the builder's 3-day release-age cooldown (`FROMAGER_MIN_RELEASE_AGE=3`). This indicates recently-published pymilvus 3.x versions exist that are no longer visible on PyPI (possibly yanked or removed since the pipeline ran).

**aarch64:** The resolver found no match at all when searching for source distributions. Since pymilvus 3.0.0 is published as a wheel only (no sdist), and fromager requires sdists to build from source, no candidate was available.

**Variant-Specific Differences**

The x86_64 and aarch64 jobs exhibit different error messages: x86_64 finds candidates that are too new (cooldown), while aarch64 finds no sdist candidates at all. Both ultimately stem from the same root cause — pymilvus 3.x is not available in a form that fromager can use. The s390x and ppc64le jobs had their logs truncated at the 4MB limit before the error was captured, but their bootstrap progress (~85%) and the same collection context make it highly likely they hit the identical failure.

**Caveats**

The x86_64 error references "2 candidates" for pymilvus 3.x that were "2 days old," but the current PyPI index only shows pymilvus 3.0.0 (published 2026-05-07, well outside the cooldown window). This suggests additional 3.x versions were briefly published and subsequently removed. The diagnosis does not depend on identifying those specific versions — the resolution failure is confirmed by the logs regardless.
