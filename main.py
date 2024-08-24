import datetime
import os

# ANSI escape sequences for color
COLOR_GREEN = '\033[92m'  # Green text
COLOR_RED = '\033[91m'    # Red text
COLOR_RESET = '\033[0m'   # Reset to default color

def list_to_string(lst):
    tasks_str = ""
    for task in lst:
        tasks_str += f"Task: {task['task']}, Status: {'Done' if task['done'] else 'Not Done'}, Date Created: {task['date']}, Deadline: {task['deadline']}\n"
    return tasks_str

def load_tasks_from_file(file_name):
    tasks = []
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:  # Check if file exists and is not empty
        with open(file_name, 'r') as file:
            for line in file:
                task_data = line.strip().split(' , ')
                if len(task_data) == 4:
                    task, done, date, deadline = task_data
                    tasks.append({
                        "task": task,
                        "done": done == "Done",
                        "date": date,
                        "deadline": deadline
                    })
    return tasks

def save_tasks_to_file(file_name, tasks):
    with open(file_name, 'w') as file:
        for task in tasks:
            done_str = "Done" if task['done'] else "Not Done"
            file.write(f"{task['task']} , {done_str} , {task['date']} , {task['deadline']}\n")

def main():
    file_name = "report.txt"  # Use report.txt to load and save tasks

    # MAIN MENU
    while True:
        print("\n--- <<< To-Do List >>> ---")
        print("1. Add Task(s)")
        print("2. Show Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Input your choice: ")

        if choice == '1':
            print()
            tasks = load_tasks_from_file(file_name)  # Load tasks from file before adding new ones
            n_tasks = int(input("How many tasks do you want to add?: "))

            for i in range(n_tasks):
                print(f"Adding task number {i + 1} of {n_tasks}...")
                task = input("Enter the task. If you want to stop adding more tasks, enter 'stop': ")

                if task.lower() == "stop":
                    break

                dt = datetime.datetime.today()
                date = dt.strftime('%Y-%m-%d %H:%M')

                deadline = input("Enter deadline for task (if none, enter 'none'): ")

                tasks.append({"task": task, "done": False, "date": date, "deadline": deadline})
                print(f"Task '{task}' was added!")

            save_tasks_to_file(file_name, tasks)  # Save tasks back to file after adding

        elif choice == '2':
            tasks = load_tasks_from_file(file_name)  # Load tasks each time to show the most updated list
            print("\n===== Tasks =====")
            if not tasks:
                print("No tasks found. Enter '1' to add new task(s).")
            else:
                for index, task in enumerate(tasks):
                    status = "Done" if task["done"] else "Not Done"
                    color = COLOR_GREEN if task["done"] else COLOR_RED  # Choose color based on task status
                    print(f"{index + 1}. {task['task']} - {color}{status}{COLOR_RESET}. Date of creation: {task['date']} . Deadline: {task['deadline']}")

        elif choice == '3':
            tasks = load_tasks_from_file(file_name)  # Load tasks from file to mark the correct task as done
            task_index = int(input("Enter the task number to mark as done: ")) - 1
            if 0 <= task_index < len(tasks):
                tasks[task_index]["done"] = True
                print(f"Task '{tasks[task_index]['task']}' marked as done!")
                save_tasks_to_file(file_name, tasks)  # Save changes back to file
            else:
                print("Invalid task number.")

        elif choice == '4':
            tasks = load_tasks_from_file(file_name)  # Load tasks from file to delete the correct task
            task_index = int(input("Enter the task number to delete: ")) - 1
            if 0 <= task_index < len(tasks):
                removed_task = tasks.pop(task_index)
                print(f"Task '{removed_task['task']}' has been deleted.")
                save_tasks_to_file(file_name, tasks)  # Save changes back to file
            else:
                print("Invalid task number.")

        elif choice == '5':
            print("Exiting the To-Do List...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
