import customtkinter as ctk
from datetime import datetime


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

    # -------------------------------------------------
    # HEADER
    # -------------------------------------------------

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
            font=ctk.CTkFont(size=15)
        )

        subtitle.grid(
            row=1,
            column=0,
            columnspan=4,
            padx=25,
            pady=(0, 20),
            sticky="w"
        )

    # -------------------------------------------------
    # STAT CARDS
    # -------------------------------------------------

    def create_stat_cards(self):

        stats = [
            ("Tasks", "7 / 10", "70% completed"),
            ("Focus Time", "2h 30m", "Today"),
            ("Pomodoros", "5", "Sessions"),
            ("Productivity", "82%", "Good")
        ]

        for column, data in enumerate(stats):

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

            card.grid_propagate(False)

            title = ctk.CTkLabel(
                card,
                text=data[0],
                font=ctk.CTkFont(
                    size=15,
                    weight="bold"
                )
            )

            title.pack(
                anchor="w",
                padx=18,
                pady=(18, 5)
            )

            value = ctk.CTkLabel(
                card,
                text=data[1],
                font=ctk.CTkFont(
                    size=28,
                    weight="bold"
                )
            )

            value.pack(
                anchor="w",
                padx=18
            )

            subtitle = ctk.CTkLabel(
                card,
                text=data[2],
                font=ctk.CTkFont(size=13)
            )

            subtitle.pack(
                anchor="w",
                padx=18,
                pady=(3, 10)
            )

    # -------------------------------------------------
    # MAIN SECTION
    # -------------------------------------------------

    def create_main_section(self):

        # Today's Tasks
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

        title = ctk.CTkLabel(
            tasks_card,
            text="Today's Tasks",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        tasks = [
            "Complete Python Project",
            "Review Database Notes",
            "Finish Assignment",
            "Read Chapter 4"
        ]

        for task in tasks:

            checkbox = ctk.CTkCheckBox(
                tasks_card,
                text=task
            )

            checkbox.pack(
                anchor="w",
                padx=20,
                pady=7
            )

        add_task = ctk.CTkButton(
            tasks_card,
            text="+ Add Task",
            width=120
        )

        add_task.pack(
            anchor="w",
            padx=20,
            pady=20
        )

        # Quick Focus
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

        focus_title = ctk.CTkLabel(
            focus_card,
            text="Quick Focus",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        focus_title.pack(
            pady=(25, 10)
        )

        timer = ctk.CTkLabel(
            focus_card,
            text="25:00",
            font=ctk.CTkFont(
                size=46,
                weight="bold"
            )
        )

        timer.pack(
            pady=15
        )

        task_label = ctk.CTkLabel(
            focus_card,
            text="Current Task: Python Project"
        )

        task_label.pack(
            pady=5
        )

        start_button = ctk.CTkButton(
            focus_card,
            text="Start Focus",
            width=150,
            height=42
        )

        start_button.pack(
            pady=20
        )

    # -------------------------------------------------
    # SECONDARY SECTION
    # -------------------------------------------------

    def create_secondary_section(self):

        # Analytics placeholder
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

        analytics_card.grid_propagate(False)

        title = ctk.CTkLabel(
            analytics_card,
            text="Weekly Productivity",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=20
        )

        placeholder = ctk.CTkLabel(
            analytics_card,
            text="Productivity chart will appear here",
            font=ctk.CTkFont(size=15)
        )

        placeholder.pack(
            expand=True
        )

        # Quick Notes
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

        notes_title = ctk.CTkLabel(
            notes_card,
            text="Quick Note",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        notes_title.pack(
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

        save_button = ctk.CTkButton(
            notes_card,
            text="Save Note",
            width=120
        )

        save_button.pack(
            anchor="e",
            padx=20,
            pady=(5, 20)
        )

    # -------------------------------------------------
    # PLANNER
    # -------------------------------------------------

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

        title = ctk.CTkLabel(
            planner_card,
            text="Today's Plan",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        schedule = [
            "09:00   Study Python",
            "11:00   College Work",
            "14:00   LifeOS Development",
            "18:00   Workout",
            "21:00   Revision"
        ]

        for activity in schedule:

            label = ctk.CTkLabel(
                planner_card,
                text=activity,
                font=ctk.CTkFont(size=14)
            )

            label.pack(
                anchor="w",
                padx=20,
                pady=5
            )

        ctk.CTkLabel(
            planner_card,
            text=""
        ).pack()