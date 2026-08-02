# Comments on Tasks Feature Plan

## 1. Data Model

Add comment schemas to [app/models.py](C:\Applications\AICourse\task-tracker-api\app\models.py), alongside the existing Pydantic task request/response models:

| Model | Fields and behavior |
|---|---|
| `CommentCreate` | `author` and `body` only; reject undeclared fields, matching `TaskCreate.model_config = ConfigDict(extra="forbid")`. |
| `CommentResponse` | `id`, `task_id`, `author`, `body`, and `created_at`. |

Validation should follow the task title convention in `app/models.py`: normalize input by trimming surrounding whitespace, then validate the normalized value. `author` must be 1–100 characters and `body` 1–2,000 characters. This makes whitespace-only values invalid.

Do not add a `comments` field to `TaskResponse`. [app/CLAUDE.md](C:\Applications\AICourse\task-tracker-api\app\CLAUDE.md) says not to change public response shapes without explicit approval; separate task-comment endpoints avoid changing existing task API responses.

In [app/storage.py](C:\Applications\AICourse\task-tracker-api\app\storage.py), add comment storage and helpers next to the existing module-level `_tasks` dictionary and CRUD helpers. The storage layer should generate `str(uuid4())` IDs and `datetime.now(timezone.utc)` timestamps, consistent with `add_task`.

## 2. API Routes

Add the routes directly in [app/main.py](C:\Applications\AICourse\task-tracker-api\app\main.py), which currently owns all FastAPI route handlers.

| Method and path | Request body | Success response | Error cases |
|---|---|---|---|
| `POST /tasks/{task_id}/comments` | JSON object containing `author` and `body` | `201 Created` with a `CommentResponse` | `404` when the task does not exist; `422` for missing, blank, over-limit, incorrectly typed, or unknown fields. |
| `GET /tasks/{task_id}/comments` | None | `200 OK` with a list of `CommentResponse` objects in creation order | `404` when the task does not exist. Return `[]` when the task exists but has no comments. |

The create route should verify that the task exists before storing the comment, making `task_id` a valid in-memory task reference. Both routes should use FastAPI response models, as the task routes already do.

No comment edit/delete endpoints are proposed in this first slice because the requested data contract specifies creation metadata only, and the repository has no authentication or ownership model.

## 3. Tests

Add comment API tests in a new [tests/test_comments.py](C:\Applications\AICourse\task-tracker-api\tests/test_comments.py), using the existing pytest/TestClient fixture style in [tests/conftest.py](C:\Applications\AICourse\task-tracker-api\tests\conftest.py) and the straightforward status/body assertions in [tests/test_tasks.py](C:\Applications\AICourse\task-tracker-api\tests\test_tasks.py).

### Happy path

- `test_create_comment_valid_returns_201_with_full_body`
- `test_create_comment_generates_uuid_and_utc_created_at`
- `test_list_comments_for_task_returns_200_and_empty_list`
- `test_list_comments_returns_only_comments_for_requested_task`
- `test_list_comments_returns_comments_in_creation_order`

### Validation

- `test_create_comment_missing_author_returns_422`
- `test_create_comment_blank_author_returns_422`
- `test_create_comment_author_at_100_characters_returns_201`
- `test_create_comment_author_over_100_characters_returns_422`
- `test_create_comment_missing_body_returns_422`
- `test_create_comment_blank_body_returns_422`
- `test_create_comment_body_at_2000_characters_returns_201`
- `test_create_comment_body_over_2000_characters_returns_422`
- `test_create_comment_unknown_field_returns_422`
- `test_create_comment_client_supplied_id_or_created_at_returns_422`

### Edge cases

- `test_create_comment_for_missing_task_returns_404_with_detail`
- `test_list_comments_for_missing_task_returns_404_with_detail`
- `test_create_comment_trims_author_and_body`
- `test_reset_storage_removes_comments_between_tests`
- `test_deleting_task_handles_associated_comments_according_to_selected_policy`

Update the autouse reset fixture in `tests/conftest.py` through the existing `storage._reset()` convention so comments cannot leak between tests.

No frontend test framework or frontend test files are visible in the repository, so browser-level automated test conventions are not confirmed.

## 4. Frontend Changes

Change [frontend/index.html](C:\Applications\AICourse\task-tracker-api\frontend\index.html), the repository’s only visible frontend artifact.

The current UI renders task cards through `renderTaskCard`, opens the existing task modal through `handleBoardClick`, and uses a single `task-form` for create/edit. Extend the edit-task experience to include a comments section for the selected task:

- Add a visible “Comments” action on each rendered task card, or distinguish the existing “Edit” action from a new comments action.
- When comments are opened for a task, request `GET /tasks/{task_id}/comments`.
- Display an empty state when none exist; otherwise show author, body, and a human-readable creation time in creation order.
- Add author and body inputs plus a submit control that calls `POST /tasks/{task_id}/comments`.
- Apply browser-side required/length feedback, while retaining server-response handling as the source of truth.
- After a successful submission, clear the comment body, refresh the displayed comments, and show any request failure in the existing error-feedback style.
- Escape comment author and body with the existing `escapeHtml` helper before rendering, consistent with task card rendering.
- Keep the current board loading, empty, error, populated, modal-close, and drag-and-drop status-update behaviors intact.

The existing `baseUrl`, `fetch`, error extraction, modal patterns, and inline CSS all live in this same file. No separate component, stylesheet, or frontend routing structure is visible.

## 5. Migration Notes

No database, ORM, migration tooling, or durable storage implementation is present in the actual runtime code. [app/storage.py](C:\Applications\AICourse\task-tracker-api\app\storage.py) stores tasks in a module-level dictionary and explicitly states state is lost on restart. Therefore, this feature requires an in-memory storage-shape extension, not a database migration.

Recommended storage shape:

- Keep tasks in the existing `_tasks` dictionary.
- Keep comments in a separate comment collection keyed by comment ID, with `task_id` on each comment; list helpers filter by `task_id`.
- Extend `_reset()` to clear both task and comment state.
- Preserve existing task response JSON exactly; comments are retrieved through their own endpoints.

Task deletion needs an explicit policy. If cascade deletion is selected, `delete_task` must remove associated comments from the in-memory store. If retention is selected, listing comments after task deletion needs a defined behavior. For this repository, cascade deletion is the simpler fit because a comment cannot have a valid task reference after task removal.

[README.md](C:\Applications\AICourse\task-tracker-api\README.md) mentions “optionally JSON-backed” storage, but the actual `app/storage.py` implementation contains no JSON persistence. JSON persistence and any corresponding migration behavior are not confirmed.

## 6. Open Questions

1. Should author/body whitespace be trimmed before validation and persistence, as task titles are, or should comment body whitespace be preserved verbatim?
2. Should deleting a task cascade-delete its comments, reject task deletion while comments exist, or retain comments separately?
3. Should comments be immutable in the initial release, or should edit/delete routes be included?
4. Should the comments experience be embedded in the existing edit-task modal, shown in a dedicated modal, or displayed inline on the board?
5. Should comments eventually appear in `GET /tasks/{task_id}` responses? This would change an existing public response shape and requires explicit approval under [app/CLAUDE.md](C:\Applications\AICourse\task-tracker-api\app\CLAUDE.md).
6. The repository has no authentication or authorization. Is free-text `author` acceptable for this learning-project scope, or should comments wait for an approved identity model?

# Files read

- [docs/AGENTS.md](C:\Applications\AICourse\task-tracker-api\docs\AGENTS.md)
- [app/CLAUDE.md](C:\Applications\AICourse\task-tracker-api\app\CLAUDE.md)
- [app/models.py](C:\Applications\AICourse\task-tracker-api\app\models.py)
- [app/main.py](C:\Applications\AICourse\task-tracker-api\app\main.py)
- [app/storage.py](C:\Applications\AICourse\task-tracker-api\app\storage.py)
- [app/business_rules.py](C:\Applications\AICourse\task-tracker-api\app\business_rules.py)
- [app/schemas/health.py](C:\Applications\AICourse\task-tracker-api\app\schemas\health.py)
- [tests/conftest.py](C:\Applications\AICourse\task-tracker-api\tests\conftest.py)
- [tests/test_tasks.py](C:\Applications\AICourse\task-tracker-api\tests\test_tasks.py)
- [frontend/index.html](C:\Applications\AICourse\task-tracker-api\frontend\index.html)
- [README.md](C:\Applications\AICourse\task-tracker-api\README.md)
- [docs/architecture-A.md](C:\Applications\AICourse\task-tracker-api\docs\architecture-A.md)
- [docs/user-stories.md](C:\Applications\AICourse\task-tracker-api\docs\user-stories.md)
- [docs/security-review.md](C:\Applications\AICourse\task-tracker-api\docs\security-review.md)
- [requirements.txt](C:\Applications\AICourse\task-tracker-api\requirements.txt)
- [.env.example](C:\Applications\AICourse\task-tracker-api\.env.example)

# Assumptions to verify

- The plan assumes the nested `/tasks/{task_id}/comments` route shape is acceptable.
- The plan recommends creation-order results; no existing comment-order convention exists.
- The plan recommends task-deletion cascade behavior; no repository rule currently defines it.
- The plan recommends trimmed author/body validation based on title behavior; body-whitespace preservation is not specified.
- The actual application code does not show JSON-backed storage, despite README wording; persistence beyond process memory is not confirmed.