# AI Reflection

To implement the two new features—**due dates with an overdue filter** and **search with combined filters**—I used different AI tools for different parts of the project.

For planning, I used **ChatGPT** to generate the user stories and acceptance criteria. It helped me quickly create well-structured stories that covered both the expected behavior and failure cases. This saved time compared to writing them manually and ensured the requirements were clear before implementation.

For the backend, I used **Cursor** to help implement the new API functionality. It generated most of the code for adding due dates and extending the filtering logic. For the frontend, I used **Visual Studio Code with GitHub Copilot** to update the user interface by adding the due date field and the new search and filter controls.

One situation where AI was particularly helpful was during the requirements phase. ChatGPT generated the user stories much faster than I could have written them myself while keeping them consistent and complete. This allowed me to focus more on implementing the features instead of spending time formatting and refining the requirements.

One situation where AI slowed me down was during the backend implementation. I only needed to add the due date field to the API response, but explaining the exact change in a prompt took longer than simply writing the code myself. For such a small modification, using AI was less efficient than making the change directly.

Although the AI-generated code provided a good starting point, I still reviewed and refined the results. On the frontend, the first version added the due date to the task creation form but did not display it on the task cards. I updated the interface so users could see the due date for each task. The initial filter layout also did not match the existing design of the application, so I adjusted the styling and placement to keep the interface consistent. These changes improved both the usability and the appearance of the application.

Overall, AI was most valuable for generating requirements and producing an initial implementation. However, reviewing the generated code and making manual improvements was necessary to ensure the final solution met both the functional requirements and the expected user experience.
