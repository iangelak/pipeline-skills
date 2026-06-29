"""CLI-driven group builder for pipeline failure analysis.

The grouping sub-agent calls subcommands as tool invocations to build
grouping.json incrementally. Mutations go to a work file; finalize
validates completeness and writes the consumer-facing grouping.json.

Usage:
    uv run manage-groups.py add-group --state work.json --summary "..." --jobs id1,id2 --error "..."
    uv run manage-groups.py add-job   --state work.json --group 1 --job id3 --error "..."
    uv run manage-groups.py status    --state work.json --expected-jobs id1,id2,id3
    uv run manage-groups.py finalize  --state work.json --expected-jobs id1,id2,id3 --output grouping.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# --- Helpers ---


def load_state(path: Path) -> dict:
    """Load work file or return empty state."""
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"groups": {}}


def save_state(state: dict, path: Path) -> None:
    """Write state to work file."""
    path.write_text(
        json.dumps(state, indent=2, sort_keys=False) + "\n", encoding="utf-8"
    )


def assigned_jobs(state: dict) -> set[str]:
    """Return all job IDs currently assigned to any group."""
    result: set[str] = set()
    for g in state["groups"].values():
        result.update(g["job_ids"])
    return result


def next_key(state: dict) -> str:
    """Return the next sequential integer key for a new group."""
    if not state["groups"]:
        return "1"
    return str(max(int(k) for k in state["groups"]) + 1)


def parse_ids(raw: str) -> list[str]:
    """Parse comma-separated IDs, strip whitespace, deduplicate preserving order."""
    seen: set[str] = set()
    result: list[str] = []
    for item in raw.split(","):
        item = item.strip()
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def slugify(text: str, max_len: int = 60) -> str:
    """Convert text to a filesystem-friendly slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if len(slug) > max_len:
        slug = slug[:max_len].rsplit("-", 1)[0]
    return slug or "unnamed"


def store_expected(state: dict, raw: str | None) -> None:
    """Store expected job IDs in state if provided."""
    if raw:
        state["expected_jobs"] = parse_ids(raw)


def unassigned_msg(state: dict) -> str:
    """Return terse unassigned count, or empty string if expected jobs unknown."""
    expected = state.get("expected_jobs")
    if not expected:
        return ""
    n = len(set(expected) - assigned_jobs(state))
    return f"{n} unassigned"


# --- Subcommands ---


def cmd_add_group(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    store_expected(state, args.expected_jobs)

    job_ids = parse_ids(args.jobs)
    if not job_ids:
        print("error: --jobs requires at least one job ID", file=sys.stderr)
        return 1

    if not args.summary.strip():
        print("error: --summary must not be empty", file=sys.stderr)
        return 1

    # Validate against expected jobs (if known)
    expected = set(state.get("expected_jobs", []))
    if expected:
        unknown = set(job_ids) - expected
        if unknown:
            print(
                f"error: unknown job IDs: {', '.join(sorted(unknown))}", file=sys.stderr
            )
            return 1

    # Reject duplicates across groups
    existing = assigned_jobs(state)
    dupes = set(job_ids) & existing
    if dupes:
        locations = []
        for d in sorted(dupes):
            for gk, gv in state["groups"].items():
                if d in gv["job_ids"]:
                    locations.append(f"{d} (group {gk})")
                    break
        print(f"error: duplicate job IDs: {', '.join(locations)}", file=sys.stderr)
        return 1

    # Deduplicate error messages preserving order
    errors = list(dict.fromkeys(args.error)) if args.error else []

    key = next_key(state)
    state["groups"][key] = {
        "summary": args.summary.strip(),
        "job_ids": job_ids,
        "error_messages": errors,
    }
    save_state(state, args.state)

    msg = f"group {key}: {len(job_ids)} jobs, {len(errors)} errors"
    extra = unassigned_msg(state)
    print(f"{msg} | {extra}" if extra else msg)
    return 0


def cmd_add_job(args: argparse.Namespace) -> int:
    state = load_state(args.state)

    if args.group not in state["groups"]:
        print(f"error: group {args.group} does not exist", file=sys.stderr)
        return 1

    # Validate against stored expected jobs
    expected = set(state.get("expected_jobs", []))
    if expected and args.job not in expected:
        print(f"error: unknown job ID: {args.job}", file=sys.stderr)
        return 1

    # Reject duplicates
    if args.job in assigned_jobs(state):
        for gk, gv in state["groups"].items():
            if args.job in gv["job_ids"]:
                print(f"error: job {args.job} already in group {gk}", file=sys.stderr)
                return 1

    group = state["groups"][args.group]
    group["job_ids"].append(args.job)
    if args.error and args.error not in group["error_messages"]:
        group["error_messages"].append(args.error)
    save_state(state, args.state)

    msg = f"added job {args.job} to group {args.group}"
    extra = unassigned_msg(state)
    print(f"{msg} | {extra}" if extra else msg)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    if args.expected_jobs:
        store_expected(state, args.expected_jobs)
        save_state(state, args.state)

    groups = state["groups"]
    total = sum(len(g["job_ids"]) for g in groups.values())
    print(f"groups: {len(groups)} | jobs assigned: {total}")

    for key in sorted(groups, key=int):
        g = groups[key]
        print(
            f"  group {key}: {len(g['job_ids'])} jobs, "
            f"{len(g['error_messages'])} errors — {g['summary']}"
        )

    expected = set(state.get("expected_jobs", []))
    if expected:
        remaining = sorted(expected - assigned_jobs(state))
        if remaining:
            print(f"unassigned ({len(remaining)}): {', '.join(remaining)}")
        else:
            print("all jobs assigned")
    return 0


def cmd_finalize(args: argparse.Namespace) -> int:
    state = load_state(args.state)

    if not state["groups"]:
        print("error: no groups to finalize", file=sys.stderr)
        return 1

    expected = set(parse_ids(args.expected_jobs))
    if not expected:
        print(
            "error: --expected-jobs must contain at least one job ID", file=sys.stderr
        )
        return 1

    existing = assigned_jobs(state)

    # Reject assigned jobs that aren't in the expected set
    unknown = existing - expected
    if unknown:
        print(
            f"error: jobs not in expected set: {', '.join(sorted(unknown))}",
            file=sys.stderr,
        )
        return 1

    # Fail on unassigned jobs
    orphans = sorted(expected - existing)
    if orphans:
        print(
            f"error: {len(orphans)} unassigned jobs: {', '.join(orphans)}",
            file=sys.stderr,
        )
        for key in sorted(state["groups"], key=int):
            g = state["groups"][key]
            print(
                f"  group {key} ({len(g['job_ids'])} jobs): {g['summary']}",
                file=sys.stderr,
            )
        print("assign with add-job or add-group, then re-finalize", file=sys.stderr)
        return 1

    # Sort groups by smallest numeric job ID
    sorted_groups = sorted(
        state["groups"].values(),
        key=lambda g: min(int(j) for j in g["job_ids"]),
    )

    # Build final output with sequential slug IDs
    final = []
    for i, g in enumerate(sorted_groups, 1):
        final.append(
            {
                "id": f"{i:02d}-{slugify(g['summary'])}",
                "summary": g["summary"],
                "job_ids": sorted(g["job_ids"], key=int),
                "error_messages": g["error_messages"],
            }
        )

    output_path = Path(args.output)
    output_path.write_text(
        json.dumps({"groups": final}, indent=2) + "\n", encoding="utf-8"
    )

    total = sum(len(g["job_ids"]) for g in final)
    print(f"finalized: {len(final)} groups, {total} jobs → {output_path}")
    return 0


# --- Main ---


def main() -> int:
    parser = argparse.ArgumentParser(
        description="CLI-driven group builder for pipeline failure analysis.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # add-group
    p = sub.add_parser("add-group", help="Create a new group")
    p.add_argument("--state", type=Path, required=True, help="Work file path")
    p.add_argument("--summary", required=True, help="Group summary")
    p.add_argument("--jobs", required=True, help="Comma-separated job IDs")
    p.add_argument("--error", action="append", help="Error message (repeatable)")
    p.add_argument("--expected-jobs", help="Comma-separated expected job IDs")

    # add-job
    p = sub.add_parser("add-job", help="Add a job to an existing group")
    p.add_argument("--state", type=Path, required=True, help="Work file path")
    p.add_argument("--group", required=True, help="Group key")
    p.add_argument("--job", required=True, help="Job ID")
    p.add_argument("--error", help="Error message")

    # status
    p = sub.add_parser("status", help="Show current grouping state")
    p.add_argument("--state", type=Path, required=True, help="Work file path")
    p.add_argument("--expected-jobs", help="Comma-separated expected job IDs")

    # finalize
    p = sub.add_parser("finalize", help="Validate and write grouping.json")
    p.add_argument("--state", type=Path, required=True, help="Work file path")
    p.add_argument(
        "--expected-jobs", required=True, help="Comma-separated expected job IDs"
    )
    p.add_argument("--output", required=True, help="Output path for grouping.json")

    args = parser.parse_args()
    return {
        "add-group": cmd_add_group,
        "add-job": cmd_add_job,
        "status": cmd_status,
        "finalize": cmd_finalize,
    }[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
