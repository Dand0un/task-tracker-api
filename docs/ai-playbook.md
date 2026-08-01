# Personal AI Coding Playbook

## When I reach for AI first

- I use AI for drafting or reviewing docs, brainstorming implementation options, generating boilerplate, and helping with debugging when I already understand the problem.
- I use it to save time, explore alternatives, and improve clarity, but I still make the final decision myself.

## When I do not reach for AI first

- I avoid AI for sensitive or high-risk work, especially anything involving secrets, private data, production credentials, or code I do not understand well enough to review.
- I also slow down when the task is about architecture decisions, security hardening, or anything where a wrong suggestion could create hidden risk.

## My non-negotiables

- I never paste credentials, tokens, or private customer data into AI tools.
- I review, test, and explain every AI suggestion before I accept it.
- I am responsible for the final result, so I do not rely on AI without verification.

## My review rules

- I check correctness, security, maintainability, and whether the change matches the repository scope.
- I run the relevant commands myself: tests, health checks, Docker checks, and diff review.
- If an AI suggestion seems vague, risky, or unnecessary, I reject it or rewrite it before using it.

## What I am still figuring out

- I am still learning when AI is most helpful for fast iteration and when it is better to solve something manually.
- I want to improve my prompting so I can get more useful, less noisy results from AI tools.

## Decision Card

- New feature: I may use AI for brainstorming and scaffolding, but I will verify the actual implementation myself.
- Code review: I use AI to spot likely issues, but I still inspect the diff and the surrounding code manually.
- Debugging: I use AI to suggest a hypothesis, then I verify it with the repo, tests, and runtime behavior.
- Infrastructure: I use AI for guidance, but I verify the workflow, Docker config, and commands directly.
- Never paste: secrets, credentials, environment values, or personal data.
