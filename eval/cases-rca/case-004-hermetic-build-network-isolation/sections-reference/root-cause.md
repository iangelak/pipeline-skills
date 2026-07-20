The aotriton package's cmake build process creates an internal Python virtual environment (`build/venv`) and uses pip to install runtime dependencies (`filelock`, `numpy`) into it during the configure phase. This pip invocation attempts to reach PyPI over the network. However, Fromager's `run_network_isolation.sh` blocks all outbound network access during the wheel build phase to enforce hermetic, reproducible builds.

**Failure Chain**

1. Fromager begins building `aotriton==0.11.2b0` as a build-system dependency of `torch==2.10.0`
2. The build is launched through `run_network_isolation.sh`, which disables network access
3. aotriton's cmake `CMakeLists.txt` creates a virtual environment and runs pip to install `filelock` and other packages
4. pip cannot reach PyPI (`Name or service not known`) and fails after exhausting retries
5. Without `filelock`, the subsequent `v3python.generate` module also fails because `numpy` was never installed either (`ModuleNotFoundError: No module named 'numpy'`)
6. cmake configure fails, which causes the wheel build to fail, which causes the bootstrap job to fail

**Why this is not transient**: The DNS failures occur inside Fromager's hermetic build sandbox, where network access is intentionally blocked. The fix requires updating the aotriton Fromager plugin or override to pre-install the required pip dependencies (`filelock`, `numpy`) into the build venv before entering network isolation, or patching aotriton's cmake to skip the pip invocation. Retrying the job will produce the same failure.
