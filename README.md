# pipeline-skills

Agentic-ci skills for AIPCC pipeline failure analysis — error grouping and root cause analysis.

## Overview

This plugin is the inner layer of the pipeline failure analysis system, the skills that run inside the Claude Code container. The outer layer (Python orchestration, GitLab CI, report assembly, Jira/Slack notifications) lives in [pipeline-failure-analyzer](https://github.com/opendatahub-io/pipeline-failure-analyzer) and [agentic-ci](https://github.com/opendatahub-io/agentic-ci) (generic CI framework).

### Skills

- **pipeline-grouping** — Groups failed pipeline jobs by error similarity using log analysis and Jira ticket deduplication
- **pipeline-rca** — Performs root cause analysis on a single error group, producing structured findings with error overview, diagnosis, and resolution guidance

## License

Apache-2.0
