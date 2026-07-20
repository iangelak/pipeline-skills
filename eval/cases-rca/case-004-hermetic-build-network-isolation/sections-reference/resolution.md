The aotriton Fromager plugin needs to ensure that all Python packages required by the cmake build (at minimum `filelock` and `numpy`) are pre-installed into the build virtual environment before the network-isolated cmake step runs.

**Option 1: Update the aotriton Fromager plugin** (`package_plugins/aotriton.py`)

Add a step in the `build_wheel` override that installs the cmake-time Python dependencies into the build venv before invoking cmake under network isolation:

```python
# In the build_wheel override, before cmake configure:
venv_pip = build_dir / "venv" / "bin" / "pip"
subprocess.run([str(venv_pip), "install", "filelock", "numpy"], check=True)
```

**Option 2: Patch aotriton's CMakeLists.txt**

Modify the cmake configuration to either:
- Skip the pip install when packages are already available in the venv
- Use pre-vendored copies of the required packages
- Install from local wheels instead of PyPI
