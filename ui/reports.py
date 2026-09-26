from __future__ import annotations

from datetime import datetime
from pathlib import Path

import customtkinter as ctk

from tkinter import (
    filedialog,
    messagebox,
)

from database.database import (
    get_report_summary,
    get_report_completed_tasks,
    get_report_category_summary,
)

from utils.settings_manager import (
    get_setting,
    get_default_export_path,
)

from ui.theme import (
    CATEGORY_COLORS,
    COLORS,
    FONT_BODY,
    FONT_DISPLAY,
    module_accent,
    module_accent_hover,
)


# =================================================
# REPORTS PAGE
# =================================================

class ReportsPage(ctk.CTkScrollableFrame):

    def __init__(
        self,
        parent
    ):

        super().__init__(
            parent,
            corner_radius=0,
            fg_color=COLORS["app_bg"],
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        # =================================================
        # STATE
        # =================================================

        self.report_type = "Daily"

        self.accent = (
            module_accent(
                "Reports"
            )
        )

        self.accent_hover = (
            module_accent_hover(
                "Reports"
            )
        )

        self._stacked_layout = None
        self._resize_job = None

        # =================================================
        # BUILD
        # =================================================

        self.create_workspace()

        self.create_header()

        self.create_period_selector()

        self.create_summary_cards()

        self.create_report_body()

        # =================================================
        # RESPONSIVE
        # =================================================

        self.workspace.bind(
            "<Configure>",
            self._schedule_layout_check,
            add="+",
        )

        self.after(
            120,
            self.apply_responsive_layout
        )

        # =================================================
        # INITIAL DATA
        # =================================================

        self.refresh_reports()

    # =================================================
    # WORKSPACE
    # =================================================

    def create_workspace(
        self
    ):

        self.workspace = (
            ctk.CTkFrame(
                self,
                fg_color="transparent",
            )
        )

        self.workspace.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=30,
            pady=(0, 32),
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
                fg_color="transparent",
            )
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(26, 18),
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
                fg_color="transparent",
            )
        )

        left.grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            left,
            text="Reports",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=31,
                weight="bold",
            ),
            text_color=self.accent,
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            left,
            text=(
                "Review completed work and understand "
                "where your effort is going."
            ),
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=13,
            ),
            text_color=COLORS["muted"],
        ).pack(
            anchor="w",
            pady=(5, 0),
        )

        # ---------------------------------------------
        # EXPORT
        # ---------------------------------------------

        self.export_button = (
            ctk.CTkButton(
                self.header,
                text="Export Report",
                width=145,
                height=42,
                corner_radius=11,
                fg_color=self.accent,
                hover_color=self.accent_hover,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=11,
                    weight="bold",
                ),
                command=self.export_report,
            )
        )

        self.export_button.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(16, 0),
        )

    # =================================================
    # REPORT PERIOD
    # =================================================

    def create_period_selector(
        self
    ):

        self.period_card = (
            ctk.CTkFrame(
                self.workspace,
                corner_radius=17,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"],
            )
        )

        self.period_card.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 14),
        )

        self.period_card.grid_columnconfigure(
            1,
            weight=1
        )

        # ---------------------------------------------
        # LABEL
        # ---------------------------------------------

        ctk.CTkLabel(
            self.period_card,
            text="Report Period",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold",
            ),
            text_color=COLORS["muted"],
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(18, 14),
            pady=16,
        )

        # ---------------------------------------------
        # SELECTOR
        # ---------------------------------------------

        self.period_selector = (
            ctk.CTkSegmentedButton(
                self.period_card,
                values=[
                    "Daily",
                    "Weekly",
                    "Monthly",
                ],
                command=self.change_report_type,
                selected_color=self.accent,
                selected_hover_color=self.accent_hover,
                unselected_color=COLORS["surface_soft"],
                unselected_hover_color=COLORS["border"],
                height=38,
            )
        )

        self.period_selector.set(
            "Daily"
        )

        self.period_selector.grid(
            row=0,
            column=1,
            sticky="w",
            pady=14,
        )

        # ---------------------------------------------
        # RANGE BADGE
        # ---------------------------------------------

        self.range_badge = (
            ctk.CTkFrame(
                self.period_card,
                corner_radius=100,
                fg_color=COLORS["surface_alt"],
                border_width=1,
                border_color=COLORS["border_soft"],
            )
        )

        self.range_badge.grid(
            row=0,
            column=2,
            sticky="e",
            padx=18,
            pady=14,
        )

        self.range_label = (
            ctk.CTkLabel(
                self.range_badge,
                text="",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                    weight="bold",
                ),
                text_color=COLORS["text"],
            )
        )

        self.range_label.pack(
            padx=12,
            pady=6,
        )

    # =================================================
    # SUMMARY CARDS
    # =================================================

    def create_summary_cards(
        self
    ):

        self.summary_frame = (
            ctk.CTkFrame(
                self.workspace,
                fg_color="transparent",
            )
        )

        self.summary_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 14),
        )

        for column in range(
            3
        ):

            self.summary_frame.grid_columnconfigure(
                column,
                weight=1,
                uniform="report_summary",
            )

        # ---------------------------------------------
        # COMPLETED
        # ---------------------------------------------

        (
            self.tasks_card,
            self.tasks_value
        ) = self.create_summary_card(
            column=0,
            title="Tasks Completed",
            subtitle="Finished in this period",
            value="0",
            accent=COLORS["emerald"],
            icon="✓",
            padx=(0, 6),
        )

        # ---------------------------------------------
        # CATEGORIES
        # ---------------------------------------------

        (
            self.categories_card,
            self.categories_value
        ) = self.create_summary_card(
            column=1,
            title="Categories Used",
            subtitle="Areas you worked across",
            value="0",
            accent=COLORS["amber"],
            icon="▦",
            padx=6,
        )

        # ---------------------------------------------
        # TOP CATEGORY
        # ---------------------------------------------

        (
            self.top_category_card,
            self.top_category_value
        ) = self.create_summary_card(
            column=2,
            title="Top Category",
            subtitle="Most completed tasks",
            value="None",
            accent=COLORS["indigo"],
            icon="↗",
            padx=(6, 0),
        )

    # =================================================
    # CREATE SUMMARY CARD
    # =================================================

    def create_summary_card(
        self,
        column,
        title,
        subtitle,
        value,
        accent,
        icon,
        padx,
    ):

        card = (
            ctk.CTkFrame(
                self.summary_frame,
                height=138,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"],
            )
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=padx,
        )

        card.grid_propagate(
            False
        )

        card.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # HEADER ROW
        # ---------------------------------------------

        top = (
            ctk.CTkFrame(
                card,
                fg_color="transparent",
            )
        )

        top.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=17,
            pady=(15, 2),
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
                weight="bold",
            ),
            text_color=COLORS["muted"],
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        icon_box = (
            ctk.CTkFrame(
                top,
                width=34,
                height=34,
                corner_radius=10,
                fg_color=accent,
            )
        )

        icon_box.grid(
            row=0,
            column=1,
            sticky="e",
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
                weight="bold",
            ),
            text_color=COLORS["white"],
        ).place(
            relx=0.5,
            rely=0.5,
            anchor="center",
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
                    size=27,
                    weight="bold",
                ),
                text_color=accent,
            )
        )

        value_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=17,
        )

        # ---------------------------------------------
        # SUBTITLE
        # ---------------------------------------------

        ctk.CTkLabel(
            card,
            text=subtitle,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
            ),
            text_color=COLORS["subtle"],
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=17,
            pady=(0, 14),
        )

        return (
            card,
            value_label,
        )

    # =================================================
    # REPORT BODY
    # =================================================

    def create_report_body(
        self
    ):

        self.report_body = (
            ctk.CTkFrame(
                self.workspace,
                fg_color="transparent",
            )
        )

        self.report_body.grid(
            row=3,
            column=0,
            sticky="ew",
        )

        self.report_body.grid_columnconfigure(
            0,
            weight=65,
            minsize=540,
        )

        self.report_body.grid_columnconfigure(
            1,
            weight=35,
            minsize=330,
        )

        self.create_tasks_section()

        self.create_category_section()

    # =================================================
    # TASK SECTION
    # =================================================

    def create_tasks_section(
        self
    ):

        self.tasks_section = (
            ctk.CTkFrame(
                self.report_body,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"],
            )
        )

        self.tasks_section.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8),
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        header = (
            ctk.CTkFrame(
                self.tasks_section,
                fg_color="transparent",
            )
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(18, 9),
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        left = (
            ctk.CTkFrame(
                header,
                fg_color="transparent",
            )
        )

        left.grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            left,
            text="Completed Tasks",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=19,
                weight="bold",
            ),
            text_color=COLORS["text"],
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            left,
            text=(
                "Tasks completed during the selected period."
            ),
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
            ),
            text_color=COLORS["muted"],
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        self.completed_count_label = (
            ctk.CTkLabel(
                header,
                text="0 tasks",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                    weight="bold",
                ),
                text_color=COLORS["emerald"],
            )
        )

        self.completed_count_label.grid(
            row=0,
            column=1,
            sticky="e",
        )

        # ---------------------------------------------
        # CONTAINER
        # ---------------------------------------------

        self.tasks_container = (
            ctk.CTkFrame(
                self.tasks_section,
                fg_color="transparent",
            )
        )

        self.tasks_container.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(2, 14),
        )

    # =================================================
    # CATEGORY SECTION
    # =================================================

    def create_category_section(
        self
    ):

        self.category_section = (
            ctk.CTkFrame(
                self.report_body,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"],
            )
        )

        self.category_section.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0),
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        header = (
            ctk.CTkFrame(
                self.category_section,
                fg_color="transparent",
            )
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(18, 9),
        )

        ctk.CTkLabel(
            header,
            text="Category Summary",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=19,
                weight="bold",
            ),
            text_color=COLORS["text"],
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            header,
            text=(
                "Distribution of your completed work."
            ),
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
            ),
            text_color=COLORS["muted"],
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        # ---------------------------------------------
        # CONTAINER
        # ---------------------------------------------

        self.category_container = (
            ctk.CTkFrame(
                self.category_section,
                fg_color="transparent",
            )
        )

        self.category_container.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(2, 14),
        )

    # =================================================
    # REPORT TYPE
    # =================================================

    def change_report_type(
        self,
        value
    ):

        self.report_type = value

        self.refresh_reports()

    # =================================================
    # REFRESH
    # =================================================

    def refresh_reports(
        self
    ):

        self.load_summary()

        self.load_completed_tasks()

        self.load_category_summary()

        self.after_idle(
            self._refresh_scroll_region
        )

    # =================================================
    # SUMMARY
    # =================================================

    def load_summary(
        self
    ):

        summary = (
            get_report_summary(
                self.report_type
            )
        )

        # ---------------------------------------------
        # VALUES
        # ---------------------------------------------

        self.tasks_value.configure(
            text=str(
                summary[
                    "tasks_completed"
                ]
            )
        )

        self.categories_value.configure(
            text=str(
                summary[
                    "category_count"
                ]
            )
        )

        self.top_category_value.configure(
            text=summary[
                "top_category"
            ]
        )

        # ---------------------------------------------
        # DATE RANGE
        # ---------------------------------------------

        start = (
            self.format_date_only(
                summary[
                    "start_date"
                ]
            )
        )

        end = (
            self.format_date_only(
                summary[
                    "end_date"
                ]
            )
        )

        if (
            summary[
                "start_date"
            ]
            == summary[
                "end_date"
            ]
        ):

            range_text = start

        else:

            range_text = (
                f"{start}  –  {end}"
            )

        self.range_label.configure(
            text=range_text
        )

    # =================================================
    # COMPLETED TASKS
    # =================================================

    def load_completed_tasks(
        self
    ):

        # ---------------------------------------------
        # CLEAR
        # ---------------------------------------------

        for widget in (
            self.tasks_container
            .winfo_children()
        ):

            widget.destroy()

        # ---------------------------------------------
        # LOAD
        # ---------------------------------------------

        tasks = (
            get_report_completed_tasks(
                self.report_type
            )
        )

        self.completed_count_label.configure(
            text=(
                f"{len(tasks)} "
                f"{'task' if len(tasks) == 1 else 'tasks'}"
            )
        )

        # =================================================
        # EMPTY
        # =================================================

        if not tasks:

            empty = (
                ctk.CTkFrame(
                    self.tasks_container,
                    corner_radius=14,
                    fg_color=COLORS["surface_alt"],
                    border_width=1,
                    border_color=COLORS["border_soft"],
                )
            )

            empty.pack(
                fill="x",
                pady=5,
            )

            ctk.CTkLabel(
                empty,
                text="✓",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=27,
                    weight="bold",
                ),
                text_color=COLORS["emerald"],
            ).pack(
                pady=(22, 5),
            )

            ctk.CTkLabel(
                empty,
                text="No completed tasks",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=13,
                    weight="bold",
                ),
                text_color=COLORS["text"],
            ).pack()

            ctk.CTkLabel(
                empty,
                text=(
                    "There are no completed tasks "
                    "for this report period."
                ),
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                ),
                text_color=COLORS["muted"],
            ).pack(
                pady=(4, 22),
            )

            return

        # =================================================
        # TASK ROWS
        # =================================================

        for task in tasks:

            (
                task_id,
                title,
                priority,
                category,
                due_date,
                completed_at,
                created_at,
            ) = task

            # -----------------------------------------
            # COLORS
            # -----------------------------------------

            category_color = (
                CATEGORY_COLORS.get(
                    category,
                    self.accent,
                )
            )

            if priority == "High":

                priority_color = (
                    COLORS["danger"]
                )

            elif priority == "Medium":

                priority_color = (
                    COLORS["amber"]
                )

            else:

                priority_color = (
                    COLORS["emerald"]
                )

            # -----------------------------------------
            # CARD
            # -----------------------------------------

            row = (
                ctk.CTkFrame(
                    self.tasks_container,
                    corner_radius=13,
                    fg_color=COLORS["surface_alt"],
                    border_width=1,
                    border_color=COLORS["border_soft"],
                )
            )

            row.pack(
                fill="x",
                pady=5,
            )

            row.grid_columnconfigure(
                1,
                weight=1
            )

            # -----------------------------------------
            # COMPLETED ICON
            # -----------------------------------------

            icon_box = (
                ctk.CTkFrame(
                    row,
                    width=42,
                    height=42,
                    corner_radius=12,
                    fg_color=COLORS["emerald"],
                )
            )

            icon_box.grid(
                row=0,
                column=0,
                rowspan=3,
                padx=(12, 11),
                pady=13,
            )

            icon_box.grid_propagate(
                False
            )

            ctk.CTkLabel(
                icon_box,
                text="✓",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=17,
                    weight="bold",
                ),
                text_color=COLORS["white"],
            ).place(
                relx=0.5,
                rely=0.5,
                anchor="center",
            )

            # -----------------------------------------
            # TITLE
            # -----------------------------------------

            ctk.CTkLabel(
                row,
                text=title,
                anchor="w",
                justify="left",
                wraplength=560,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=13,
                    weight="bold",
                ),
                text_color=COLORS["text"],
            ).grid(
                row=0,
                column=1,
                sticky="ew",
                padx=(0, 10),
                pady=(11, 2),
            )

            # -----------------------------------------
            # BADGES
            # -----------------------------------------

            meta = (
                ctk.CTkFrame(
                    row,
                    fg_color="transparent",
                )
            )

            meta.grid(
                row=1,
                column=1,
                sticky="w",
                padx=(0, 10),
                pady=2,
            )

            category_badge = (
                ctk.CTkFrame(
                    meta,
                    corner_radius=100,
                    fg_color=category_color,
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
                    weight="bold",
                ),
                text_color=COLORS["white"],
            ).pack(
                padx=8,
                pady=3,
            )

            priority_badge = (
                ctk.CTkFrame(
                    meta,
                    corner_radius=100,
                    fg_color=priority_color,
                )
            )

            priority_badge.pack(
                side="left",
                padx=(6, 0),
            )

            ctk.CTkLabel(
                priority_badge,
                text=(
                    f"{priority} Priority"
                ),
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=9,
                    weight="bold",
                ),
                text_color=COLORS["white"],
            ).pack(
                padx=8,
                pady=3,
            )

            # -----------------------------------------
            # DUE DATE
            # -----------------------------------------

            if due_date:

                due_text = (
                    "Due "
                    + self.format_date_only(
                        due_date
                    )
                )

            else:

                due_text = (
                    "No due date"
                )

            ctk.CTkLabel(
                row,
                text=due_text,
                anchor="w",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                ),
                text_color=COLORS["muted"],
            ).grid(
                row=2,
                column=1,
                sticky="w",
                padx=(0, 10),
                pady=(2, 11),
            )

            # -----------------------------------------
            # COMPLETED DATE
            # -----------------------------------------

            history_date = (
                completed_at
                or created_at
            )

            date_frame = (
                ctk.CTkFrame(
                    row,
                    fg_color="transparent",
                )
            )

            date_frame.grid(
                row=0,
                column=2,
                rowspan=3,
                sticky="e",
                padx=(10, 14),
                pady=10,
            )

            (
                formatted_date,
                formatted_time,
            ) = self.format_datetime_parts(
                history_date
            )

            ctk.CTkLabel(
                date_frame,
                text=formatted_date,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                    weight="bold",
                ),
                text_color=COLORS["text"],
            ).pack(
                anchor="e"
            )

            ctk.CTkLabel(
                date_frame,
                text=formatted_time,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=9,
                ),
                text_color=COLORS["muted"],
            ).pack(
                anchor="e",
                pady=(2, 0),
            )

    # =================================================
    # CATEGORY SUMMARY
    # =================================================

    def load_category_summary(
        self
    ):

        # ---------------------------------------------
        # CLEAR
        # ---------------------------------------------

        for widget in (
            self.category_container
            .winfo_children()
        ):

            widget.destroy()

        # ---------------------------------------------
        # LOAD
        # ---------------------------------------------

        categories = (
            get_report_category_summary(
                self.report_type
            )
        )

        # =================================================
        # EMPTY
        # =================================================

        if not categories:

            empty = (
                ctk.CTkFrame(
                    self.category_container,
                    corner_radius=14,
                    fg_color=COLORS["surface_alt"],
                    border_width=1,
                    border_color=COLORS["border_soft"],
                )
            )

            empty.pack(
                fill="x",
                pady=5,
            )

            ctk.CTkLabel(
                empty,
                text="▦",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=26,
                    weight="bold",
                ),
                text_color=COLORS["amber"],
            ).pack(
                pady=(22, 5),
            )

            ctk.CTkLabel(
                empty,
                text="No category data",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=13,
                    weight="bold",
                ),
                text_color=COLORS["text"],
            ).pack()

            ctk.CTkLabel(
                empty,
                text=(
                    "Complete some tasks to build "
                    "a category breakdown."
                ),
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                ),
                text_color=COLORS["muted"],
            ).pack(
                pady=(4, 22),
            )

            return

        # ---------------------------------------------
        # TOTAL
        # ---------------------------------------------

        total = sum(
            count
            for (
                category,
                count
            ) in categories
        )

        # =================================================
        # CATEGORY ROWS
        # =================================================

        for (
            category,
            count
        ) in categories:

            percentage = 0

            if total:

                percentage = round(
                    (
                        count
                        / total
                    )
                    * 100
                )

            category_color = (
                CATEGORY_COLORS.get(
                    category,
                    self.accent,
                )
            )

            row = (
                ctk.CTkFrame(
                    self.category_container,
                    corner_radius=13,
                    fg_color=COLORS["surface_alt"],
                    border_width=1,
                    border_color=COLORS["border_soft"],
                )
            )

            row.pack(
                fill="x",
                pady=5,
            )

            row.grid_columnconfigure(
                0,
                weight=1
            )

            # -----------------------------------------
            # TITLE ROW
            # -----------------------------------------

            title_row = (
                ctk.CTkFrame(
                    row,
                    fg_color="transparent",
                )
            )

            title_row.grid(
                row=0,
                column=0,
                sticky="ew",
                padx=14,
                pady=(12, 7),
            )

            title_row.grid_columnconfigure(
                0,
                weight=1
            )

            left = (
                ctk.CTkFrame(
                    title_row,
                    fg_color="transparent",
                )
            )

            left.grid(
                row=0,
                column=0,
                sticky="w",
            )

            dot = (
                ctk.CTkFrame(
                    left,
                    width=9,
                    height=9,
                    corner_radius=100,
                    fg_color=category_color,
                )
            )

            dot.pack(
                side="left",
                padx=(0, 7),
            )

            dot.pack_propagate(
                False
            )

            ctk.CTkLabel(
                left,
                text=category,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=11,
                    weight="bold",
                ),
                text_color=COLORS["text"],
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                title_row,
                text=(
                    f"{count} "
                    f"{'task' if count == 1 else 'tasks'}"
                    f"  •  {percentage}%"
                ),
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=9,
                    weight="bold",
                ),
                text_color=COLORS["muted"],
            ).grid(
                row=0,
                column=1,
                sticky="e",
            )

            # -----------------------------------------
            # PROGRESS
            # -----------------------------------------

            progress = (
                ctk.CTkProgressBar(
                    row,
                    height=8,
                    corner_radius=100,
                    fg_color=COLORS["surface_soft"],
                    progress_color=category_color,
                )
            )

            progress.grid(
                row=1,
                column=0,
                sticky="ew",
                padx=14,
                pady=(0, 13),
            )

            progress.set(
                percentage
                / 100
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

        should_stack = (
            width < 980
        )

        if (
            should_stack
            == self._stacked_layout
        ):

            return

        self._stacked_layout = (
            should_stack
        )

        # =================================================
        # COMPACT
        # =================================================

        if should_stack:

            # -----------------------------------------
            # HEADER EXPORT BELOW
            # -----------------------------------------

            self.export_button.grid_configure(
                row=1,
                column=0,
                sticky="w",
                padx=0,
                pady=(14, 0),
            )

            # -----------------------------------------
            # PERIOD SELECTOR
            # -----------------------------------------

            self.period_selector.grid_configure(
                row=1,
                column=0,
                columnspan=3,
                sticky="ew",
                padx=18,
                pady=(0, 10),
            )

            self.range_badge.grid_configure(
                row=2,
                column=0,
                columnspan=3,
                sticky="w",
                padx=18,
                pady=(0, 14),
            )

            # -----------------------------------------
            # SUMMARY
            # 2 + 1
            # -----------------------------------------

            self.summary_frame.grid_columnconfigure(
                0,
                weight=1,
            )

            self.summary_frame.grid_columnconfigure(
                1,
                weight=1,
            )

            self.summary_frame.grid_columnconfigure(
                2,
                weight=0,
            )

            self.tasks_card.grid_configure(
                row=0,
                column=0,
                padx=(0, 6),
                pady=(0, 6),
            )

            self.categories_card.grid_configure(
                row=0,
                column=1,
                padx=(6, 0),
                pady=(0, 6),
            )

            self.top_category_card.grid_configure(
                row=1,
                column=0,
                columnspan=2,
                padx=0,
                pady=(6, 0),
            )

            # -----------------------------------------
            # REPORT BODY STACK
            # -----------------------------------------

            self.report_body.grid_columnconfigure(
                0,
                weight=1,
                minsize=0,
            )

            self.report_body.grid_columnconfigure(
                1,
                weight=0,
                minsize=0,
            )

            self.tasks_section.grid_configure(
                row=0,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0,
                pady=(0, 14),
            )

            self.category_section.grid_configure(
                row=1,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0,
                pady=0,
            )

        # =================================================
        # DESKTOP
        # =================================================

        else:

            # -----------------------------------------
            # HEADER
            # -----------------------------------------

            self.export_button.grid_configure(
                row=0,
                column=1,
                sticky="e",
                padx=(16, 0),
                pady=0,
            )

            # -----------------------------------------
            # PERIOD
            # -----------------------------------------

            self.period_selector.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                sticky="w",
                padx=0,
                pady=14,
            )

            self.range_badge.grid_configure(
                row=0,
                column=2,
                columnspan=1,
                sticky="e",
                padx=18,
                pady=14,
            )

            # -----------------------------------------
            # SUMMARY
            # -----------------------------------------

            for column in range(
                3
            ):

                self.summary_frame.grid_columnconfigure(
                    column,
                    weight=1,
                    uniform="report_summary",
                )

            self.tasks_card.grid_configure(
                row=0,
                column=0,
                columnspan=1,
                padx=(0, 6),
                pady=0,
            )

            self.categories_card.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                padx=6,
                pady=0,
            )

            self.top_category_card.grid_configure(
                row=0,
                column=2,
                columnspan=1,
                padx=(6, 0),
                pady=0,
            )

            # -----------------------------------------
            # BODY
            # -----------------------------------------

            self.report_body.grid_columnconfigure(
                0,
                weight=65,
                minsize=540,
            )

            self.report_body.grid_columnconfigure(
                1,
                weight=35,
                minsize=330,
            )

            self.tasks_section.grid_configure(
                row=0,
                column=0,
                columnspan=1,
                sticky="nsew",
                padx=(0, 8),
                pady=0,
            )

            self.category_section.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                sticky="nsew",
                padx=(8, 0),
                pady=0,
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
    # EXPORT TXT
    # =================================================

    def export_report(
        self
    ):

        summary = (
            get_report_summary(
                self.report_type
            )
        )

        tasks = (
            get_report_completed_tasks(
                self.report_type
            )
        )

        categories = (
            get_report_category_summary(
                self.report_type
            )
        )

        # ---------------------------------------------
        # EXPORT FOLDER
        # ---------------------------------------------

        export_folder = (
            get_setting(
                "export_folder",
                get_default_export_path(),
            )
        )

        Path(
            export_folder
        ).mkdir(
            parents=True,
            exist_ok=True,
        )

        # ---------------------------------------------
        # DEFAULT FILE
        # ---------------------------------------------

        filename = (
            f"LifeOS_"
            f"{self.report_type}_Report_"
            f"{datetime.now().strftime('%Y-%m-%d')}"
            f".txt"
        )

        # ---------------------------------------------
        # SAVE DIALOG
        # ---------------------------------------------

        file_path = (
            filedialog.asksaveasfilename(
                parent=self,
                title="Export LifeOS Report",
                defaultextension=".txt",
                initialdir=export_folder,
                initialfile=filename,
                filetypes=[
                    (
                        "Text File",
                        "*.txt",
                    )
                ],
            )
        )

        if not file_path:

            return

        # =================================================
        # BUILD REPORT
        # =================================================

        lines = []

        lines.append(
            "=" * 60
        )

        lines.append(
            "LIFEOS PRODUCTIVITY REPORT"
        )

        lines.append(
            "=" * 60
        )

        lines.append("")

        lines.append(
            f"Report Type: "
            f"{self.report_type}"
        )

        lines.append(
            f"Period: "
            f"{summary['start_date']} "
            f"to "
            f"{summary['end_date']}"
        )

        lines.append(
            f"Generated: "
            f"{datetime.now().strftime('%d %B %Y %I:%M %p')}"
        )

        lines.append("")

        # =================================================
        # SUMMARY
        # =================================================

        lines.append(
            "-" * 60
        )

        lines.append(
            "SUMMARY"
        )

        lines.append(
            "-" * 60
        )

        lines.append(
            f"Tasks Completed: "
            f"{summary['tasks_completed']}"
        )

        lines.append(
            f"Categories Used: "
            f"{summary['category_count']}"
        )

        lines.append(
            f"Top Category: "
            f"{summary['top_category']}"
        )

        lines.append("")

        # =================================================
        # COMPLETED TASKS
        # =================================================

        lines.append(
            "-" * 60
        )

        lines.append(
            "COMPLETED TASKS"
        )

        lines.append(
            "-" * 60
        )

        if tasks:

            for (
                index,
                task
            ) in enumerate(
                tasks,
                start=1,
            ):

                (
                    task_id,
                    title,
                    priority,
                    category,
                    due_date,
                    completed_at,
                    created_at,
                ) = task

                history_date = (
                    completed_at
                    or created_at
                )

                lines.append(
                    f"{index}. {title}"
                )

                lines.append(
                    f"   Category: "
                    f"{category}"
                )

                lines.append(
                    f"   Priority: "
                    f"{priority}"
                )

                if due_date:

                    lines.append(
                        f"   Due Date: "
                        f"{due_date}"
                    )

                lines.append(
                    f"   Completed: "
                    f"{history_date}"
                )

                lines.append("")

        else:

            lines.append(
                "No completed tasks."
            )

            lines.append("")

        # =================================================
        # CATEGORY SUMMARY
        # =================================================

        lines.append(
            "-" * 60
        )

        lines.append(
            "CATEGORY SUMMARY"
        )

        lines.append(
            "-" * 60
        )

        if categories:

            total_tasks = sum(
                count
                for (
                    category,
                    count
                ) in categories
            )

            for (
                category,
                count
            ) in categories:

                percentage = 0

                if total_tasks:

                    percentage = round(
                        (
                            count
                            / total_tasks
                        )
                        * 100
                    )

                lines.append(
                    f"{category}: "
                    f"{count} tasks "
                    f"({percentage}%)"
                )

        else:

            lines.append(
                "No category data."
            )

        lines.append("")

        lines.append(
            "=" * 60
        )

        lines.append(
            "Generated by LifeOS"
        )

        lines.append(
            "=" * 60
        )

        # =================================================
        # WRITE
        # =================================================

        try:

            with open(
                file_path,
                "w",
                encoding="utf-8",
            ) as file:

                file.write(
                    "\n".join(
                        lines
                    )
                )

            messagebox.showinfo(
                "Report Exported",
                (
                    "The report was exported "
                    "successfully."
                ),
                parent=self,
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                (
                    "The report could not "
                    "be exported.\n\n"
                    f"{error}"
                ),
                parent=self,
            )

    # =================================================
    # DATE / TIME HELPERS
    # =================================================

    def format_datetime(
        self,
        value
    ):

        if not value:

            return "Unknown"

        try:

            parsed = (
                datetime.strptime(
                    value,
                    "%Y-%m-%d %H:%M:%S",
                )
            )

            return parsed.strftime(
                "%d %b %Y\n"
                "%I:%M %p"
            )

        except ValueError:

            return value

    # =================================================
    # SPLIT DATETIME
    # =================================================

    def format_datetime_parts(
        self,
        value
    ):

        if not value:

            return (
                "Unknown",
                "",
            )

        try:

            parsed = (
                datetime.strptime(
                    value,
                    "%Y-%m-%d %H:%M:%S",
                )
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
                str(value),
                "",
            )

    # =================================================
    # DATE ONLY
    # =================================================

    def format_date_only(
        self,
        value
    ):

        if not value:

            return ""

        try:

            parsed = (
                datetime.strptime(
                    value,
                    "%Y-%m-%d",
                )
            )

            return parsed.strftime(
                "%d %b %Y"
            )

        except ValueError:

            return value