The root cause is a transient network disruption on aarch64 runners. The HTTP connection was broken mid-transfer with an `IncompleteRead` error during package resolution, causing the fromager bootstrap to fail fatally. Both affected jobs ran on aarch64 runners and failed with the same network error pattern.

This is an infrastructure issue, not a code defect. The network disruption was transient — retrying the affected jobs should resolve the failure. No code changes are needed, and no resolution file should be produced.

The confidence is high because the error message directly names the failure mechanism (IncompleteRead / ConnectionError during HTTP transfer) and both jobs exhibit the same pattern on the same architecture, consistent with a localized network issue on the aarch64 runner pool.
