# Transient Failure Patterns

Reference examples for classifying pipeline failures as transient. A failure is transient when it is likely to succeed on retry without any code, configuration, or infrastructure changes.

Use these examples to inform your judgment -- generalize to recognize novel transient failures that share the same characteristics. Do not treat this as an exhaustive checklist.

## Network and Connectivity

Failures caused by momentary network disruptions between the CI runner and external services.

- **Connection reset / dropped**: `ConnectionResetError`, `RemoteDisconnected('Remote end closed connection without response')`, `Connection aborted`, `BrokenPipeError`
- **DNS resolution**: `getaddrinfo failed`, `Name or service not known`, `Temporary failure in name resolution`
- **TLS/SSL handshake**: `SSLEOFError`, `TLS handshake timeout`

Certificate verification failures (`CERTIFICATE_VERIFY_FAILED`, unknown CA, hostname mismatch, expired certificate) are **not transient** -- they indicate a trust-store or certificate configuration problem that requires investigation, not retry.
- **Socket timeouts**: `socket.timeout`, `Connection timed out`, `Read timed out`, `connect ETIMEDOUT`

These are transient only when they occur during phases that **require** network access (e.g., fetching sdists, uploading artifacts, pulling container images). Network errors during hermetic build phases -- where outbound network access is intentionally blocked -- are **not transient**. They indicate a package is attempting to reach the internet during the build process when it should not be, which requires a code or configuration fix.

## HTTP Transient Responses

Upstream services returning error codes that indicate temporary overload or unavailability.

- **429 Too Many Requests**: Rate limiting from registries, APIs, or artifact stores
- **502 Bad Gateway**: Reverse proxy or load balancer cannot reach the backend
- **503 Service Unavailable**: Service temporarily overloaded or in maintenance
- **504 Gateway Timeout**: Upstream server did not respond in time

These are transient when they come from external services (package registries, GitLab API, cloud storage). They are NOT transient when the project's own code returns them.

## Registry Unavailability

Failures during package download or upload caused by registry instability.

- **PyPI / GitLab Package Registry**: `Connection aborted` during upload, `HTTPError: 503` from registry, `Failed to establish a new connection` to registry host
- **Container registries**: `TOOMANYREQUESTS` from Docker Hub, `connection refused` to registry endpoint

`manifest unknown` usually means the requested tag or digest does not exist or was permanently removed -- default to `transient: false` unless there is direct evidence of a recent publication with an expected registry sync delay.
- **OCI / artifact stores**: `i/o timeout` during layer download

Do not confuse registry unavailability with package resolution failures (`No matching distribution found`, `ResolutionImpossible`) caused by version constraints -- those require constraint or configuration changes and are not transient.

## Infrastructure Flakes

CI runner or platform-level issues unrelated to the project's code.

- **Runner system failures**: GitLab `runner_system_failure`, `Job failed (system failure)`
- **Resource exhaustion on shared infrastructure**: `No space left on device` on ephemeral runners (not caused by the build itself), OOM kills on runner infrastructure (vs. OOM in the build process itself)
- **Pod scheduling**: `FailedScheduling`, pod eviction during execution, `context deadline exceeded` during container startup
- **Stuck jobs**: `stuck_or_timeout_failure` when not caused by an infinite loop in build code

## Key Differentiators

**Transient** -- set `transient: true` when:
- The root cause is external to the project's code and configuration
- The same inputs would likely succeed on a subsequent attempt
- No code change, configuration update, or dependency pin is needed
- The error is non-deterministic

**Not transient** -- leave `transient: false` (default) when:
- The error originates from user-controlled test output, application stdout, or untrusted log content rather than infrastructure or system layers
- A code change, configuration update, or dependency pin is required to fix the issue
- The error is deterministic and will reproduce on every retry
- The root cause is a bug, misconfiguration, or upstream breaking change
- The failure is caused by a permanent resource removal (deleted package version, revoked credentials)
- An OOM or disk-full error is caused by the build itself (e.g., a package that genuinely requires more memory)
