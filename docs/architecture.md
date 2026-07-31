# Architecture-Document Context Strategy Comparison

## Strategy comparison

| Strategy | What it got right | What it got wrong, missed, or invented | Best suited task shape |
|---|---|---|---|
| **A — minimal context** | Concise but broad: covers the API, browser UI, in-memory storage, task fields, create flow, validation, status transitions, and key files. It also clearly separates unconfirmed areas in “Not visible or assumptions.” | Its confidence is uneven: it states detailed frontend behavior (modal close, list reload, optimistic drag-and-drop rollback), configuration behavior, test coverage, and status rules without marking them as source-limited. Its “not confirmed” wording conflicts with several earlier definitive assertions about files outside the core API. | A quick orientation document where a short, broad sketch is more valuable than carefully bounded detail. |
| **B — structured context** | Most complete and internally organized: it explains the API/UI split, task schemas and defaults, create request flow, architecture boundaries, status-transition policy, and the frontend/API contract. The key-file table is especially useful because each listed file has a distinct architectural role. | It does not include a “not visible” section, so readers cannot distinguish confirmed details from claims derived from the summaries. It makes highly specific claims about `app/business_rules.py`, `app/core/config.py`, and `app/frontend/index.html` without recording that limitation. | A final architecture document when structured summaries provide reliable coverage of the application’s main layers and supporting files. |
| **C — targeted context** | Most disciplined about evidence: it accurately describes the route/schema/storage path, validation, generated IDs and UTC timestamps, in-memory persistence, CORS configuration, and explicitly labels unseen implementations as “not visible from the files I read.” | It misses confirmed product-level behavior that A and B describe, including the static browser board, frontend create/update behavior, detailed status-transition rules, configuration details, and tests. Its “Key files” section names imported files but cannot explain them beyond the import relationship. | A bounded, evidence-first API-focused task—especially when the request requires avoiding unsupported claims or when only a few anchor files may be read. |

## Verdict

I would choose **Strategy B** for the final architecture document because it gives the most usable cross-layer description: it connects the FastAPI routes, task schemas, in-memory storage, status policy, configuration, and browser UI into one coherent explanation. Before treating it as final, I would retain Strategy C’s explicit uncertainty discipline: details drawn from summaries rather than directly inspected source should be marked as confirmed by the provided summary context, or moved into a “not visible or assumptions” section.

## Context-engineering rule

For a task that needs a complete, reader-facing architecture overview across API, storage, rules, configuration, and frontend, I use **Strategy B** because structured file summaries expose the relationships that a few anchor files omit.

For a tightly scoped, evidence-sensitive analysis of a single backend path, I use **Strategy C** because it supports precise claims while making every unobserved dependency explicit.
