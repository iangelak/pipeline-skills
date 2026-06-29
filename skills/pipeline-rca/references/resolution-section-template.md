# Resolution Section Template

Guide for writing `sections/resolution.md` — the suggested fix. Write this file when you can propose an actionable fix — code changes, configuration updates, constraint modifications, or operational steps. Set `has_resolution_file: true` in `finding.json`.

**When to omit**: Infrastructure failures (`runner_system_failure`, `stuck_or_timeout_failure`) or situations where no actionable fix exists. Set `has_resolution_file: false` in `finding.json`.

## Expected Content

1. **Recommended fix** — Actionable steps to resolve the failure. Before each code snippet or proposed change, specify the full file path being modified using canonical repository paths:

   **File: `<repo/path/to/file>`**
   ```<language>
   <proposed change>
   ```

2. **Alternatives** (optional) — If multiple approaches exist, list them with trade-offs. Indicate the recommended approach.

3. **Caveats** (optional) — Conditions, risks, or prerequisites for the fix. State explicitly if the fix has not been verified. Note if the fix may have side effects on other collections or variants.

## Guidelines

- Use canonical repository paths (stripped of `repositories/` prefix).
- Be specific about file locations — the reader should be able to apply the fix without searching.
- If the resolution involves constraint changes, specify the exact constraint file and the change needed.
- Use bold labels (`**Option 1: ...**`, `**Caveats**`) for all internal structure. Section files are embedded at different nesting depths across report templates, so headings would create hierarchy conflicts.

## Example

````
<Description of what to change and why>:

**File: `<canonical/path/to/file>`**
```
<proposed content>
```

<Explanation connecting the change to the root cause.>

**Caveats**

<Risks, prerequisites, or verification steps. State if the fix has not been tested. Note potential side effects on other collections or variants.>
````
