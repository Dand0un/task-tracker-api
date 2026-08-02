# --- POST /tasks ---

def test_create_task_valid_returns_201_with_full_body(client):
    r = client.post("/tasks", json={"title": "write tests"})
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
    r = client.post("/tasks", json={"description": "no title here"})
    assert r.status_code == 422


def test_create_task_blank_title_returns_422(client):
    r = client.post("/tasks", json={"title": "   "})
    assert r.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    r = client.post("/tasks", json={"title": "bad priority", "priority": "Urgent"})
    assert r.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    r = client.post("/tasks", json={"title": "extra field", "foo": "bar"})
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
    client.post("/tasks", json={"title": "low task", "priority": "Low"})
    client.post("/tasks", json={"title": "high task", "priority": "High"})

    r = client.get("/tasks", params={"priority": "High"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["title"] == "high task"
    assert body[0]["priority"] == "High"


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


def test_patch_null_title_returns_422(client, created_task):
    task_id = created_task["id"]
    r = client.patch(f"/tasks/{task_id}", json={"title": None})
    assert r.status_code == 422


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
