from __future__ import annotations

from datetime import datetime

import customtkinter as ctk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from database.database import (
    add_note,
    get_productivity_metrics,
    get_task_statistics,
    get_today_focus_stats,
    get_today_planner,
    get_today_pomodoro_stats,
    get_today_tasks,
    get_weekly_productivity_metrics,
    toggle_task,
)

from ui.theme import (
    CATEGORY_COLORS,
    COLORS,
    FONT_BODY,
    FONT_DISPLAY,
    chart_palette,
    module_accent,
    module_accent_hover,
    style_matplotlib_figure,
)

from utils.productivity import (
    calculate_productivity_score,
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
            corner_radius=0,
            fg_color=COLORS["app_bg"]
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # MODULE COLORS
        # ---------------------------------------------

        self.accent = (
            module_accent(
                "Dashboard"
            )
        )

        self.accent_hover = (
            module_accent_hover(
                "Dashboard"
            )
        )

        # ---------------------------------------------
        # DATA STATE
        # ---------------------------------------------

        self.quick_focus_lookup = {}

        # ---------------------------------------------
        # CHART STATE
        # ---------------------------------------------

        self.weekly_figure = None
        self.weekly_axis = None
        self.weekly_chart_canvas = None

        # ---------------------------------------------
        # RESPONSIVE STATE
        # ---------------------------------------------

        self._compact_layout = None
        self._resize_job = None

        # ---------------------------------------------
        # BUILD
        # ---------------------------------------------

        self.create_workspace()

        self.create_header()

        self.create_stat_cards()

        self.create_primary_section()

        self.create_secondary_section()

        self.create_today_plan()

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

        self.refresh_dashboard()

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
        # GREETING
        # ---------------------------------------------

        heading_area = (
            ctk.CTkFrame(
                self.header,
                fg_color="transparent"
            )
        )

        heading_area.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.greeting_label = (
            ctk.CTkLabel(
                heading_area,
                text="",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=32,
                    weight="bold"
                ),
                text_color=self.accent
            )
        )

        self.greeting_label.pack(
            anchor="w"
        )

        ctk.CTkLabel(
            heading_area,
            text=(
                "Your day, priorities and progress "
                "in one place."
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
        # DAY BADGE
        # ---------------------------------------------

        day_card = (
            ctk.CTkFrame(
                self.header,
                corner_radius=15,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        day_card.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(18, 0)
        )

        self.day_label = (
            ctk.CTkLabel(
                day_card,
                text="",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=15,
                    weight="bold"
                ),
                text_color=COLORS["text"]
            )
        )

        self.day_label.pack(
            padx=18,
            pady=(10, 1)
        )

        self.date_label = (
            ctk.CTkLabel(
                day_card,
                text="",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10
                ),
                text_color=COLORS["muted"]
            )
        )

        self.date_label.pack(
            padx=18,
            pady=(0, 10)
        )

    # =================================================
    # STAT CARDS
    # =================================================

    def create_stat_cards(
        self
    ):

        self.stats_frame = (
            ctk.CTkFrame(
                self.workspace,
                fg_color="transparent"
            )
        )

        self.stats_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 14)
        )

        for column in range(
            4
        ):

            self.stats_frame.grid_columnconfigure(
                column,
                weight=1,
                uniform="dashboard_stats"
            )

        # ---------------------------------------------
        # TASKS
        # ---------------------------------------------

        (
            self.tasks_card,
            self.tasks_value
        ) = self.create_stat_card(
            self.stats_frame,
            column=0,
            title="Tasks",
            value="0 / 0",
            subtitle="Pending / Total",
            icon="✓",
            accent=COLORS["emerald"],
            padx=(0, 6)
        )

        # ---------------------------------------------
        # FOCUS
        # ---------------------------------------------

        (
            self.focus_card,
            self.focus_value
        ) = self.create_stat_card(
            self.stats_frame,
            column=1,
            title="Focus Time",
            value="0m",
            subtitle="Tracked Today",
            icon="◎",
            accent=COLORS["violet"],
            padx=6
        )

        # ---------------------------------------------
        # POMODORO
        # ---------------------------------------------

        (
            self.pomodoro_card,
            self.pomodoro_value
        ) = self.create_stat_card(
            self.stats_frame,
            column=2,
            title="Pomodoros",
            value="0",
            subtitle="Focus Sessions",
            icon="◷",
            accent=COLORS["coral"],
            padx=6
        )

        # ---------------------------------------------
        # PRODUCTIVITY
        # ---------------------------------------------

        (
            self.productivity_card,
            self.productivity_value
        ) = self.create_stat_card(
            self.stats_frame,
            column=3,
            title="Productivity",
            value="0%",
            subtitle="Today's Score",
            icon="↗",
            accent=COLORS["cyan"],
            padx=(6, 0)
        )

    # =================================================
    # CREATE STAT CARD
    # =================================================

    def create_stat_card(
        self,
        parent,
        column,
        title,
        value,
        subtitle,
        icon,
        accent,
        padx
    ):

        card = (
            ctk.CTkFrame(
                parent,
                corner_radius=18,
                height=138,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=padx
        )

        card.grid_propagate(
            False
        )

        card.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # TOP ROW
        # ---------------------------------------------

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
            padx=17,
            pady=(15, 1)
        )

        top.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            top,
            text=title,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
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
                width=34,
                height=34,
                corner_radius=10,
                fg_color=accent
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
            text=icon,
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=15,
                weight="bold"
            ),
            text_color=COLORS["white"]
        ).place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # ---------------------------------------------
        # VALUE
        # ---------------------------------------------

        value_label = (
            ctk.CTkLabel(
                card,
                text=value,
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=28,
                    weight="bold"
                ),
                text_color=accent
            )
        )

        value_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=17,
            pady=(0, 0)
        )

        # ---------------------------------------------
        # SUBTITLE
        # ---------------------------------------------

        ctk.CTkLabel(
            card,
            text=subtitle,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10
            ),
            text_color=COLORS["subtle"]
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=17,
            pady=(0, 13)
        )

        return (
            card,
            value_label
        )

    # =================================================
    # PRIMARY SECTION
    # =================================================

    def create_primary_section(
        self
    ):

        self.primary_frame = (
            ctk.CTkFrame(
                self.workspace,
                fg_color="transparent"
            )
        )

        self.primary_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 14)
        )

        self.primary_frame.grid_columnconfigure(
            0,
            weight=6
        )

        self.primary_frame.grid_columnconfigure(
            1,
            weight=4
        )

        self.create_tasks_card()

        self.create_quick_focus_card()

    # =================================================
    # TODAY TASKS
    # =================================================

    def create_tasks_card(
        self
    ):

        self.tasks_panel = (
            ctk.CTkFrame(
                self.primary_frame,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        self.tasks_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        header = (
            ctk.CTkFrame(
                self.tasks_panel,
                fg_color="transparent"
            )
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(18, 8)
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        title_area = (
            ctk.CTkFrame(
                header,
                fg_color="transparent"
            )
        )

        title_area.grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            title_area,
            text="Today's Tasks",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=19,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            title_area,
            text="Finish what's due today.",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10
            ),
            text_color=COLORS["muted"]
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        self.today_task_count = (
            ctk.CTkLabel(
                header,
                text="0 pending",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                    weight="bold"
                ),
                text_color=COLORS["emerald"]
            )
        )

        self.today_task_count.grid(
            row=0,
            column=1,
            sticky="e"
        )

        # ---------------------------------------------
        # CONTAINER
        # ---------------------------------------------

        self.dashboard_tasks_container = (
            ctk.CTkFrame(
                self.tasks_panel,
                fg_color="transparent"
            )
        )

        self.dashboard_tasks_container.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(3, 16)
        )

    # =================================================
    # QUICK FOCUS
    # =================================================

    def create_quick_focus_card(
        self
    ):

        self.quick_focus_card = (
            ctk.CTkFrame(
                self.primary_frame,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        self.quick_focus_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        self.quick_focus_card.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        ctk.CTkLabel(
            self.quick_focus_card,
            text="Quick Focus",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=19,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            pady=(20, 3)
        )

        ctk.CTkLabel(
            self.quick_focus_card,
            text="Jump directly into a 25-minute session.",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10
            ),
            text_color=COLORS["muted"]
        ).grid(
            row=1,
            column=0,
            pady=(0, 12)
        )

        # ---------------------------------------------
        # TASK
        # ---------------------------------------------

        self.quick_focus_menu = (
            ctk.CTkOptionMenu(
                self.quick_focus_card,
                values=[
                    "General"
                ],
                height=38
            )
        )

        self.quick_focus_menu.set(
            "General"
        )

        self.quick_focus_menu.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=24
        )

        # ---------------------------------------------
        # TIMER
        # ---------------------------------------------

        timer_shell = (
            ctk.CTkFrame(
                self.quick_focus_card,
                corner_radius=16,
                fg_color=COLORS["surface_alt"],
                border_width=1,
                border_color=COLORS["border_soft"]
            )
        )

        timer_shell.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=24,
            pady=15
        )

        self.focus_timer_label = (
            ctk.CTkLabel(
                timer_shell,
                text="25:00",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=42,
                    weight="bold"
                ),
                text_color=COLORS["violet"]
            )
        )

        self.focus_timer_label.pack(
            pady=(16, 0)
        )

        ctk.CTkLabel(
            timer_shell,
            text="One focused block",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10
            ),
            text_color=COLORS["muted"]
        ).pack(
            pady=(0, 15)
        )

        # ---------------------------------------------
        # START
        # ---------------------------------------------

        self.focus_button = (
            ctk.CTkButton(
                self.quick_focus_card,
                text="Start Quick Focus",
                height=41,
                corner_radius=11,
                fg_color=COLORS["violet"],
                hover_color=COLORS["violet_hover"],
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                command=self.open_quick_focus
            )
        )

        self.focus_button.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=24,
            pady=(0, 20)
        )

    # =================================================
    # SECONDARY SECTION
    # =================================================

    def create_secondary_section(
        self
    ):

        self.secondary_frame = (
            ctk.CTkFrame(
                self.workspace,
                fg_color="transparent"
            )
        )

        self.secondary_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(0, 14)
        )

        self.secondary_frame.grid_columnconfigure(
            0,
            weight=7
        )

        self.secondary_frame.grid_columnconfigure(
            1,
            weight=3
        )

        self.create_weekly_chart_card()

        self.create_quick_note_card()

    # =================================================
    # WEEKLY CHART
    # =================================================

    def create_weekly_chart_card(
        self
    ):

        self.analytics_card = (
            ctk.CTkFrame(
                self.secondary_frame,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        self.analytics_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        header = (
            ctk.CTkFrame(
                self.analytics_card,
                fg_color="transparent"
            )
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(18, 4)
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        left = (
            ctk.CTkFrame(
                header,
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
            text="Weekly Productivity",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=19,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            left,
            text="Your last seven days at a glance.",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10
            ),
            text_color=COLORS["muted"]
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        self.weekly_average_label = (
            ctk.CTkLabel(
                header,
                text="Avg 0%",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=11,
                    weight="bold"
                ),
                text_color=self.accent
            )
        )

        self.weekly_average_label.grid(
            row=0,
            column=1,
            sticky="e"
        )

        # ---------------------------------------------
        # CHART FRAME
        # ---------------------------------------------

        self.weekly_chart_frame = (
            ctk.CTkFrame(
                self.analytics_card,
                height=300,
                corner_radius=14,
                fg_color=COLORS["surface_alt"]
            )
        )

        self.weekly_chart_frame.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(8, 14)
        )

        self.weekly_chart_frame.pack_propagate(
            False
        )

    # =================================================
    # QUICK NOTE
    # =================================================

    def create_quick_note_card(
        self
    ):

        self.note_card = (
            ctk.CTkFrame(
                self.secondary_frame,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        self.note_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        self.note_card.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        ctk.CTkLabel(
            self.note_card,
            text="Quick Note",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=19,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 2)
        )

        ctk.CTkLabel(
            self.note_card,
            text="Capture it before you forget it.",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10
            ),
            text_color=COLORS["muted"]
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20
        )

        # ---------------------------------------------
        # TEXT BOX
        # ---------------------------------------------

        self.note_box = (
            ctk.CTkTextbox(
                self.note_card,
                height=150,
                corner_radius=12,
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        self.note_box.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(14, 8)
        )

        # ---------------------------------------------
        # MESSAGE
        # ---------------------------------------------

        self.quick_note_message = (
            ctk.CTkLabel(
                self.note_card,
                text="",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10
                ),
                text_color=COLORS["emerald"]
            )
        )

        self.quick_note_message.grid(
            row=3,
            column=0,
            sticky="w",
            padx=20
        )

        # ---------------------------------------------
        # SAVE
        # ---------------------------------------------

        ctk.CTkButton(
            self.note_card,
            text="Save Note",
            height=40,
            corner_radius=11,
            fg_color=COLORS["amber"],
            hover_color=COLORS["amber_hover"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=12,
                weight="bold"
            ),
            command=self.save_quick_note
        ).grid(
            row=4,
            column=0,
            sticky="ew",
            padx=20,
            pady=(8, 18)
        )

    # =================================================
    # TODAY PLAN
    # =================================================

    def create_today_plan(
        self
    ):

        self.plan_card = (
            ctk.CTkFrame(
                self.workspace,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        self.plan_card.grid(
            row=4,
            column=0,
            sticky="ew"
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        header = (
            ctk.CTkFrame(
                self.plan_card,
                fg_color="transparent"
            )
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(18, 9)
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        left = (
            ctk.CTkFrame(
                header,
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
            text="Today's Plan",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=19,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            left,
            text="Your scheduled activities for today.",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10
            ),
            text_color=COLORS["muted"]
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        self.plan_count_label = (
            ctk.CTkLabel(
                header,
                text="0 activities",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                    weight="bold"
                ),
                text_color=COLORS["indigo"]
            )
        )

        self.plan_count_label.grid(
            row=0,
            column=1,
            sticky="e"
        )

        # ---------------------------------------------
        # CONTAINER
        # ---------------------------------------------

        self.planner_container = (
            ctk.CTkFrame(
                self.plan_card,
                fg_color="transparent"
            )
        )

        self.planner_container.pack(
            fill="x",
            padx=14,
            pady=(3, 16)
        )

    # =================================================
    # RESPONSIVE CHECK
    # =================================================

    def _schedule_layout_check(
        self,
        event=None
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
    # RESPONSIVE LAYOUT
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
        # COMPACT / SMALL WINDOW
        # =================================================

        if compact:

            # -----------------------------------------
            # HEADER DATE BELOW TITLE
            # -----------------------------------------

            self.header.grid_columnconfigure(
                0,
                weight=1
            )

            self.day_label.master.grid_configure(
                row=1,
                column=0,
                sticky="w",
                padx=0,
                pady=(12, 0)
            )

            # -----------------------------------------
            # STATS 2 x 2
            # -----------------------------------------

            self.stats_frame.grid_columnconfigure(
                0,
                weight=1
            )

            self.stats_frame.grid_columnconfigure(
                1,
                weight=1
            )

            self.stats_frame.grid_columnconfigure(
                2,
                weight=0
            )

            self.stats_frame.grid_columnconfigure(
                3,
                weight=0
            )

            self.tasks_card.grid_configure(
                row=0,
                column=0,
                padx=(0, 6),
                pady=(0, 6)
            )

            self.focus_card.grid_configure(
                row=0,
                column=1,
                padx=(6, 0),
                pady=(0, 6)
            )

            self.pomodoro_card.grid_configure(
                row=1,
                column=0,
                padx=(0, 6),
                pady=(6, 0)
            )

            self.productivity_card.grid_configure(
                row=1,
                column=1,
                padx=(6, 0),
                pady=(6, 0)
            )

            # -----------------------------------------
            # PRIMARY STACK
            # -----------------------------------------

            self.primary_frame.grid_columnconfigure(
                0,
                weight=1
            )

            self.primary_frame.grid_columnconfigure(
                1,
                weight=0
            )

            self.tasks_panel.grid_configure(
                row=0,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0,
                pady=(0, 12)
            )

            self.quick_focus_card.grid_configure(
                row=1,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0
            )

            # -----------------------------------------
            # SECONDARY STACK
            # -----------------------------------------

            self.secondary_frame.grid_columnconfigure(
                0,
                weight=1
            )

            self.secondary_frame.grid_columnconfigure(
                1,
                weight=0
            )

            self.analytics_card.grid_configure(
                row=0,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0,
                pady=(0, 12)
            )

            self.note_card.grid_configure(
                row=1,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0
            )

        # =================================================
        # DESKTOP
        # =================================================

        else:

            # -----------------------------------------
            # HEADER
            # -----------------------------------------

            self.day_label.master.grid_configure(
                row=0,
                column=1,
                sticky="e",
                padx=(18, 0),
                pady=0
            )

            # -----------------------------------------
            # STATS
            # -----------------------------------------

            for column in range(
                4
            ):

                self.stats_frame.grid_columnconfigure(
                    column,
                    weight=1,
                    uniform="dashboard_stats"
                )

            self.tasks_card.grid_configure(
                row=0,
                column=0,
                padx=(0, 6),
                pady=0
            )

            self.focus_card.grid_configure(
                row=0,
                column=1,
                padx=6,
                pady=0
            )

            self.pomodoro_card.grid_configure(
                row=0,
                column=2,
                padx=6,
                pady=0
            )

            self.productivity_card.grid_configure(
                row=0,
                column=3,
                padx=(6, 0),
                pady=0
            )

            # -----------------------------------------
            # PRIMARY
            # -----------------------------------------

            self.primary_frame.grid_columnconfigure(
                0,
                weight=6
            )

            self.primary_frame.grid_columnconfigure(
                1,
                weight=4
            )

            self.tasks_panel.grid_configure(
                row=0,
                column=0,
                columnspan=1,
                sticky="nsew",
                padx=(0, 8),
                pady=0
            )

            self.quick_focus_card.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                sticky="nsew",
                padx=(8, 0),
                pady=0
            )

            # -----------------------------------------
            # SECONDARY
            # -----------------------------------------

            self.secondary_frame.grid_columnconfigure(
                0,
                weight=7
            )

            self.secondary_frame.grid_columnconfigure(
                1,
                weight=3
            )

            self.analytics_card.grid_configure(
                row=0,
                column=0,
                columnspan=1,
                sticky="nsew",
                padx=(0, 8),
                pady=0
            )

            self.note_card.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                sticky="nsew",
                padx=(8, 0),
                pady=0
            )

        self.after_idle(
            self._refresh_scroll_region
        )

    # =================================================
    # REFRESH SCROLL REGION
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

    # =================================================
    # REFRESH DASHBOARD
    # =================================================

    def refresh_dashboard(
        self
    ):

        self.update_header()

        self.load_statistics()

        self.load_dashboard_tasks()

        self.load_quick_focus_tasks()

        self.load_today_plan()

        self.load_weekly_chart()

        self.after_idle(
            self._refresh_scroll_region
        )

    # =================================================
    # HEADER DATA
    # =================================================

    def update_header(
        self
    ):

        now = (
            datetime.now()
        )

        if now.hour < 12:

            greeting = (
                "Good Morning"
            )

        elif now.hour < 18:

            greeting = (
                "Good Afternoon"
            )

        else:

            greeting = (
                "Good Evening"
            )

        self.greeting_label.configure(
            text=(
                f"{greeting} 👋"
            )
        )

        self.day_label.configure(
            text=now.strftime(
                "%A"
            )
        )

        self.date_label.configure(
            text=now.strftime(
                "%d %B %Y"
            )
        )

    # =================================================
    # STATISTICS
    # =================================================

    def load_statistics(
        self
    ):

        task_stats = (
            get_task_statistics()
        )

        focus_stats = (
            get_today_focus_stats()
        )

        pomodoro_stats = (
            get_today_pomodoro_stats()
        )

        productivity = (
            get_productivity_metrics()
        )

        score = (
            calculate_productivity_score(
                productivity[
                    "tasks_completed"
                ],
                productivity[
                    "tasks_total"
                ],
                productivity[
                    "focus_minutes"
                ],
                productivity[
                    "planner_completed"
                ],
                productivity[
                    "planner_total"
                ],
            )
        )

        self.tasks_value.configure(
            text=(
                f"{task_stats['pending']} / "
                f"{task_stats['total']}"
            )
        )

        self.focus_value.configure(
            text=self.format_seconds(
                focus_stats[
                    "focus_seconds"
                ]
            )
        )

        self.pomodoro_value.configure(
            text=str(
                pomodoro_stats[
                    "sessions"
                ]
            )
        )

        self.productivity_value.configure(
            text=f"{score}%"
        )

    # =================================================
    # DASHBOARD TASKS
    # =================================================

    def load_dashboard_tasks(
        self
    ):

        for widget in (
            self.dashboard_tasks_container
            .winfo_children()
        ):

            widget.destroy()

        tasks = (
            get_today_tasks(
                limit=6
            )
        )

        self.today_task_count.configure(
            text=(
                f"{len(tasks)} "
                f"{'task' if len(tasks) == 1 else 'tasks'}"
            )
        )

        # ---------------------------------------------
        # EMPTY
        # ---------------------------------------------

        if not tasks:

            empty = (
                ctk.CTkFrame(
                    self.dashboard_tasks_container,
                    corner_radius=13,
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
                text="✓",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=25,
                    weight="bold"
                ),
                text_color=COLORS["emerald"]
            ).pack(
                pady=(18, 4)
            )

            ctk.CTkLabel(
                empty,
                text="Nothing due today",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                text_color=COLORS["text"]
            ).pack()

            ctk.CTkLabel(
                empty,
                text="Your task list is clear for today.",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10
                ),
                text_color=COLORS["muted"]
            ).pack(
                pady=(3, 18)
            )

            return

        # ---------------------------------------------
        # TASK CARDS
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

            row = (
                ctk.CTkFrame(
                    self.dashboard_tasks_container,
                    corner_radius=12,
                    fg_color=COLORS["surface_alt"],
                    border_width=1,
                    border_color=COLORS["border_soft"]
                )
            )

            row.pack(
                fill="x",
                pady=5
            )

            row.grid_columnconfigure(
                1,
                weight=1
            )

            checkbox = (
                ctk.CTkCheckBox(
                    row,
                    text="",
                    width=24,
                    fg_color=COLORS["emerald"],
                    hover_color=COLORS["emerald_hover"],
                    command=(
                        lambda task_id=task_id:
                        self.complete_dashboard_task(
                            task_id
                        )
                    )
                )
            )

            checkbox.grid(
                row=0,
                column=0,
                rowspan=2,
                padx=(13, 8),
                pady=12
            )

            # -----------------------------------------
            # TITLE
            # -----------------------------------------

            ctk.CTkLabel(
                row,
                text=title,
                anchor="w",
                justify="left",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                text_color=COLORS["text"]
            ).grid(
                row=0,
                column=1,
                sticky="ew",
                padx=(2, 8),
                pady=(11, 1)
            )

            # -----------------------------------------
            # META
            # -----------------------------------------

            meta = (
                ctk.CTkFrame(
                    row,
                    fg_color="transparent"
                )
            )

            meta.grid(
                row=1,
                column=1,
                sticky="w",
                padx=(2, 8),
                pady=(1, 11)
            )

            category_color = (
                CATEGORY_COLORS.get(
                    category,
                    COLORS["muted"]
                )
            )

            category_badge = (
                ctk.CTkFrame(
                    meta,
                    corner_radius=100,
                    fg_color=category_color
                )
            )

            category_badge.pack(
                side="left"
            )

            ctk.CTkLabel(
                category_badge,
                text=category,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=9,
                    weight="bold"
                ),
                text_color=COLORS["white"]
            ).pack(
                padx=7,
                pady=2
            )

            priority_color = (
                COLORS["danger"]
                if priority == "High"
                else (
                    COLORS["amber"]
                    if priority == "Medium"
                    else COLORS["emerald"]
                )
            )

            ctk.CTkLabel(
                meta,
                text=(
                    f"  •  {priority}"
                ),
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                    weight="bold"
                ),
                text_color=priority_color
            ).pack(
                side="left"
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

    def load_quick_focus_tasks(
        self
    ):

        tasks = (
            get_today_tasks(
                limit=100
            )
        )

        current_value = (
            self.quick_focus_menu
            .get()
        )

        self.quick_focus_lookup = {
            "General": {
                "id": None,
                "title": "General"
            }
        }

        values = [
            "General"
        ]

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
                f"{title} • {priority}"
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

    def open_quick_focus(
        self
    ):

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

        app.show_focus()

        focus_page = (
            app.pages.get(
                "Focus"
            )
        )

        if (
            focus_page
            is None
        ):

            return

        focus_page.load_tasks()

        if (
            selected
            in focus_page.task_lookup
        ):

            focus_page.task_menu.set(
                selected
            )

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

    def save_quick_note(
        self
    ):

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
                ),
                text_color=COLORS["danger"]
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
            text="Note saved.",
            text_color=COLORS["emerald"]
        )

    # =================================================
    # TODAY PLAN
    # =================================================

    def load_today_plan(
        self
    ):

        for widget in (
            self.planner_container
            .winfo_children()
        ):

            widget.destroy()

        activities = (
            get_today_planner(
                limit=8
            )
        )

        self.plan_count_label.configure(
            text=(
                f"{len(activities)} "
                f"{'activity' if len(activities) == 1 else 'activities'}"
            )
        )

        # ---------------------------------------------
        # EMPTY
        # ---------------------------------------------

        if not activities:

            empty = (
                ctk.CTkFrame(
                    self.planner_container,
                    corner_radius=13,
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
                text="▦",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=23,
                    weight="bold"
                ),
                text_color=COLORS["indigo"]
            ).pack(
                pady=(16, 3)
            )

            ctk.CTkLabel(
                empty,
                text="Nothing planned for today",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                text_color=COLORS["text"]
            ).pack()

            ctk.CTkLabel(
                empty,
                text="Open Planner whenever you want to schedule something.",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10
                ),
                text_color=COLORS["muted"]
            ).pack(
                pady=(3, 16)
            )

            return

        # ---------------------------------------------
        # ACTIVITY ROWS
        # ---------------------------------------------

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

            row = (
                ctk.CTkFrame(
                    self.planner_container,
                    corner_radius=12,
                    fg_color=COLORS["surface_alt"],
                    border_width=1,
                    border_color=COLORS["border_soft"]
                )
            )

            row.pack(
                fill="x",
                pady=5
            )

            row.grid_columnconfigure(
                1,
                weight=1
            )

            # -----------------------------------------
            # TIME
            # -----------------------------------------

            time_box = (
                ctk.CTkFrame(
                    row,
                    width=92,
                    corner_radius=10,
                    fg_color=COLORS["surface_soft"]
                )
            )

            time_box.grid(
                row=0,
                column=0,
                rowspan=2,
                sticky="ns",
                padx=(11, 10),
                pady=10
            )

            time_box.grid_propagate(
                False
            )

            ctk.CTkLabel(
                time_box,
                text=self.format_time(
                    start_time
                ),
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                    weight="bold"
                ),
                text_color=COLORS["indigo"]
            ).place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )

            # -----------------------------------------
            # TITLE
            # -----------------------------------------

            title_text = (
                f"✓ {title}"
                if completed
                else title
            )

            ctk.CTkLabel(
                row,
                text=title_text,
                anchor="w",
                justify="left",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                text_color=COLORS["text"]
            ).grid(
                row=0,
                column=1,
                sticky="ew",
                padx=(2, 8),
                pady=(11, 1)
            )

            # -----------------------------------------
            # CATEGORY
            # -----------------------------------------

            category_color = (
                CATEGORY_COLORS.get(
                    category,
                    COLORS["muted"]
                )
            )

            category_badge = (
                ctk.CTkFrame(
                    row,
                    corner_radius=100,
                    fg_color=category_color
                )
            )

            category_badge.grid(
                row=1,
                column=1,
                sticky="w",
                padx=(2, 8),
                pady=(3, 11)
            )

            ctk.CTkLabel(
                category_badge,
                text=category,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=9,
                    weight="bold"
                ),
                text_color=COLORS["white"]
            ).pack(
                padx=8,
                pady=2
            )

    # =================================================
    # WEEKLY CHART
    # =================================================

    def load_weekly_chart(
        self
    ):

        metrics = (
            get_weekly_productivity_metrics(
                days=7
            )
        )

        labels = []
        scores = []

        for day in metrics:

            try:

                parsed_date = (
                    datetime.strptime(
                        day["date"],
                        "%Y-%m-%d"
                    )
                )

                labels.append(
                    parsed_date.strftime(
                        "%a"
                    )
                )

            except Exception:

                labels.append(
                    day["date"]
                )

            score = (
                calculate_productivity_score(
                    day[
                        "tasks_completed"
                    ],
                    day[
                        "tasks_total"
                    ],
                    day[
                        "focus_minutes"
                    ],
                    day[
                        "planner_completed"
                    ],
                    day[
                        "planner_total"
                    ],
                )
            )

            scores.append(
                score
            )

        average = (
            round(
                sum(scores)
                / len(scores)
            )
            if scores
            else 0
        )

        self.weekly_average_label.configure(
            text=f"Avg {average}%"
        )

        # ---------------------------------------------
        # REMOVE PREVIOUS CANVAS
        # ---------------------------------------------

        if self.weekly_chart_canvas is not None:

            try:
                self.weekly_chart_canvas.get_tk_widget().destroy()

            except Exception:
                pass

            self.weekly_chart_canvas = None

        # ---------------------------------------------
        # FIGURE
        # ---------------------------------------------

        self.weekly_figure = Figure(
            figsize=(7.2, 2.7),
            dpi=100
        )

        self.weekly_axis = (
            self.weekly_figure
            .add_subplot(
                111
            )
        )

        palette = (
            chart_palette(
                "Dashboard"
            )
        )

        # ---------------------------------------------
        # BAR BACKDROP
        # ---------------------------------------------

        self.weekly_axis.bar(
            labels,
            scores,
            width=0.55,
            color=palette[1],
            alpha=0.22
        )

        # ---------------------------------------------
        # LINE
        # ---------------------------------------------

        self.weekly_axis.plot(
            labels,
            scores,
            linewidth=2.6,
            marker="o",
            markersize=6,
            color=palette[0]
        )

        # ---------------------------------------------
        # POINT VALUES
        # ---------------------------------------------

        for (
            index,
            score
        ) in enumerate(
            scores
        ):

            self.weekly_axis.annotate(
                f"{score}%",
                (
                    index,
                    score
                ),
                textcoords="offset points",
                xytext=(0, 8),
                ha="center",
                fontsize=8
            )

        self.weekly_axis.set_ylim(
            0,
            110
        )

        self.weekly_axis.set_ylabel(
            "Score"
        )

        self.weekly_axis.set_xlabel(
            ""
        )

        self.weekly_axis.set_yticks(
            [
                0,
                25,
                50,
                75,
                100
            ]
        )

        # ---------------------------------------------
        # THEME
        # ---------------------------------------------

        style_matplotlib_figure(
            self.weekly_figure,
            self.weekly_axis,
            "Dashboard"
        )

        self.weekly_figure.tight_layout(
            pad=1.35
        )

        # ---------------------------------------------
        # CANVAS
        # ---------------------------------------------

        self.weekly_chart_canvas = (
            FigureCanvasTkAgg(
                self.weekly_figure,
                master=self.weekly_chart_frame
            )
        )

        canvas_widget = (
            self.weekly_chart_canvas
            .get_tk_widget()
        )

        canvas_widget.configure(
            highlightthickness=0,
            borderwidth=0
        )

        canvas_widget.pack(
            fill="both",
            expand=True,
            padx=4,
            pady=4
        )

        self.weekly_chart_canvas.draw()

    # =================================================
    # FORMAT PLANNER TIME
    # =================================================

    def format_time(
        self,
        value
    ):

        if not value:

            return "--"

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

            return value

    # =================================================
    # FORMAT FOCUS TIME
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

        remaining_seconds = (
            seconds
            % 60
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

        if minutes:

            return (
                f"{minutes}m"
            )

        if remaining_seconds:

            return (
                f"{remaining_seconds}s"
            )

        return "0m"