import customtkinter as ctk

from datetime import datetime

from database.database import (
    get_task_statistics,
    get_today_tasks,
    toggle_task
)


class DashboardPage(ctk.CTkScrollableFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            corner_radius=0
        )

        self.grid_columnconfigure(
            (0, 1, 2, 3),
            weight=1
        )

        self.create_header()
        self.create_stat_cards()
        self.create_main_section()
        self.create_secondary_section()
        self.create_planner_section()

        self.refresh_dashboard()

    # =================================================
    # HEADER
    # =================================================

    def create_header(self):

        current_hour = datetime.now().hour

        if current_hour < 12:
            greeting = "Good Morning"

        elif current_hour < 18:
            greeting = "Good Afternoon"

        else:
            greeting = "Good Evening"

        title = ctk.CTkLabel(
            self,
            text=f"{greeting} 👋",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=25,
            pady=(25, 5),
            sticky="w"
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Here's your day at a glance.",
            font=ctk.CTkFont(
                size=15
            )
        )

        subtitle.grid(
            row=1,
            column=0,
            columnspan=4,
            padx=25,
            pady=(0, 20),
            sticky="w"
        )

    # =================================================
    # STAT CARDS
    # =================================================

    def create_stat_cards(self):

        self.tasks_value = self.create_stat_card(
            0,
            "Tasks",
            "0 / 0",
            "Pending / Total"
        )

        self.focus_value = self.create_stat_card(
            1,
            "Focus Time",
            "0m",
            "Today"
        )

        self.pomodoro_value = self.create_stat_card(
            2,
            "Pomodoros",
            "0",
            "Sessions"
        )

        self.productivity_value = self.create_stat_card(
            3,
            "Productivity",
            "0%",
            "Today's Score"
        )

    def create_stat_card(
        self,
        column,
        title,
        value,
        subtitle
    ):

        card = ctk.CTkFrame(
            self,
            corner_radius=15,
            height=130
        )

        card.grid(
            row=2,
            column=column,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        card.grid_propagate(
            False
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        value_label.pack(
            anchor="w",
            padx=18
        )

        ctk.CTkLabel(
            card,
            text=subtitle,
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(3, 10)
        )

        return value_label

    # =================================================
    # MAIN SECTION
    # =================================================

    def create_main_section(self):

        # ---------------------------------------------
        # TODAY'S TASKS
        # ---------------------------------------------

        tasks_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        tasks_card.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        ctk.CTkLabel(
            tasks_card,
            text="Today's Tasks",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        today_text = datetime.now().strftime(
            "%d %b %Y"
        )

        ctk.CTkLabel(
            tasks_card,
            text=today_text,
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 8)
        )

        self.dashboard_tasks_container = (
            ctk.CTkFrame(
                tasks_card,
                fg_color="transparent"
            )
        )

        self.dashboard_tasks_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        # ---------------------------------------------
        # QUICK FOCUS
        # ---------------------------------------------

        focus_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        focus_card.grid(
            row=3,
            column=2,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        ctk.CTkLabel(
            focus_card,
            text="Quick Focus",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            pady=(25, 10)
        )

        self.focus_timer_label = ctk.CTkLabel(
            focus_card,
            text="25:00",
            font=ctk.CTkFont(
                size=46,
                weight="bold"
            )
        )

        self.focus_timer_label.pack(
            pady=15
        )

        self.focus_task_label = ctk.CTkLabel(
            focus_card,
            text="Select a task before starting focus."
        )

        self.focus_task_label.pack(
            pady=5
        )

        self.focus_button = ctk.CTkButton(
            focus_card,
            text="Start Focus",
            width=150,
            height=42
        )

        self.focus_button.pack(
            pady=20
        )

    # =================================================
    # SECONDARY SECTION
    # =================================================

    def create_secondary_section(self):

        analytics_card = ctk.CTkFrame(
            self,
            corner_radius=15,
            height=260
        )

        analytics_card.grid(
            row=4,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        analytics_card.grid_propagate(
            False
        )

        ctk.CTkLabel(
            analytics_card,
            text="Weekly Productivity",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            analytics_card,
            text="Productivity chart will appear here.",
            font=ctk.CTkFont(
                size=15
            )
        ).pack(
            expand=True
        )

        # ---------------------------------------------
        # QUICK NOTES
        # ---------------------------------------------

        notes_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        notes_card.grid(
            row=4,
            column=2,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        ctk.CTkLabel(
            notes_card,
            text="Quick Note",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        self.note_box = ctk.CTkTextbox(
            notes_card,
            height=130
        )

        self.note_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        ctk.CTkButton(
            notes_card,
            text="Save Note",
            width=120
        ).pack(
            anchor="e",
            padx=20,
            pady=(5, 20)
        )

    # =================================================
    # PLANNER
    # =================================================

    def create_planner_section(self):

        planner_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        planner_card.grid(
            row=5,
            column=0,
            columnspan=4,
            padx=10,
            pady=(10, 25),
            sticky="nsew"
        )

        ctk.CTkLabel(
            planner_card,
            text="Today's Plan",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            planner_card,
            text=(
                "Planner activities will appear here "
                "once the Planner module is built."
            ),
            font=ctk.CTkFont(
                size=14
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 20)
        )

    # =================================================
    # REFRESH
    # =================================================

    def refresh_dashboard(self):

        self.load_task_statistics()
        self.load_dashboard_tasks()

    # =================================================
    # TASK STATISTICS
    # =================================================

    def load_task_statistics(self):

        stats = get_task_statistics()

        self.tasks_value.configure(
            text=(
                f"{stats['pending']} / "
                f"{stats['total']}"
            )
        )

    # =================================================
    # TODAY'S TASKS
    # =================================================

    def load_dashboard_tasks(self):

        for widget in (
            self.dashboard_tasks_container
            .winfo_children()
        ):
            widget.destroy()

        tasks = get_today_tasks()

        if not tasks:

            ctk.CTkLabel(
                self.dashboard_tasks_container,
                text="No tasks due today."
            ).pack(
                anchor="w",
                padx=5,
                pady=20
            )

            return

        for task in tasks:

            (
                task_id,
                title,
                due_date,
                priority,
                category,
                completed
            ) = task

            task_frame = ctk.CTkFrame(
                self.dashboard_tasks_container,
                fg_color="transparent"
            )

            task_frame.pack(
                fill="x",
                pady=5
            )

            checkbox = ctk.CTkCheckBox(
                task_frame,
                text=title,
                command=lambda task_id=task_id: (
                    self.complete_dashboard_task(
                        task_id
                    )
                )
            )

            checkbox.pack(
                side="left",
                padx=5
            )

            details = (
                f"{category} • {priority}"
            )

            ctk.CTkLabel(
                task_frame,
                text=details,
                font=ctk.CTkFont(
                    size=11
                )
            ).pack(
                side="right",
                padx=5
            )

    # =================================================
    # COMPLETE DASHBOARD TASK
    # =================================================

    def complete_dashboard_task(
        self,
        task_id
    ):

        toggle_task(
            task_id,
            1
        )

        self.refresh_dashboard()