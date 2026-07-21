The root cause is that `langchain-milvus` 0.4.0 introduced a new dependency on `pymilvus>=3.0.0,<4.0` (previously `pymilvus>=2.6.0,<3.0`). The `pymilvus` 3.x series was published to PyPI very recently, causing resolution failures through two distinct mechanisms:

On x86_64: pymilvus 3.0.0 and 3.0.1 candidates exist but are blocked by the fromager release-age cooldown (packages published within the last 3 days are excluded to avoid unstable releases).

On aarch64: pymilvus 3.x is wheel-only (no source distribution), and no compatible wheel exists for aarch64, so fromager finds no match at all.

The group consistency is "mixed" because the error messages differ across architectures despite sharing the same root cause (the langchain-milvus version bump).

The fix is to constrain `langchain-milvus<0.4` in the requirements files (`collections/rhai/*/requirements/team-notebooks-images.txt`) to stay on the pymilvus 2.x series until pymilvus 3.x stabilizes and provides cross-platform source distributions.
