# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI code review mini-log

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| CI should install dependencies explicitly and run pytest in a predictable way. | Useful | The workflow now installs requirements before testing and uses an explicit Python version. This is important for reproducible CI. | Confirmed by inspection of `.github/workflows/ci.yml`. |
| Docker should avoid leaking secrets and should run with a non-root user. | Useful | The Docker setup already excludes environment files and uses a dedicated `app` user at runtime. | Confirmed by inspection of `Dockerfile` and `.dockerignore`, and by a successful container run. |
| README should describe the actual health endpoint and the exact local/test/Docker commands. | Useful | The documentation should match what the repo actually provides. I kept the commands aligned with the verified app entry point and health endpoint. | Confirmed by comparing `README.md`, `app/main.py`, and local verification results. |

## AI security mini-review

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| Potential secret exposure from `.env` during container builds. | `.dockerignore` excludes `.env` and `.env.*`; `Dockerfile` does not copy environment files. | False Positive | The repository already avoids baking secrets into the image. | Keep the ignore rules in place and continue to avoid committing local env files. |
| The runtime container should not run as root. | `Dockerfile` creates an `app` user and uses `USER app`. | Valid | This is a real hardening improvement and was verified by inspection. | Keep the non-root runtime behavior. |
| The app should expose a simple health endpoint that can be verified from the container. | `app/main.py`, local and container health checks. | Valid | The `/health` path responded successfully during local and Docker verification. | Keep the endpoint documented and monitored during release checks. |

## Manual security check

I manually reviewed the CI workflow, Docker build context, and the repository documentation. I confirmed that the workflow does not use dangerous shortcuts such as `continue-on-error` or skipped pytest steps, that `.dockerignore` excludes `.env` files, and that the container runtime switches to a non-root user. This matters because it reduces the risk of accidental secret exposure and ensures the release process is more reproducible and safer to hand off.

## One AI output I rejected or corrected

One AI-style suggestion I did not accept as-is was to present the Docker verification as completed without a real container check. I corrected that by building the image, running the container, calling `/health`, and recording the actual response. I also rejected a generic “just use any Docker run command” approach and aligned the command with the repository’s real entry point and runtime behavior.

## Three AI usage rules

1. Never paste: credentials, API keys, `.env` contents, personal data, or private customer information into any AI tool.
2. Always verify: run the tests, confirm the app health endpoint, inspect the diff, and check the docs against the actual repository before accepting a suggestion.
3. Record AI contributions by: noting the file changed, the reason for the change, and whether the result was accepted, corrected, or rejected.

## Ownership statement

I am comfortable submitting this repository as my own work because I reviewed the app, verified the baseline behavior, and documented the evidence rather than accepting AI output blindly. I can explain the repository structure, the runtime commands, the CI workflow, and the Docker setup because I verified them directly in this environment. The changes I prepared are limited to documentation and evidence files, which keeps the work aligned with the course scope. I also checked that the repository remains focused on a small task-tracker API and does not introduce unrelated product features.
