# Decision Note

## Project Scope

The original Task Tracker supports creating, viewing, updating, and deleting tasks. Tasks are stored in memory, and users can filter them by status and priority.

Two additional features were added:

* Due dates with an overdue filter
* Search with combined filters

## 1. Due Dates and Overdue Filter

### Implementation

I added an optional `dueDate` field to each task. A task is considered overdue if its due date has passed and its status is not **Done**.

The existing task list endpoint was extended with an optional `overdue` filter that returns only overdue tasks.

### AI Suggestions

AI suggested several alternatives, including:

* Adding a separate **Overdue** status.
* Storing an `isOverdue` field.
* Using scheduled jobs to update overdue tasks automatically.

### Rejected Alternatives

These options were rejected because they added unnecessary complexity for a simple in-memory application. Calculating whether a task is overdue when filtering is simpler and always accurate.

---

## 2. Search with Combined Filters

### Implementation

I added a text search that matches task titles. The search can be combined with the existing filters, such as status, priority, assignee, and the overdue filter.

### AI Suggestions

AI suggested more advanced search features, including:

* Full-text search.
* Fuzzy matching.
* Searching both the title and description.

### Rejected Alternatives

These options were considered out of scope for a simple Task Tracker. Searching only the task title keeps the implementation straightforward while meeting the project requirements.

---

## Conclusion

The implementation focuses on keeping the application simple and easy to maintain while meeting the required functionality. More advanced AI suggestions were intentionally left out because they were beyond the scope of this project.
