from __future__ import annotations

from datetime import datetime

import customtkinter as ctk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from database.database import (
    get_productivity_metrics,
    get_weekly_productivity_metrics,
)

from ui.theme import (
    COLORS,
    FONT_BODY,
    FONT_DISPLAY,
    chart_palette,
    chart_theme_values,
    module_accent,
    style_matplotlib_figure,
)

from utils.productivity import (
    calculate_productivity_score,
    score_label,
)


# =================================================
# ANALYTICS PAGE
# =================================================

class AnalyticsPage(ctk.CTkScrollableFrame):

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

        self.accent = (
            module_accent(
                "Analytics"
            )
        )

        self.palette = (
            chart_palette(
                "Analytics"
            )
        )

        self.chart_canvases = []
        self.chart_figures = []

        self._compact_layout = None
        self._resize_job = None

        # ---------------------------------------------
        # BUILD
        # ---------------------------------------------

        self.create_workspace()

        self.create_header()

        self.create_summary_cards()

        self.create_score_explanation()

        self.create_chart_area()

        # ---------------------------------------------
        # RESPONSIVE
        # ---------------------------------------------

        self.workspace.bind(
            "<Configure>",
            self._schedule_layout_check,
            add="+"
        )

        self.after(
            150,
            self.apply_responsive_layout
        )

        # ---------------------------------------------
        # LOAD
        # ---------------------------------------------

        self.refresh_analytics()

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

        header = (
            ctk.CTkFrame(
                self.workspace,
                fg_color="transparent"
            )
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(26, 18)
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
            text="Analytics",
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
                "Understand your tasks, focus time "
                "and productivity patterns."
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
        # PERIOD PILL
        # ---------------------------------------------

        period = (
            ctk.CTkFrame(
                header,
                corner_radius=100,
                fg_color=COLORS["surface_soft"]
            )
        )

        period.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(15, 0)
        )

        ctk.CTkLabel(
            period,
            text="7-Day Overview",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).pack(
            padx=13,
            pady=7
        )

    # =================================================
    # SUMMARY CARDS
    # =================================================

    def create_summary_cards(
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
                uniform="analytics_stats"
            )

        (
            self.score_card,
            self.score_value,
            self.score_subtitle
        ) = self.create_summary_card(
            self.stats_frame,
            0,
            "Productivity",
            "0%",
            "Today's Score",
            COLORS["pink"],
            "↗",
            (0, 6)
        )

        (
            self.task_card,
            self.task_value,
            _
        ) = self.create_summary_card(
            self.stats_frame,
            1,
            "Tasks",
            "0 / 0",
            "Completed Today",
            COLORS["emerald"],
            "✓",
            6
        )

        (
            self.focus_card,
            self.focus_value,
            _
        ) = self.create_summary_card(
            self.stats_frame,
            2,
            "Focus",
            "0m",
            "Tracked Today",
            COLORS["violet"],
            "◎",
            6
        )

        (
            self.planner_card,
            self.planner_value,
            _
        ) = self.create_summary_card(
            self.stats_frame,
            3,
            "Planner",
            "0 / 0",
            "Completed Today",
            COLORS["indigo"],
            "▦",
            (6, 0)
        )

    # =================================================
    # SUMMARY CARD
    # =================================================

    def create_summary_card(
        self,
        parent,
        column,
        title,
        value,
        subtitle,
        accent,
        icon,
        padx
    ):

        card = (
            ctk.CTkFrame(
                parent,
                height=140,
                corner_radius=18,
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
        # TOP
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
            pady=(15, 3)
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
                    size=29,
                    weight="bold"
                ),
                text_color=accent
            )
        )

        value_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=17
        )

        # ---------------------------------------------
        # SUBTITLE
        # ---------------------------------------------

        subtitle_label = (
            ctk.CTkLabel(
                card,
                text=subtitle,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10
                ),
                text_color=COLORS["subtle"]
            )
        )

        subtitle_label.grid(
            row=2,
            column=0,
            sticky="w",
            padx=17,
            pady=(0, 14)
        )

        return (
            card,
            value_label,
            subtitle_label
        )

    # =================================================
    # SCORE EXPLANATION
    # =================================================

    def create_score_explanation(
        self
    ):

        self.score_card_info = (
            ctk.CTkFrame(
                self.workspace,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        self.score_card_info.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 14)
        )

        # ---------------------------------------------
        # LEFT ACCENT
        # ---------------------------------------------

        accent_strip = (
            ctk.CTkFrame(
                self.score_card_info,
                width=5,
                corner_radius=100,
                fg_color=self.accent
            )
        )

        accent_strip.pack(
            side="left",
            fill="y",
            padx=(0, 0),
            pady=14
        )

        # ---------------------------------------------
        # TEXT
        # ---------------------------------------------

        content = (
            ctk.CTkFrame(
                self.score_card_info,
                fg_color="transparent"
            )
        )

        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=16
        )

        ctk.CTkLabel(
            content,
            text="How the Productivity Score Works",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=18,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            content,
            text=(
                "Tasks contribute 50%  •  "
                "Focus contributes 30%  •  "
                "Planner contributes 20%  •  "
                "120 focus minutes gives the full focus component"
            ),
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11
            ),
            text_color=COLORS["muted"],
            justify="left",
            wraplength=1000
        ).pack(
            anchor="w",
            pady=(6, 0)
        )

    # =================================================
    # CHART AREA
    # =================================================

    def create_chart_area(
        self
    ):

        self.chart_area = (
            ctk.CTkFrame(
                self.workspace,
                fg_color="transparent"
            )
        )

        self.chart_area.grid(
            row=3,
            column=0,
            sticky="ew"
        )

        self.chart_area.grid_columnconfigure(
            0,
            weight=1
        )

        self.chart_area.grid_columnconfigure(
            1,
            weight=1
        )

        # ---------------------------------------------
        # TOP CHARTS
        # ---------------------------------------------

        self.productivity_chart_card = (
            self.create_chart_card(
                self.chart_area,
                title="7-Day Productivity Score",
                subtitle="Daily score from tasks, focus and planner activity",
                row=0,
                column=0,
                padx=(0, 8)
            )
        )

        self.focus_chart_card = (
            self.create_chart_card(
                self.chart_area,
                title="7-Day Focus Time",
                subtitle="Tracked focus minutes by day",
                row=0,
                column=1,
                padx=(8, 0)
            )
        )

        # ---------------------------------------------
        # TASK CHART
        # ---------------------------------------------

        self.tasks_chart_card = (
            self.create_chart_card(
                self.chart_area,
                title="7-Day Task Completion",
                subtitle="Compare tasks due with tasks completed",
                row=1,
                column=0,
                columnspan=2,
                padx=0,
                pady=(14, 0)
            )
        )

    # =================================================
    # CHART CARD
    # =================================================

    def create_chart_card(
        self,
        parent,
        title,
        subtitle,
        row,
        column,
        padx=0,
        pady=0,
        columnspan=1
    ):

        card = (
            ctk.CTkFrame(
                parent,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        card.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            sticky="nsew",
            padx=padx,
            pady=pady
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        header = (
            ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(18, 4)
        )

        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=18,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            header,
            text=subtitle,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10
            ),
            text_color=COLORS["muted"]
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        # ---------------------------------------------
        # CHART HOLDER
        # ---------------------------------------------

        chart_holder = (
            ctk.CTkFrame(
                card,
                height=300,
                corner_radius=14,
                fg_color=COLORS["surface_alt"]
            )
        )

        chart_holder.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(8, 14)
        )

        chart_holder.pack_propagate(
            False
        )

        card.chart_holder = chart_holder

        return card

    # =================================================
    # RESPONSIVE
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
    # APPLY RESPONSIVE LAYOUT
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
            width < 940
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

            self.score_card.grid_configure(
                row=0,
                column=0,
                padx=(0, 6),
                pady=(0, 6)
            )

            self.task_card.grid_configure(
                row=0,
                column=1,
                padx=(6, 0),
                pady=(0, 6)
            )

            self.focus_card.grid_configure(
                row=1,
                column=0,
                padx=(0, 6),
                pady=(6, 0)
            )

            self.planner_card.grid_configure(
                row=1,
                column=1,
                padx=(6, 0),
                pady=(6, 0)
            )

            # -----------------------------------------
            # CHARTS STACK
            # -----------------------------------------

            self.chart_area.grid_columnconfigure(
                0,
                weight=1
            )

            self.chart_area.grid_columnconfigure(
                1,
                weight=0
            )

            self.productivity_chart_card.grid_configure(
                row=0,
                column=0,
                columnspan=2,
                padx=0,
                pady=(0, 14)
            )

            self.focus_chart_card.grid_configure(
                row=1,
                column=0,
                columnspan=2,
                padx=0,
                pady=(0, 14)
            )

            self.tasks_chart_card.grid_configure(
                row=2,
                column=0,
                columnspan=2,
                padx=0,
                pady=0
            )

        # =================================================
        # DESKTOP
        # =================================================

        else:

            for column in range(
                4
            ):

                self.stats_frame.grid_columnconfigure(
                    column,
                    weight=1,
                    uniform="analytics_stats"
                )

            self.score_card.grid_configure(
                row=0,
                column=0,
                padx=(0, 6),
                pady=0
            )

            self.task_card.grid_configure(
                row=0,
                column=1,
                padx=6,
                pady=0
            )

            self.focus_card.grid_configure(
                row=0,
                column=2,
                padx=6,
                pady=0
            )

            self.planner_card.grid_configure(
                row=0,
                column=3,
                padx=(6, 0),
                pady=0
            )

            # -----------------------------------------
            # CHARTS 2 + 1
            # -----------------------------------------

            self.chart_area.grid_columnconfigure(
                0,
                weight=1
            )

            self.chart_area.grid_columnconfigure(
                1,
                weight=1
            )

            self.productivity_chart_card.grid_configure(
                row=0,
                column=0,
                columnspan=1,
                padx=(0, 8),
                pady=0
            )

            self.focus_chart_card.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                padx=(8, 0),
                pady=0
            )

            self.tasks_chart_card.grid_configure(
                row=1,
                column=0,
                columnspan=2,
                padx=0,
                pady=(14, 0)
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

    # =================================================
    # REFRESH ANALYTICS
    # =================================================

    def refresh_analytics(
        self
    ):

        self.load_today_metrics()

        self.load_charts()

        self.after_idle(
            self._refresh_scroll_region
        )

    # =================================================
    # TODAY METRICS
    # =================================================

    def load_today_metrics(
        self
    ):

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

        self.score_value.configure(
            text=f"{score}%"
        )

        self.score_subtitle.configure(
            text=(
                f"{score_label(score)} today"
            )
        )

        self.task_value.configure(
            text=(
                f"{metrics['tasks_completed']} / "
                f"{metrics['tasks_total']}"
            )
        )

        self.focus_value.configure(
            text=self.format_minutes(
                metrics[
                    "focus_minutes"
                ]
            )
        )

        self.planner_value.configure(
            text=(
                f"{metrics['planner_completed']} / "
                f"{metrics['planner_total']}"
            )
        )

    # =================================================
    # DESTROY OLD CHARTS
    # =================================================

    def clear_charts(
        self
    ):

        for canvas in (
            self.chart_canvases
        ):

            try:

                canvas.get_tk_widget().destroy()

            except Exception:

                pass

        self.chart_canvases.clear()

        self.chart_figures.clear()

    # =================================================
    # LOAD CHARTS
    # =================================================

    def load_charts(
        self
    ):

        self.clear_charts()

        weekly = (
            get_weekly_productivity_metrics(
                7
            )
        )

        labels = []
        scores = []
        focus_minutes = []
        task_completed = []
        task_total = []

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

                label = metrics["date"]

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

            focus_minutes.append(
                metrics[
                    "focus_minutes"
                ]
            )

            task_completed.append(
                metrics[
                    "tasks_completed"
                ]
            )

            task_total.append(
                metrics[
                    "tasks_total"
                ]
            )

        # ---------------------------------------------
        # FALLBACK
        # ---------------------------------------------

        if not labels:

            labels = [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun",
            ]

            scores = [
                0
            ] * 7

            focus_minutes = [
                0
            ] * 7

            task_completed = [
                0
            ] * 7

            task_total = [
                0
            ] * 7

        # ---------------------------------------------
        # PRODUCTIVITY
        # ---------------------------------------------

        self.draw_productivity_chart(
            labels,
            scores
        )

        # ---------------------------------------------
        # FOCUS
        # ---------------------------------------------

        self.draw_focus_chart(
            labels,
            focus_minutes
        )

        # ---------------------------------------------
        # TASKS
        # ---------------------------------------------

        self.draw_task_chart(
            labels,
            task_total,
            task_completed
        )

    # =================================================
    # PRODUCTIVITY CHART
    # =================================================

    def draw_productivity_chart(
        self,
        labels,
        scores
    ):

        holder = (
            self.productivity_chart_card
            .chart_holder
        )

        figure = Figure(
            figsize=(6.5, 3.0),
            dpi=100
        )

        axis = figure.add_subplot(
            111
        )

        x_positions = list(
            range(
                len(labels)
            )
        )

        # ---------------------------------------------
        # SUBTLE BACKDROP
        # ---------------------------------------------

        axis.bar(
            x_positions,
            scores,
            width=0.55,
            color=self.palette[1],
            alpha=0.15
        )

        # ---------------------------------------------
        # AREA
        # ---------------------------------------------

        axis.fill_between(
            x_positions,
            scores,
            0,
            color=self.palette[0],
            alpha=0.10
        )

        # ---------------------------------------------
        # LINE
        # ---------------------------------------------

        axis.plot(
            x_positions,
            scores,
            color=self.palette[0],
            linewidth=2.7,
            marker="o",
            markersize=6
        )

        # ---------------------------------------------
        # LABELS
        # ---------------------------------------------

        for (
            index,
            value
        ) in enumerate(
            scores
        ):

            axis.annotate(
                f"{value}%",
                (
                    index,
                    value
                ),
                textcoords="offset points",
                xytext=(0, 8),
                ha="center",
                fontsize=8
            )

        axis.set_xticks(
            x_positions
        )

        axis.set_xticklabels(
            labels
        )

        axis.set_ylim(
            0,
            110
        )

        axis.set_yticks(
            [
                0,
                25,
                50,
                75,
                100
            ]
        )

        axis.set_ylabel(
            "Score"
        )

        style_matplotlib_figure(
            figure,
            axis,
            "Analytics"
        )

        figure.tight_layout(
            pad=1.3
        )

        self.embed_chart(
            figure,
            holder
        )

    # =================================================
    # FOCUS CHART
    # =================================================

    def draw_focus_chart(
        self,
        labels,
        values
    ):

        holder = (
            self.focus_chart_card
            .chart_holder
        )

        figure = Figure(
            figsize=(6.5, 3.0),
            dpi=100
        )

        axis = figure.add_subplot(
            111
        )

        x_positions = list(
            range(
                len(labels)
            )
        )

        bars = axis.bar(
            x_positions,
            values,
            width=0.56,
            color=self.palette[1],
            alpha=0.90
        )

        # ---------------------------------------------
        # VALUE LABELS
        # ---------------------------------------------

        for (
            bar,
            value
        ) in zip(
            bars,
            values
        ):

            axis.annotate(
                f"{round(value, 1)}m",
                (
                    bar.get_x()
                    + bar.get_width()
                    / 2,
                    bar.get_height()
                ),
                textcoords="offset points",
                xytext=(0, 6),
                ha="center",
                fontsize=8
            )

        axis.set_xticks(
            x_positions
        )

        axis.set_xticklabels(
            labels
        )

        axis.set_ylabel(
            "Minutes"
        )

        top = max(
            values
        ) if values else 0

        axis.set_ylim(
            0,
            max(
                10,
                top * 1.25
            )
        )

        style_matplotlib_figure(
            figure,
            axis,
            "Analytics"
        )

        figure.tight_layout(
            pad=1.3
        )

        self.embed_chart(
            figure,
            holder
        )

    # =================================================
    # TASK CHART
    # =================================================

    def draw_task_chart(
        self,
        labels,
        due_values,
        completed_values
    ):

        holder = (
            self.tasks_chart_card
            .chart_holder
        )

        figure = Figure(
            figsize=(12, 3.2),
            dpi=100
        )

        axis = figure.add_subplot(
            111
        )

        x_positions = list(
            range(
                len(labels)
            )
        )

        width = 0.34

        due_bars = axis.bar(
            [
                x - width / 2
                for x in x_positions
            ],
            due_values,
            width,
            label="Due",
            color=self.palette[4],
            alpha=0.78
        )

        completed_bars = axis.bar(
            [
                x + width / 2
                for x in x_positions
            ],
            completed_values,
            width,
            label="Completed",
            color=self.palette[2],
            alpha=0.92
        )

        # ---------------------------------------------
        # VALUE LABELS
        # ---------------------------------------------

        for bar in (
            list(due_bars)
            + list(completed_bars)
        ):

            value = (
                int(
                    round(
                        bar.get_height()
                    )
                )
            )

            if value <= 0:

                continue

            axis.annotate(
                str(value),
                (
                    bar.get_x()
                    + bar.get_width()
                    / 2,
                    bar.get_height()
                ),
                textcoords="offset points",
                xytext=(0, 5),
                ha="center",
                fontsize=8
            )

        axis.set_xticks(
            x_positions
        )

        axis.set_xticklabels(
            labels
        )

        axis.set_ylabel(
            "Tasks"
        )

        top = max(
            due_values
            + completed_values
        ) if (
            due_values
            or completed_values
        ) else 0

        axis.set_ylim(
            0,
            max(
                2,
                top * 1.30
            )
        )

        axis.legend(
            loc="upper left",
            frameon=True
        )

        style_matplotlib_figure(
            figure,
            axis,
            "Analytics"
        )

        figure.tight_layout(
            pad=1.3
        )

        self.embed_chart(
            figure,
            holder
        )

    # =================================================
    # EMBED CHART
    # =================================================

    def embed_chart(
        self,
        figure,
        holder
    ):

        theme = (
            chart_theme_values()
        )

        canvas = (
            FigureCanvasTkAgg(
                figure,
                master=holder
            )
        )

        widget = (
            canvas
            .get_tk_widget()
        )

        widget.configure(
            bg=theme["figure"],
            highlightthickness=0,
            borderwidth=0
        )

        widget.pack(
            fill="both",
            expand=True,
            padx=4,
            pady=4
        )

        canvas.draw()

        self.chart_canvases.append(
            canvas
        )

        self.chart_figures.append(
            figure
        )

    # =================================================
    # FORMAT MINUTES
    # =================================================

    def format_minutes(
        self,
        minutes
    ):

        minutes = int(
            round(
                minutes
            )
        )

        if minutes < 60:

            return (
                f"{minutes}m"
            )

        hours = (
            minutes
            // 60
        )

        remaining = (
            minutes
            % 60
        )

        if remaining == 0:

            return (
                f"{hours}h"
            )

        return (
            f"{hours}h "
            f"{remaining}m"
        )