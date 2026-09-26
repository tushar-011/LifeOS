import customtkinter as ctk

import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg
)

from database.database import (
    get_task_statistics,
    get_today_tasks,
    toggle_task,
    add_note,
    get_today_planner,
    get_today_pomodoro_stats,
    get_today_focus_stats,
    get_productivity_metrics,
    get_weekly_productivity_metrics
)

from utils.productivity import (
    calculate_productivity_score
)


# =================================================
# DASHBOARD
# =================================================

class DashboardPage(
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
            (0, 1, 2, 3),
            weight=1
        )

        # Quick Focus task mapping
        self.quick_focus_lookup = {}

        # Weekly chart reference
        self.weekly_chart_canvas = None

        self.create_header()

        self.create_stat_cards()

        self.create_main_section()

        self.create_secondary_section()

        self.create_today_section()

        self.refresh_dashboard()

    # =================================================
    # HEADER
    # =================================================

    def create_header(self):

        current_hour = (
            datetime.now().hour
        )

        if current_hour < 12:

            greeting = (
                "Good Morning"
            )

        elif current_hour < 18:

            greeting = (
                "Good Afternoon"
            )

        else:

            greeting = (
                "Good Evening"
            )

        ctk.CTkLabel(
            self,
            text=f"{greeting} 👋",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            padx=25,
            pady=(25, 5),
            sticky="w"
        )

        ctk.CTkLabel(
            self,
            text=(
                "Here's your day "
                "at a glance."
            ),
            font=ctk.CTkFont(
                size=15
            )
        ).grid(
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

        # ---------------------------------------------
        # TASKS
        # ---------------------------------------------

        self.tasks_value = (
            self.create_stat_card(
                0,
                "Tasks",
                "0 / 0",
                "Pending / Total"
            )
        )

        # ---------------------------------------------
        # FOCUS
        # ---------------------------------------------

        self.focus_value = (
            self.create_stat_card(
                1,
                "Focus Time",
                "0m",
                "Today"
            )
        )

        # ---------------------------------------------
        # POMODORO
        # ---------------------------------------------

        self.pomodoro_value = (
            self.create_stat_card(
                2,
                "Pomodoros",
                "0",
                "Sessions Today"
            )
        )

        # ---------------------------------------------
        # PRODUCTIVITY
        # ---------------------------------------------

        self.productivity_value = (
            self.create_stat_card(
                3,
                "Productivity",
                "0%",
                "Today's Score"
            )
        )

    # =================================================
    # CREATE STAT CARD
    # =================================================

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

        value_label = (
            ctk.CTkLabel(
                card,
                text=value,
                font=ctk.CTkFont(
                    size=28,
                    weight="bold"
                )
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

        # =================================================
        # TODAY'S TASKS
        # =================================================

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

        # =================================================
        # QUICK FOCUS
        # =================================================

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
            pady=(20, 10)
        )

        # ---------------------------------------------
        # TASK DROPDOWN
        # ---------------------------------------------

        self.quick_focus_menu = (
            ctk.CTkOptionMenu(
                focus_card,
                values=[
                    "General"
                ],
                width=300
            )
        )

        self.quick_focus_menu.set(
            "General"
        )

        self.quick_focus_menu.pack(
            pady=(5, 10)
        )

        # ---------------------------------------------
        # TIMER
        # ---------------------------------------------

        self.focus_timer_label = (
            ctk.CTkLabel(
                focus_card,
                text="25:00",
                font=ctk.CTkFont(
                    size=46,
                    weight="bold"
                )
            )
        )

        self.focus_timer_label.pack(
            pady=5
        )

        ctk.CTkLabel(
            focus_card,
            text=(
                "25 minute Focus Mode session"
            )
        ).pack(
            pady=5
        )

        # ---------------------------------------------
        # START
        # ---------------------------------------------

        self.focus_button = (
            ctk.CTkButton(
                focus_card,
                text="Start Quick Focus",
                width=170,
                height=42,
                command=self.open_quick_focus
            )
        )

        self.focus_button.pack(
            pady=(10, 20)
        )

    # =================================================
    # SECONDARY SECTION
    # =================================================

    def create_secondary_section(self):

        # =================================================
        # WEEKLY PRODUCTIVITY
        # =================================================

        self.analytics_card = (
            ctk.CTkFrame(
                self,
                corner_radius=15,
                height=290
            )
        )

        self.analytics_card.grid(
            row=4,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        self.analytics_card.grid_propagate(
            False
        )

        ctk.CTkLabel(
            self.analytics_card,
            text="Weekly Productivity",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        self.weekly_chart_frame = (
            ctk.CTkFrame(
                self.analytics_card,
                fg_color="transparent"
            )
        )

        self.weekly_chart_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        # =================================================
        # QUICK NOTE
        # =================================================

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

        self.note_box = (
            ctk.CTkTextbox(
                notes_card,
                height=130
            )
        )

        self.note_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.quick_note_message = (
            ctk.CTkLabel(
                notes_card,
                text=""
            )
        )

        self.quick_note_message.pack(
            anchor="w",
            padx=20
        )

        ctk.CTkButton(
            notes_card,
            text="Save Note",
            width=120,
            command=self.save_quick_note
        ).pack(
            anchor="e",
            padx=20,
            pady=(5, 20)
        )

    # =================================================
    # TODAY SECTION
    # =================================================

    def create_today_section(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.grid(
            row=5,
            column=0,
            columnspan=4,
            padx=10,
            pady=(10, 25),
            sticky="nsew"
        )

        card.grid_columnconfigure(
            0,
            weight=1
        )

        card.grid_columnconfigure(
            1,
            weight=3
        )

        # =================================================
        # DATE
        # =================================================

        date_frame = (
            ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
        )

        date_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=20,
            pady=20
        )

        now = (
            datetime.now()
        )

        ctk.CTkLabel(
            date_frame,
            text="TODAY",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            date_frame,
            text=now.strftime(
                "%A"
            ),
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(8, 0)
        )

        ctk.CTkLabel(
            date_frame,
            text=now.strftime(
                "%d %B %Y"
            ),
            font=ctk.CTkFont(
                size=15
            )
        ).pack(
            anchor="w"
        )

        # =================================================
        # TODAY'S PLAN
        # =================================================

        plan_frame = (
            ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
        )

        plan_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            plan_frame,
            text="Today's Plan",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        self.planner_container = (
            ctk.CTkFrame(
                plan_frame,
                fg_color="transparent"
            )
        )

        self.planner_container.pack(
            fill="both",
            expand=True
        )

    # =================================================
    # REFRESH DASHBOARD
    # =================================================

    def refresh_dashboard(self):

        self.load_task_statistics()

        self.load_focus_statistics()

        self.load_productivity()

        self.load_dashboard_tasks()

        self.load_today_plan()

        self.load_quick_focus_tasks()

        self.load_weekly_productivity()

    # =================================================
    # TASK STATISTICS
    # =================================================

    def load_task_statistics(self):

        stats = (
            get_task_statistics()
        )

        self.tasks_value.configure(
            text=(
                f"{stats['pending']} / "
                f"{stats['total']}"
            )
        )

    # =================================================
    # FOCUS STATISTICS
    # =================================================

    def load_focus_statistics(self):

        pomodoro = (
            get_today_pomodoro_stats()
        )

        focus = (
            get_today_focus_stats()
        )

        # ---------------------------------------------
        # POMODORO COUNT
        # ---------------------------------------------

        self.pomodoro_value.configure(
            text=str(
                pomodoro[
                    "sessions"
                ]
            )
        )

        # ---------------------------------------------
        # TOTAL FOCUS TIME
        # ---------------------------------------------

        total_seconds = (
            (
                pomodoro[
                    "focus_minutes"
                ]
                * 60
            )
            +
            focus[
                "focus_seconds"
            ]
        )

        self.focus_value.configure(
            text=self.format_seconds(
                total_seconds
            )
        )

    # =================================================
    # PRODUCTIVITY
    # =================================================

    def load_productivity(self):

        metrics = (
            get_productivity_metrics()
        )

        score = (
            calculate_productivity_score(
                metrics[
                    "tasks_completed"
                ],

                metrics[
                    "tasks_total"
                ],

                metrics[
                    "focus_minutes"
                ],

                metrics[
                    "planner_completed"
                ],

                metrics[
                    "planner_total"
                ]
            )
        )

        self.productivity_value.configure(
            text=f"{score}%"
        )

    # =================================================
    # WEEKLY PRODUCTIVITY CHART
    # =================================================

    def load_weekly_productivity(self):

        # ---------------------------------------------
        # CLEAR OLD CHART
        # ---------------------------------------------

        for widget in (
            self.weekly_chart_frame
            .winfo_children()
        ):

            widget.destroy()

        weekly = (
            get_weekly_productivity_metrics(
                7
            )
        )

        labels = []
        scores = []

        for metrics in weekly:

            try:

                day = datetime.strptime(
                    metrics["date"],
                    "%Y-%m-%d"
                )

                label = day.strftime(
                    "%a"
                )

            except Exception:

                label = (
                    metrics["date"]
                )

            labels.append(
                label
            )

            score = (
                calculate_productivity_score(
                    metrics[
                        "tasks_completed"
                    ],
                    metrics[
                        "tasks_total"
                    ],
                    metrics[
                        "focus_minutes"
                    ],
                    metrics[
                        "planner_completed"
                    ],
                    metrics[
                        "planner_total"
                    ]
                )
            )

            scores.append(
                score
            )

        # ---------------------------------------------
        # MATPLOTLIB FIGURE
        # ---------------------------------------------

        figure, axis = (
            plt.subplots(
                figsize=(5.4, 2.3)
            )
        )

        sns.lineplot(
            x=labels,
            y=scores,
            marker="o",
            ax=axis
        )

        axis.set_ylim(
            0,
            100
        )

        axis.set_ylabel(
            "Score"
        )

        axis.set_xlabel(
            ""
        )

        axis.grid(
            True,
            alpha=0.2
        )

        figure.tight_layout()

        # ---------------------------------------------
        # EMBED IN CUSTOMTKINTER
        # ---------------------------------------------

        canvas = (
            FigureCanvasTkAgg(
                figure,
                master=(
                    self
                    .weekly_chart_frame
                )
            )
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        self.weekly_chart_canvas = (
            canvas
        )

        plt.close(
            figure
        )

    # =================================================
    # DASHBOARD TASKS
    # =================================================

    def load_dashboard_tasks(self):

        for widget in (
            self
            .dashboard_tasks_container
            .winfo_children()
        ):

            widget.destroy()

        tasks = (
            get_today_tasks()
        )

        if not tasks:

            ctk.CTkLabel(
                self
                .dashboard_tasks_container,
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

            row = ctk.CTkFrame(
                self
                .dashboard_tasks_container,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                pady=5
            )

            checkbox = (
                ctk.CTkCheckBox(
                    row,
                    text=title,
                    command=(
                        lambda task_id=task_id:
                        self.complete_dashboard_task(
                            task_id
                        )
                    )
                )
            )

            checkbox.pack(
                side="left",
                padx=5
            )

            ctk.CTkLabel(
                row,
                text=(
                    f"{category} • "
                    f"{priority}"
                ),
                font=ctk.CTkFont(
                    size=11
                )
            ).pack(
                side="right",
                padx=5
            )

    # =================================================
    # COMPLETE TASK
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

    # =================================================
    # QUICK FOCUS TASKS
    # =================================================

    def load_quick_focus_tasks(self):

        tasks = (
            get_today_tasks(
                limit=100
            )
        )

        current_value = (
            self.quick_focus_menu
            .get()
        )

        # ---------------------------------------------
        # GENERAL ALWAYS AVAILABLE
        # ---------------------------------------------

        self.quick_focus_lookup = {

            "General": {
                "id": None,
                "title": "General"
            }

        }

        values = [
            "General"
        ]

        # ---------------------------------------------
        # TODAY'S TASKS
        # ---------------------------------------------

        for task in tasks:

            (
                task_id,
                title,
                due_date,
                priority,
                category,
                completed
            ) = task

            display = (
                f"{title} • "
                f"{priority}"
            )

            values.append(
                display
            )

            self.quick_focus_lookup[
                display
            ] = {
                "id": task_id,
                "title": title
            }

        self.quick_focus_menu.configure(
            values=values
        )

        if (
            current_value
            in values
        ):

            self.quick_focus_menu.set(
                current_value
            )

        else:

            self.quick_focus_menu.set(
                "General"
            )

    # =================================================
    # OPEN QUICK FOCUS
    # =================================================

    def open_quick_focus(self):

        selected = (
            self.quick_focus_menu
            .get()
        )

        app = (
            self.winfo_toplevel()
        )

        if not hasattr(
            app,
            "show_focus"
        ):

            return

        # ---------------------------------------------
        # OPEN FOCUS PAGE
        # ---------------------------------------------

        app.show_focus()

        focus_page = (
            app.pages.get(
                "Focus"
            )
        )

        if focus_page is None:

            return

        # ---------------------------------------------
        # REFRESH TASKS
        # ---------------------------------------------

        focus_page.load_tasks()

        # ---------------------------------------------
        # SELECT CHOSEN ITEM
        # ---------------------------------------------

        if (
            selected
            in focus_page.task_lookup
        ):

            focus_page.task_menu.set(
                selected
            )

        # ---------------------------------------------
        # START 25 MINUTES
        # ---------------------------------------------

        if not (
            focus_page
            .is_session_active()
        ):

            focus_page.duration_menu.set(
                "25 minutes"
            )

            focus_page.change_duration(
                "25 minutes"
            )

            focus_page.start_focus()

    # =================================================
    # QUICK NOTE
    # =================================================

    def save_quick_note(self):

        content = (
            self.note_box
            .get(
                "1.0",
                "end"
            )
            .strip()
        )

        if not content:

            self.quick_note_message.configure(
                text=(
                    "Write something first."
                )
            )

            return

        title = (
            datetime.now()
            .strftime(
                "Quick Note - "
                "%d %b %Y "
                "%I:%M %p"
            )
        )

        add_note(
            title,
            content,
            "General"
        )

        self.note_box.delete(
            "1.0",
            "end"
        )

        self.quick_note_message.configure(
            text="Note saved."
        )

    # =================================================
    # TODAY'S PLAN
    # =================================================

    def load_today_plan(self):

        for widget in (
            self
            .planner_container
            .winfo_children()
        ):

            widget.destroy()

        activities = (
            get_today_planner(
                limit=10
            )
        )

        if not activities:

            ctk.CTkLabel(
                self
                .planner_container,
                text=(
                    "Nothing planned "
                    "for today."
                )
            ).pack(
                anchor="w",
                pady=10
            )

            return

        for activity in activities:

            (
                activity_id,
                title,
                activity_date,
                start_time,
                end_time,
                category,
                completed
            ) = activity

            row = ctk.CTkFrame(
                self.planner_container,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                pady=5
            )

            # -----------------------------------------
            # TIME
            # -----------------------------------------

            ctk.CTkLabel(
                row,
                text=self.format_time(
                    start_time
                ),
                width=90,
                anchor="w",
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                )
            ).pack(
                side="left"
            )

            # -----------------------------------------
            # TITLE
            # -----------------------------------------

            activity_text = (
                f"✓ {title}"
                if completed
                else title
            )

            ctk.CTkLabel(
                row,
                text=activity_text,
                font=ctk.CTkFont(
                    size=14
                )
            ).pack(
                side="left",
                padx=10
            )

    # =================================================
    # FORMAT PLANNER TIME
    # =================================================

    def format_time(
        self,
        value
    ):

        try:

            parsed = (
                datetime.strptime(
                    value,
                    "%H:%M"
                )
            )

            return (
                parsed.strftime(
                    "%I:%M %p"
                )
                .lstrip("0")
            )

        except (
            ValueError,
            TypeError
        ):

            return (
                value
                if value
                else "--"
            )

    # =================================================
    # FORMAT SECONDS
    # =================================================

    def format_seconds(
        self,
        seconds
    ):

        seconds = int(
            seconds
        )

        hours = (
            seconds
            // 3600
        )

        minutes = (
            (
                seconds
                % 3600
            )
            // 60
        )

        if hours:

            if minutes:

                return (
                    f"{hours}h "
                    f"{minutes}m"
                )

            return (
                f"{hours}h"
            )

        return (
            f"{minutes}m"
        )