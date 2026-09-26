import sqlite3
from pathlib import Path
from datetime import date


# -------------------------------------------------
# DATABASE PATH
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "lifeos.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------
# CONNECTION
# -------------------------------------------------

def get_connection():
    return sqlite3.connect(DB_PATH)


# -------------------------------------------------
# DATABASE INITIALIZATION
# -------------------------------------------------

def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            priority TEXT DEFAULT 'Medium',
            category TEXT DEFAULT 'General',
            completed INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    
    connection.commit()
    connection.close()


# -------------------------------------------------
# ADD TASK
# -------------------------------------------------

def add_task(
    title,
    description="",
    due_date="",
    priority="Medium",
    category="General"
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (
            title,
            description,
            due_date,
            priority,
            category
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            title,
            description,
            due_date,
            priority,
            category
        )
    )

    connection.commit()
    connection.close()


# -------------------------------------------------
# GET ALL TASKS
# -------------------------------------------------

def get_tasks():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            description,
            due_date,
            priority,
            category,
            completed
        FROM tasks

        ORDER BY

            completed ASC,

            CASE
                WHEN due_date IS NULL
                OR due_date = ''
                THEN 1
                ELSE 0
            END ASC,

            due_date ASC,

            CASE priority
                WHEN 'High' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Low' THEN 3
                ELSE 4
            END ASC,

            id DESC
        """
    )

    tasks = cursor.fetchall()

    connection.close()

    return tasks


# -------------------------------------------------
# UPDATE TASK
# -------------------------------------------------

def update_task(
    task_id,
    title,
    description,
    due_date,
    priority,
    category
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks

        SET
            title = ?,
            description = ?,
            due_date = ?,
            priority = ?,
            category = ?

        WHERE id = ?
        """,
        (
            title,
            description,
            due_date,
            priority,
            category,
            task_id
        )
    )

    connection.commit()
    connection.close()


# -------------------------------------------------
# TASK COMPLETION STATUS
# -------------------------------------------------

def toggle_task(
    task_id,
    completed
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET completed = ?
        WHERE id = ?
        """,
        (
            completed,
            task_id
        )
    )

    connection.commit()
    connection.close()


# -------------------------------------------------
# DELETE TASK
# -------------------------------------------------

def delete_task(task_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (task_id,)
    )

    connection.commit()
    connection.close()


# -------------------------------------------------
# TASK STATISTICS
# -------------------------------------------------

def get_task_statistics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        """
    )

    total = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE completed = 1
        """
    )

    completed = cursor.fetchone()[0]

    pending = total - completed

    connection.close()

    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }


# -------------------------------------------------
# TODAY'S TASKS
# -------------------------------------------------

def get_today_tasks(limit=5):

    today = date.today().isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            due_date,
            priority,
            category,
            completed

        FROM tasks

        WHERE
            completed = 0
            AND due_date = ?

        ORDER BY

            CASE priority
                WHEN 'High' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Low' THEN 3
                ELSE 4
            END ASC,

            id ASC

        LIMIT ?
        """,
        (
            today,
            limit
        )
    )

    tasks = cursor.fetchall()

    connection.close()

    return tasks

# =================================================
# NOTES
# =================================================


def add_note(
    title,
    content,
    category="General"
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO notes (
            title,
            content,
            category
        )
        VALUES (?, ?, ?)
        """,
        (
            title,
            content,
            category
        )
    )

    connection.commit()
    connection.close()


def get_notes(
    search_text="",
    category="All Categories"
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            id,
            title,
            content,
            category,
            created_at,
            updated_at
        FROM notes
        WHERE 1 = 1
    """

    parameters = []

    if search_text:

        query += """
            AND (
                title LIKE ?
                OR content LIKE ?
            )
        """

        search_pattern = f"%{search_text}%"

        parameters.extend([
            search_pattern,
            search_pattern
        ])

    if category != "All Categories":

        query += """
            AND category = ?
        """

        parameters.append(category)

    query += """
        ORDER BY updated_at DESC, id DESC
    """

    cursor.execute(
        query,
        parameters
    )

    notes = cursor.fetchall()

    connection.close()

    return notes


def update_note(
    note_id,
    title,
    content,
    category
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE notes

        SET
            title = ?,
            content = ?,
            category = ?,
            updated_at = CURRENT_TIMESTAMP

        WHERE id = ?
        """,
        (
            title,
            content,
            category,
            note_id
        )
    )

    connection.commit()
    connection.close()


def delete_note(note_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM notes
        WHERE id = ?
        """,
        (note_id,)
    )

    connection.commit()
    connection.close()


def get_note_count():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM notes
        """
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count

