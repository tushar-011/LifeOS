import customtkinter as ctk

from datetime import datetime

from database.database import (
    get_history_counts,
    get_focus_history,
    get_pomodoro_history,
    get_stopwatch_history,
    get_task_history,
    get_planner_history
)


class HistoryPage(
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

        self.selected_type = (
            "All"
        )

        self.selected_period = (
            "All Time"
        )

        self.create_header()
        self.create_summary()
        self.create_filters()
        self.create_history_section()

        self.refresh_history()

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
            text="History",
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
                "Review your LifeOS activity "
                "by category and time period."
            ),
            font=ctk.CTkFont(
                size=14
            )
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

    # =================================================
    # SUMMARY CARDS
    # =================================================

    def create_summary(self):

        self.summary_frame = (
            ctk.CTkFrame(
                self,
                fg_color="transparent"
            )
        )

        self.summary_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        self.summary_frame.grid_columnconfigure(
            (0, 1, 2, 3, 4),
            weight=1
        )

        self.summary_labels = {}

        categories = [
            "Focus",
            "Pomodoro",
            "Stopwatch",
            "Tasks",
            "Planner"
        ]

        for (
            index,
            category
        ) in enumerate(
            categories
        ):

            card = ctk.CTkFrame(
                self.summary_frame,
                corner_radius=15
            )

            card.grid(
                row=0,
                column=index,
                padx=5,
                sticky="nsew"
            )

            ctk.CTkLabel(
                card,
                text=category,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                )
            ).pack(
                anchor="w",
                padx=14,
                pady=(14, 3)
            )

            value = ctk.CTkLabel(
                card,
                text="0",
                font=ctk.CTkFont(
                    size=24,
                    weight="bold"
                )
            )

            value.pack(
                anchor="w",
                padx=14,
                pady=(0, 14)
            )

            self.summary_labels[
                category
            ] = value

    # =================================================
    # FILTERS
    # =================================================

    def create_filters(self):

        filter_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        filter_card.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        top = ctk.CTkFrame(
            filter_card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=20,
            pady=18
        )

        # ---------------------------------------------
        # CATEGORY
        # ---------------------------------------------

        ctk.CTkLabel(
            top,
            text="Category",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            side="left",
            padx=(0, 10)
        )

        self.type_filter = (
            ctk.CTkSegmentedButton(
                top,
                values=[
                    "All",
                    "Focus",
                    "Pomodoro",
                    "Stopwatch",
                    "Tasks",
                    "Planner"
                ],
                command=self.change_type
            )
        )

        self.type_filter.set(
            "All"
        )

        self.type_filter.pack(
            side="left"
        )

        # ---------------------------------------------
        # PERIOD
        # ---------------------------------------------

        self.period_menu = (
            ctk.CTkOptionMenu(
                top,
                values=[
                    "All Time",
                    "Today",
                    "Last 7 Days",
                    "Last 30 Days"
                ],
                command=self.change_period,
                width=150
            )
        )

        self.period_menu.set(
            "All Time"
        )

        self.period_menu.pack(
            side="right"
        )

        ctk.CTkLabel(
            top,
            text="Period",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            side="right",
            padx=10
        )

    # =================================================
    # HISTORY SECTION
    # =================================================

    def create_history_section(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=25,
            pady=(10, 25)
        )

        self.history_title = (
            ctk.CTkLabel(
                card,
                text="All Activity",
                font=ctk.CTkFont(
                    size=20,
                    weight="bold"
                )
            )
        )

        self.history_title.pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        self.history_container = (
            ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
        )

        self.history_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

    # =================================================
    # FILTER CALLBACKS
    # =================================================

    def change_type(
        self,
        value
    ):

        self.selected_type = value

        self.load_history()

    def change_period(
        self,
        value
    ):

        self.selected_period = value

        self.load_history()

    # =================================================
    # REFRESH
    # =================================================

    def refresh_history(self):

        self.load_counts()

        self.load_history()

    # =================================================
    # COUNTS
    # =================================================

    def load_counts(self):

        counts = (
            get_history_counts()
        )

        for (
            category,
            label
        ) in self.summary_labels.items():

            label.configure(
                text=str(
                    counts.get(
                        category,
                        0
                    )
                )
            )

    # =================================================
    # LOAD HISTORY
    # =================================================

    def load_history(self):

        # ---------------------------------------------
        # CLEAR OLD CONTENT
        # ---------------------------------------------

        for widget in (
            self.history_container
            .winfo_children()
        ):

            widget.destroy()

        category = (
            self.selected_type
        )

        period = (
            self.selected_period
        )

        records = []

        # =================================================
        # ALL
        # =================================================

        if category == "All":

            self.history_title.configure(
                text="All Activity"
            )

            for row in (
                get_focus_history(
                    period
                )
            ):

                records.append(
                    self.build_focus_record(
                        row
                    )
                )

            for row in (
                get_pomodoro_history(
                    period
                )
            ):

                records.append(
                    self.build_pomodoro_record(
                        row
                    )
                )

            for row in (
                get_stopwatch_history(
                    period
                )
            ):

                records.append(
                    self.build_stopwatch_record(
                        row
                    )
                )

            for row in (
                get_task_history(
                    period
                )
            ):

                records.append(
                    self.build_task_record(
                        row
                    )
                )

            for row in (
                get_planner_history(
                    period
                )
            ):

                records.append(
                    self.build_planner_record(
                        row
                    )
                )

            records.sort(
                key=lambda item:
                item["sort_date"],
                reverse=True
            )

        # =================================================
        # FOCUS
        # =================================================

        elif category == "Focus":

            self.history_title.configure(
                text="Focus History"
            )

            records = [
                self.build_focus_record(
                    row
                )
                for row
                in get_focus_history(
                    period
                )
            ]

        # =================================================
        # POMODORO
        # =================================================

        elif category == "Pomodoro":

            self.history_title.configure(
                text="Pomodoro History"
            )

            records = [
                self.build_pomodoro_record(
                    row
                )
                for row
                in get_pomodoro_history(
                    period
                )
            ]

        # =================================================
        # STOPWATCH
        # =================================================

        elif category == "Stopwatch":

            self.history_title.configure(
                text="Stopwatch History"
            )

            records = [
                self.build_stopwatch_record(
                    row
                )
                for row
                in get_stopwatch_history(
                    period
                )
            ]

        # =================================================
        # TASKS
        # =================================================

        elif category == "Tasks":

            self.history_title.configure(
                text="Task History"
            )

            records = [
                self.build_task_record(
                    row
                )
                for row
                in get_task_history(
                    period
                )
            ]

        # =================================================
        # PLANNER
        # =================================================

        elif category == "Planner":

            self.history_title.configure(
                text="Planner History"
            )

            records = [
                self.build_planner_record(
                    row
                )
                for row
                in get_planner_history(
                    period
                )
            ]

        # =================================================
        # NO RESULTS
        # =================================================

        if not records:

            ctk.CTkLabel(
                self.history_container,
                text=(
                    "No history found "
                    "for this category "
                    "and period."
                ),
                font=ctk.CTkFont(
                    size=14
                )
            ).pack(
                pady=35
            )

            return

        # =================================================
        # DISPLAY RECORDS
        # =================================================

        for record in records:

            self.create_history_card(
                record
            )

    # =================================================
    # FOCUS RECORD
    # =================================================

    def build_focus_record(
        self,
        row
    ):

        (
            session_id,
            task_title,
            planned_minutes,
            actual_seconds,
            status,
            completed_at
        ) = row

        if not actual_seconds:

            actual_seconds = (
                planned_minutes
                * 60
            )

        return {
            "type": "Focus",
            "title": task_title,
            "details": (
                f"{self.format_seconds(actual_seconds)}"
                f" • {status}"
            ),
            "date": completed_at,
            "sort_date":
                self.parse_date(
                    completed_at
                )
        }

    # =================================================
    # POMODORO RECORD
    # =================================================

    def build_pomodoro_record(
        self,
        row
    ):

        (
            session_id,
            session_type,
            duration,
            completed_at
        ) = row

        return {
            "type": "Pomodoro",
            "title": (
                f"{session_type} Session"
            ),
            "details": (
                f"{duration} minutes"
            ),
            "date": completed_at,
            "sort_date":
                self.parse_date(
                    completed_at
                )
        }

    # =================================================
    # STOPWATCH RECORD
    # =================================================

    def build_stopwatch_record(
        self,
        row
    ):

        (
            session_id,
            duration_seconds,
            lap_count,
            completed_at
        ) = row

        return {
            "type": "Stopwatch",
            "title": "Stopwatch Session",
            "details": (
                f"{self.format_seconds(duration_seconds)}"
                f" • {lap_count} laps"
            ),
            "date": completed_at,
            "sort_date":
                self.parse_date(
                    completed_at
                )
        }

    # =================================================
    # TASK RECORD
    # =================================================

    def build_task_record(
        self,
        row
    ):

        (
            task_id,
            title,
            due_date,
            priority,
            category,
            completed_at,
            created_at
        ) = row

        history_date = (
            completed_at
            or created_at
        )

        details = (
            f"{category} • "
            f"{priority} priority"
        )

        if due_date:

            details += (
                f" • Due {due_date}"
            )

        return {
            "type": "Tasks",
            "title": title,
            "details": details,
            "date": history_date,
            "sort_date":
                self.parse_date(
                    history_date
                )
        }

    # =================================================
    # PLANNER RECORD
    # =================================================

    def build_planner_record(
        self,
        row
    ):

        (
            activity_id,
            title,
            activity_date,
            start_time,
            end_time,
            category,
            completed_at,
            created_at
        ) = row

        history_date = (
            completed_at
            or created_at
        )

        time_text = ""

        if start_time:

            time_text = (
                self.format_clock_time(
                    start_time
                )
            )

        if end_time:

            time_text += (
                " - "
                + self.format_clock_time(
                    end_time
                )
            )

        details = category

        if time_text:

            details += (
                f" • {time_text}"
            )

        if activity_date:

            details += (
                f" • {activity_date}"
            )

        return {
            "type": "Planner",
            "title": title,
            "details": details,
            "date": history_date,
            "sort_date":
                self.parse_date(
                    history_date
                )
        }

    # =================================================
    # HISTORY CARD
    # =================================================

    def create_history_card(
        self,
        record
    ):

        card = ctk.CTkFrame(
            self.history_container,
            corner_radius=10
        )

        card.pack(
            fill="x",
            pady=5
        )

        # ---------------------------------------------
        # LEFT CONTENT
        # ---------------------------------------------

        left = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=15,
            pady=12
        )

        ctk.CTkLabel(
            left,
            text=record["type"].upper(),
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            left,
            text=record["title"],
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(3, 1)
        )

        ctk.CTkLabel(
            left,
            text=record["details"],
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w"
        )

        # ---------------------------------------------
        # DATE
        # ---------------------------------------------

        ctk.CTkLabel(
            card,
            text=self.format_date(
                record["date"]
            ),
            justify="right",
            font=ctk.CTkFont(
                size=11
            )
        ).pack(
            side="right",
            padx=15
        )

    # =================================================
    # PARSE DATE
    # =================================================

    def parse_date(
        self,
        value
    ):

        if not value:

            return datetime.min

        try:

            return datetime.strptime(
                value,
                "%Y-%m-%d %H:%M:%S"
            )

        except ValueError:

            return datetime.min

    # =================================================
    # DISPLAY DATE
    # =================================================

    def format_date(
        self,
        value
    ):

        if not value:

            return "Unknown"

        try:

            parsed = datetime.strptime(
                value,
                "%Y-%m-%d %H:%M:%S"
            )

            return parsed.strftime(
                "%d %b %Y\n"
                "%I:%M %p"
            )

        except ValueError:

            return value

    # =================================================
    # CLOCK TIME
    # =================================================

    def format_clock_time(
        self,
        value
    ):

        try:

            parsed = datetime.strptime(
                value,
                "%H:%M"
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
                else ""
            )

    # =================================================
    # DURATION
    # =================================================

    def format_seconds(
        self,
        seconds
    ):

        seconds = int(
            seconds
        )

        hours = (
            seconds // 3600
        )

        minutes = (
            (
                seconds % 3600
            )
            // 60
        )

        remaining = (
            seconds % 60
        )

        if hours:

            return (
                f"{hours}h "
                f"{minutes}m "
                f"{remaining}s"
            )

        if minutes:

            return (
                f"{minutes}m "
                f"{remaining}s"
            )

        return (
            f"{remaining}s"
        )