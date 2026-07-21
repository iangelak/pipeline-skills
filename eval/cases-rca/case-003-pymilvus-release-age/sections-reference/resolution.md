**Recommended fix:** Constrain `langchain-milvus` to the 0.3.x series, which depends on `pymilvus<3.0,>=2.6.0` — a version range that fromager can resolve successfully.

**File: `collections/rhai/cpu-ubi9/requirements/team-notebooks-images.txt`**
```
langchain-milvus<0.4  # AIPCC-10403
```

Apply the same constraint to the other collections that list `langchain-milvus`:

**File: `collections/rhai/cuda12.9-ubi9/requirements/team-notebooks-images.txt`**
```
langchain-milvus<0.4  # AIPCC-10403
```

**File: `collections/rhai/cuda13.0-ubi9/requirements/team-notebooks-images.txt`**
```
langchain-milvus<0.4  # AIPCC-10403
```

**File: `collections/rhai/rocm7.1-ubi9/requirements/team-notebooks-images.txt`**
```
langchain-milvus<0.4  # AIPCC-10403
```

**File: `collections/rhai/rocm7.14-ubi9/requirements/team-notebooks-images.txt`**
```
langchain-milvus<0.4  # AIPCC-10403
```

This pins langchain-milvus to the latest 0.3.x release (currently 0.3.3), which uses `pymilvus<3.0,>=2.6.0`. The pymilvus 2.x series has stable sdist availability and is well past the release-age cooldown.

**Alternative: Bypass cooldown for pymilvus**

If upgrading to langchain-milvus 0.4.0 and pymilvus 3.x is desired, two changes are needed:

1. Add a cooldown bypass in the builder repo:

**File: `wheels/builder/overrides/settings/pymilvus.yaml`**
```yaml
resolver_dist:
  min_release_age: 0
```

2. Address the missing sdist — pymilvus 3.0.0 is published as a wheel-only package. This requires either waiting for upstream to publish an sdist, or adding a `pre_built: true` configuration to use the wheel directly.

This alternative has higher risk because pymilvus 3.x is a new major version with limited published artifacts. The `langchain-milvus<0.4` constraint is the safer short-term fix.

**Caveats**

The recommended fix does not address the underlying issue of unpinned top-level dependencies resolving to new major versions. If langchain-milvus 0.4.0 functionality is specifically needed, the alternative approach must be used, but it requires coordination with the pymilvus upstream to publish sdists.
