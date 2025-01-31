import json
from enum import Enum

TASKS_FILE = "tasks.json"
tasks = []

class PriorityLevel(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class MenuOptions(Enum):
    DISPLAY = '1'
    ADD = '2'
    COMPLETE = '3'
    REMOVE = '4'
    QUIT = '5'


def load_tasks():
    """Load tasks from a JSON file."""
    global tasks
    try:
        with open(TASKS_FILE, 'r') as file:
            tasks.extend(json.load(file))
    except FileNotFoundError:
        tasks.clear()


def save_tasks():
    """Save tasks to a JSON file."""
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=2)


def display_tasks():
    """Display tasks sorted by priority and completion status."""
    if not tasks:
        print("Your to-do list is empty.")
        return

    # Sort tasks by priority and then by completion status
    sorted_tasks = sorted(tasks, key=lambda x: (x["completed"], x["priority"]))

    print("\nTo-Do List:")
    for i, task in enumerate(sorted_tasks, start=1):
        status = "Done" if task["completed"] else "Not Done"
        print(f"{i}. {task['task']} | Priority: {task['priority']} | Status: {status}")


def add_task():
    """Add a new task with priority to the list."""
    task_name = input("Enter the task: ").strip()
    if not task_name:
        print("Task name cannot be empty!")
        return

    priority = get_priority_level()
    tasks.append({"task": task_name, "completed": False, "priority": priority.value})
    save_tasks()
    print(f"Task '{task_name}' with priority '{priority.value}' added to your to-do list.")


def get_priority_level():
    """Get priority level from the user."""
    print("Select priority level:")
    for level in PriorityLevel:
        print(f"{level.value}: {level.name.capitalize()}")

    while True:
        choice = input("Enter priority (High/Medium/Low): ").strip().capitalize()
        if choice in PriorityLevel._member_names_:
            return PriorityLevel[choice]
        elif choice in [level.value for level in PriorityLevel]:
            return PriorityLevel(choice)
        else:
            print("Invalid priority. Please choose High, Medium, or Low.")


def mark_completed():
    """Mark a task as completed by its number."""
    if not tasks:
        print("No tasks available to mark as completed.")
        return

    display_tasks()
    try:
        task_number = int(input("Enter the task number to mark as completed: "))
        if 1 <= task_number <= len(tasks):
            task = tasks[task_number - 1]
            if task["completed"]:
                print(f"Task '{task['task']}' is already completed.")
            else:
                task["completed"] = True
                save_tasks()
                print(f"Task '{task['task']}' marked as completed.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


def remove_task():
    """Remove a task by its number."""
    if not tasks:
        print("No tasks available to remove.")
        return

    display_tasks()
    try:
        task_number = int(input("Enter the task number to remove: "))
        if 1 <= task_number <= len(tasks):
            removed_task = tasks.pop(task_number - 1)
            save_tasks()
            print(f"Task '{removed_task['task']}' removed from your to-do list.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


def main():
    """Main program loop to handle user choices."""
    load_tasks()
    while True:
        print("\nOptions:")
        print("1. Display to-do list")
        print("2. Add a task")
        print("3. Mark a task as completed")
        print("4. Remove a task")
        print("5. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == MenuOptions.DISPLAY.value:
            display_tasks()
        elif choice == MenuOptions.ADD.value:
            add_task()
        elif choice == MenuOptions.COMPLETE.value:
            mark_completed()
        elif choice == MenuOptions.REMOVE.value:
            remove_task()
        elif choice == MenuOptions.QUIT.value:
            print("Goodbye!")
            break
        else:
            print("Invalid choice, Please enter valid option")


if __name__ == "__main__":
    main()
