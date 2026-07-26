
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

**weak prompt**:Help me build add due date to my task tracker.
weak prompt does not tell the AI what to use and where to add the field, it suggested adding an new api to add a due date which i rejected

**Strong prompt**:

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
Why it is better

Specifies the exact file and models to modify.
States that the project already exists.
Specifies Pydantic v2.
Defines the validation rules.
Prevents unrelated changes.

AI response summary

The AI updated the TaskCreate and TaskUpdate models by adding a due_date field and implementing validation for past and invalid dates.

What I accepted

Added the due_date field.
Used Pydantic v2 validators.
Kept the existing models unchanged.

What I edited

The AI did not include due_date in the response model, so I created another prompt asking it to update TaskResponse.

What I rejected

I did not use the AI's earlier suggestion of creating a separate endpoint because the existing create/update endpoints already handled this functionality.

-------------
You are a senior Python backend engineer. Update the existing TaskResponse response model to include due_date, at first it added it without format then i adjusted the prompt to include the format i want:



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
AI response summary

The AI added due_date to the response model but returned it using the default date format.

Accepted

Adding the field to the response model.

Edited

I refined the prompt to require the dd/MM/yyyy format.

Rejected

The default date formatting.

Search + combined filters
-------------------------

**weak version** add filters to the get tasks list

Problem: The AI assumed filters should be added for every field, including description, and did not include the overdue filter.

**Strong version**

Strong version includes, planning first not directly changing code accepting each change seperately 

You are  a Senior python backend engineer 
PLan the possibility of adding  filters where the api search for task names, or  assignee or passed due dates or a specific due date. 

Do not change anything yet just plan the code keep the same structure.
 Use Pydantic v2 syntax only.
 ---------------------------
Why it is better

Requests planning before implementation.
Keeps the existing architecture.
Prevents unnecessary code changes.

AI response summary

The AI produced a step-by-step implementation plan covering models, routes, filtering logic, and testing.

Accepted

The incremental implementation plan.

Edited

Broke the work into smaller prompts for each file.

Rejected

Any suggestions outside the requested project structure.


**Add TaskFilter (Pydantic v2) in models.py**


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

AI response summary

The AI generated the TaskFilter model with the requested filter fields.

Accepted

Title search.
Assignee filter.
Due-date filter.
Overdue filter.

Rejected

Any additional models or unrelated changes.

**fix the layout**

at first AI generated the filter front end but the layout was not compatible with the project exiting design the spacing was to narrow.
 **weak prompt** fid the layout
 
**strong prompt**:
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
AI response summary

The AI updated the filter spacing and button layout without modifying the backend.

Accepted

Additional spacing.
Improved button alignment.

Edited

Minor CSS adjustments to better match the existing design.

Rejected

Any changes affecting other UI elements.
