import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


DATABASE_NAME = "students.db"


def connect_database():
    """Create and return a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    """Create the students table when it does not already exist."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            course TEXT,
            grade TEXT
        )
        """
    )

    connection.commit()
    connection.close()


def clear_fields():
    """Clear all input fields."""
    student_id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    grade_entry.delete(0, tk.END)


def add_student():
    """Add a new student to the database."""
    student_id = student_id_entry.get().strip()
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    course = course_entry.get().strip()
    grade = grade_entry.get().strip()

    if not student_id or not name:
        messagebox.showwarning(
            "Missing information",
            "Student ID and name are required.",
        )
        return

    try:
        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO students (student_id, name, email, course, grade)
            VALUES (?, ?, ?, ?, ?)
            """,
            (student_id, name, email, course, grade),
        )

        connection.commit()
        connection.close()

        messagebox.showinfo("Success", "Student added successfully.")
        clear_fields()
        view_students()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Duplicate Student ID",
            "A student with this ID already exists.",
        )


def view_students(search_text=""):
    """Display all students or matching search results."""
    for item in student_table.get_children():
        student_table.delete(item)

    connection = connect_database()
    cursor = connection.cursor()

    if search_text:
        cursor.execute(
            """
            SELECT * FROM students
            WHERE student_id LIKE ?
               OR name LIKE ?
               OR email LIKE ?
               OR course LIKE ?
               OR grade LIKE ?
            ORDER BY name
            """,
            tuple([f"%{search_text}%"] * 5),
        )
    else:
        cursor.execute("SELECT * FROM students ORDER BY name")

    rows = cursor.fetchall()
    connection.close()

    for row in rows:
        student_table.insert("", tk.END, values=row)


def search_students():
    """Search students using the search box."""
    search_text = search_entry.get().strip()
    view_students(search_text)


def show_all_students():
    """Clear the search box and display every student."""
    search_entry.delete(0, tk.END)
    view_students()


def select_student(_event=None):
    """Load the selected student's information into the input fields."""
    selected_item = student_table.selection()

    if not selected_item:
        return

    values = student_table.item(selected_item[0], "values")

    clear_fields()

    student_id_entry.insert(0, values[1])
    name_entry.insert(0, values[2])
    email_entry.insert(0, values[3])
    course_entry.insert(0, values[4])
    grade_entry.insert(0, values[5])


def update_student():
    """Update the selected student's information."""
    selected_item = student_table.selection()

    if not selected_item:
        messagebox.showwarning(
            "No selection",
            "Select a student from the table first.",
        )
        return

    database_id = student_table.item(selected_item[0], "values")[0]

    student_id = student_id_entry.get().strip()
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    course = course_entry.get().strip()
    grade = grade_entry.get().strip()

    if not student_id or not name:
        messagebox.showwarning(
            "Missing information",
            "Student ID and name are required.",
        )
        return

    try:
        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE students
            SET student_id = ?, name = ?, email = ?, course = ?, grade = ?
            WHERE id = ?
            """,
            (student_id, name, email, course, grade, database_id),
        )

        connection.commit()
        connection.close()

        messagebox.showinfo("Success", "Student updated successfully.")
        clear_fields()
        view_students()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Duplicate Student ID",
            "Another student already uses this ID.",
        )


def delete_student():
    """Delete the selected student."""
    selected_item = student_table.selection()

    if not selected_item:
        messagebox.showwarning(
            "No selection",
            "Select a student from the table first.",
        )
        return

    confirm = messagebox.askyesno(
        "Confirm deletion",
        "Are you sure you want to delete this student?",
    )

    if not confirm:
        return

    database_id = student_table.item(selected_item[0], "values")[0]

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM students WHERE id = ?", (database_id,))

    connection.commit()
    connection.close()

    messagebox.showinfo("Success", "Student deleted successfully.")
    clear_fields()
    view_students()


# Create the database before opening the interface.
create_table()

# Main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("1050x650")
root.minsize(900, 550)

title_label = tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 22, "bold"),
)
title_label.pack(pady=15)

# Student form
form_frame = tk.LabelFrame(
    root,
    text="Student Information",
    padx=15,
    pady=15,
)
form_frame.pack(fill="x", padx=20)

tk.Label(form_frame, text="Student ID:").grid(
    row=0, column=0, padx=5, pady=8, sticky="w"
)
student_id_entry = tk.Entry(form_frame, width=30)
student_id_entry.grid(row=0, column=1, padx=5, pady=8)

tk.Label(form_frame, text="Name:").grid(
    row=0, column=2, padx=5, pady=8, sticky="w"
)
name_entry = tk.Entry(form_frame, width=30)
name_entry.grid(row=0, column=3, padx=5, pady=8)

tk.Label(form_frame, text="Email:").grid(
    row=1, column=0, padx=5, pady=8, sticky="w"
)
email_entry = tk.Entry(form_frame, width=30)
email_entry.grid(row=1, column=1, padx=5, pady=8)

tk.Label(form_frame, text="Course:").grid(
    row=1, column=2, padx=5, pady=8, sticky="w"
)
course_entry = tk.Entry(form_frame, width=30)
course_entry.grid(row=1, column=3, padx=5, pady=8)

tk.Label(form_frame, text="Grade:").grid(
    row=2, column=0, padx=5, pady=8, sticky="w"
)
grade_entry = tk.Entry(form_frame, width=30)
grade_entry.grid(row=2, column=1, padx=5, pady=8)

button_frame = tk.Frame(form_frame)
button_frame.grid(row=3, column=0, columnspan=4, pady=12)

tk.Button(
    button_frame,
    text="Add Student",
    width=15,
    command=add_student,
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Update Student",
    width=15,
    command=update_student,
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Delete Student",
    width=15,
    command=delete_student,
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Clear Fields",
    width=15,
    command=clear_fields,
).pack(side="left", padx=5)

# Search area
search_frame = tk.Frame(root)
search_frame.pack(fill="x", padx=20, pady=15)

tk.Label(search_frame, text="Search:").pack(side="left")

search_entry = tk.Entry(search_frame, width=40)
search_entry.pack(side="left", padx=8)

tk.Button(
    search_frame,
    text="Search",
    command=search_students,
).pack(side="left", padx=4)

tk.Button(
    search_frame,
    text="Show All",
    command=show_all_students,
).pack(side="left", padx=4)

# Student table
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

columns = (
    "database_id",
    "student_id",
    "name",
    "email",
    "course",
    "grade",
)

student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
)

student_table.heading("database_id", text="No.")
student_table.heading("student_id", text="Student ID")
student_table.heading("name", text="Name")
student_table.heading("email", text="Email")
student_table.heading("course", text="Course")
student_table.heading("grade", text="Grade")

student_table.column("database_id", width=50, anchor="center")
student_table.column("student_id", width=100, anchor="center")
student_table.column("name", width=160)
student_table.column("email", width=220)
student_table.column("course", width=160)
student_table.column("grade", width=80, anchor="center")

vertical_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=student_table.yview,
)

student_table.configure(yscrollcommand=vertical_scrollbar.set)

student_table.pack(side="left", fill="both", expand=True)
vertical_scrollbar.pack(side="right", fill="y")

student_table.bind("<<TreeviewSelect>>", select_student)

view_students()
root.mainloop()
