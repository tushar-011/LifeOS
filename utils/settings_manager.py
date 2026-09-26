import json
import shutil

from pathlib import Path


# =================================================
# PATHS
# =================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

DATA_DIR = (
    BASE_DIR
    / "data"
)

EXPORT_DIR = (
    BASE_DIR
    / "exports"
)

SETTINGS_PATH = (
    DATA_DIR
    / "settings.json"
)

DATABASE_PATH = (
    DATA_DIR
    / "lifeos.db"
)


DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

EXPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =================================================
# DEFAULT SETTINGS
# =================================================

DEFAULT_SETTINGS = {

    "appearance_mode":
        "Dark",

    "export_folder":
        str(
            EXPORT_DIR
        ),

    "app_version":
        "1.0.0"
}


# =================================================
# LOAD SETTINGS
# =================================================

def load_settings():

    if not SETTINGS_PATH.exists():

        save_settings(
            DEFAULT_SETTINGS.copy()
        )

        return (
            DEFAULT_SETTINGS.copy()
        )

    try:

        with open(
            SETTINGS_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            saved_settings = (
                json.load(
                    file
                )
            )

    except (
        json.JSONDecodeError,
        OSError
    ):

        saved_settings = {}

    settings = (
        DEFAULT_SETTINGS.copy()
    )

    settings.update(
        saved_settings
    )

    return settings


# =================================================
# SAVE SETTINGS
# =================================================

def save_settings(
    settings
):

    with open(
        SETTINGS_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            settings,
            file,
            indent=4
        )


# =================================================
# GET SETTING
# =================================================

def get_setting(
    key,
    default=None
):

    settings = (
        load_settings()
    )

    return settings.get(
        key,
        default
    )


# =================================================
# UPDATE SETTING
# =================================================

def update_setting(
    key,
    value
):

    settings = (
        load_settings()
    )

    settings[
        key
    ] = value

    save_settings(
        settings
    )


# =================================================
# RESET SETTINGS
# =================================================

def reset_settings():

    settings = (
        DEFAULT_SETTINGS.copy()
    )

    save_settings(
        settings
    )

    return settings


# =================================================
# BACKUP DATABASE
# =================================================

def backup_database(
    destination_path
):

    if not DATABASE_PATH.exists():

        raise FileNotFoundError(
            "LifeOS database was not found."
        )

    shutil.copy2(
        DATABASE_PATH,
        destination_path
    )


# =================================================
# RESTORE DATABASE
# =================================================

def restore_database(
    source_path
):

    source = Path(
        source_path
    )

    if not source.exists():

        raise FileNotFoundError(
            "Selected backup file does not exist."
        )

    if (
        source.resolve()
        == DATABASE_PATH.resolve()
    ):

        return

    # Keep an automatic safety copy
    # before replacing the current database.

    safety_backup = (
        DATA_DIR
        / "lifeos_before_restore.db"
    )

    if DATABASE_PATH.exists():

        shutil.copy2(
            DATABASE_PATH,
            safety_backup
        )

    shutil.copy2(
        source,
        DATABASE_PATH
    )


# =================================================
# PATH GETTERS
# =================================================

def get_database_path():

    return str(
        DATABASE_PATH
    )


def get_settings_path():

    return str(
        SETTINGS_PATH
    )


def get_default_export_path():

    return str(
        EXPORT_DIR
    )