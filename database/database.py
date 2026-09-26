import sqlite3

from pathlib import Path
from datetime import date


# =================================================
# DATABASE PATH
# =================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "lifeos.db"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =================================================
# CONNECTION
# =================================================

def get_connection():

    return sqlite3.connect(
        DB_PATH
    )


# =================================================
# INITIALIZE DATABASE
# =================================================

def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # =================================================
    # TASKS
    # =================================================

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

    # =================================================
    # NOTES
    # =================================================

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

    # =================================================
    # PLANNER
    # =================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS planner (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            activity_date TEXT NOT NULL,
            start_time TEXT,
            end_time TEXT,
            category TEXT DEFAULT 'General',
            completed INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # =================================================
    # POMODORO
    # =================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pomodoro_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_type TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            completed_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # =================================================
    # STOPWATCH
    # =================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS stopwatch_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            duration_seconds INTEGER NOT NULL,
            lap_count INTEGER DEFAULT 0,
            completed_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # =================================================
    # FOCUS MODE
    # =================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS focus_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            task_title TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            actual_seconds INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Completed',
            completed_at TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (task_id)
            REFERENCES tasks(id)
        )
        """
    )

    # =================================================
    # DATABASE MIGRATION
    # =================================================
    # This upgrades an older focus_sessions table
    # without deleting the user's existing database.
    # =================================================

    cursor.execute(
        """
        PRAGMA table_info(focus_sessions)
        """
    )

    focus_columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    if (
        "actual_seconds"
        not in focus_columns
    ):

        cursor.execute(
            """
            ALTER TABLE focus_sessions
            ADD COLUMN actual_seconds
            INTEGER DEFAULT 0
            """
        )

    if (
        "status"
        not in focus_columns
    ):

        cursor.execute(
            """
            ALTER TABLE focus_sessions
            ADD COLUMN status
            TEXT DEFAULT 'Completed'
            """
        )

    connection.commit()
    connection.close()


# =================================================
# TASK FUNCTIONS
# =================================================

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

                WHEN 'High'
                THEN 1

                WHEN 'Medium'
                THEN 2

                WHEN 'Low'
                THEN 3

                ELSE 4

            END ASC,

            id DESC
        """
    )

    tasks = cursor.fetchall()

    connection.close()

    return tasks


def get_pending_tasks():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            due_date,
            priority,
            category

        FROM tasks

        WHERE completed = 0

        ORDER BY

            CASE

                WHEN due_date IS NULL
                OR due_date = ''

                THEN 1

                ELSE 0

            END,

            due_date ASC,

            CASE priority

                WHEN 'High'
                THEN 1

                WHEN 'Medium'
                THEN 2

                WHEN 'Low'
                THEN 3

                ELSE 4

            END,

            id ASC
        """
    )

    tasks = cursor.fetchall()

    connection.close()

    return tasks


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


def delete_task(
    task_id
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM tasks

        WHERE id = ?
        """,
        (
            task_id,
        )
    )

    connection.commit()
    connection.close()


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

    connection.close()

    return {
        "total": total,
        "completed": completed,
        "pending": (
            total - completed
        )
    }


def get_today_tasks(
    limit=5
):

    today = (
        date.today()
        .isoformat()
    )

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

                WHEN 'High'
                THEN 1

                WHEN 'Medium'
                THEN 2

                WHEN 'Low'
                THEN 3

                ELSE 4

            END,

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

        pattern = (
            f"%{search_text}%"
        )

        parameters.extend(
            [
                pattern,
                pattern
            ]
        )

    if (
        category
        != "All Categories"
    ):

        query += """
            AND category = ?
        """

        parameters.append(
            category
        )

    query += """
        ORDER BY
            updated_at DESC,
            id DESC
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


def delete_note(
    note_id
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM notes

        WHERE id = ?
        """,
        (
            note_id,
        )
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


# =================================================
# PLANNER
# =================================================

def add_planner_activity(
    title,
    activity_date,
    start_time="",
    end_time="",
    category="General"
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO planner (
            title,
            activity_date,
            start_time,
            end_time,
            category
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            title,
            activity_date,
            start_time,
            end_time,
            category
        )
    )

    connection.commit()
    connection.close()


def get_planner_activities(
    activity_date=None
):

    connection = get_connection()
    cursor = connection.cursor()

    if activity_date:

        cursor.execute(
            """
            SELECT
                id,
                title,
                activity_date,
                start_time,
                end_time,
                category,
                completed

            FROM planner

            WHERE activity_date = ?

            ORDER BY
                completed ASC,
                start_time ASC,
                id ASC
            """,
            (
                activity_date,
            )
        )

    else:

        cursor.execute(
            """
            SELECT
                id,
                title,
                activity_date,
                start_time,
                end_time,
                category,
                completed

            FROM planner

            ORDER BY
                activity_date ASC,
                start_time ASC,
                id ASC
            """
        )

    activities = cursor.fetchall()

    connection.close()

    return activities


def toggle_planner_activity(
    activity_id,
    completed
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE planner

        SET completed = ?

        WHERE id = ?
        """,
        (
            completed,
            activity_id
        )
    )

    connection.commit()
    connection.close()


def delete_planner_activity(
    activity_id
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM planner

        WHERE id = ?
        """,
        (
            activity_id,
        )
    )

    connection.commit()
    connection.close()


def get_today_planner(
    limit=10
):

    today = (
        date.today()
        .isoformat()
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            activity_date,
            start_time,
            end_time,
            category,
            completed

        FROM planner

        WHERE activity_date = ?

        ORDER BY
            completed ASC,
            start_time ASC,
            id ASC

        LIMIT ?
        """,
        (
            today,
            limit
        )
    )

    activities = cursor.fetchall()

    connection.close()

    return activities


# =================================================
# POMODORO
# =================================================

def add_pomodoro_session(
    session_type,
    duration_minutes
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO pomodoro_sessions (
            session_type,
            duration_minutes
        )
        VALUES (?, ?)
        """,
        (
            session_type,
            duration_minutes
        )
    )

    connection.commit()
    connection.close()


def get_today_pomodoro_stats():

    today = (
        date.today()
        .isoformat()
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*),

            COALESCE(
                SUM(duration_minutes),
                0
            )

        FROM pomodoro_sessions

        WHERE
            session_type = 'Focus'

            AND DATE(
                completed_at
            ) = ?
        """,
        (
            today,
        )
    )

    result = cursor.fetchone()

    connection.close()

    return {
        "sessions": result[0],
        "focus_minutes": result[1]
    }


def get_recent_pomodoro_sessions(
    limit=10
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            session_type,
            duration_minutes,
            completed_at

        FROM pomodoro_sessions

        ORDER BY id DESC

        LIMIT ?
        """,
        (
            limit,
        )
    )

    sessions = cursor.fetchall()

    connection.close()

    return sessions


# =================================================
# STOPWATCH
# =================================================

def add_stopwatch_session(
    duration_seconds,
    lap_count=0
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO stopwatch_sessions (
            duration_seconds,
            lap_count
        )
        VALUES (?, ?)
        """,
        (
            duration_seconds,
            lap_count
        )
    )

    connection.commit()
    connection.close()


def get_today_stopwatch_stats():

    today = (
        date.today()
        .isoformat()
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*),

            COALESCE(
                SUM(duration_seconds),
                0
            )

        FROM stopwatch_sessions

        WHERE DATE(
            completed_at
        ) = ?
        """,
        (
            today,
        )
    )

    result = cursor.fetchone()

    connection.close()

    return {
        "sessions": result[0],
        "total_seconds": result[1]
    }


def get_recent_stopwatch_sessions(
    limit=10
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            duration_seconds,
            lap_count,
            completed_at

        FROM stopwatch_sessions

        ORDER BY id DESC

        LIMIT ?
        """,
        (
            limit,
        )
    )

    sessions = cursor.fetchall()

    connection.close()

    return sessions


# =================================================
# FOCUS MODE
# =================================================

def add_focus_session(
    task_id,
    task_title,
    duration_minutes,
    actual_seconds=None,
    status="Completed"
):

    # -------------------------------------------------
    # If an old caller does not provide actual time,
    # assume the whole selected duration completed.
    # -------------------------------------------------

    if actual_seconds is None:

        actual_seconds = (
            duration_minutes
            * 60
        )

    # Prevent negative values
    actual_seconds = max(
        0,
        int(actual_seconds)
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO focus_sessions (
            task_id,
            task_title,
            duration_minutes,
            actual_seconds,
            status
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            task_id,
            task_title,
            duration_minutes,
            actual_seconds,
            status
        )
    )

    connection.commit()
    connection.close()


def get_today_focus_stats():

    today = (
        date.today()
        .isoformat()
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*),

            COALESCE(
                SUM(
                    CASE

                        WHEN actual_seconds > 0
                        THEN actual_seconds

                        ELSE duration_minutes * 60

                    END
                ),
                0
            )

        FROM focus_sessions

        WHERE DATE(
            completed_at
        ) = ?
        """,
        (
            today,
        )
    )

    result = cursor.fetchone()

    connection.close()

    sessions = (
        result[0]
        if result
        else 0
    )

    total_seconds = (
        result[1]
        if (
            result
            and result[1]
        )
        else 0
    )

    return {
        "sessions": sessions,

        "focus_seconds":
            total_seconds,

        "focus_minutes":
            round(
                total_seconds
                / 60
            )
    }


def get_recent_focus_sessions(
    limit=10
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            task_id,
            task_title,
            duration_minutes,
            actual_seconds,
            status,
            completed_at

        FROM focus_sessions

        ORDER BY id DESC

        LIMIT ?
        """,
        (
            limit,
        )
    )

    sessions = cursor.fetchall()

    connection.close()

    return sessions