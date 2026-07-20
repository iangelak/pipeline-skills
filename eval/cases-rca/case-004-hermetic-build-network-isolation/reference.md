The root cause is that aotriton's cmake build process attempts to pip-install dependencies (filelock, numpy) from PyPI during the configure phase, but the build runs under Fromager's `run_network_isolation.sh` which intentionally blocks all outbound network access to enforce hermetic, reproducible builds.

The DNS resolution failures (`Name or service not known`) are NOT transient -- they are the expected behavior of the network isolation sandbox. Retrying the job will produce the same failure. The fix requires updating the aotriton Fromager plugin to pre-install the required pip dependencies into the build venv before entering network isolation, or patching aotriton's CMakeLists.txt to avoid the pip invocation.

This is an adversarial case for transient classification: the error pattern (DNS failures, connection errors) matches typical transient network symptoms, but the hermetic build context makes this a deterministic, non-transient failure requiring a code change.
