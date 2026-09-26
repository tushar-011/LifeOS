import sqlite3

from pathlib import Path
from datetime import date, timedelta


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
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            completed_at TEXT
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
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            completed_at TEXT
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
    # MIGRATIONS
    # =================================================

    # Focus Mode
    cursor.execute(
        """
        PRAGMA table_info(focus_sessions)
        """
    )

    focus_columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if "actual_seconds" not in focus_columns:

        cursor.execute(
            """
            ALTER TABLE focus_sessions
            ADD COLUMN actual_seconds INTEGER DEFAULT 0
            """
        )

    if "status" not in focus_columns:

        cursor.execute(
            """
            ALTER TABLE focus_sessions
            ADD COLUMN status TEXT DEFAULT 'Completed'
            """
        )

    # Tasks
    cursor.execute(
        """
        PRAGMA table_info(tasks)
        """
    )

    task_columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if "completed_at" not in task_columns:

        cursor.execute(
            """
            ALTER TABLE tasks
            ADD COLUMN completed_at TEXT
            """
        )

    # Planner
    cursor.execute(
        """
        PRAGMA table_info(planner)
        """
    )

    planner_columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if "completed_at" not in planner_columns:

        cursor.execute(
            """
            ALTER TABLE planner
            ADD COLUMN completed_at TEXT
            """
        )

    connection.commit()
    connection.close()


# =================================================
# TASKS
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
                WHEN 'High' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Low' THEN 3
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

    if completed:

        cursor.execute(
            """
            UPDATE tasks

            SET
                completed = 1,
                completed_at = CURRENT_TIMESTAMP

            WHERE id = ?
            """,
            (
                task_id,
            )
        )

    else:

        cursor.execute(
            """
            UPDATE tasks

            SET
                completed = 0,
                completed_at = NULL

            WHERE id = ?
            """,
            (
                task_id,
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
                WHEN 'High' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Low' THEN 3
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

    if category != "All Categories":

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
                CASE
                    WHEN start_time IS NULL
                    OR start_time = ''
                    THEN 1
                    ELSE 0
                END,

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

                CASE
                    WHEN start_time IS NULL
                    OR start_time = ''
                    THEN 1
                    ELSE 0
                END,

                start_time ASC,
                id ASC
            """
        )

    activities = cursor.fetchall()

    connection.close()

    return activities


def update_planner_activity(
    activity_id,
    title,
    activity_date,
    start_time,
    end_time,
    category
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE planner

        SET
            title = ?,
            activity_date = ?,
            start_time = ?,
            end_time = ?,
            category = ?

        WHERE id = ?
        """,
        (
            title,
            activity_date,
            start_time,
            end_time,
            category,
            activity_id
        )
    )

    connection.commit()
    connection.close()


def toggle_planner_activity(
    activity_id,
    completed
):

    connection = get_connection()
    cursor = connection.cursor()

    if completed:

        cursor.execute(
            """
            UPDATE planner

            SET
                completed = 1,
                completed_at = CURRENT_TIMESTAMP

            WHERE id = ?
            """,
            (
                activity_id,
            )
        )

    else:

        cursor.execute(
            """
            UPDATE planner

            SET
                completed = 0,
                completed_at = NULL

            WHERE id = ?
            """,
            (
                activity_id,
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
            CASE
                WHEN start_time IS NULL
                OR start_time = ''
                THEN 1
                ELSE 0
            END,

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
            AND DATE(completed_at) = ?
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

        WHERE DATE(completed_at) = ?
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

    if actual_seconds is None:

        actual_seconds = (
            duration_minutes * 60
        )

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

        WHERE DATE(completed_at) = ?
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
        if result
        else 0
    )

    return {
        "sessions": sessions,
        "focus_seconds": total_seconds,
        "focus_minutes": (
            total_seconds / 60
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


# =================================================
# PRODUCTIVITY / ANALYTICS
# =================================================

def get_productivity_metrics(
    target_date=None
):

    if target_date is None:

        target_date = (
            date.today()
            .isoformat()
        )

    connection = get_connection()
    cursor = connection.cursor()

    # Tasks
    cursor.execute(
        """
        SELECT
            COUNT(*),

            COALESCE(
                SUM(
                    CASE
                        WHEN completed = 1
                        THEN 1
                        ELSE 0
                    END
                ),
                0
            )

        FROM tasks

        WHERE due_date = ?
        """,
        (
            target_date,
        )
    )

    task_result = cursor.fetchone()

    tasks_total = task_result[0]
    tasks_completed = task_result[1]

    # Planner
    cursor.execute(
        """
        SELECT
            COUNT(*),

            COALESCE(
                SUM(
                    CASE
                        WHEN completed = 1
                        THEN 1
                        ELSE 0
                    END
                ),
                0
            )

        FROM planner

        WHERE activity_date = ?
        """,
        (
            target_date,
        )
    )

    planner_result = cursor.fetchone()

    planner_total = planner_result[0]
    planner_completed = planner_result[1]

    # Pomodoro
    cursor.execute(
        """
        SELECT
            COALESCE(
                SUM(duration_minutes),
                0
            )

        FROM pomodoro_sessions

        WHERE
            session_type = 'Focus'
            AND DATE(completed_at) = ?
        """,
        (
            target_date,
        )
    )

    pomodoro_minutes = (
        cursor.fetchone()[0]
    )

    # Focus Mode
    cursor.execute(
        """
        SELECT
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

        WHERE DATE(completed_at) = ?
        """,
        (
            target_date,
        )
    )

    focus_seconds = (
        cursor.fetchone()[0]
    )

    focus_mode_minutes = (
        focus_seconds / 60
    )

    total_focus_minutes = (
        pomodoro_minutes
        + focus_mode_minutes
    )

    # Stopwatch
    cursor.execute(
        """
        SELECT
            COALESCE(
                SUM(duration_seconds),
                0
            )

        FROM stopwatch_sessions

        WHERE DATE(completed_at) = ?
        """,
        (
            target_date,
        )
    )

    stopwatch_seconds = (
        cursor.fetchone()[0]
    )

    connection.close()

    return {
        "date":
            target_date,

        "tasks_total":
            tasks_total,

        "tasks_completed":
            tasks_completed,

        "planner_total":
            planner_total,

        "planner_completed":
            planner_completed,

        "pomodoro_minutes":
            pomodoro_minutes,

        "focus_mode_minutes":
            focus_mode_minutes,

        "focus_minutes":
            total_focus_minutes,

        "stopwatch_seconds":
            stopwatch_seconds
    }


def get_weekly_productivity_metrics(
    days=7
):

    today = date.today()

    results = []

    for offset in reversed(
        range(days)
    ):

        target = (
            today
            - timedelta(
                days=offset
            )
        )

        metrics = (
            get_productivity_metrics(
                target.isoformat()
            )
        )

        results.append(
            metrics
        )

    return results


# =================================================
# HISTORY
# =================================================

def get_history_counts():

    connection = get_connection()
    cursor = connection.cursor()

    counts = {}

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM focus_sessions
        """
    )

    counts["Focus"] = (
        cursor.fetchone()[0]
    )

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM pomodoro_sessions
        """
    )

    counts["Pomodoro"] = (
        cursor.fetchone()[0]
    )

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM stopwatch_sessions
        """
    )

    counts["Stopwatch"] = (
        cursor.fetchone()[0]
    )

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE completed = 1
        """
    )

    counts["Tasks"] = (
        cursor.fetchone()[0]
    )

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM planner
        WHERE completed = 1
        """
    )

    counts["Planner"] = (
        cursor.fetchone()[0]
    )

    counts["All"] = sum(
        counts.values()
    )

    connection.close()

    return counts


def _history_date_condition(
    period,
    column_name
):

    if period == "Today":

        return (
            f"DATE({column_name}) "
            f"= DATE('now', 'localtime')"
        )

    if period == "Last 7 Days":

        return (
            f"DATE({column_name}) >= "
            f"DATE('now', 'localtime', '-6 days')"
        )

    if period == "Last 30 Days":

        return (
            f"DATE({column_name}) >= "
            f"DATE('now', 'localtime', '-29 days')"
        )

    return "1 = 1"


def get_focus_history(
    period="All Time"
):

    connection = get_connection()
    cursor = connection.cursor()

    condition = (
        _history_date_condition(
            period,
            "completed_at"
        )
    )

    cursor.execute(
        f"""
        SELECT
            id,
            task_title,
            duration_minutes,
            actual_seconds,
            status,
            completed_at

        FROM focus_sessions

        WHERE {condition}

        ORDER BY
            completed_at DESC,
            id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_pomodoro_history(
    period="All Time"
):

    connection = get_connection()
    cursor = connection.cursor()

    condition = (
        _history_date_condition(
            period,
            "completed_at"
        )
    )

    cursor.execute(
        f"""
        SELECT
            id,
            session_type,
            duration_minutes,
            completed_at

        FROM pomodoro_sessions

        WHERE {condition}

        ORDER BY
            completed_at DESC,
            id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_stopwatch_history(
    period="All Time"
):

    connection = get_connection()
    cursor = connection.cursor()

    condition = (
        _history_date_condition(
            period,
            "completed_at"
        )
    )

    cursor.execute(
        f"""
        SELECT
            id,
            duration_seconds,
            lap_count,
            completed_at

        FROM stopwatch_sessions

        WHERE {condition}

        ORDER BY
            completed_at DESC,
            id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_task_history(
    period="All Time"
):

    connection = get_connection()
    cursor = connection.cursor()

    condition = (
        _history_date_condition(
            period,
            "COALESCE(completed_at, created_at)"
        )
    )

    cursor.execute(
        f"""
        SELECT
            id,
            title,
            due_date,
            priority,
            category,
            completed_at,
            created_at

        FROM tasks

        WHERE
            completed = 1
            AND {condition}

        ORDER BY
            COALESCE(
                completed_at,
                created_at
            ) DESC,

            id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_planner_history(
    period="All Time"
):

    connection = get_connection()
    cursor = connection.cursor()

    condition = (
        _history_date_condition(
            period,
            "COALESCE(completed_at, created_at)"
        )
    )

    cursor.execute(
        f"""
        SELECT
            id,
            title,
            activity_date,
            start_time,
            end_time,
            category,
            completed_at,
            created_at

        FROM planner

        WHERE
            completed = 1
            AND {condition}

        ORDER BY
            COALESCE(
                completed_at,
                created_at
            ) DESC,

            id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


# =================================================
# REPORTS
# =================================================

def get_report_date_range(
    report_type
):

    today = date.today()

    # Daily
    if report_type == "Daily":

        start_date = today
        end_date = today

    # Weekly - Monday through today
    elif report_type == "Weekly":

        start_date = (
            today
            - timedelta(
                days=today.weekday()
            )
        )

        end_date = today

    # Monthly
    else:

        start_date = today.replace(
            day=1
        )

        end_date = today

    return (
        start_date,
        end_date
    )


# =================================================
# REPORT TASKS
# =================================================

def get_report_completed_tasks(
    report_type="Daily"
):

    (
        start_date,
        end_date
    ) = get_report_date_range(
        report_type
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            priority,
            category,
            due_date,
            completed_at,
            created_at

        FROM tasks

        WHERE
            completed = 1

            AND DATE(
                COALESCE(
                    completed_at,
                    created_at
                )
            )
            BETWEEN ? AND ?

        ORDER BY
            COALESCE(
                completed_at,
                created_at
            ) DESC,
            id DESC
        """,
        (
            start_date.isoformat(),
            end_date.isoformat()
        )
    )

    tasks = cursor.fetchall()

    connection.close()

    return tasks


# =================================================
# REPORT CATEGORY SUMMARY
# =================================================

def get_report_category_summary(
    report_type="Daily"
):

    (
        start_date,
        end_date
    ) = get_report_date_range(
        report_type
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            category,
            COUNT(*)

        FROM tasks

        WHERE
            completed = 1

            AND DATE(
                COALESCE(
                    completed_at,
                    created_at
                )
            )
            BETWEEN ? AND ?

        GROUP BY category

        ORDER BY
            COUNT(*) DESC,
            category ASC
        """,
        (
            start_date.isoformat(),
            end_date.isoformat()
        )
    )

    categories = cursor.fetchall()

    connection.close()

    return categories


# =================================================
# REPORT SUMMARY
# =================================================

def get_report_summary(
    report_type="Daily"
):

    (
        start_date,
        end_date
    ) = get_report_date_range(
        report_type
    )

    tasks = (
        get_report_completed_tasks(
            report_type
        )
    )

    categories = (
        get_report_category_summary(
            report_type
        )
    )

    top_category = "None"

    if categories:

        top_category = (
            categories[0][0]
        )

    return {
        "report_type":
            report_type,

        "start_date":
            start_date.isoformat(),

        "end_date":
            end_date.isoformat(),

        "tasks_completed":
            len(tasks),

        "category_count":
            len(categories),

        "top_category":
            top_category
    }