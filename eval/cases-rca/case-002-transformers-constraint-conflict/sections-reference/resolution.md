Remove or update the `transformers<5` constraint in the rhaiis cpu-ubi9 collection constraints file to accommodate vllm 0.24.0's requirement for `transformers>=5.6.0`.

**Option 1 (recommended): Remove the constraint**

**File: `collections/rhaiis/cpu-ubi9/constraints.txt`**
```
# Constrain packages we are patching to ensure reliable and repeatable build
```

The AIPCC-9443 constraint was added to enforce vllm's own `transformers<5` upper bound. Since vllm 0.24.0 now requires `transformers>=5.6.0`, the constraint is counterproductive and should be removed. The fromager resolver will use vllm's own specifier to determine the appropriate transformers version.

**Option 2: Update the constraint to allow transformers 5.x**

**File: `collections/rhaiis/cpu-ubi9/constraints.txt`**
```
# Constrain packages we are patching to ensure reliable and repeatable build

# Updated for vllm 0.24.0 which requires transformers>=5.6.0
transformers<6
```

This preserves a major-version upper bound to prevent unexpected major version jumps.

**Caveats**

- Verify that `transformers>=5.6.0` is available on PyPI. The error log shows PyPI had no match for `transformers>=5.6.0`, which may indicate that transformers 5.x has not yet been released. If so, the resolution requires either waiting for the transformers 5.x release or pinning vllm to a version compatible with transformers 4.x.
- Allowing transformers 5.x may require constraint updates in other collections that share the same builder infrastructure (check `torch-2.11.0` variant constraints).
- After updating the constraint, confirm that `compressed-tensors` and other vllm dependencies resolve correctly with the new transformers version.
