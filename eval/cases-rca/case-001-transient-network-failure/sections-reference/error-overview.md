The bootstrap-and-onboard action for the `rhai-innovation` collection failed on two aarch64 jobs (cpu and cuda12.9 variants) when an HTTP connection was severed mid-transfer during package resolution, producing an `IncompleteRead` error:

```error
L3582: 00:22:18 ERROR ('Connection broken: IncompleteRead(228449 bytes read, 185764 more expected)', IncompleteRead(228449 bytes read, 185764 more expected))
```

```error
L5526: 00:30:08 ERROR ('Connection broken: IncompleteRead(1144989 bytes read, 344486 more expected)', IncompleteRead(1144989 bytes read, 344486 more expected))
```

The error terminated the bootstrap process immediately with no retry, triggering cleanup (nginx shutdown) and job failure.
