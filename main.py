import datetime

def list_to_string(lst):
    return " ".join(map(str, lst))

def main():
    tasks = []

#MAIN MENU
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
            task_query = 0;
            n_tasks = int(input("How many tasks do you want to add?: "))

            for i in range(n_tasks):
                print("Adding task number", task_query, " of ", n_tasks,"...")
                task = input("Enter the task. If you want to stop adding more tasks, enter 'stop': ")

                if task == "stop":
                    break
    
                dt = datetime.datetime.today()
                date = dt.strftime('%Y-%m-%d %H:%M')

                deadline = input("Enter deadline for task (if not, enter 'none'): ")

                tasks.append({"task": task, "done": False, "date": date, "deadline": deadline})

                print(f"Task '{task}' was added!")
                task_query = task_query + 1


        elif choice == '2':
            print("\n===== Tasks =====")
            for index, task in enumerate(tasks):
                status = "Done" if task["done"] else "Not Done"
                print(f"{index + 1}. {task['task']} - {status} . Date of creation: {task['date']} . Deadline: {task['deadline']}")

            if len(tasks) == 0:
                print("\nNo tasks. Enter '1' to add a new task(s).")

            else:
                print()

        elif choice == '3':
            task_index = int(input("Enter the task number to mark as done ")) - 1
            if 0 <= task_index < len(tasks):
                tasks[task_index]["done"] = True
                print(f"Task '{task['task']}' marked as done!")
            else:
                print("Invalid task number.")

        elif choice == '4':
            task_index = int(input("Enter the task number to delete: ")) - 1
            if 0 <= task_index < len(tasks):
                tasks.pop(task_index)


        elif choice == '5':
            if len(tasks) > 1:
                ask = input("Would you like to save your tasks in .txt file?(y/n): ")

                if ask == 'y':
                    print("Saved successfuly! Exiting the To-Do List...")
                    format_str = list_to_string(tasks)
                    text_file = open("report.txt", "w")
                    text_file.write(format_str)
                    text_file.close()
                    break

                else:
                    print("Not saved. Exiting the To-Do List...")
                    break
            else:
                print("Not saved. Exiting the To-Do List...")
                break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
