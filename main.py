import datetime
import os
import json
import copy
import shutil
import re

# ANSI escape sequences for color
COLOR_GREEN = '\033[92m'  # Green text
COLOR_RED = '\033[91m'    # Red text
COLOR_RESET = '\033[0m'   # Reset to default color

PRIORITY_COLORS = {
    'High': '\033[91m',    # Red
    'Medium': '\033[93m',  # Yellow
    'Low': '\033[92m'      # Green
}

UNDO_STACK = {}
REDO_STACK = {}
USER_FILE_PREFIX = "tasks_"
BACKUP_FILE_PREFIX = "backup_"

def get_user_file_name(username):
    return f"{USER_FILE_PREFIX}{username}.json"

def get_backup_file_name(username):
    return f"{BACKUP_FILE_PREFIX}{username}.json"

def push_to_undo_stack(username, tasks):
    if username not in UNDO_STACK:
        UNDO_STACK[username] = []
    UNDO_STACK[username].append(copy.deepcopy(tasks))

def push_to_redo_stack(username, tasks):
    if username not in REDO_STACK:
        REDO_STACK[username] = []
    REDO_STACK[username].append(copy.deepcopy(tasks))

def clear_redo_stack(username):
    if username in REDO_STACK:
        REDO_STACK[username].clear()

def load_tasks_from_file(file_name):
    try:
        if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
            with open(file_name, 'r') as file:
                return json.load(file)
        return []
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading tasks: {e}")
        return []

def save_tasks_to_file(file_name, tasks):
    try:
        with open(file_name, 'w') as file:
            json.dump(tasks, file, indent=4)
    except IOError as e:
        print(f"Error saving tasks: {e}")

def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_priority(priority):
    return priority in ['High', 'Medium', 'Low']

def validate_recurrence(recurrence):
    return recurrence in ['Daily', 'Weekly', 'None']

def edit_task(tasks, task_index):
    print("Editing task...")
    new_task_description = input("Enter new task description (leave blank to keep unchanged): ")
    new_deadline = input("Enter new deadline (leave blank to keep unchanged): ")
    new_priority = input("Enter new priority (High, Medium, Low) or leave blank to keep unchanged: ")
    new_recurrence = input("Enter new recurrence (Daily, Weekly, None) or leave blank to keep unchanged: ")

    if new_task_description:
        tasks[task_index]['task'] = new_task_description
    if new_deadline and validate_date(new_deadline):
        tasks[task_index]['deadline'] = new_deadline
    if new_priority and validate_priority(new_priority):
        tasks[task_index]['priority'] = new_priority
    if new_recurrence and validate_recurrence(new_recurrence):
        tasks[task_index]['recurrence'] = new_recurrence

    save_tasks_to_file(get_user_file_name(current_user), tasks)  # Auto-save after editing

def sort_tasks(tasks, sort_by='priority'):
    priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
    if sort_by == 'priority':
        tasks.sort(key=lambda x: priority_order.get(x['priority'], 4))
    elif sort_by == 'date':
        tasks.sort(key=lambda x: x['date'])
    elif sort_by == 'deadline':
        tasks.sort(key=lambda x: x['deadline'] if x['deadline'] else '9999-12-31')
    save_tasks_to_file(get_user_file_name(current_user), tasks)  # Auto-save after sorting

def filter_tasks(tasks, filter_by='all', value=None):
    filtered_tasks = []
    for task in tasks:
        if filter_by == 'status':
            if value == 'done' and task['done']:
                filtered_tasks.append(task)
            elif value == 'not_done' and not task['done']:
                filtered_tasks.append(task)
        elif filter_by == 'deadline':
            if value and task['deadline'] == value:
                filtered_tasks.append(task)
        elif filter_by == 'priority':
            if value and task['priority'] == value:
                filtered_tasks.append(task)
        elif filter_by == 'recurrence':
            if value and task['recurrence'] == value:
                filtered_tasks.append(task)
        elif filter_by == 'all':
            filtered_tasks = tasks
    return filtered_tasks

def handle_recurring_tasks(tasks):
    today = datetime.datetime.today().date()
    for task in tasks:
        if task['recurrence'] == 'Daily':
            last_date = datetime.datetime.strptime(task['date'], '%Y-%m-%d').date()
            if (today - last_date).days >= 1:
                new_date = today.strftime('%Y-%m-%d')
                tasks.append({
                    'task': task['task'],
                    'done': False,
                    'date': new_date,
                    'deadline': task['deadline'],
                    'priority': task['priority'],
                    'recurrence': 'Daily'
                })
        elif task['recurrence'] == 'Weekly':
            last_date = datetime.datetime.strptime(task['date'], '%Y-%m-%d').date()
            if (today - last_date).days >= 7:
                new_date = today.strftime('%Y-%m-%d')
                tasks.append({
                    'task': task['task'],
                    'done': False,
                    'date': new_date,
                    'deadline': task['deadline'],
                    'priority': task['priority'],
                    'recurrence': 'Weekly'
                })

def backup_tasks(username):
    src_file = get_user_file_name(username)
    dst_file = get_backup_file_name(username)
    try:
        shutil.copy2(src_file, dst_file)
        print(f"Tasks have been backed up to {dst_file}.")
    except IOError as e:
        print(f"Error backing up tasks: {e}")

def restore_tasks(username):
    src_file = get_backup_file_name(username)
    dst_file = get_user_file_name(username)
    if os.path.exists(src_file):
        try:
            shutil.copy2(src_file, dst_file)
            print(f"Tasks have been restored from {src_file}.")
        except IOError as e:
            print(f"Error restoring tasks: {e}")
    else:
        print("No backup file found.")

def user_login():
    global current_user
    username = input("Enter your username: ")
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        print("Invalid username. Only alphanumeric characters and underscores are allowed.")
        return
    current_user = username
    if not os.path.exists(get_user_file_name(username)):
        with open(get_user_file_name(username), 'w') as file:
            json.dump([], file, indent=4)
    print(f"Logged in as {username}.")

def main():
    global current_user
    current_user = None

    # MAIN MENU
    while True:
        if not current_user:
            print("\n--- <<< To-Do List >>> ---")
            print("1. Login")
            print("2. Exit")

            choice = input("Input your choice: ")

            if choice == '1':
                user_login()
            elif choice == '2':
                print("Exiting the To-Do List...")
                break
            else:
                print("Invalid choice. Please try again.")
                continue

        print("\n--- <<< To-Do List >>> ---")
        print("1. Add Task(s)")
        print("2. Show Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Edit Task")
        print("6. Sort Tasks")
        print("7. Filter Tasks")
        print("8. Undo")
        print("9. Redo")
        print("10. Backup Tasks")
        print("11. Restore Tasks")
        print("12. Logout")
        print("13. Exit")

        choice = input("Input your choice: ")

        if choice == '1':
            tasks = load_tasks_from_file(get_user_file_name(current_user))  # Load tasks from file before adding new ones
            push_to_undo_stack(current_user, tasks)  # Save state before making changes
            clear_redo_stack(current_user)  # Clear redo stack on new action

            n_tasks = input("How many tasks do you want to add?: ")
            if not n_tasks.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            n_tasks = int(n_tasks)

            for i in range(n_tasks):
                print(f"Adding task number {i + 1} of {n_tasks}...")
                task = input("Enter the task. If you want to stop adding more tasks, enter 'stop': ")

                if task.lower() == "stop":
                    break

                dt = datetime.datetime.today()
                date = dt.strftime('%Y-%m-%d')

                deadline = input("Enter deadline for task (if none, enter 'none'): ")
                if deadline.lower() == 'none':
                    deadline = ""

                priority = input("Enter priority for task (High, Medium, Low): ").capitalize()
                if not validate_priority(priority):
                    print("Invalid priority. Setting priority to 'Low'.")
                    priority = 'Low'

                recurrence = input("Enter recurrence (Daily, Weekly, None): ").capitalize()
                if not validate_recurrence(recurrence):
                    print("Invalid recurrence. Setting recurrence to 'None'.")
                    recurrence = 'None'

                tasks.append({"task": task, "done": False, "date": date, "deadline": deadline, "priority": priority, "recurrence": recurrence})
                print(f"Task '{task}' was added!")

            save_tasks_to_file(get_user_file_name(current_user), tasks)  # Auto-save after adding tasks

        elif choice == '2':
            tasks = load_tasks_from_file(get_user_file_name(current_user))  # Load tasks each time to show the most updated list
            handle_recurring_tasks(tasks)  # Handle any recurring tasks
            print("\n===== Tasks =====")
            if not tasks:
                print("No tasks found. Enter '1' to add new task(s).")
            else:
                for index, task in enumerate(tasks):
                    status = "Done" if task["done"] else "Not Done"
                    color = COLOR_GREEN if task["done"] else COLOR_RED  # Choose color based on task status
                    print(f"{index + 1}. {task['task']} - {color}{status}{COLOR_RESET}. "
                          f"Date of creation: {task['date']} . Deadline: {task['deadline']} . Priority: "
                          f"{PRIORITY_COLORS.get(task['priority'], '')}{task['priority']}{COLOR_RESET}, "
                          f"Recurrence: {task['recurrence']}")

        elif choice == '3':
            tasks = load_tasks_from_file(get_user_file_name(current_user))  # Load tasks from file to mark the correct task as done
            push_to_undo_stack(current_user, tasks)  # Save state before making changes
            clear_redo_stack(current_user)  # Clear redo stack on new action

            task_index = input("Enter the task number to mark as done: ")
            if not task_index.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            task_index = int(task_index) - 1
            if 0 <= task_index < len(tasks):
                tasks[task_index]["done"] = True
                print(f"Task '{tasks[task_index]['task']}' marked as done!")
                save_tasks_to_file(get_user_file_name(current_user), tasks)  # Auto-save after marking as done
            else:
                print("Invalid task number.")

        elif choice == '4':
            tasks = load_tasks_from_file(get_user_file_name(current_user))  # Load tasks from file to delete the correct task
            push_to_undo_stack(current_user, tasks)  # Save state before making changes
            clear_redo_stack(current_user)  # Clear redo stack on new action

            task_index = input("Enter the task number to delete: ")
            if not task_index.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            task_index = int(task_index) - 1
            if 0 <= task_index < len(tasks):
                removed_task = tasks.pop(task_index)
                print(f"Task '{removed_task['task']}' has been deleted.")
                save_tasks_to_file(get_user_file_name(current_user), tasks)  # Auto-save after deleting
            else:
                print("Invalid task number.")

        elif choice == '5':
            tasks = load_tasks_from_file(get_user_file_name(current_user))  # Load tasks from file to edit
            push_to_undo_stack(current_user, tasks)  # Save state before making changes
            clear_redo_stack(current_user)  # Clear redo stack on new action

            task_index = input("Enter the task number to edit: ")
            if not task_index.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            task_index = int(task_index) - 1
            if 0 <= task_index < len(tasks):
                edit_task(tasks, task_index)
                print(f"Task '{tasks[task_index]['task']}' has been updated.")
            else:
                print("Invalid task number.")

        elif choice == '6':
            print("Sort by:")
            print("1. Creation Date")
            print("2. Deadline")
            print("3. Priority")
            sort_choice = input("Input your choice: ")
            if sort_choice == '1':
                sort_tasks(load_tasks_from_file(get_user_file_name(current_user)), sort_by='date')
            elif sort_choice == '2':
                sort_tasks(load_tasks_from_file(get_user_file_name(current_user)), sort_by='deadline')
            elif sort_choice == '3':
                sort_tasks(load_tasks_from_file(get_user_file_name(current_user)), sort_by='priority')
            else:
                print("Invalid choice. No sorting applied.")

        elif choice == '7':
            print("Filter by:")
            print("1. Status (Done/Not Done)")
            print("2. Deadline")
            print("3. Priority")
            print("4. Recurrence")
            filter_choice = input("Input your choice: ")
            value = input("Enter the value to filter by: ").capitalize()
            tasks = load_tasks_from_file(get_user_file_name(current_user))
            filtered_tasks = filter_tasks(tasks, filter_by={
                '1': 'status',
                '2': 'deadline',
                '3': 'priority',
                '4': 'recurrence'
            }.get(filter_choice, 'all'), value=value)
            print("\n===== Filtered Tasks =====")
            if not filtered_tasks:
                print("No tasks match the filter criteria.")
            else:
                for index, task in enumerate(filtered_tasks):
                    status = "Done" if task["done"] else "Not Done"
                    color = COLOR_GREEN if task["done"] else COLOR_RED  # Choose color based on task status
                    print(f"{index + 1}. {task['task']} - {color}{status}{COLOR_RESET}. "
                          f"Date of creation: {task['date']} . Deadline: {task['deadline']} . Priority: "
                          f"{PRIORITY_COLORS.get(task['priority'], '')}{task['priority']}{COLOR_RESET}, "
                          f"Recurrence: {task['recurrence']}")

        elif choice == '8':  # Undo
            if current_user in UNDO_STACK and UNDO_STACK[current_user]:
                tasks = load_tasks_from_file(get_user_file_name(current_user))
                push_to_redo_stack(current_user, tasks)
                tasks = UNDO_STACK[current_user].pop()
                save_tasks_to_file(get_user_file_name(current_user), tasks)
                print("Undo completed.")
            else:
                print("Nothing to undo.")

        elif choice == '9':  # Redo
            if current_user in REDO_STACK and REDO_STACK[current_user]:
                tasks = load_tasks_from_file(get_user_file_name(current_user))
                push_to_undo_stack(current_user, tasks)
                tasks = REDO_STACK[current_user].pop()
                save_tasks_to_file(get_user_file_name(current_user), tasks)
                print("Redo completed.")
            else:
                print("Nothing to redo.")

        elif choice == '10':
            backup_tasks(current_user)

        elif choice == '11':
            restore_tasks(current_user)

        elif choice == '12':
            current_user = None
            print("Logged out successfully.")

        elif choice == '13':
            print("Exiting the To-Do List...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
