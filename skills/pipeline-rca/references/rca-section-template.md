# Root Cause Section Template

Guide for writing `sections/root-cause.md` — the failure diagnosis. This section explains **why** the error occurred — the underlying cause, contributing factors, and chain of events.

The Error Overview section (from `error-overview.md`) presents the error symptom with quoted log lines. This section focuses on analysis — refer to errors conceptually and quote only additional diagnostic log lines (e.g., earlier lines showing build step sequence, configuration loading, or dependency resolution).

## Expected Content

1. **Direct diagnosis** — Why the failure occurred, explained in terms a human engineer with project context would understand. Include what was being attempted, why it failed, and the underlying cause.

2. **Failure chain** (optional) — The dependency or build chain that led to the failure, if applicable. For dependency resolution errors, show the full chain. For build failures, show the build step sequence. Omit if the failure is straightforward with no chain.

3. **Variant-specific differences** (optional) — If affected jobs fail differently across variants or architectures, note the differences. Omit if all jobs fail identically.

4. **Caveats** (optional) — Uncertainties in the diagnosis, conditions that may affect accuracy, or analysis limitations (truncated logs, ambiguous errors, inaccessible resources). Omit entirely if the diagnosis is straightforward. State explicitly if the diagnosis might be wrong and why.

## Guidelines

- Focus on the first error in each log — later errors are cascading failures.
- Use canonical repository paths when referencing files (stripped of `repositories/` prefix).

## Example

````
<Direct diagnosis — why the failure occurred, the underlying cause, and contributing factors.>

**Failure Chain**

1. <Root event that initiated the failure>
2. <Intermediate cause or contributing factor>
3. <Resulting build/test/deploy failure>

<Additional context — where the relevant configuration is defined, why the issue arose, and how it connects to the failure.>
````
