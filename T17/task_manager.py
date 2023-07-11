import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Load task data from text file
def load_tasks():
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        curr_t = {}
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)

    return task_list

# Saves task data to tasks.txt

def save_tasks(task_list):
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

# Loads user data from user.txt
def load_users():
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")
        user_data = [u for u in user_data if u != ""]

    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    return username_password

# Saves user data to user.txt
def save_users(username_password):
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_password:
            user_data.append(f"{k};{username_password[k]}")
        out_file.write("\n".join(user_data))

# Registers a new user
def reg_user():
    username_password = load_users()

    new_username = input("New Username: ")
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        if new_username in username_password.keys():
            print("Username already exists. Please choose a different username.")
            return
        username_password[new_username] = new_password
        save_users(username_password)
        print("New user added")
    else:
        print("Passwords do not match")

# Adds a new task
username_password = load_users()

def add_task():
    task_list = load_tasks()

    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            task_due_date = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
            
        except ValueError:
            print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")

    task_assigned_date = date.today()
    task_completed = False

    new_task = {
        'username': task_username,
        'title': task_title,
        'description': task_description,
        'due_date': task_due_date,
        'assigned_date': task_assigned_date,
        'completed': task_completed
    }

    task_list.append(new_task)
    save_tasks(task_list)
    print("Task added successfully.")

# Displays all the tasks
def view_all_tasks():
    task_list = load_tasks()
    print("All Tasks:")
    for task in task_list:
        print("Title:", task['title'])
        print("Description:", task['description'])
        print("Due Date:", task['due_date'].strftime(DATETIME_STRING_FORMAT))
        print("Assigned Date:", task['assigned_date'].strftime(DATETIME_STRING_FORMAT))
        print("Completed:", "Yes" if task['completed'] else "No")
        print("-------------------")

# Displays tasks assigned to a specific user
def view_user_tasks(username):
    task_list = load_tasks()
    print(f"Tasks assigned to {username}:")
    for task in task_list:
        if task['username'] == username:
            print("Title:", task['title'])
            print("Description:", task['description'])
            print("Due Date:", task['due_date'].strftime(DATETIME_STRING_FORMAT))
            print("Assigned Date:", task['assigned_date'].strftime(DATETIME_STRING_FORMAT))
            print("Completed:", "Yes" if task['completed'] else "No")
            print("-------------------")

# Generates reports
def generate_report():
    task_list = load_tasks()
    report_filename = input("Enter the filename for the report: ")
    with open(report_filename, 'w') as report_file:
        report_file.write("Task Report\n")
        report_file.write("------------\n\n")
        for task in task_list:
            report_file.write("Title: {}\n".format(task['title']))
            report_file.write("Description: {}\n".format(task['description']))
            report_file.write("Due Date: {}\n".format(task['due_date'].strftime(DATETIME_STRING_FORMAT)))
            report_file.write("Assigned Date: {}\n".format(task['assigned_date'].strftime(DATETIME_STRING_FORMAT)))
            report_file.write("Completed: {}\n".format("Yes" if task['completed'] else "No"))
            report_file.write("-------------------\n\n")
    print("Report generated successfully.")

# Displays the statistics
def display_statistics():
    username_password = load_users()
    task_list = load_tasks()

    num_users = len(username_password)
    num_tasks = len(task_list)

    print("Statistics:")
    print("Number of users:", num_users)
    print("Number of tasks:", num_tasks)
    print("-------------------")

# Runs the main program
def main():
    print("Welcome to the Task Manager")
    print("---------------------------")

    while True:
        print()
        print("Menu:")
        print("1. Register User")
        print("2. Add Task")
        print("3. View All Tasks")
        print("4. View User Tasks")
        print("5. Generate Report")
        print("6. Display Statistics")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            reg_user()
        elif choice == "2":
            add_task()
        elif choice == "3":
            view_all_tasks()
        elif choice == "4":
            username = input("Enter the username: ")
            view_user_tasks(username)
        elif choice == "5":
            generate_report()  # Call generate_report() function here
        elif choice == "6":
            display_statistics()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")

if __name__ == "__main__":
    main()
    