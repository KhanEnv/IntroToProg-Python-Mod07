# ==========================================================================================
# Title: Assignment07
# Desc: This assignment demonstrates using data classes (Person & Student) with
#       functions, JSON files, properties, inheritance, and structured error handling.
# Change Log: (Who, When, What)
# Mohiuddin Khan,11/26/2025,Created script based on Assignment07 starter and Mod07 labs.
# ========================================================================================== 

import json  # Used to read/write list of dictionaries from/to a JSON file.

# ----------------------------------------
# Data Constants
# ----------------------------------------
# MENU: This constant holds the menu text shown to the user.
# It does NOT change while the program runs.

MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course
    2. Show current data  
    3. Save data to a file
    4. Exit the program
----------------------------------------- 
'''

# FILE_NAME: This constant holds the name of the JSON file we use for storage.
# It does NOT change while the program runs.
FILE_NAME: str = "Enrollments.json"

# ----------------------------------------
# Data Variables
# ----------------------------------------
# These variables will store the data while the program runs.
students: list = []      # A table (list) of Student objects.
menu_choice: str = ""    # Holds the choice made by the user.


# ------------------------------------------------------------------------------------------ 
# Data Classes (Person and Student)
# ------------------------------------------------------------------------------------------
class Person:
    """
    A class representing basic person data.

    Properties:
        first_name (str): The person's first name (default: empty string).
        last_name  (str): The person's last name  (default: empty string).

    The name properties include simple validation:
      - Only alphabetic characters are allowed (or an empty string for default).
    """

    def __init__(self, first_name: str = "", last_name: str = ""):
        """
        Constructor that uses property setters for validation.

        :param first_name: Initial first name (default: empty string).
        :param last_name: Initial last name (default: empty string).
        """
        self.first_name = first_name
        self.last_name = last_name

    # first_name property ------------------------------------
    @property
    def first_name(self) -> str:
        """Gets a formatted version of the first name."""
        return self.__first_name.title()

    @first_name.setter
    def first_name(self, value: str) -> None:
        """
        Sets the first name after simple validation.

        - Must be all letters or an empty string.
        """
        if value.isalpha() or value == "":
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers or symbols.")

    # last_name property -------------------------------------
    @property
    def last_name(self) -> str:
        """Gets a formatted version of the last name."""
        return self.__last_name.title()

    @last_name.setter
    def last_name(self, value: str) -> None:
        """
        Sets the last name after simple validation.

        - Must be all letters or an empty string.
        """
        if value.isalpha() or value == "":
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers or symbols.")

    # String representation ----------------------------------
    def __str__(self) -> str:
        """
        Returns a comma-separated string of the Person data.

        :return: "FirstName,LastName"
        """
        return f"{self.first_name},{self.last_name}"


class Student(Person):
    """
    A class representing student data, inherited from Person.

    Inherits:
        first_name (str)
        last_name  (str)

    Adds:
        course_name (str): The name of the course (default: empty string).

    The course_name property includes simple validation:
      - Defaults to empty string.
      - When set from user input, it cannot be empty.
    """

    def __init__(self,
                 first_name: str = "",
                 last_name: str = "",
                 course_name: str = ""):
        """
        Constructor for Student.

        Calls the Person constructor for first/last name,
        then sets the course_name.

        :param first_name: Student's first name.
        :param last_name: Student's last name.
        :param course_name: Name of the course.
        """
        super().__init__(first_name=first_name, last_name=last_name)

        # IMPORTANT FIX:
        # Default course_name is allowed to be empty here.
        # We only enforce "not empty" when setting from user input.
        self.__course_name = ""     # private attribute default
        if course_name != "":
            self.course_name = course_name  # use validation for non-empty values

    # course_name property -----------------------------------
    @property
    def course_name(self) -> str:
        """Gets the course name."""
        return self.__course_name

    @course_name.setter
    def course_name(self, value: str) -> None:
        """
        Sets the course name after simple validation.

        - Cannot be an empty string when set explicitly.
        """
        value = value.strip()
        if value == "":
            raise ValueError("The course name cannot be empty.")
        self.__course_name = value

    # String representation ----------------------------------
    def __str__(self) -> str:
        """
        Returns a comma-separated string of the Student data.

        :return: "FirstName,LastName,CourseName"
        """
        return f"{self.first_name},{self.last_name},{self.course_name}"


# ------------------------------------------------------------------------------------------
# Processing Layer (FileProcessor Class)
# ------------------------------------------------------------------------------------------
class FileProcessor:
    """
    A collection of processing layer functions that work with JSON files.

    Responsibilities:
        - Reading student registration data from a JSON file.
        - Writing student registration data to a JSON file.

    All methods are static and do not depend on instances of this class.
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list) -> list:
        """
        Reads data from a JSON file into a list of Student objects.

        Processing Steps:
          1. Opens the JSON file in read mode.
          2. Uses json.load() to get a list of dictionary rows.
          3. Converts each dictionary into a Student object.
          4. Handles file and JSON errors with structured error handling.

        :param file_name: Name of the file to read from.
        :param student_data: The list that will receive the Student objects.
        :return: The updated list of Student objects.
        """
        file = None
        try:
            file = open(file_name, "r")
            list_of_dict_rows = json.load(file)  # Expecting a list of dictionaries.

            # Clear any existing data before refilling. It's essential:
            student_data.clear()

            # Convert dictionary rows into Student objects.
            for row in list_of_dict_rows:
                first = row.get("FirstName", "")
                last = row.get("LastName", "")
                course = row.get("CourseName", "")

                try:
                    student_obj = Student(first_name=first,
                                          last_name=last,
                                          course_name=course)
                    student_data.append(student_obj)
                except Exception as e:
                    # If one row has invalid data, show a message and skip that row.
                    IO.output_error_messages(
                        "Warning: A row in the file had invalid data and was skipped.", e
                    )

        except FileNotFoundError as e:
            IO.output_error_messages(
                "Notice: The enrollment file was not found. "
                "A new file will be created when you save.",
                e
            )
        except json.JSONDecodeError as e: # I preferred using JSON Decode Error to inform the data structure.
            IO.output_error_messages(
                "Error: The enrollment file contains invalid JSON data.",
                e
            )
        except Exception as e:
            IO.output_error_messages(
                "Error: There was a non-specific problem reading the file.",
                e
            )
        finally:
            if file is not None and file.closed is False:
                file.close()

        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list) -> None:
        """
        Writes a list of Student objects to a JSON file as a list of dictionaries.

        Processing Steps:
          1. Converts each Student object into a dictionary row.
          2. Opens the file in write mode.
          3. Uses json.dump() to write the list of dictionaries into the file.
          4. Uses structured error handling to handle write issues.
          5. Displays what was saved using IO.output_student_courses().

        :param file_name: Name of the file to write to.
        :param student_data: The list of Student objects to save.
        :return: None
        """
        file = None
        try:
            # Convert Student objects into dictionaries.
            list_of_dict_rows: list = []
            for student in student_data:
                row = {
                    "FirstName": student.first_name,
                    "LastName": student.last_name,
                    "CourseName": student.course_name
                }
                list_of_dict_rows.append(row)

            file = open(file_name, "w")
            json.dump(list_of_dict_rows, file, indent=2)

            print("The following data was saved to file:\n")
            IO.output_student_courses(student_data=student_data)

        except TypeError as e:
            IO.output_error_messages(
                "Error: Data could not be converted into valid JSON format.", e
            )
        except Exception as e:
            message = "Error: There was a problem writing to the file.\n"
            message += "Please check that the file is not open in another program."
            IO.output_error_messages(message, e)
        finally:
            if file is not None and file.closed is False:
                file.close()


# ------------------------------------------------------------------------------------------
# Presentation Layer (IO Class). I prefer using IO, instead of IOProcessor
# ------------------------------------------------------------------------------------------
class IO:
    """
    A collection of presentation layer functions that manage user input and output.

    Responsibilities:
      - Showing menus and messages to the user.
      - Getting menu choices from the user.
      - Getting new student registration data from the user.
      - Displaying the current list of student registrations.
      - Displaying user-friendly error messages.

    All methods are static and do not depend on instances of this class.
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None) -> None:
        """
        Displays a custom error message to the user.
        If an error object is provided, it can also show technical details.

        :param message: A user-friendly error message.
        :param error: (Optional) The original Exception object.
        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message --")
            print(error, error.__doc__, type(error), sep="\n")
            print()  # Blank line for readability.

    @staticmethod
    def output_menu(menu: str) -> None:
        """
        Displays the main menu of choices to the user.

        :param menu: The menu text to display.
        :return: None
        """
        print()  # Extra space to make it look nicer.
        print(menu)
        print()  # Extra space to make it look nicer.

    @staticmethod
    def input_menu_choice() -> str:
        """
        Gets a menu choice from the user and validates it.

        Valid choices are: "1", "2", "3", or "4".

        :return: A string with the user's valid choice (or "" if invalid).
        """
        choice: str = ""
        try:
            choice = input("Enter your menu choice number: ").strip()
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Please choose only 1, 2, 3, or 4.")
        except Exception as e:
            # Show a simple error message (no technical details here).
            IO.output_error_messages(e.__str__())
            choice = ""  # Signal invalid choice.
        return choice

    @staticmethod
    def output_student_courses(student_data: list) -> None:
        """
        Displays the current list of student registrations.

        For each Student object, it prints a comma-separated string:
          FirstName,LastName,CourseName

        :param student_data: The list of Student objects to display.
        :return: None
        """
        if not student_data:
            print("No registrations to display yet.\n")
            return

        print("-" * 50)
        for student in student_data:
            # Using the __str__ method of Student for comma-separated data.
            print(str(student))
        print("-" * 50)
        print()

    @staticmethod
    def input_student_data(student_data: list) -> list:
        """
        Prompts the user for a student's first name, last name, and course name.

        Uses the Student properties for validation:
          - First name: alphabetic characters only.
          - Last name: alphabetic characters only.
          - Course name: cannot be empty.

        If valid, a new Student object is added to the student_data list.

        :param student_data: The existing list of Student objects.
        :return: The updated list of Student objects.
        """
        try:
            # Create a Student object; default course_name is allowed to be empty here.
            student = Student()

            # Set first name (validation enforced by property).
            student.first_name = input("Enter the student's first name: ").strip()

            # Set last name (validation enforced by property).
            student.last_name = input("Enter the student's last name: ").strip()

            # Get and validate course name before setting property.
            course = input("Please enter the name of the course: ").strip()
            if course == "":
                raise ValueError("The course name cannot be empty.")
            student.course_name = course  # property enforces validation

            # Add to list.
            student_data.append(student)

            print()
            print(f"We have registered {student.first_name} {student.last_name} "
                  f"for {student.course_name}.")
            print()
        except ValueError as e:
            IO.output_error_messages(
                "One of the values was not the correct type of data!", e
            )
        except Exception as e:
            IO.output_error_messages(
                "Error: There was a problem with your entered data.", e
            )

        return student_data


# ------------------------------------------------------------------------------------------
# Main Body of the Script
# ------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Startup: read the file data into a list of Student objects (table)
    students = FileProcessor.read_data_from_file(file_name=FILE_NAME,
                                                 student_data=students)

    # Main program loop: present the menu and process choices
    while True:
        IO.output_menu(menu=MENU)
        menu_choice = IO.input_menu_choice()

        # 1. Register a Student for a Course
        if menu_choice == "1":
            students = IO.input_student_data(student_data=students)
            continue

        # 2. Show current data
        elif menu_choice == "2":
            IO.output_student_courses(student_data=students)
            continue

        # 3. Save data to a file
        elif menu_choice == "3":
            FileProcessor.write_data_to_file(file_name=FILE_NAME,
                                             student_data=students)
            continue

        # 4. Exit the program
        elif menu_choice == "4":
            print("Program Ended. Thank you for using the Course Registration Program. \n HAPPY 2025 THANKSGIVING!!!")
            break

        # Extra safety for invalid/empty choice
        else:
            IO.output_error_messages("Please choose only 1, 2, 3, or 4.")
            continue
