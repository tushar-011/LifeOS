import os

import customtkinter as ctk

from tkinter import (
    filedialog,
    messagebox
)

from utils.settings_manager import (
    load_settings,
    update_setting,
    reset_settings,
    backup_database,
    restore_database,
    get_database_path,
    get_settings_path,
    get_default_export_path
)


# =================================================
# SETTINGS PAGE
# =================================================

class SettingsPage(
    ctk.CTkScrollableFrame
):

    def __init__(
        self,
        parent
    ):

        super().__init__(
            parent,
            corner_radius=0
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.settings = (
            load_settings()
        )

        self.create_header()

        self.create_appearance_section()

        self.create_export_section()

        self.create_data_section()

        self.create_about_section()

    # =================================================
    # HEADER
    # =================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(25, 10)
        )

        ctk.CTkLabel(
            header,
            text="Settings",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            header,
            text=(
                "Customize LifeOS and "
                "manage your local data."
            ),
            font=ctk.CTkFont(
                size=14
            )
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

    # =================================================
    # APPEARANCE
    # =================================================

    def create_appearance_section(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        ctk.CTkLabel(
            card,
            text="Appearance",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        ctk.CTkLabel(
            card,
            text=(
                "Choose how LifeOS should "
                "look when the application starts."
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        row = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        ctk.CTkLabel(
            row,
            text="Theme",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        self.theme_menu = (
            ctk.CTkOptionMenu(
                row,
                values=[
                    "Dark",
                    "Light",
                    "System"
                ],
                width=160,
                command=self.change_theme
            )
        )

        self.theme_menu.set(
            self.settings.get(
                "appearance_mode",
                "Dark"
            )
        )

        self.theme_menu.pack(
            side="right"
        )

    # =================================================
    # CHANGE THEME
    # =================================================

    def change_theme(
        self,
        value
    ):

        update_setting(
            "appearance_mode",
            value
        )

        self.settings[
            "appearance_mode"
        ] = value

        ctk.set_appearance_mode(
            value.lower()
        )

        app = (
            self.winfo_toplevel()
        )

        if hasattr(
            app,
            "sync_theme_controls"
        ):

            app.sync_theme_controls()

    # =================================================
    # EXPORT SETTINGS
    # =================================================

    def create_export_section(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        ctk.CTkLabel(
            card,
            text="Exports",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        ctk.CTkLabel(
            card,
            text=(
                "Choose the default folder used "
                "when exporting LifeOS reports."
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        row = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        self.export_path_label = (
            ctk.CTkLabel(
                row,
                text=self.settings.get(
                    "export_folder",
                    get_default_export_path()
                ),
                anchor="w"
            )
        )

        self.export_path_label.pack(
            side="left",
            fill="x",
            expand=True
        )

        ctk.CTkButton(
            row,
            text="Choose Folder",
            width=130,
            command=self.choose_export_folder
        ).pack(
            side="right",
            padx=(10, 0)
        )

        ctk.CTkButton(
            row,
            text="Open",
            width=80,
            command=self.open_export_folder
        ).pack(
            side="right",
            padx=(10, 0)
        )

    # =================================================
    # CHOOSE EXPORT FOLDER
    # =================================================

    def choose_export_folder(self):

        current_folder = (
            self.settings.get(
                "export_folder",
                get_default_export_path()
            )
        )

        folder = (
            filedialog.askdirectory(
                parent=self,
                title=(
                    "Choose LifeOS "
                    "Export Folder"
                ),
                initialdir=current_folder
            )
        )

        if not folder:

            return

        update_setting(
            "export_folder",
            folder
        )

        self.settings[
            "export_folder"
        ] = folder

        self.export_path_label.configure(
            text=folder
        )

    # =================================================
    # OPEN EXPORT FOLDER
    # =================================================

    def open_export_folder(self):

        folder = (
            self.settings.get(
                "export_folder",
                get_default_export_path()
            )
        )

        try:

            os.makedirs(
                folder,
                exist_ok=True
            )

            if os.name == "nt":

                os.startfile(
                    folder
                )

            else:

                messagebox.showinfo(
                    "Export Folder",
                    folder,
                    parent=self
                )

        except Exception as error:

            messagebox.showerror(
                "Folder Error",
                (
                    "The export folder "
                    "could not be opened.\n\n"
                    f"{error}"
                ),
                parent=self
            )

    # =================================================
    # DATA MANAGEMENT
    # =================================================

    def create_data_section(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        ctk.CTkLabel(
            card,
            text="Data Management",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        ctk.CTkLabel(
            card,
            text=(
                "LifeOS stores its data locally "
                "inside an SQLite database."
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # ---------------------------------------------
        # DATABASE PATH
        # ---------------------------------------------

        database_frame = (
            ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
        )

        database_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        ctk.CTkLabel(
            database_frame,
            text="Database:",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            database_frame,
            text=get_database_path(),
            anchor="w"
        ).pack(
            side="left",
            padx=10,
            fill="x",
            expand=True
        )

        # ---------------------------------------------
        # BUTTONS
        # ---------------------------------------------

        button_frame = (
            ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=(15, 20)
        )

        ctk.CTkButton(
            button_frame,
            text="Backup Database",
            width=150,
            command=self.backup_data
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ctk.CTkButton(
            button_frame,
            text="Restore Database",
            width=150,
            command=self.restore_data
        ).pack(
            side="left"
        )

        ctk.CTkButton(
            button_frame,
            text="Reset Settings",
            width=130,
            fg_color="transparent",
            border_width=1,
            command=self.reset_app_settings
        ).pack(
            side="right"
        )

    # =================================================
    # BACKUP
    # =================================================

    def backup_data(self):

        filename = (
            "LifeOS_Backup.db"
        )

        file_path = (
            filedialog.asksaveasfilename(
                parent=self,
                title=(
                    "Backup LifeOS Database"
                ),
                defaultextension=".db",
                initialfile=filename,
                filetypes=[
                    (
                        "SQLite Database",
                        "*.db"
                    )
                ]
            )
        )

        if not file_path:

            return

        try:

            backup_database(
                file_path
            )

            messagebox.showinfo(
                "Backup Complete",
                (
                    "Your LifeOS database "
                    "was backed up successfully."
                ),
                parent=self
            )

        except Exception as error:

            messagebox.showerror(
                "Backup Error",
                (
                    "The database could not "
                    "be backed up.\n\n"
                    f"{error}"
                ),
                parent=self
            )

    # =================================================
    # RESTORE
    # =================================================

    def restore_data(self):

        file_path = (
            filedialog.askopenfilename(
                parent=self,
                title=(
                    "Restore LifeOS Database"
                ),
                filetypes=[
                    (
                        "SQLite Database",
                        "*.db"
                    )
                ]
            )
        )

        if not file_path:

            return

        confirm = (
            messagebox.askyesno(
                "Restore Database",
                (
                    "Restoring a database will "
                    "replace the current LifeOS data.\n\n"
                    "A safety backup of the current "
                    "database will be created automatically.\n\n"
                    "Continue?"
                ),
                parent=self
            )
        )

        if not confirm:

            return

        try:

            restore_database(
                file_path
            )

            messagebox.showinfo(
                "Restore Complete",
                (
                    "The database was restored "
                    "successfully.\n\n"
                    "Restart LifeOS to ensure all "
                    "pages reload the restored data."
                ),
                parent=self
            )

        except Exception as error:

            messagebox.showerror(
                "Restore Error",
                (
                    "The database could not "
                    "be restored.\n\n"
                    f"{error}"
                ),
                parent=self
            )

    # =================================================
    # RESET SETTINGS
    # =================================================

    def reset_app_settings(self):

        confirm = (
            messagebox.askyesno(
                "Reset Settings",
                (
                    "Reset LifeOS settings "
                    "to their default values?"
                ),
                parent=self
            )
        )

        if not confirm:

            return

        self.settings = (
            reset_settings()
        )

        theme = (
            self.settings[
                "appearance_mode"
            ]
        )

        ctk.set_appearance_mode(
            theme.lower()
        )

        self.theme_menu.set(
            theme
        )

        self.export_path_label.configure(
            text=self.settings[
                "export_folder"
            ]
        )

        app = (
            self.winfo_toplevel()
        )

        if hasattr(
            app,
            "sync_theme_controls"
        ):

            app.sync_theme_controls()

        messagebox.showinfo(
            "Settings Reset",
            (
                "LifeOS settings were "
                "restored to defaults."
            ),
            parent=self
        )

    # =================================================
    # ABOUT
    # =================================================

    def create_about_section(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=25,
            pady=(10, 30)
        )

        # ---------------------------------------------
        # TITLE
        # ---------------------------------------------

        ctk.CTkLabel(
            card,
            text="About LifeOS",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(22, 5)
        )

        ctk.CTkLabel(
            card,
            text=(
                "Personal Productivity "
                "Management System"
            ),
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25
        )

        version = (
            self.settings.get(
                "app_version",
                "1.0.0"
            )
        )

        ctk.CTkLabel(
            card,
            text=f"Version {version}",
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(3, 18)
        )

        # ---------------------------------------------
        # OVERVIEW
        # ---------------------------------------------

        self.create_about_subsection(
            card,
            "Overview",
            (
                "LifeOS is an offline desktop productivity "
                "application designed to bring everyday "
                "planning, task management, focus tracking, "
                "time management, notes, analytics, history "
                "and reporting into one application.\n\n"
                "The project is designed as a Python-based "
                "desktop system rather than a web application. "
                "All core functionality works locally without "
                "requiring an internet connection or an "
                "external cloud service."
            )
        )

        # ---------------------------------------------
        # CORE MODULES
        # ---------------------------------------------

        self.create_about_subsection(
            card,
            "Core Modules",
            (
                "• Dashboard — daily overview containing "
                "tasks, plans, focus statistics, productivity "
                "score, weekly productivity and quick actions.\n\n"

                "• Task Manager — create, edit, prioritize, "
                "categorize, schedule, filter, complete and "
                "delete tasks.\n\n"

                "• Planner — interactive monthly calendar "
                "with dated activities, start/end times, "
                "categories and completion tracking.\n\n"

                "• Focus Mode — distraction-oriented timer "
                "linked to General or a task. Leaving Focus "
                "Mode requires confirmation and elapsed focus "
                "time is stored even when a session is stopped.\n\n"

                "• Pomodoro — Focus, Short Break and Long "
                "Break timers with stored session history.\n\n"

                "• Stopwatch — time tracking with pause, "
                "resume, lap recording and saved sessions.\n\n"

                "• Notes — local categorized notes with "
                "searching and editing support.\n\n"

                "• Analytics — productivity scoring and "
                "Matplotlib/Seaborn visualizations based on "
                "real LifeOS activity.\n\n"

                "• History — categorized activity history "
                "for Focus, Pomodoro, Stopwatch, Tasks and "
                "Planner records.\n\n"

                "• Reports — Daily, Weekly and Monthly task "
                "completion reports with category summaries "
                "and TXT export.\n\n"

                "• Settings — appearance preferences, export "
                "configuration, local database backup/restore "
                "and application information."
            )
        )

        # ---------------------------------------------
        # PRODUCTIVITY SCORE
        # ---------------------------------------------

        self.create_about_subsection(
            card,
            "Productivity Score",
            (
                "LifeOS calculates an explainable productivity "
                "score rather than using an unexplained random "
                "rating. The current model uses task completion, "
                "tracked focus time and planner completion.\n\n"
                "Tasks contribute 50%, Focus contributes 30%, "
                "and Planner completion contributes 20% of the "
                "daily score."
            )
        )

        # ---------------------------------------------
        # TECHNOLOGY
        # ---------------------------------------------

        self.create_about_subsection(
            card,
            "Technology Stack",
            (
                "Language: Python 3\n"
                "Interface: CustomTkinter / Tkinter\n"
                "Database: SQLite\n"
                "Charts: Matplotlib and Seaborn\n"
                "Image Support: Pillow\n"
                "Configuration: JSON\n"
                "Packaging Target: PyInstaller\n\n"
                "Python standard-library modules are also used "
                "for dates, file handling, paths, SQLite access, "
                "JSON configuration and application utilities."
            )
        )

        # ---------------------------------------------
        # DATA / PRIVACY
        # ---------------------------------------------

        self.create_about_subsection(
            card,
            "Offline Data & Privacy",
            (
                "LifeOS is designed as an offline-first desktop "
                "application. Tasks, planner activities, notes, "
                "focus sessions, Pomodoro sessions, Stopwatch "
                "sessions and related history are stored in a "
                "local SQLite database.\n\n"
                "The application does not require a LifeOS "
                "account, online login, remote database or cloud "
                "synchronization for its core functionality."
            )
        )

        # ---------------------------------------------
        # FILE LOCATIONS
        # ---------------------------------------------

        file_info = (
            f"Database:\n"
            f"{get_database_path()}\n\n"

            f"Settings:\n"
            f"{get_settings_path()}\n\n"

            f"Current Export Folder:\n"
            f"{self.settings.get('export_folder')}"
        )

        self.create_about_subsection(
            card,
            "Local Storage",
            file_info
        )

        # ---------------------------------------------
        # PROJECT PURPOSE
        # ---------------------------------------------

        self.create_about_subsection(
            card,
            "Project Purpose",
            (
                "LifeOS was developed as a Python mini-project "
                "that demonstrates practical application of "
                "GUI programming, functions, conditional logic, "
                "loops, collections, modules, exception handling, "
                "file handling, object-oriented programming, "
                "SQLite database operations and data visualization "
                "inside a single usable desktop application."
            )
        )

        # ---------------------------------------------
        # FOOTER
        # ---------------------------------------------

        ctk.CTkLabel(
            card,
            text=(
                "LifeOS • Local productivity, "
                "planning and focus in one place."
            ),
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            anchor="center",
            padx=25,
            pady=(10, 25)
        )

    # =================================================
    # ABOUT SUBSECTION HELPER
    # =================================================

    def create_about_subsection(
        self,
        parent,
        title,
        content
    ):

        frame = ctk.CTkFrame(
            parent,
            corner_radius=12
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=7
        )

        ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 5)
        )

        ctk.CTkLabel(
            frame,
            text=content,
            justify="left",
            anchor="w",
            wraplength=1050
        ).pack(
            anchor="w",
            fill="x",
            padx=18,
            pady=(0, 15)
        )

    # =================================================
    # REFRESH
    # =================================================

    def refresh_settings(self):

        self.settings = (
            load_settings()
        )

        self.theme_menu.set(
            self.settings.get(
                "appearance_mode",
                "Dark"
            )
        )

        self.export_path_label.configure(
            text=self.settings.get(
                "export_folder",
                get_default_export_path()
            )
        )