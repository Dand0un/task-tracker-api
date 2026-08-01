# Governance Retrospective — AI-Assisted Coding

## What I Shared With AI

| Item | Module | Risk Level | Reason |
|------|--------|------------|--------|
| Task Tracker code | 2-5 | Medium | Shared only the relevant code needed for implementation and review. |
| Test output and stack traces | 2-4 | Low | Used to help identify bugs and understand failing tests. |
| Frontend code | 3 | Medium | Shared UI components to generate and review frontend logic. |
| Dockerfile and CI YAML | 4 | Medium | Shared build and deployment configuration to troubleshoot CI and Docker issues. |
| Any real external data I used by mistake | N/A | None | No production, customer, or confidential data was shared. |

## What I Received From AI

| GeneratedThing | Module | Do I Understand It Line by Line? | Action |
|---------------|--------|-----------------------------------|--------|
| Backend models and validators | 2 | Yes | Reviewed, tested, and adapted before committing. |
| Frontend board and drag-and-drop logic | 3 | Yes | Verified behavior manually and integrated only after understanding the implementation. even though am not frontend expert|
| CI workflow | 4 | Yes | Reviewed each step and validated it through pipeline execution before use. |
| Dockerfile | 4 | Yes | Built and tested locally before accepting the changes. |
| Security findings and plans | 5 | Yes | Used as recommendations only and validated each finding before acting on it. |
