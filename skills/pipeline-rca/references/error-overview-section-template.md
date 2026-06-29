# Error Overview Section Template

Guide for writing `sections/error-overview.md` — the error symptom. Present the error as it appears to an engineer reading the logs — what went wrong, shown through the actual error messages. The Root Cause Analysis section covers the "why."

## Expected Content

1. **Brief narrative** (1-3 sentences) — Describe what failed and the visible symptom, in terms an engineer scanning the report would immediately understand.

2. **Quoted error messages** — The key error lines from the logs, using ` ```error ` fenced blocks (not plain ` ``` `) for distinct error styling in the HTML report. Include enough context to show the error clearly (typically 2-8 lines). Use `L<num>:` line number prefixes when available.

3. **Additional context** (optional, 1-2 sentences) — Brief clarification connecting the quoted errors if needed. Keep minimal — deeper analysis belongs in `root-cause.md`.

## Guidelines

- Keep it concise — typically 5-20 lines total. The reader should grasp the error in seconds.
- Quote the PRIMARY error, not cascading failures. If there is a wrapper error and an inner error, quote both.

## Example

````
<Brief description of what failed and the visible symptom>:

```error
<primary error message from the log, with L-prefixed line numbers if available>
<supporting context or inner error>
```

<Optional: brief additional context connecting the error to the broader situation, if not self-evident from the quotes.>
````
