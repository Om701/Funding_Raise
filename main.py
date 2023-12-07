from User import User
from project import Project
from datetime import datetime
import json
import os


def register():
    print("Registration:")
    first_name = input("Enter your First Name: ")
    last_name = input("Enter your Last Name: ")
    email = input("Enter your Email: ")
    password = input("Enter your Password: ")
    phone_number = input("Enter your Phone (Egyptian number): ")

    user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "phone_number": phone_number
    }

    with open("users.txt", "a") as file:
        file.write(json.dumps(user_data) + "\n")

    print("Registration successful!")


def login():
    print("Login:")
    first_name = input("Enter your First Name: ")
    last_name = input("Enter your Last Name: ")
    full_name = f"{first_name} {last_name}"

    found_user = None

    if os.path.exists("users.txt"):
        with open("users.txt", "r") as file:
            for line in file:
                user_data = json.loads(line)
                if f"{user_data['first_name']} {user_data['last_name']}" == full_name:
                    found_user = User(**user_data)
                    print("Login successful!")
                    user_menu(found_user)
                    return found_user  # Moved the return statement inside the if block

    print("User not found. Please register first.")
    return None


def save_project_data(project):
    with open("projects.txt", "a") as file:
        project_data = {
            "title": project.title,
            "details": project.details,
            "target_amount": project.target_amount,
            "start_date": project.start_date.strftime('%d-%m-%Y'),
            "end_date": project.end_date.strftime('%d-%m-%Y'),
            "owner": {
                "first_name": project.owner.first_name,
                "last_name": project.owner.last_name,
                "email": project.owner.email,
                "password": project.owner.password,
                "phone_number": project.owner.phone_number
            }
        }
        file.write(json.dumps(project_data) + "\n")


def user_menu(user):
    while True:
        print(f"Welcome, {user.first_name} {user.last_name}!")
        print("User Menu:")
        print("1 - View all projects")
        print("2 - Edit your projects")
        print("3 - Delete your project")
        print("4 - Search for a project by date")
        print("5 - Create a new project")
        print("6 - Logout")

        user_choice = input("Choose an option: ")

        if user_choice == '1':
            view_all_projects(user)
        elif user_choice == '2':
            edit_user_projects(user)
        elif user_choice == '3':
            delete_user_project(user)
        elif user_choice == '4':
            search_project_by_date(user)
        elif user_choice == '5':
            create_new_project(user)
        elif user_choice == '6':
            print("Logging out. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

        # Add a newline for better readability
        print()


# Add a new function for creating a project
def create_new_project(user):
    print("Creating a new project:")
    title = input("Enter project title: ")
    details = input("Enter project details: ")
    target_amount = input("Enter target amount (EGP): ")
    start_date = input("Enter start date (dd-mm-yyyy): ")
    end_date = input("Enter end date (dd-mm-yyyy): ")

    # Validate the input and create the project
    # You can implement the validation logic here

    # For now, let's assume the validation passes
    project = Project(title, details, target_amount, start_date, end_date, user)
    user.projects.append(project)
    save_project_data(project)
    print("Project created successfully!")


def view_all_projects(self):
    # Load projects from the file
    all_projects = load_projects_from_file()

    if all_projects:
        print("All Projects:")
        for project in all_projects:
            print(f"Title: {project.title}, Target Amount: {project.target_amount} EGP")
    else:
        print("No projects available.")


def load_projects_from_file():
    projects = []

    try:
        with open("projects.txt", "r") as file:
            for line in file:
                project_data = json.loads(line)
                owner_data = project_data.pop("owner")
                owner = User(**owner_data)
                project = Project(owner=owner, **project_data)
                projects.append(project)
    except FileNotFoundError:
        # Handle file not found error
        pass

    return projects


def edit_user_projects(user):
    if user.projects:
        print("Your Projects:")
        for i, project in enumerate(user.projects, 1):
            print(f"{i} - Title: {project.title}, Target Amount: {project.target_amount} EGP")

        project_index = int(input("Select the project number to edit: ")) - 1

        if 0 <= project_index < len(user.projects):
            selected_project = user.projects[project_index]
            print(f"Editing project: {selected_project.title}")

            while True:
                print("Choose an option to edit:")
                print("1 - Edit Title")
                print("2 - Edit Details")
                print("3 - Edit Target Amount")
                print("4 - Edit End Date")
                print("5 - Finish Editing (Enter 'k')")

                edit_option = input("Enter your choice: ")

                if edit_option == '1':
                    selected_project.title = input("Enter the new title: ")
                elif edit_option == '2':
                    selected_project.details = input("Enter the new details: ")
                elif edit_option == '3':
                    selected_project.target_amount = float(input("Enter the new target amount: "))
                elif edit_option == '4':
                    selected_project.end_date = datetime.strptime(
                        input("Enter the new end date (dd-mm-yyyy): "), '%d-%m-%Y'
                    )
                elif edit_option.lower() == 'k':
                    print("Finished editing.")
                    break
                else:
                    print("Invalid option. Please try again.")
        else:
            print("Invalid project number.")
    else:
        print("No projects available to edit.")


def delete_user_project(user):
    if user.projects:
        print("Your Projects:")
        for i, project in enumerate(user.projects, 1):
            print(f"{i} - Title: {project.title}, Target Amount: {project.target_amount} EGP")

        project_index = int(input("Select the project number to delete: ")) - 1

        if 0 <= project_index < len(user.projects):
            deleted_project = user.projects.pop(project_index)
            save_projects_to_file(user.projects)  # Update the file after deletion
            print(f"Project '{deleted_project.title}' deleted.")
        else:
            print("Invalid project number.")
    else:
        print("No projects available to delete.")


def save_projects_to_file(projects):
    with open("projects.txt", "w") as file:
        for project in projects:
            project_data = {
                "title": project.title,
                "details": project.details,
                "target_amount": project.target_amount,
                "start_date": project.start_date.strftime('%d-%m-%Y'),
                "end_date": project.end_date.strftime('%d-%m-%Y'),
                "owner": {
                    "first_name": project.owner.first_name,
                    "last_name": project.owner.last_name,
                    "email": project.owner.email,
                    "password": project.owner.password,
                    "phone_number": project.owner.phone_number
                }
            }
            file.write(json.dumps(project_data) + "\n")


def search_project_by_date(user):
    if user.projects:
        search_date_str = input("Enter the date to search for projects (dd-mm-yyyy): ")
        try:
            search_date = datetime.strptime(search_date_str, '%d-%m-%Y')
            matching_projects = [project for project in user.projects if
                                  project.start_date <= search_date <= project.end_date]

            if matching_projects:
                print("Matching Projects:")
                for project in matching_projects:
                    print(f"Title: {project.title}, Target Amount: {project.target_amount} EGP")
            else:
                print("No projects match the specified date.")
        except ValueError:
            print("Invalid date format. Please enter a valid date.")
    else:
        print("No projects available to search.")


def main():
    user = None  # Initialize user to None

    while True:
        print("Welcome to the Fund raising App!")
        print("1 - Register")
        print("2 - Login")
        print("3 - Exit")

        initial_choice = input("Choose an option: ")

        if initial_choice == '1':
            register()
        elif initial_choice == '2':
            user = login()  # Set the user variable with the returned user
            if user:
                break  # Break out of the initial loop if login is successful
        elif initial_choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

    while user:  # Check if the user is logged in
        print(f"Welcome, {user.first_name} {user.last_name}!")
        print("User Menu:")
        print("1 - View all projects")
        print("2 - Edit your projects")
        print("3 - Delete your project")
        print("4 - Search for a project by date")
        print("5 - Create a new project")
        print("6 - Logout")

        user_choice = input("Choose an option: ")

        if user_choice == '1':
            view_all_projects(self)
        elif user_choice == '2':
            edit_user_projects(user)
        elif user_choice == '3':
            delete_user_project(user)
        elif user_choice == '4':
            search_project_by_date(self)
        elif user_choice == '5':
            create_new_project(user)
        elif user_choice == '6':
            print("Logging out. Goodbye!")
            user = None  # Set user to None to exit the user menu loop
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
