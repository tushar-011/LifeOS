import customtkinter as ctk

import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg
)

from database.database import (
    get_productivity_metrics,
    get_weekly_productivity_metrics
)

from utils.productivity import (
    calculate_productivity_score,
    score_label
)


class AnalyticsPage(
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

        self.chart_canvases = []

        self.create_header()
        self.create_summary_cards()
        self.create_score_explanation()

        self.refresh_analytics()

    # =================================================
    # HEADER
    # =================================================

    def create_header(self):

        ctk.CTkLabel(
            self,
            text="Analytics",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            padx=25,
            pady=(25, 5)
        )

        ctk.CTkLabel(
            self,
            text=(
                "Understand your tasks, "
                "focus time and productivity."
            )
        ).grid(
            row=1,
            column=0,
            columnspan=4,
            sticky="w",
            padx=25,
            pady=(0, 20)
        )

    # =================================================
    # SUMMARY CARDS
    # =================================================

    def create_summary_cards(self):

        self.score_value = (
            self.create_card(
                0,
                "Productivity",
                "0%",
                "Today's Score"
            )
        )

        self.task_value = (
            self.create_card(
                1,
                "Tasks",
                "0 / 0",
                "Completed Today"
            )
        )

        self.focus_value = (
            self.create_card(
                2,
                "Focus",
                "0m",
                "Tracked Today"
            )
        )

        self.planner_value = (
            self.create_card(
                3,
                "Planner",
                "0 / 0",
                "Completed Today"
            )
        )

    def create_card(
        self,
        column,
        title,
        value,
        subtitle
    ):

        card = ctk.CTkFrame(
            self,
            corner_radius=15,
            height=125
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
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 4)
        )

        value_label = (
            ctk.CTkLabel(
                card,
                text=value,
                font=ctk.CTkFont(
                    size=27,
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
                size=12
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(4, 12)
        )

        return value_label

    # =================================================
    # SCORE EXPLANATION
    # =================================================

    def create_score_explanation(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.grid(
            row=3,
            column=0,
            columnspan=4,
            padx=10,
            pady=10,
            sticky="ew"
        )

        ctk.CTkLabel(
            card,
            text="How the Productivity Score Works",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 8)
        )

        ctk.CTkLabel(
            card,
            text=(
                "Tasks: 50%   •   "
                "Focus Time: 30%   •   "
                "Planner: 20%   •   "
                "120 focus minutes = full focus score"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 18)
        )

    # =================================================
    # REFRESH
    # =================================================

    def refresh_analytics(self):

        self.load_today_metrics()
        self.load_charts()

    # =================================================
    # TODAY
    # =================================================

    def load_today_metrics(self):

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

        self.task_value.configure(
            text=(
                f"{metrics['tasks_completed']}"
                f" / "
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
                f"{metrics['planner_completed']}"
                f" / "
                f"{metrics['planner_total']}"
            )
        )

    # =================================================
    # CHARTS
    # =================================================

    def load_charts(self):

        # Destroy old chart widgets
        for widget in (
            self.grid_slaves()
        ):

            try:

                if getattr(
                    widget,
                    "analytics_chart",
                    False
                ):

                    widget.destroy()

            except Exception:

                pass

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

            day = datetime.strptime(
                metrics["date"],
                "%Y-%m-%d"
            )

            labels.append(
                day.strftime(
                    "%a"
                )
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

        # =================================================
        # PRODUCTIVITY CHART
        # =================================================

        productivity_card = (
            ctk.CTkFrame(
                self,
                corner_radius=15
            )
        )

        productivity_card.analytics_chart = True

        productivity_card.grid(
            row=4,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        ctk.CTkLabel(
            productivity_card,
            text="7-Day Productivity Score",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        figure1, axis1 = (
            plt.subplots(
                figsize=(6, 3)
            )
        )

        sns.lineplot(
            x=labels,
            y=scores,
            marker="o",
            ax=axis1
        )

        axis1.set_ylim(
            0,
            100
        )

        axis1.set_ylabel(
            "Score (%)"
        )

        axis1.set_xlabel(
            ""
        )

        figure1.tight_layout()

        canvas1 = (
            FigureCanvasTkAgg(
                figure1,
                master=productivity_card
            )
        )

        canvas1.draw()

        canvas1.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(5, 15)
        )

        plt.close(
            figure1
        )

        # =================================================
        # FOCUS CHART
        # =================================================

        focus_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        focus_card.analytics_chart = True

        focus_card.grid(
            row=4,
            column=2,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        ctk.CTkLabel(
            focus_card,
            text="7-Day Focus Time",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        figure2, axis2 = (
            plt.subplots(
                figsize=(6, 3)
            )
        )

        sns.barplot(
            x=labels,
            y=focus_minutes,
            ax=axis2
        )

        axis2.set_ylabel(
            "Minutes"
        )

        axis2.set_xlabel(
            ""
        )

        figure2.tight_layout()

        canvas2 = (
            FigureCanvasTkAgg(
                figure2,
                master=focus_card
            )
        )

        canvas2.draw()

        canvas2.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(5, 15)
        )

        plt.close(
            figure2
        )

        # =================================================
        # TASK COMPLETION CHART
        # =================================================

        tasks_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        tasks_card.analytics_chart = True

        tasks_card.grid(
            row=5,
            column=0,
            columnspan=4,
            padx=10,
            pady=(10, 25),
            sticky="nsew"
        )

        ctk.CTkLabel(
            tasks_card,
            text="7-Day Task Completion",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        figure3, axis3 = (
            plt.subplots(
                figsize=(10, 3.2)
            )
        )

        x_positions = list(
            range(
                len(labels)
            )
        )

        width = 0.35

        axis3.bar(
            [
                x - width / 2
                for x in x_positions
            ],
            task_total,
            width,
            label="Due"
        )

        axis3.bar(
            [
                x + width / 2
                for x in x_positions
            ],
            task_completed,
            width,
            label="Completed"
        )

        axis3.set_xticks(
            x_positions
        )

        axis3.set_xticklabels(
            labels
        )

        axis3.set_ylabel(
            "Tasks"
        )

        axis3.legend()

        figure3.tight_layout()

        canvas3 = (
            FigureCanvasTkAgg(
                figure3,
                master=tasks_card
            )
        )

        canvas3.draw()

        canvas3.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(5, 15)
        )

        plt.close(
            figure3
        )

    # =================================================
    # HELPERS
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
            minutes // 60
        )

        remaining = (
            minutes % 60
        )

        if remaining == 0:

            return (
                f"{hours}h"
            )

        return (
            f"{hours}h "
            f"{remaining}m"
        )