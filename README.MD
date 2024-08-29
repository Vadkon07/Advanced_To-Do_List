# To-Do List Application
## Overview
This is **Advanced**, command-line-based To-Do List application written in Python. The program allows users to add, display, mark as done, sort, filter, delete tasks, create different users etc.. Each task can also have an optional deadline. The application stores all tasks of user in a data file, ensuring tasks persist between different sessions.

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

*maybe you will need to install some packages
```

## Requirements
- Python 3.x

## Future Improvements
1. - Implement auto-saving of tasks after every action to prevent data loss in case of an unexpected exit. IDEA FOR CODE: If something bad as **Ctrl + C** happens, app should read it before closing herself and run a def to save file.

2. **Advanced Filtering and Sorting:**
- Add options to filter tasks by status (done/not done), deadline, or priority.
- Enable sorting tasks by creation date, deadline, or priority

3. **Graphical User Interface (GUI):**
- Develop a GUI version using PyQt6 for better user interaction.

## Contributions
Contributions are welcome! If you have any suggestions, please open an issue or submit a pull request.
## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
