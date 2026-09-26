from __future__ import annotations

from datetime import datetime

import customtkinter as ctk

from database.database import (
    get_history_counts,
    get_focus_history,
    get_pomodoro_history,
    get_stopwatch_history,
    get_task_history,
    get_planner_history,
)

from ui.theme import (
    COLORS,
    FONT_BODY,
    FONT_DISPLAY,
    module_accent,
)


# =================================================
# HISTORY PAGE
# =================================================

class HistoryPage(ctk.CTkScrollableFrame):

    def __init__(
        self,
        parent
    ):

        super().__init__(
            parent,
            corner_radius=0,
            fg_color=COLORS["app_bg"]
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # STATE
        # ---------------------------------------------

        self.selected_type = "All"
        self.selected_period = "All Time"

        self.accent = (
            module_accent(
                "History"
            )
        )

        self._compact_layout = None
        self._resize_job = None

        # ---------------------------------------------
        # TYPE VISUALS
        # ---------------------------------------------

        self.type_styles = {

            "Focus": {
                "color": COLORS["violet"],
                "icon": "◎",
            },

            "Pomodoro": {
                "color": COLORS["coral"],
                "icon": "◷",
            },

            "Stopwatch": {
                "color": COLORS["cyan"],
                "icon": "◴",
            },

            "Tasks": {
                "color": COLORS["emerald"],
                "icon": "✓",
            },

            "Planner": {
                "color": COLORS["indigo"],
                "icon": "▦",
            },
        }

        # ---------------------------------------------
        # BUILD
        # ---------------------------------------------

        self.create_workspace()

        self.create_header()

        self.create_summary()

        self.create_filters()

        self.create_history_section()

        # ---------------------------------------------
        # RESPONSIVE
        # ---------------------------------------------

        self.workspace.bind(
            "<Configure>",
            self._schedule_layout_check,
            add="+"
        )

        self.after(
            120,
            self.apply_responsive_layout
        )

        # ---------------------------------------------
        # INITIAL DATA
        # ---------------------------------------------

        self.refresh_history()

    # =================================================
    # WORKSPACE
    # =================================================

    def create_workspace(
        self
    ):

        self.workspace = (
            ctk.CTkFrame(
                self,
                fg_color="transparent"
            )
        )

        self.workspace.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=30,
            pady=(0, 32)
        )

        self.workspace.grid_columnconfigure(
            0,
            weight=1
        )

    # =================================================
    # HEADER
    # =================================================

    def create_header(
        self
    ):

        self.header = (
            ctk.CTkFrame(
                self.workspace,
                fg_color="transparent"
            )
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(26, 18)
        )

        self.header.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # LEFT
        # ---------------------------------------------

        left = (
            ctk.CTkFrame(
                self.header,
                fg_color="transparent"
            )
        )

        left.grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            left,
            text="History",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=31,
                weight="bold"
            ),
            text_color=self.accent
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            left,
            text=(
                "Review your LifeOS activity "
                "across tasks, timers and planning."
            ),
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=13
            ),
            text_color=COLORS["muted"]
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        # ---------------------------------------------
        # CURRENT FILTER
        # ---------------------------------------------

        self.header_badge = (
            ctk.CTkFrame(
                self.header,
                corner_radius=100,
                fg_color=COLORS["surface_soft"]
            )
        )

        self.header_badge.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(15, 0)
        )

        self.header_badge_label = (
            ctk.CTkLabel(
                self.header_badge,
                text="All Activity",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                    weight="bold"
                ),
                text_color=self.accent
            )
        )

        self.header_badge_label.pack(
            padx=13,
            pady=7
        )

    # =================================================
    # SUMMARY
    # =================================================

    def create_summary(
        self
    ):

        self.summary_frame = (
            ctk.CTkFrame(
                self.workspace,
                fg_color="transparent"
            )
        )

        self.summary_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 14)
        )

        self.summary_labels = {}
        self.summary_cards = {}

        categories = [
            "Focus",
            "Pomodoro",
            "Stopwatch",
            "Tasks",
            "Planner",
        ]

        for column in range(
            5
        ):

            self.summary_frame.grid_columnconfigure(
                column,
                weight=1,
                uniform="history_stats"
            )

        for (
            index,
            category
        ) in enumerate(
            categories
        ):

            style = (
                self.type_styles[
                    category
                ]
            )

            card = (
                ctk.CTkFrame(
                    self.summary_frame,
                    height=128,
                    corner_radius=17,
                    fg_color=COLORS["surface"],
                    border_width=1,
                    border_color=COLORS["border"]
                )
            )

            card.grid(
                row=0,
                column=index,
                sticky="nsew",
                padx=(
                    (0, 5)
                    if index == 0
                    else (
                        (5, 0)
                        if index == 4
                        else 5
                    )
                )
            )

            card.grid_propagate(
                False
            )

            card.grid_columnconfigure(
                0,
                weight=1
            )

            self.summary_cards[
                category
            ] = card

            # -----------------------------------------
            # TOP
            # -----------------------------------------

            top = (
                ctk.CTkFrame(
                    card,
                    fg_color="transparent"
                )
            )

            top.grid(
                row=0,
                column=0,
                sticky="ew",
                padx=15,
                pady=(14, 2)
            )

            top.grid_columnconfigure(
                0,
                weight=1
            )

            ctk.CTkLabel(
                top,
                text=category,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                    weight="bold"
                ),
                text_color=COLORS["muted"]
            ).grid(
                row=0,
                column=0,
                sticky="w"
            )

            icon_box = (
                ctk.CTkFrame(
                    top,
                    width=32,
                    height=32,
                    corner_radius=9,
                    fg_color=style[
                        "color"
                    ]
                )
            )

            icon_box.grid(
                row=0,
                column=1,
                sticky="e"
            )

            icon_box.grid_propagate(
                False
            )

            ctk.CTkLabel(
                icon_box,
                text=style[
                    "icon"
                ],
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=14,
                    weight="bold"
                ),
                text_color=COLORS["white"]
            ).place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )

            # -----------------------------------------
            # VALUE
            # -----------------------------------------

            value = (
                ctk.CTkLabel(
                    card,
                    text="0",
                    font=ctk.CTkFont(
                        family=FONT_DISPLAY,
                        size=26,
                        weight="bold"
                    ),
                    text_color=style[
                        "color"
                    ]
                )
            )

            value.grid(
                row=1,
                column=0,
                sticky="w",
                padx=15
            )

            # -----------------------------------------
            # DESCRIPTION
            # -----------------------------------------

            ctk.CTkLabel(
                card,
                text="Recorded",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=9
                ),
                text_color=COLORS["subtle"]
            ).grid(
                row=2,
                column=0,
                sticky="w",
                padx=15,
                pady=(0, 13)
            )

            self.summary_labels[
                category
            ] = value

    # =================================================
    # FILTERS
    # =================================================

    def create_filters(
        self
    ):

        self.filter_card = (
            ctk.CTkFrame(
                self.workspace,
                corner_radius=17,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        self.filter_card.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 14)
        )

        self.filter_card.grid_columnconfigure(
            0,
            weight=1
        )

        # =================================================
        # DESKTOP FILTER ROW
        # =================================================

        self.desktop_filters = (
            ctk.CTkFrame(
                self.filter_card,
                fg_color="transparent"
            )
        )

        self.desktop_filters.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=18,
            pady=15
        )

        self.desktop_filters.grid_columnconfigure(
            1,
            weight=1
        )

        # ---------------------------------------------
        # CATEGORY LABEL
        # ---------------------------------------------

        ctk.CTkLabel(
            self.desktop_filters,
            text="Category",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold"
            ),
            text_color=COLORS["muted"]
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10)
        )

        # ---------------------------------------------
        # SEGMENTED FILTER
        # ---------------------------------------------

        self.type_filter = (
            ctk.CTkSegmentedButton(
                self.desktop_filters,
                values=[
                    "All",
                    "Focus",
                    "Pomodoro",
                    "Stopwatch",
                    "Tasks",
                    "Planner",
                ],
                command=self.change_type,
                height=38
            )
        )

        self.type_filter.set(
            "All"
        )

        self.type_filter.grid(
            row=0,
            column=1,
            sticky="w"
        )

        # ---------------------------------------------
        # PERIOD
        # ---------------------------------------------

        ctk.CTkLabel(
            self.desktop_filters,
            text="Period",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold"
            ),
            text_color=COLORS["muted"]
        ).grid(
            row=0,
            column=2,
            sticky="e",
            padx=(15, 8)
        )

        self.period_menu = (
            ctk.CTkOptionMenu(
                self.desktop_filters,
                values=[
                    "All Time",
                    "Today",
                    "Last 7 Days",
                    "Last 30 Days",
                ],
                command=self.change_period,
                width=150,
                height=38
            )
        )

        self.period_menu.set(
            "All Time"
        )

        self.period_menu.grid(
            row=0,
            column=3,
            sticky="e"
        )

        # =================================================
        # COMPACT FILTER ROW
        # =================================================

        self.compact_filters = (
            ctk.CTkFrame(
                self.filter_card,
                fg_color="transparent"
            )
        )

        self.compact_filters.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        # ---------------------------------------------
        # CATEGORY
        # ---------------------------------------------

        category_holder = (
            ctk.CTkFrame(
                self.compact_filters,
                fg_color="transparent"
            )
        )

        category_holder.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 6)
        )

        category_holder.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            category_holder,
            text="Category",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold"
            ),
            text_color=COLORS["muted"]
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 5)
        )

        self.compact_type_menu = (
            ctk.CTkOptionMenu(
                category_holder,
                values=[
                    "All",
                    "Focus",
                    "Pomodoro",
                    "Stopwatch",
                    "Tasks",
                    "Planner",
                ],
                command=self.change_type,
                height=40
            )
        )

        self.compact_type_menu.set(
            "All"
        )

        self.compact_type_menu.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        # ---------------------------------------------
        # PERIOD
        # ---------------------------------------------

        period_holder = (
            ctk.CTkFrame(
                self.compact_filters,
                fg_color="transparent"
            )
        )

        period_holder.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(6, 0)
        )

        period_holder.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            period_holder,
            text="Period",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold"
            ),
            text_color=COLORS["muted"]
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 5)
        )

        self.compact_period_menu = (
            ctk.CTkOptionMenu(
                period_holder,
                values=[
                    "All Time",
                    "Today",
                    "Last 7 Days",
                    "Last 30 Days",
                ],
                command=self.change_period,
                height=40
            )
        )

        self.compact_period_menu.set(
            "All Time"
        )

        self.compact_period_menu.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        # Hidden until compact mode is needed.
        self.compact_filters.grid_remove()

    # =================================================
    # HISTORY SECTION
    # =================================================

    def create_history_section(
        self
    ):

        self.history_card = (
            ctk.CTkFrame(
                self.workspace,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        self.history_card.grid(
            row=3,
            column=0,
            sticky="ew"
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        history_header = (
            ctk.CTkFrame(
                self.history_card,
                fg_color="transparent"
            )
        )

        history_header.pack(
            fill="x",
            padx=20,
            pady=(18, 9)
        )

        history_header.grid_columnconfigure(
            0,
            weight=1
        )

        heading = (
            ctk.CTkFrame(
                history_header,
                fg_color="transparent"
            )
        )

        heading.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.history_title = (
            ctk.CTkLabel(
                heading,
                text="All Activity",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=19,
                    weight="bold"
                ),
                text_color=COLORS["text"]
            )
        )

        self.history_title.pack(
            anchor="w"
        )

        self.history_subtitle = (
            ctk.CTkLabel(
                heading,
                text="Everything recorded in LifeOS",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10
                ),
                text_color=COLORS["muted"]
            )
        )

        self.history_subtitle.pack(
            anchor="w",
            pady=(2, 0)
        )

        self.record_count_label = (
            ctk.CTkLabel(
                history_header,
                text="0 records",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                    weight="bold"
                ),
                text_color=self.accent
            )
        )

        self.record_count_label.grid(
            row=0,
            column=1,
            sticky="e"
        )

        # ---------------------------------------------
        # LIST
        # ---------------------------------------------

        self.history_container = (
            ctk.CTkFrame(
                self.history_card,
                fg_color="transparent"
            )
        )

        self.history_container.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(2, 14)
        )

    # =================================================
    # FILTER CALLBACKS
    # =================================================

    def change_type(
        self,
        value
    ):

        self.selected_type = value

        # Keep desktop / compact controls synced.
        try:

            self.type_filter.set(
                value
            )

        except Exception:

            pass

        try:

            self.compact_type_menu.set(
                value
            )

        except Exception:

            pass

        self.load_history()

    def change_period(
        self,
        value
    ):

        self.selected_period = value

        try:

            self.period_menu.set(
                value
            )

        except Exception:

            pass

        try:

            self.compact_period_menu.set(
                value
            )

        except Exception:

            pass

        self.load_history()

    # =================================================
    # REFRESH
    # =================================================

    def refresh_history(
        self
    ):

        self.load_counts()

        self.load_history()

    # =================================================
    # COUNTS
    # =================================================

    def load_counts(
        self
    ):

        counts = (
            get_history_counts()
        )

        for (
            category,
            label
        ) in (
            self.summary_labels
            .items()
        ):

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

    def load_history(
        self
    ):

        # ---------------------------------------------
        # CLEAR
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

            title = "All Activity"

            subtitle = (
                "Everything recorded in LifeOS"
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

            title = "Focus History"

            subtitle = (
                "Deep-work sessions "
                "recorded in Focus Mode"
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

            title = "Pomodoro History"

            subtitle = (
                "Completed Pomodoro sessions"
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

            title = "Stopwatch History"

            subtitle = (
                "Saved open-ended sessions"
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

            title = "Task History"

            subtitle = (
                "Completed and recorded tasks"
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

        else:

            title = "Planner History"

            subtitle = (
                "Completed and recorded "
                "planner activities"
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

        # ---------------------------------------------
        # SORT SINGLE CATEGORIES TOO
        # ---------------------------------------------

        records.sort(
            key=lambda item:
            item["sort_date"],
            reverse=True
        )

        # ---------------------------------------------
        # TITLES
        # ---------------------------------------------

        self.history_title.configure(
            text=title
        )

        self.history_subtitle.configure(
            text=subtitle
        )

        self.header_badge_label.configure(
            text=(
                title
            )
        )

        count = len(
            records
        )

        self.record_count_label.configure(
            text=(
                f"{count} "
                f"{'record' if count == 1 else 'records'}"
            )
        )

        # =================================================
        # EMPTY
        # =================================================

        if not records:

            self.create_empty_state()

            self.after_idle(
                self._refresh_scroll_region
            )

            return

        # =================================================
        # RECORDS
        # =================================================

        for (
            index,
            record
        ) in enumerate(
            records
        ):

            self.create_history_card(
                record,
                index
            )

        self.after_idle(
            self._refresh_scroll_region
        )

    # =================================================
    # EMPTY
    # =================================================

    def create_empty_state(
        self
    ):

        empty = (
            ctk.CTkFrame(
                self.history_container,
                corner_radius=14,
                fg_color=COLORS["surface_alt"],
                border_width=1,
                border_color=COLORS["border_soft"]
            )
        )

        empty.pack(
            fill="x",
            pady=5
        )

        ctk.CTkLabel(
            empty,
            text="↺",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=28,
                weight="bold"
            ),
            text_color=self.accent
        ).pack(
            pady=(22, 5)
        )

        ctk.CTkLabel(
            empty,
            text="No history found",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=13,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).pack()

        ctk.CTkLabel(
            empty,
            text=(
                "There are no records for "
                "the selected category and period."
            ),
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10
            ),
            text_color=COLORS["muted"]
        ).pack(
            pady=(4, 22)
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

            "title": (
                task_title
                or "General"
            ),

            "details": (
                f"{self.format_seconds(actual_seconds)}"
                f"  •  {status}"
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

            "title": (
                "Stopwatch Session"
            ),

            "details": (
                f"{self.format_seconds(duration_seconds)}"
                f"  •  "
                f"{lap_count} "
                f"{'lap' if lap_count == 1 else 'laps'}"
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
            f"{category}"
            f"  •  "
            f"{priority} priority"
        )

        if due_date:

            details += (
                "  •  Due "
                + self.format_simple_date(
                    due_date
                )
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

        details_parts = []

        if category:

            details_parts.append(
                category
            )

        # ---------------------------------------------
        # TIME
        # ---------------------------------------------

        if (
            start_time
            and end_time
        ):

            details_parts.append(
                f"{self.format_clock_time(start_time)}"
                f" – "
                f"{self.format_clock_time(end_time)}"
            )

        elif start_time:

            details_parts.append(
                self.format_clock_time(
                    start_time
                )
            )

        # ---------------------------------------------
        # DATE
        # ---------------------------------------------

        if activity_date:

            details_parts.append(
                self.format_simple_date(
                    activity_date
                )
            )

        return {
            "type": "Planner",

            "title": title,

            "details": (
                "  •  ".join(
                    details_parts
                )
            ),

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
        record,
        index
    ):

        record_type = (
            record[
                "type"
            ]
        )

        style = (
            self.type_styles.get(
                record_type,
                {
                    "color": self.accent,
                    "icon": "•",
                }
            )
        )

        card = (
            ctk.CTkFrame(
                self.history_container,
                corner_radius=14,
                fg_color=COLORS["surface_alt"],
                border_width=1,
                border_color=COLORS["border_soft"]
            )
        )

        card.pack(
            fill="x",
            pady=6
        )

        card.grid_columnconfigure(
            2,
            weight=1
        )

        # ---------------------------------------------
        # TYPE COLOR BAR
        # ---------------------------------------------

        accent_strip = (
            ctk.CTkFrame(
                card,
                width=5,
                corner_radius=100,
                fg_color=style[
                    "color"
                ]
            )
        )

        accent_strip.grid(
            row=0,
            column=0,
            rowspan=3,
            sticky="ns",
            padx=(9, 8),
            pady=11
        )

        # ---------------------------------------------
        # ICON
        # ---------------------------------------------

        icon_box = (
            ctk.CTkFrame(
                card,
                width=42,
                height=42,
                corner_radius=12,
                fg_color=style[
                    "color"
                ]
            )
        )

        icon_box.grid(
            row=0,
            column=1,
            rowspan=3,
            padx=(0, 12),
            pady=13
        )

        icon_box.grid_propagate(
            False
        )

        ctk.CTkLabel(
            icon_box,
            text=style[
                "icon"
            ],
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=17,
                weight="bold"
            ),
            text_color=COLORS["white"]
        ).place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # ---------------------------------------------
        # TYPE
        # ---------------------------------------------

        ctk.CTkLabel(
            card,
            text=record_type.upper(),
            anchor="w",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=9,
                weight="bold"
            ),
            text_color=style[
                "color"
            ]
        ).grid(
            row=0,
            column=2,
            sticky="ew",
            padx=(0, 10),
            pady=(11, 1)
        )

        # ---------------------------------------------
        # TITLE
        # ---------------------------------------------

        ctk.CTkLabel(
            card,
            text=record[
                "title"
            ],
            anchor="w",
            justify="left",
            wraplength=700,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=13,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=1,
            column=2,
            sticky="ew",
            padx=(0, 12),
            pady=1
        )

        # ---------------------------------------------
        # DETAILS
        # ---------------------------------------------

        ctk.CTkLabel(
            card,
            text=record[
                "details"
            ],
            anchor="w",
            justify="left",
            wraplength=760,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10
            ),
            text_color=COLORS["muted"]
        ).grid(
            row=2,
            column=2,
            sticky="ew",
            padx=(0, 12),
            pady=(2, 11)
        )

        # ---------------------------------------------
        # DATE
        # ---------------------------------------------

        date_area = (
            ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
        )

        date_area.grid(
            row=0,
            column=3,
            rowspan=3,
            sticky="e",
            padx=(10, 14),
            pady=10
        )

        date_text = (
            self.format_date_parts(
                record[
                    "date"
                ]
            )
        )

        ctk.CTkLabel(
            date_area,
            text=date_text[
                0
            ],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).pack(
            anchor="e"
        )

        ctk.CTkLabel(
            date_area,
            text=date_text[
                1
            ],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=9
            ),
            text_color=COLORS["muted"]
        ).pack(
            anchor="e",
            pady=(2, 0)
        )

    # =================================================
    # DATE PARSING
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
    # DATE DISPLAY
    # =================================================

    def format_date_parts(
        self,
        value
    ):

        if not value:

            return (
                "Unknown",
                ""
            )

        try:

            parsed = datetime.strptime(
                value,
                "%Y-%m-%d %H:%M:%S"
            )

            return (
                parsed.strftime(
                    "%d %b %Y"
                ),

                parsed.strftime(
                    "%I:%M %p"
                ),
            )

        except ValueError:

            return (
                str(
                    value
                ),
                ""
            )

    # =================================================
    # SIMPLE DATE
    # =================================================

    def format_simple_date(
        self,
        value
    ):

        if not value:

            return ""

        try:

            parsed = datetime.strptime(
                value,
                "%Y-%m-%d"
            )

            return parsed.strftime(
                "%d %b %Y"
            )

        except ValueError:

            return str(
                value
            )

    # =================================================
    # CLOCK TIME
    # =================================================

    def format_clock_time(
        self,
        value
    ):

        if not value:

            return ""

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

            return str(
                value
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

        remaining = (
            seconds
            % 60
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

    # =================================================
    # RESPONSIVE
    # =================================================

    def _schedule_layout_check(
        self,
        _event=None
    ):

        if self._resize_job:

            try:

                self.after_cancel(
                    self._resize_job
                )

            except Exception:

                pass

        self._resize_job = (
            self.after(
                100,
                self.apply_responsive_layout
            )
        )

    # =================================================
    # APPLY RESPONSIVE
    # =================================================

    def apply_responsive_layout(
        self
    ):

        self._resize_job = None

        try:

            self.update_idletasks()

            width = (
                self.workspace
                .winfo_width()
            )

        except Exception:

            width = 1200

        if width <= 1:

            return

        compact = (
            width < 930
        )

        if (
            compact
            == self._compact_layout
        ):

            return

        self._compact_layout = (
            compact
        )

        # =================================================
        # COMPACT
        # =================================================

        if compact:

            # -----------------------------------------
            # HEADER
            # -----------------------------------------

            self.header_badge.grid_configure(
                row=1,
                column=0,
                sticky="w",
                padx=0,
                pady=(12, 0)
            )

            # -----------------------------------------
            # SUMMARY 2 + 2 + 1
            # -----------------------------------------

            for column in range(
                5
            ):

                self.summary_frame.grid_columnconfigure(
                    column,
                    weight=0,
                    uniform=""
                )

            self.summary_frame.grid_columnconfigure(
                0,
                weight=1
            )

            self.summary_frame.grid_columnconfigure(
                1,
                weight=1
            )

            self.summary_cards[
                "Focus"
            ].grid_configure(
                row=0,
                column=0,
                padx=(0, 6),
                pady=(0, 6)
            )

            self.summary_cards[
                "Pomodoro"
            ].grid_configure(
                row=0,
                column=1,
                padx=(6, 0),
                pady=(0, 6)
            )

            self.summary_cards[
                "Stopwatch"
            ].grid_configure(
                row=1,
                column=0,
                padx=(0, 6),
                pady=6
            )

            self.summary_cards[
                "Tasks"
            ].grid_configure(
                row=1,
                column=1,
                padx=(6, 0),
                pady=6
            )

            self.summary_cards[
                "Planner"
            ].grid_configure(
                row=2,
                column=0,
                columnspan=2,
                padx=0,
                pady=(6, 0)
            )

            # -----------------------------------------
            # FILTERS
            # -----------------------------------------

            self.desktop_filters.grid_remove()

            self.compact_filters.grid(
                row=0,
                column=0,
                sticky="ew",
                padx=18,
                pady=15
            )

        # =================================================
        # DESKTOP
        # =================================================

        else:

            # -----------------------------------------
            # HEADER
            # -----------------------------------------

            self.header_badge.grid_configure(
                row=0,
                column=1,
                sticky="e",
                padx=(15, 0),
                pady=0
            )

            # -----------------------------------------
            # SUMMARY
            # -----------------------------------------

            for column in range(
                5
            ):

                self.summary_frame.grid_columnconfigure(
                    column,
                    weight=1,
                    uniform="history_stats"
                )

            categories = [
                "Focus",
                "Pomodoro",
                "Stopwatch",
                "Tasks",
                "Planner",
            ]

            for (
                index,
                category
            ) in enumerate(
                categories
            ):

                self.summary_cards[
                    category
                ].grid_configure(
                    row=0,
                    column=index,
                    columnspan=1,
                    padx=(
                        (0, 5)
                        if index == 0
                        else (
                            (5, 0)
                            if index == 4
                            else 5
                        )
                    ),
                    pady=0
                )

            # -----------------------------------------
            # FILTERS
            # -----------------------------------------

            self.compact_filters.grid_remove()

            self.desktop_filters.grid(
                row=0,
                column=0,
                sticky="ew",
                padx=18,
                pady=15
            )

        self.after_idle(
            self._refresh_scroll_region
        )

    # =================================================
    # SCROLL REGION
    # =================================================

    def _refresh_scroll_region(
        self
    ):

        try:

            self.update_idletasks()

            canvas = (
                self._parent_canvas
            )

            canvas.configure(
                scrollregion=(
                    canvas.bbox(
                        "all"
                    )
                )
            )

        except Exception:

            pass