
add Due dates
-------------

You are helping me work inside my existing FastAPI project .

Explain the existing create endpoint in this file.
Please include:
1. The route path and HTTP method.
2. What the route returns.
3. Whether it uses the existing FastAPI app instance.
4. One simple command or browser check I can use to verify it returns HTTP 200.
Do NOT suggest code changes yet. I only want to confirm that you can read the real file.

--------------------

You are a senior Python backend engineer. Update the existing TaskCreate and TaskUpdate Models to support due_date

Context:
- This project currently has a working routes endpoints.
- This module uses in-memory storage only.

============================================================
FILE 1 - app/models.py
============================================================
Use Pydantic v2 syntax only.

Add due_date: date with date format(dd/MM/yyyy) to these existing models:
1. TaskCreate
- Include a field_validator for due_date that  rejects past date(date must be greater than now), and rejects invalid date (ex 31/02) .
-- DO NOT include any new fields do not change any existing field.
2. TaskUpdate
- use the same due_date validator behavior only when due_date is provided.
- DO NOT include any new fields do not change any existing field.
- DO NOT change any of the other existing models 

-----------------
it did not include the due date in the response

-------------
You are a senior Python backend engineer. Update the existing TaskResponse response model to include due_date

Context:
- This project currently has a working routes endpoints.
- This module uses in-memory storage only.


Use Pydantic v2 syntax only.


1. TaskCreate
-- Add due_date to the task creation endpoint response with the same format of the request model (dd/MM/yyyy):
-- DO NOT include any new fields do not change any existing field.
2. TaskUpdate
- -- Add due_date to the task update endpoint response with the same format of the request model (dd/MM/yyyy):

- DO NOT include any new fields do not change any existing field.
- DO NOT change any of the other existing models 

-------------

Search + combined filters
-------------------------
You are  a Senior python backend engineer 
PLan the possibility of adding  filters where the api search for task names, or  assignee or passed due dates or a specific due date. 

Do not change anything yet just plan the code keep the same structure.
 Use Pydantic v2 syntax only.
 ---------------------------


Add TaskFilter (Pydantic v2) in models.py


You are a senior Python backend engineer. Add TaskFilter (Pydantic v2) in models.py

Context:
- This project currently has a working routes endpoints.
- This module uses in-memory storage only.


Use Pydantic v2 syntax only.

add the TaskFilter model
1. TaskFilter

Params:
- title: str | None ,Case-insensitive substring match on task.title (name search)
- assignee:  str | None,  Exact match on task.assignee (or case-insensitive exact — pick one and stick to it)
- due_date date | None, Exact match: task.due_date == due_date
- overdue  bool | None, When true: task.due_date < date.today() and preferably status != Done

- DO NOT include any new models do not change any existing models.
- DO NOT change any of the other existing models

  --------------------------------------------------------------------


  Before writing code, give me an incremental plan for building this feature in small Copilot/Codex loops.
Feature: [add a filter on the top to allow the filter by
- title: str | None ,Case-insensitive substring match on task.title (name search)
- assignee:  str | None,  Exact match on task.assignee (or case-insensitive exact — pick one and stick to it)
- due_date date | None, Exact match: task.due_date == due_date
- overdue  bool | None, When true: task.due_date < date.today() and preferably status != Done]

Output format:
Return a table with columns: Step, File or selection, What changes, How I verify it.

Constraints:
- Do not write code yet.
- Keep the plan aligned with Module 3: small changes, inspect the diff, run the app or tests, then refine.
- Do not introduce frameworks, new backend features, or unrelated files
------------------------------------------------------------
fix the layout

fix the filter layout in frontend/index.html.
Context:
- frontend index.html

- add some space between the filter and the cards
-fix the clear and apply buttons layout
Task:
-  add some space between the filter and the cards without changing how they look
- fix the clear and apply buttons layout make compatible with entire look similar to the create task button
Constraints:

- Do not change the look of any other element.
- Do not change the backend.
