The `test-torch-2.10.0-rocm7.1-ubi9-x86_64-bootstrap-and-onboard` job failed during the bootstrap phase while building `aotriton` (a build-system dependency of `torch`).

The build was executed under Fromager's network isolation wrapper (`run_network_isolation.sh`), which blocks outbound network access. During cmake configure, the aotriton build attempted to pip-install dependencies from PyPI:

```error
L2313: WARNING: Retrying ... after connection broken by 'NewConnectionError(...: Failed to establish a new connection: [Errno -2] Name or service not known')': /simple/filelock/
L2318: ERROR: Could not find a version that satisfies the requirement filelock (from versions: none)
L2319: ERROR: No matching distribution found for filelock
```

The subsequent cmake code generation step failed because numpy was also unavailable:

```error
L2369: aotriton: ModuleNotFoundError: No module named 'numpy'
L2371: CMake Error at v3src/CMakeLists.txt:83 (execute_process)
```
