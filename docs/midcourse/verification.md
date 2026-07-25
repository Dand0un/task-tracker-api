================================= test session starts =================================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Applications\AICourse\task-tracker-api
configfile: pytest.ini
plugins: anyio-4.14.1
collected 23 items                                                                     

tests\test_tasks.py ............F......F...                                      [100%]

====================================== FAILURES =======================================
____________ test_list_tasks_filter_by_overdue_returns_only_overdue_items _____________

client = <starlette.testclient.TestClient object at 0x000001FD78388C00>

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
>       assert len(body) == 1
E       assert 0 == 1
E        +  where 0 = len([])

tests\test_tasks.py:180: AssertionError
______ test_patch_task_from_done_back_to_todo_returns_422_for_invalid_transition ______

client = <starlette.testclient.TestClient object at 0x000001FD7818F460>
created_task = {'id': '108d381c-1cee-4cc7-ac4f-062606278082', 'title': 'fixture task', 'description': '', 'status': 'ToDo', ...}

    def test_patch_task_from_done_back_to_todo_returns_422_for_invalid_transition(client, created_task):
        task_id = created_task["id"]
    
        setup_r = client.patch(f"/tasks/{task_id}", json={"status": "Done"})
>       assert setup_r.status_code == 200
E       assert 422 == 200
E        +  where 422 = <Response [422 Unprocessable Entity]>.status_code

tests\test_tasks.py:235: AssertionError
================================== warnings summary ===================================
venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Applications\AICourse\task-tracker-api\venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422
tests/test_tasks.py::test_patch_task_from_done_back_to_todo_returns_422_for_invalid_transition
  C:\Applications\AICourse\task-tracker-api\app\main.py:74: StarletteDeprecationWarning: 'HTTP_422_UNPROCESSABLE_ENTITY' is deprecated. Use 'HTTP_422_UNPROCESSABLE_CONTENT' instead.
    validate_status_transition(existing.status, payload.status)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================== short test summary info ===============================
FAILED tests/test_tasks.py::test_list_tasks_filter_by_overdue_returns_only_overdue_items - assert 0 == 1
FAILED tests/test_tasks.py::test_patch_task_from_done_back_to_todo_returns_422_for_invalid_transition - assert 422 == 200
====================== 2 failed, 21 passed, 3 warnings in 1


after fix test:


=============================== short test summary info ===============================
FAILED tests/test_tasks.py::test_list_tasks_filter_by_overdue_returns_only_overdue_items - assert 0 == 1
FAILED tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422 - assert 200 == 422
====================== 2 failed, 21 passed, 2 warnings in 1.10s =======================
(venv) PS C:\Applications\AICourse\task-tracker-api> pytest tests/test_tasks.py
================================= test session starts =================================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Applications\AICourse\task-tracker-api
configfile: pytest.ini
plugins: anyio-4.14.1
collected 23 items                                                                     

tests\test_tasks.py .......................                                      [100%]

================================== warnings summary ===================================
venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Applications\AICourse\task-tracker-api\venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422
tests/test_tasks.py::test_patch_task_from_done_back_to_todo_returns_422_for_invalid_transition
  C:\Applications\AICourse\task-tracker-api\app\main.py:74: StarletteDeprecationWarning: 'HTTP_422_UNPROCESSABLE_ENTITY' is deprecated. Use 'HTTP_422_UNPROCESSABLE_CONTENT' instead.
    validate_status_transition(existing.status, payload.status)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== 23 passed, 3 warnings in 0.89s ============================
