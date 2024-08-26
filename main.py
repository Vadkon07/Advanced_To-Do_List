import datetime
import os
import json

# ANSI escape sequences for color
COLOR_GREEN = '\033[92m'  # Green text
COLOR_RED = '\033[91m'    # Red text
COLOR_RESET = '\033[0m'   # Reset to default color

PRIORITY_COLORS = {
    'High': '\033[91m',    # Red
    'Medium': '\033[93m',  # Yellow
    'Low': '\033[92m'      # Green
}

FILE_NAME = "tasks.json"

def list_to_string(lst):
    tasks_str = ""
    for task in lst:
        tasks_str += (f"Task: {task['task']}, Status: {'Done' if task['done'] else 'Not Done'}, "
                      f"Date Created: {task['date']}, Deadline: {task['deadline']}, Priority: "
                      f"{PRIORITY_COLORS.get(task['priority'], '')}{task['priority']}{COLOR_RESET}\n")
    return tasks_str

def load_tasks_from_file(file_name):
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        with open(file_name, 'r') as file:
            return json.load(file)
    return []

def save_tasks_to_file(file_name, tasks):
    with open(file_name, 'w') as file:
        json.dump(tasks, file, indent=4)

def edit_task(tasks, task_index):
    print("Editing task...")
    new_task_description = input("Enter new task description (leave blank to keep unchanged): ")
    new_deadline = input("Enter new deadline (leave blank to keep unchanged): ")
    new_priority = input("Enter new priority (High, Medium, Low) or leave blank to keep unchanged: ")

    if new_task_description:
        tasks[task_index]['task'] = new_task_description
    if new_deadline:
        tasks[task_index]['deadline'] = new_deadline
    if new_priority:
        if new_priority not in ['High', 'Medium', 'Low']:
            print("Invalid priority. Keeping existing priority.")
        else:
            tasks[task_index]['priority'] = new_priority
    save_tasks_to_file(FILE_NAME, tasks)  # Auto-save after editing

def sort_tasks_by_priority(tasks):
    priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
    tasks.sort(key=lambda x: priority_order.get(x['priority'], 4))
    save_tasks_to_file(FILE_NAME, tasks)  # Auto-save after sorting

def main():
    # MAIN MENU
    while True:
        print("\n--- <<< To-Do List >>> ---")
        print("1. Add Task(s)")
        print("2. Show Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Edit Task")
        print("6. Sort Tasks by Priority")
        print("7. Exit")

        choice = input("Input your choice: ")

        if choice == '1':
            tasks = load_tasks_from_file(FILE_NAME)  # Load tasks from file before adding new ones
            n_tasks = int(input("How many tasks do you want to add?: "))

            for i in range(n_tasks):
                print(f"Adding task number {i + 1} of {n_tasks}...")
                task = input("Enter the task. If you want to stop adding more tasks, enter 'stop': ")

                if task.lower() == "stop":
                    break

                dt = datetime.datetime.today()
                date = dt.strftime('%Y-%m-%d %H:%M')

                deadline = input("Enter deadline for task (if none, enter 'none'): ")
                priority = input("Enter priority for task (High, Medium, Low): ").capitalize()

                if priority not in ['High', 'Medium', 'Low']:
                    print("Invalid priority. Setting priority to 'Low'.")
                    priority = 'Low'

                tasks.append({"task": task, "done": False, "date": date, "deadline": deadline, "priority": priority})
                print(f"Task '{task}' was added!")

            save_tasks_to_file(FILE_NAME, tasks)  # Auto-save after adding tasks

        elif choice == '2':
            tasks = load_tasks_from_file(FILE_NAME)  # Load tasks each time to show the most updated list
            print("\n===== Tasks =====")
            if not tasks:
                print("No tasks found. Enter '1' to add new task(s).")
            else:
                for index, task in enumerate(tasks):
                    status = "Done" if task["done"] else "Not Done"
                    color = COLOR_GREEN if task["done"] else COLOR_RED  # Choose color based on task status
                    print(f"{index + 1}. {task['task']} - {color}{status}{COLOR_RESET}. "
                          f"Date of creation: {task['date']} . Deadline: {task['deadline']} . Priority: "
                          f"{PRIORITY_COLORS.get(task['priority'], '')}{task['priority']}{COLOR_RESET}")

        elif choice == '3':
            tasks = load_tasks_from_file(FILE_NAME)  # Load tasks from file to mark the correct task as done
            task_index = int(input("Enter the task number to mark as done: ")) - 1
            if 0 <= task_index < len(tasks):
                tasks[task_index]["done"] = True
                print(f"Task '{tasks[task_index]['task']}' marked as done!")
                save_tasks_to_file(FILE_NAME, tasks)  # Auto-save after marking as done
            else:
                print("Invalid task number.")

        elif choice == '4':
            tasks = load_tasks_from_file(FILE_NAME)  # Load tasks from file to delete the correct task
            task_index = int(input("Enter the task number to delete: ")) - 1
            if 0 <= task_index < len(tasks):
                removed_task = tasks.pop(task_index)
                print(f"Task '{removed_task['task']}' has been deleted.")
                save_tasks_to_file(FILE_NAME, tasks)  # Auto-save after deleting
            else:
                print("Invalid task number.")

        elif choice == '5':
            tasks = load_tasks_from_file(FILE_NAME)  # Load tasks from file to edit
            task_index = int(input("Enter the task number to edit: ")) - 1
            if 0 <= task_index < len(tasks):
                edit_task(tasks, task_index)
                print(f"Task '{tasks[task_index]['task']}' has been updated.")
            else:
                print("Invalid task number.")

        elif choice == '6':
            tasks = load_tasks_from_file(FILE_NAME)  # Load tasks to sort
            sort_tasks_by_priority(tasks)
            print("Tasks have been sorted by priority.")

        elif choice == '7':
            print("Exiting the To-Do List...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
