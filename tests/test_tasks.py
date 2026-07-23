from datetime import date, timedelta

from tests.conftest import FUTURE_DUE_DATE

# --- POST /tasks ---

def test_create_task_valid_returns_201_with_full_body(client):
    r = client.post(
        "/tasks",
        json={"title": "write tests", "due_date": FUTURE_DUE_DATE},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["id"]
    assert body["title"] == "write tests"
    assert body["description"] == ""
    assert body["status"] == "ToDo"
    assert body["priority"] == "Medium"
    assert body["assignee"] is None
    assert body["created_at"]
    assert body["updated_at"]


def test_create_task_missing_title_returns_422(client):
    r = client.post(
        "/tasks",
        json={"description": "no title here", "due_date": FUTURE_DUE_DATE},
    )
    assert r.status_code == 422


def test_create_task_without_due_date_returns_201(client):
    r = client.post(
        "/tasks",
        json={"title": "task without due date"},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "task without due date"
    assert body["due_date"] is None


def test_create_task_blank_title_returns_422(client):
    r = client.post(
        "/tasks",
        json={"title": "   ", "due_date": FUTURE_DUE_DATE},
    )
    assert r.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    r = client.post(
        "/tasks",
        json={
            "title": "bad priority",
            "priority": "Urgent",
            "due_date": FUTURE_DUE_DATE,
        },
    )
    assert r.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    r = client.post(
        "/tasks",
        json={
            "title": "extra field",
            "foo": "bar",
            "due_date": FUTURE_DUE_DATE,
        },
    )
    assert r.status_code == 422


# --- GET /tasks ---

def test_list_tasks_empty_returns_200_and_empty_list(client):
    r = client.get("/tasks")
    assert r.status_code == 200
    assert r.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client, created_task):
    r = client.get("/tasks", params={"status": "Done"})
    assert r.status_code == 200
    assert r.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    client.post(
        "/tasks",
        json={"title": "low task", "priority": "Low", "due_date": FUTURE_DUE_DATE},
    )
    client.post(
        "/tasks",
        json={"title": "high task", "priority": "High", "due_date": FUTURE_DUE_DATE},
    )

    r = client.get("/tasks", params={"priority": "High"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["title"] == "high task"
    assert body[0]["priority"] == "High"


def test_list_tasks_filter_by_title_is_case_insensitive(client):
    client.post(
        "/tasks",
        json={"title": "Write docs", "due_date": FUTURE_DUE_DATE},
    )
    client.post(
        "/tasks",
        json={"title": "Ship feature", "due_date": FUTURE_DUE_DATE},
    )

    r = client.get("/tasks", params={"title": "write"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["title"] == "Write docs"


def test_list_tasks_filter_by_assignee_is_case_insensitive_exact(client):
    client.post(
        "/tasks",
        json={"title": "task one", "assignee": "Ada", "due_date": FUTURE_DUE_DATE},
    )
    client.post(
        "/tasks",
        json={"title": "task two", "assignee": "Grace", "due_date": FUTURE_DUE_DATE},
    )

    r = client.get("/tasks", params={"assignee": "ada"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["title"] == "task one"
    assert body[0]["assignee"] == "Ada"


def test_list_tasks_filter_by_due_date_returns_only_matches(client):
    matching_date = (date.today() + timedelta(days=8)).strftime("%d/%m/%Y")
    other_date = (date.today() + timedelta(days=9)).strftime("%d/%m/%Y")

    client.post(
        "/tasks",
        json={"title": "matching task", "due_date": matching_date},
    )
    client.post(
        "/tasks",
        json={"title": "other task", "due_date": other_date},
    )

    r = client.get("/tasks", params={"due_date": matching_date})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["title"] == "matching task"
    assert body[0]["due_date"] == matching_date


def test_list_tasks_filter_by_overdue_returns_only_overdue_items(client):
    client.post(
        "/tasks",
        json={"title": "overdue task", "due_date": (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")},
    )
    client.post(
        "/tasks",
        json={"title": "done task", "status": "Done", "due_date": (date.today() - timedelta(days=2)).strftime("%d/%m/%Y")},
    )
    client.post(
        "/tasks",
        json={"title": "future task", "due_date": (date.today() + timedelta(days=1)).strftime("%d/%m/%Y")},
    )

    r = client.get("/tasks", params={"overdue": True})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["title"] == "overdue task"


# --- GET /tasks/{id} ---

def test_get_task_by_id_returns_task(client, created_task):
    task_id = created_task["id"]
    r = client.get(f"/tasks/{task_id}")
    assert r.status_code == 200
    assert r.json()["id"] == task_id
    assert r.json()["title"] == "fixture task"


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    r = client.get("/tasks/does-not-exist")
    assert r.status_code == 404
    assert "detail" in r.json()


# --- PATCH /tasks/{id} ---

def test_patch_partial_update_keeps_other_fields(client, created_task):
    task_id = created_task["id"]
    r = client.patch(f"/tasks/{task_id}", json={"description": "updated desc"})
    assert r.status_code == 200
    body = r.json()
    assert body["description"] == "updated desc"
    assert body["title"] == created_task["title"]
    assert body["status"] == created_task["status"]
    assert body["priority"] == created_task["priority"]


def test_patch_not_found_returns_404(client):
    r = client.patch("/tasks/does-not-exist", json={"description": "nope"})
    assert r.status_code == 404


def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    task_id = created_task["id"]
    r = client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})
    assert r.status_code == 200
    assert r.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    task_id = created_task["id"]
    r = client.patch(f"/tasks/{task_id}", json={"status": "Done"})
    assert r.status_code == 422


def test_patch_task_from_done_back_to_todo_returns_422_for_invalid_transition(client, created_task):
    task_id = created_task["id"]

    setup_r = client.patch(f"/tasks/{task_id}", json={"status": "Done"})
    assert setup_r.status_code == 200

    r = client.patch(f"/tasks/{task_id}", json={"status": "ToDo"})
    assert r.status_code == 422
    assert "Invalid status transition" in r.json()["detail"]


def test_patch_same_status_returns_200_and_preserves_status(client, created_task):
    task_id = created_task["id"]
    r = client.patch(f"/tasks/{task_id}", json={"status": "ToDo", "description": "same status update"})
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ToDo"
    assert body["description"] == "same status update"


# --- DELETE /tasks/{id} ---

def test_delete_existing_returns_204_no_body(client, created_task):
    task_id = created_task["id"]
    r = client.delete(f"/tasks/{task_id}")
    assert r.status_code == 204
    assert r.content == b""


def test_delete_missing_returns_404(client):
    r = client.delete("/tasks/does-not-exist")
    assert r.status_code == 404
