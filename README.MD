# To-Do List Application
## Overview
This is a simple command-line-based To-Do List application written in Python. The program allows users to add, display, mark as done, and delete tasks. Each task can also have an optional deadline. The application stores all tasks in a text file (`report.txt`), ensuring tasks persist between different sessions.

## Features
- **Add Tasks:** Add new tasks with an optional deadline.
- **Show Tasks:** Display all tasks with their status (Done/Not Done), creation date, and deadline.
- **Mark Tasks as Done:** Mark tasks as completed.
- **Delete Tasks:** Remove tasks from the list.
- **Persistent Storage:** All tasks are saved to a text file (`report.txt`), ensuring data is not lost when the program is closed.

## How to Use
1. **Clone the Repository**
```console
git clone https://github.com/Vadkon07/Advanced_To-Do_List.git
cd Advanced_To-Do_List
```
2. **Run the Program**
```console
python3 main.py 
```
3. **Main Menu Options**
- **Add Task(s):** Enter the number of tasks you wish to add. Follow the prompts to enter task details and deadlines.
- **Show Tasks:** Display the current list of tasks, along with their status, creation date, and deadline.
- **Mark Task as Done:** Enter the number of the task you want to mark as done.
- **Delete Task:** Enter the number of the task you want to delete.
- **Exit:** Save tasks to `report.txt` and exit the program.

## Requirements
- Python 3.x

## Future Improvements
1. **Improve User Interface:** [DONE]
- Add color coding for task statuses (e.g., green for done, red for not done).
- Include more descriptive prompts and error messages. 
2. **Enhanced Task Management:** [DONE]
- Allow users to edit task descriptions and deadlines.
- Add priorities to tasks (high, medium, low) and enable sorting based on priority.
3. **Data Storage Enhancements:** [DONE]
- Use a more structured data format (like JSON or CSV) for storing tasks instead of plain text, allowing for easier data manipulation and expansion.
- Implement auto-saving of tasks after every action to prevent data loss in case of an unexpected exit.
4. **Advanced Filtering and Sorting:** 
- Add options to filter tasks by status (done/not done), deadline, or priority.
- Enable sorting tasks by creation date, deadline, or priority.
5. **Recurring Tasks:** [DONE]
- Add functionality to handle recurring tasks (e.g., daily, weekly).
6. **Undo/Redo Feature:** [DONE]
- Implement an undo/redo feature to allow users to revert actions easily.
7. **Graphical User Interface (GUI):**
- Develop a GUI version using libraries such as Tkinter or PyQt for better user interaction.
8. **Testing and Error Handling:** [DONE]
- Add unit tests to ensure program reliability and correctness.
- Improve error handling for user inputs and file operations.
9. **Multi-User Support:** [DONE]
- Implement support for multiple users, allowing each user to have their own separate task list.
10. **Backup and Restore Functionality:** [DONE]
- Add functionality to back up the tasks to a different file and restore from backups in case of data corruption or accidental deletions.
## Contributions
Contributions are welcome! If you have any suggestions, please open an issue or submit a pull request.
## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.