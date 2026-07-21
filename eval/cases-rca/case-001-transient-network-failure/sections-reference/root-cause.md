The bootstrap process failed due to a transient network disruption on the aarch64 CI runners. During package dependency resolution, HTTP connections to the upstream package index were severed mid-response, causing Python's urllib3 to raise an `IncompleteRead` exception. This exception was not caught by the bootstrap tool (fromager), so it propagated as a fatal error.

**Failure Chain**

1. The bootstrap process was resolving package dependencies by querying remote PyPI/GitLab package indexes over HTTP.
2. A network disruption on the aarch64 runner infrastructure caused the HTTP response to be truncated mid-transfer.
3. urllib3 raised `IncompleteRead` (a subclass of `HTTPError`), which is not covered by pip's built-in retry logic that handles `RemoteDisconnected` errors.
4. The fromager bootstrap process treated this as a fatal error and exited immediately.

**Supporting Evidence**

The CPU job (15189114549) showed earlier network instability — a `RemoteDisconnected` error for `charset_normalizer` at L2885 that was retried successfully via pip's retry mechanism:

```
L2885: 00:22:03 WARNING charset_normalizer: Retrying (Retry(total=7, connect=None, read=None, redirect=None, status=None)) after connection broken by 'RemoteDisconnected('Remote end closed connection without response')': /simple/charset-normalizer/
```

This confirms network instability was present on the runner before the fatal error occurred. The difference is that `RemoteDisconnected` (connection rejected before data transfer) triggers urllib3's retry logic, while `IncompleteRead` (connection broken during data transfer) does not.

The two jobs failed at different bootstrap progress points (77% for cpu, 84% for cuda12.9) and with different byte counts (228KB vs 1.1MB), confirming the error is non-deterministic and tied to transient network conditions rather than a specific package. Other aarch64 bootstrap jobs for smaller collections (torch-deps, rhaiis, onboarding, ogx, model-opt) succeeded in this same pipeline run, which is consistent with a transient issue — longer-running bootstraps for larger collections like `rhai-innovation` have more network requests and a higher probability of hitting a transient failure.
