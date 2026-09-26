from __future__ import annotations

import calendar
from datetime import date, datetime

import customtkinter as ctk

from database.database import (
    add_task,
    delete_task,
    get_tasks,
    toggle_task,
    update_task,
)

from ui.theme import (
    CATEGORY_COLORS,
    COLORS,
    FONT_BODY,
    FONT_DISPLAY,
    module_accent,
    module_accent_hover,
)


class TasksPage(ctk.CTkScrollableFrame):
    """Responsive task manager page for LifeOS."""

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color=COLORS["app_bg"]
        )

        self.selected_task_id = None

        self.accent = module_accent("Tasks")
        self.accent_hover = module_accent_hover("Tasks")

        self._compact_layout = None
        self._resize_job = None

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.create_workspace()
        self.create_header()
        self.create_stats()
        self.create_form()
        self.create_filter_section()
        self.create_task_list()

        self.workspace.bind(
            "<Configure>",
            self._schedule_layout_check,
            add="+"
        )

        self.after(
            120,
            self.apply_responsive_layout
        )

        self.load_tasks()

    # =================================================
    # WORKSPACE
    # =================================================

    def create_workspace(self):

        self.workspace = ctk.CTkFrame(
            self,
            fg_color="transparent"
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

    def create_header(self):

        self.header = ctk.CTkFrame(
            self.workspace,
            fg_color="transparent"
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

        left = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )

        left.grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            left,
            text="Task Manager",
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
                "Capture work, set priorities and "
                "keep deadlines under control."
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

        self.header_badge = ctk.CTkFrame(
            self.header,
            corner_radius=100,
            fg_color=COLORS["surface_soft"]
        )

        self.header_badge.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(15, 0)
        )

        self.header_badge_label = ctk.CTkLabel(
            self.header_badge,
            text="0 pending",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold"
            ),
            text_color=self.accent
        )

        self.header_badge_label.pack(
            padx=13,
            pady=7
        )

    # =================================================
    # STATISTICS
    # =================================================

    def create_stats(self):

        self.stats_frame = ctk.CTkFrame(
            self.workspace,
            fg_color="transparent"
        )

        self.stats_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 14)
        )

        for column in range(3):

            self.stats_frame.grid_columnconfigure(
                column,
                weight=1,
                uniform="task_stats"
            )

        (
            self.total_card,
            self.total_label
        ) = self.create_stat_card(
            0,
            "Total Tasks",
            "0",
            "All saved tasks",
            COLORS["cyan"],
            "▤",
            (0, 6)
        )

        (
            self.pending_card,
            self.pending_label
        ) = self.create_stat_card(
            1,
            "Pending",
            "0",
            "Still to complete",
            COLORS["amber"],
            "◷",
            6
        )

        (
            self.completed_card,
            self.completed_label
        ) = self.create_stat_card(
            2,
            "Completed",
            "0",
            "Finished tasks",
            COLORS["emerald"],
            "✓",
            (6, 0)
        )

    def create_stat_card(
        self,
        column,
        title,
        value,
        subtitle,
        accent,
        icon,
        padx
    ):

        card = ctk.CTkFrame(
            self.stats_frame,
            height=136,
            corner_radius=18,
            fg_color=COLORS["surface"],
            border_width=1,
            border_color=COLORS["border"]
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

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
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

        icon_box = ctk.CTkFrame(
            top,
            width=34,
            height=34,
            corner_radius=10,
            fg_color=accent
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

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=28,
                weight="bold"
            ),
            text_color=accent
        )

        value_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=17
        )

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
            pady=(0, 14)
        )

        return card, value_label

    # =================================================
    # ADD / EDIT FORM
    # =================================================

    def create_form(self):

        self.form_card = ctk.CTkFrame(
            self.workspace,
            corner_radius=18,
            fg_color=COLORS["surface"],
            border_width=1,
            border_color=COLORS["border"]
        )

        self.form_card.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 14)
        )

        self.form_card.grid_columnconfigure(
            0,
            weight=1
        )

        header = ctk.CTkFrame(
            self.form_card,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=22,
            pady=(19, 10)
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        left.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.form_title = ctk.CTkLabel(
            left,
            text="Add Task",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=19,
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

        self.form_title.pack(
            anchor="w"
        )

        ctk.CTkLabel(
            left,
            text=(
                "Add the essentials now; "
                "you can edit the task later."
            ),
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10
            ),
            text_color=COLORS["muted"]
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        self.edit_badge = ctk.CTkLabel(
            header,
            text="NEW",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=9,
                weight="bold"
            ),
            text_color=self.accent
        )

        self.edit_badge.grid(
            row=0,
            column=1,
            sticky="e"
        )

        # ---------------------------------------------
        # FORM BODY
        # ---------------------------------------------

        self.form_body = ctk.CTkFrame(
            self.form_card,
            fg_color="transparent"
        )

        self.form_body.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=22,
            pady=(0, 4)
        )

        self.form_body.grid_columnconfigure(
            0,
            weight=3
        )

        self.form_body.grid_columnconfigure(
            1,
            weight=2
        )

        # ---------------------------------------------
        # LEFT FORM COLUMN
        # ---------------------------------------------

        self.form_left = ctk.CTkFrame(
            self.form_body,
            fg_color="transparent"
        )

        self.form_left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        self.form_left.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            self.form_left,
            text="Task",
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

        self.title_entry = ctk.CTkEntry(
            self.form_left,
            placeholder_text="Task title",
            height=42
        )

        self.title_entry.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        ctk.CTkLabel(
            self.form_left,
            text="Description",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold"
            ),
            text_color=COLORS["muted"]
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(12, 5)
        )

        self.description_entry = ctk.CTkEntry(
            self.form_left,
            placeholder_text="Short description",
            height=42
        )

        self.description_entry.grid(
            row=3,
            column=0,
            sticky="ew"
        )

        # ---------------------------------------------
        # RIGHT FORM COLUMN
        # ---------------------------------------------

        self.form_right = ctk.CTkFrame(
            self.form_body,
            fg_color="transparent"
        )

        self.form_right.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        self.form_right.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            self.form_right,
            text="Due date",
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

        self.date_frame = ctk.CTkFrame(
            self.form_right,
            fg_color="transparent"
        )

        self.date_frame.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        self.date_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        current_year = date.today().year

        self.day_menu = ctk.CTkOptionMenu(
            self.date_frame,
            values=[
                "Day"
            ] + [
                str(day)
                for day in range(
                    1,
                    32
                )
            ],
            height=42
        )

        self.day_menu.set(
            "Day"
        )

        self.day_menu.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 4)
        )

        month_values = [
            calendar.month_abbr[i]
            for i in range(
                1,
                13
            )
        ]

        self.month_menu = ctk.CTkOptionMenu(
            self.date_frame,
            values=[
                "Month"
            ] + month_values,
            command=self.update_day_values,
            height=42
        )

        self.month_menu.set(
            "Month"
        )

        self.month_menu.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=4
        )

        self.year_menu = ctk.CTkOptionMenu(
            self.date_frame,
            values=[
                "Year"
            ] + [
                str(year)
                for year in range(
                    current_year,
                    current_year + 6
                )
            ],
            command=self.update_day_values,
            height=42
        )

        self.year_menu.set(
            "Year"
        )

        self.year_menu.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=(4, 0)
        )

        # ---------------------------------------------
        # PRIORITY + CATEGORY
        # ---------------------------------------------

        self.meta_frame = ctk.CTkFrame(
            self.form_right,
            fg_color="transparent"
        )

        self.meta_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(12, 0)
        )

        self.meta_frame.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        priority_holder = ctk.CTkFrame(
            self.meta_frame,
            fg_color="transparent"
        )

        priority_holder.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 4)
        )

        priority_holder.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            priority_holder,
            text="Priority",
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

        self.priority_menu = ctk.CTkOptionMenu(
            priority_holder,
            values=[
                "Low",
                "Medium",
                "High"
            ],
            height=42
        )

        self.priority_menu.set(
            "Medium"
        )

        self.priority_menu.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        category_holder = ctk.CTkFrame(
            self.meta_frame,
            fg_color="transparent"
        )

        category_holder.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(4, 0)
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

        self.category_menu = ctk.CTkOptionMenu(
            category_holder,
            values=[
                "General",
                "Study",
                "College",
                "Personal",
                "Work",
                "Fitness",
                "Other"
            ],
            height=42
        )

        self.category_menu.set(
            "General"
        )

        self.category_menu.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        # ---------------------------------------------
        # FOOTER
        # ---------------------------------------------

        footer = ctk.CTkFrame(
            self.form_card,
            fg_color="transparent"
        )

        footer.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=22,
            pady=(8, 18)
        )

        footer.grid_columnconfigure(
            0,
            weight=1
        )

        self.form_message = ctk.CTkLabel(
            footer,
            text="",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10
            ),
            text_color=COLORS["danger"]
        )

        self.form_message.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.form_buttons = ctk.CTkFrame(
            footer,
            fg_color="transparent"
        )

        self.form_buttons.grid(
            row=0,
            column=1,
            sticky="e"
        )

        self.save_button = ctk.CTkButton(
            self.form_buttons,
            text="Add Task",
            width=122,
            height=40,
            corner_radius=11,
            fg_color=self.accent,
            hover_color=self.accent_hover,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=12,
                weight="bold"
            ),
            command=self.save_task
        )

        self.save_button.pack(
            side="left",
            padx=(0, 6)
        )

        self.cancel_button = ctk.CTkButton(
            self.form_buttons,
            text="Clear",
            width=96,
            height=40,
            corner_radius=11,
            fg_color=COLORS["surface_soft"],
            hover_color=COLORS["border"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=12,
                weight="bold"
            ),
            command=self.clear_form
        )

        self.cancel_button.pack(
            side="left"
        )

    # =================================================
    # DATE HELPERS
    # =================================================

    def update_day_values(
        self,
        _=None
    ):

        month = self.month_menu.get()
        year = self.year_menu.get()

        if (
            month == "Month"
            or year == "Year"
        ):

            return

        try:

            month_number = list(
                calendar.month_abbr
            ).index(
                month
            )

            days_in_month = calendar.monthrange(
                int(year),
                month_number
            )[1]

            values = [
                "Day"
            ] + [
                str(day)
                for day in range(
                    1,
                    days_in_month + 1
                )
            ]

            current_day = (
                self.day_menu.get()
            )

            self.day_menu.configure(
                values=values
            )

            if (
                current_day != "Day"
                and int(current_day) > days_in_month
            ):

                self.day_menu.set(
                    "Day"
                )

        except (
            ValueError,
            IndexError
        ):

            pass

    def get_selected_date(self):

        day = self.day_menu.get()
        month = self.month_menu.get()
        year = self.year_menu.get()

        if (
            day == "Day"
            and month == "Month"
            and year == "Year"
        ):

            return ""

        if (
            day == "Day"
            or month == "Month"
            or year == "Year"
        ):

            return None

        try:

            month_number = list(
                calendar.month_abbr
            ).index(
                month
            )

            selected_date = date(
                int(year),
                month_number,
                int(day)
            )

            return (
                selected_date.isoformat()
            )

        except (
            ValueError,
            IndexError
        ):

            return None

    # =================================================
    # FILTER SECTION
    # =================================================

    def create_filter_section(self):

        self.filter_card = ctk.CTkFrame(
            self.workspace,
            corner_radius=16,
            fg_color=COLORS["surface"],
            border_width=1,
            border_color=COLORS["border"]
        )

        self.filter_card.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        self.filter_card.grid_columnconfigure(
            0,
            weight=1
        )

        left = ctk.CTkFrame(
            self.filter_card,
            fg_color="transparent"
        )

        left.grid(
            row=0,
            column=0,
            sticky="w",
            padx=18,
            pady=14
        )

        ctk.CTkLabel(
            left,
            text="Your Tasks",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=18,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).pack(
            anchor="w"
        )

        self.visible_count_label = ctk.CTkLabel(
            left,
            text="0 shown",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10
            ),
            text_color=COLORS["muted"]
        )

        self.visible_count_label.pack(
            anchor="w",
            pady=(2, 0)
        )

        self.filter_menu = ctk.CTkOptionMenu(
            self.filter_card,
            width=170,
            height=38,
            values=[
                "All Tasks",
                "Pending",
                "Completed",
                "Today",
                "Upcoming",
                "Overdue"
            ],
            command=lambda _: self.load_tasks()
        )

        self.filter_menu.set(
            "All Tasks"
        )

        self.filter_menu.grid(
            row=0,
            column=1,
            sticky="e",
            padx=18,
            pady=14
        )

    # =================================================
    # TASK LIST
    # =================================================

    def create_task_list(self):

        self.list_card = ctk.CTkFrame(
            self.workspace,
            corner_radius=18,
            fg_color=COLORS["surface"],
            border_width=1,
            border_color=COLORS["border"]
        )

        self.list_card.grid(
            row=4,
            column=0,
            sticky="ew"
        )

        self.tasks_container = ctk.CTkFrame(
            self.list_card,
            fg_color="transparent"
        )

        self.tasks_container.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=14
        )

    # =================================================
    # SAVE TASK
    # =================================================

    def save_task(self):

        title = (
            self.title_entry
            .get()
            .strip()
        )

        if not title:

            self.form_message.configure(
                text="Please enter a task title.",
                text_color=COLORS["danger"]
            )

            return

        description = (
            self.description_entry
            .get()
            .strip()
        )

        due_date = (
            self.get_selected_date()
        )

        if due_date is None:

            self.form_message.configure(
                text=(
                    "Please select a complete "
                    "valid date."
                ),
                text_color=COLORS["danger"]
            )

            return

        priority = (
            self.priority_menu.get()
        )

        category = (
            self.category_menu.get()
        )

        if (
            self.selected_task_id
            is None
        ):

            add_task(
                title,
                description,
                due_date,
                priority,
                category
            )

        else:

            update_task(
                self.selected_task_id,
                title,
                description,
                due_date,
                priority,
                category
            )

        self.clear_form()

        self.load_tasks()

    # =================================================
    # LOAD TASKS
    # =================================================

    def load_tasks(self):

        for widget in (
            self.tasks_container
            .winfo_children()
        ):

            widget.destroy()

        all_tasks = (
            get_tasks()
        )

        total = (
            len(all_tasks)
        )

        completed_count = sum(
            1
            for task in all_tasks
            if task[6]
        )

        pending_count = (
            total
            - completed_count
        )

        self.total_label.configure(
            text=str(total)
        )

        self.pending_label.configure(
            text=str(
                pending_count
            )
        )

        self.completed_label.configure(
            text=str(
                completed_count
            )
        )

        self.header_badge_label.configure(
            text=(
                f"{pending_count} pending"
            )
        )

        tasks = (
            self.apply_filter(
                all_tasks
            )
        )

        self.visible_count_label.configure(
            text=(
                f"{len(tasks)} shown"
            )
        )

        if not tasks:

            empty = ctk.CTkFrame(
                self.tasks_container,
                corner_radius=14,
                fg_color=COLORS["surface_alt"],
                border_width=1,
                border_color=COLORS["border_soft"]
            )

            empty.pack(
                fill="x",
                pady=4
            )

            ctk.CTkLabel(
                empty,
                text="✓",
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
                text="No tasks found",
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
                    "Try another filter or "
                    "add a new task."
                ),
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10
                ),
                text_color=COLORS["muted"]
            ).pack(
                pady=(4, 22)
            )

            self.after_idle(
                self._refresh_scroll_region
            )

            return

        for task in tasks:

            self.create_task_card(
                task
            )

        self.after_idle(
            self._refresh_scroll_region
        )

    # =================================================
    # FILTER TASKS
    # =================================================

    def apply_filter(
        self,
        tasks
    ):

        selected_filter = (
            self.filter_menu.get()
        )

        today = date.today()

        filtered = []

        for task in tasks:

            due_date = task[3]

            completed = bool(
                task[6]
            )

            task_date = None

            if due_date:

                try:

                    task_date = (
                        datetime.strptime(
                            due_date,
                            "%Y-%m-%d"
                        )
                        .date()
                    )

                except ValueError:

                    pass

            if (
                selected_filter
                == "All Tasks"
            ):

                filtered.append(
                    task
                )

            elif (
                selected_filter
                == "Pending"
            ):

                if not completed:

                    filtered.append(
                        task
                    )

            elif (
                selected_filter
                == "Completed"
            ):

                if completed:

                    filtered.append(
                        task
                    )

            elif (
                selected_filter
                == "Today"
            ):

                if (
                    not completed
                    and task_date == today
                ):

                    filtered.append(
                        task
                    )

            elif (
                selected_filter
                == "Upcoming"
            ):

                if (
                    not completed
                    and task_date is not None
                    and task_date > today
                ):

                    filtered.append(
                        task
                    )

            elif (
                selected_filter
                == "Overdue"
            ):

                if (
                    not completed
                    and task_date is not None
                    and task_date < today
                ):

                    filtered.append(
                        task
                    )

        return filtered

    # =================================================
    # TASK CARD
    # =================================================

    def create_task_card(
        self,
        task
    ):

        (
            task_id,
            title,
            description,
            due_date,
            priority,
            category,
            completed
        ) = task

        category_color = (
            CATEGORY_COLORS.get(
                category,
                self.accent
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

        card = ctk.CTkFrame(
            self.tasks_container,
            corner_radius=14,
            fg_color=COLORS["surface_alt"],
            border_width=1,
            border_color=COLORS["border_soft"]
        )

        card.pack(
            fill="x",
            pady=6
        )

        card.grid_columnconfigure(
            1,
            weight=1
        )

        # ---------------------------------------------
        # CHECKBOX
        # ---------------------------------------------

        check = ctk.CTkCheckBox(
            card,
            text="",
            width=25,
            fg_color=self.accent,
            hover_color=self.accent_hover,
            command=lambda:
                self.change_status(
                    task_id,
                    check.get()
                )
        )

        check.grid(
            row=0,
            column=0,
            rowspan=3,
            padx=(14, 8),
            pady=15
        )

        if completed:

            check.select()

        title_color = (
            COLORS["muted"]
            if completed
            else COLORS["text"]
        )

        # ---------------------------------------------
        # TITLE
        # ---------------------------------------------

        ctk.CTkLabel(
            card,
            text=title,
            anchor="w",
            justify="left",
            wraplength=650,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=14,
                weight="bold"
            ),
            text_color=title_color
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(2, 10),
            pady=(12, 2)
        )

        # ---------------------------------------------
        # DESCRIPTION
        # ---------------------------------------------

        if description:

            ctk.CTkLabel(
                card,
                text=description,
                anchor="w",
                justify="left",
                wraplength=650,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10
                ),
                text_color=COLORS["muted"]
            ).grid(
                row=1,
                column=1,
                sticky="ew",
                padx=(2, 10),
                pady=(0, 4)
            )

        # ---------------------------------------------
        # META
        # ---------------------------------------------

        meta = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        meta.grid(
            row=2,
            column=1,
            sticky="w",
            padx=(2, 10),
            pady=(3, 12)
        )

        category_badge = ctk.CTkFrame(
            meta,
            corner_radius=100,
            fg_color=category_color
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
            padx=8,
            pady=3
        )

        priority_badge = ctk.CTkFrame(
            meta,
            corner_radius=100,
            fg_color=priority_color
        )

        priority_badge.pack(
            side="left",
            padx=(6, 0)
        )

        ctk.CTkLabel(
            priority_badge,
            text=priority,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=9,
                weight="bold"
            ),
            text_color=COLORS["white"]
        ).pack(
            padx=8,
            pady=3
        )

        (
            due_text,
            due_color
        ) = self.get_due_display(
            due_date,
            completed
        )

        ctk.CTkLabel(
            meta,
            text=(
                f"  •  {due_text}"
            ),
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold"
            ),
            text_color=due_color
        ).pack(
            side="left"
        )

        # ---------------------------------------------
        # ACTIONS
        # ---------------------------------------------

        action_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        action_frame.grid(
            row=0,
            column=2,
            rowspan=3,
            sticky="e",
            padx=(8, 13),
            pady=12
        )

        ctk.CTkButton(
            action_frame,
            text="Edit",
            width=72,
            height=36,
            corner_radius=10,
            fg_color=COLORS["indigo"],
            hover_color=COLORS["indigo_hover"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold"
            ),
            command=lambda:
                self.edit_task(
                    task
                )
        ).pack(
            side="left",
            padx=(0, 6)
        )

        ctk.CTkButton(
            action_frame,
            text="Delete",
            width=78,
            height=36,
            corner_radius=10,
            fg_color=COLORS["danger"],
            hover_color=COLORS["danger_hover"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold"
            ),
            command=lambda:
                self.remove_task(
                    task_id
                )
        ).pack(
            side="left"
        )

    # =================================================
    # DUE DISPLAY
    # =================================================

    def get_due_display(
        self,
        due_date,
        completed
    ):

        if not due_date:

            return (
                "No due date",
                COLORS["muted"]
            )

        try:

            parsed = datetime.strptime(
                due_date,
                "%Y-%m-%d"
            )

            task_date = (
                parsed.date()
            )

            formatted = (
                parsed.strftime(
                    "%d %b %Y"
                )
            )

            if completed:

                return (
                    f"Due {formatted}",
                    COLORS["muted"]
                )

            today = (
                date.today()
            )

            if task_date < today:

                return (
                    f"Overdue • {formatted}",
                    COLORS["danger"]
                )

            if task_date == today:

                return (
                    "Due Today",
                    COLORS["amber"]
                )

            return (
                f"Due {formatted}",
                COLORS["muted"]
            )

        except ValueError:

            return (
                f"Due {due_date}",
                COLORS["muted"]
            )

    # =================================================
    # STATUS / DELETE / EDIT
    # =================================================

    def change_status(
        self,
        task_id,
        completed
    ):

        toggle_task(
            task_id,
            completed
        )

        self.load_tasks()

    def remove_task(
        self,
        task_id
    ):

        delete_task(
            task_id
        )

        if (
            self.selected_task_id
            == task_id
        ):

            self.clear_form()

        self.load_tasks()

    def edit_task(
        self,
        task
    ):

        (
            task_id,
            title,
            description,
            due_date,
            priority,
            category,
            completed
        ) = task

        self.selected_task_id = (
            task_id
        )

        self.clear_entries_only()

        self.title_entry.insert(
            0,
            title
        )

        self.description_entry.insert(
            0,
            description or ""
        )

        self.priority_menu.set(
            priority
        )

        self.category_menu.set(
            category or "General"
        )

        if due_date:

            try:

                parsed_date = (
                    datetime.strptime(
                        due_date,
                        "%Y-%m-%d"
                    )
                )

                self.year_menu.set(
                    str(
                        parsed_date.year
                    )
                )

                self.month_menu.set(
                    calendar.month_abbr[
                        parsed_date.month
                    ]
                )

                self.update_day_values()

                self.day_menu.set(
                    str(
                        parsed_date.day
                    )
                )

            except ValueError:

                self.reset_date()

        self.save_button.configure(
            text="Update Task"
        )

        self.cancel_button.configure(
            text="Cancel Edit"
        )

        self.form_title.configure(
            text="Edit Task"
        )

        self.edit_badge.configure(
            text="EDITING"
        )

        self.form_message.configure(
            text=""
        )

        try:

            self._parent_canvas.yview_moveto(
                0
            )

        except Exception:

            pass

    # =================================================
    # CLEAR FORM
    # =================================================

    def clear_entries_only(self):

        self.title_entry.delete(
            0,
            "end"
        )

        self.description_entry.delete(
            0,
            "end"
        )

        self.priority_menu.set(
            "Medium"
        )

        self.category_menu.set(
            "General"
        )

        self.reset_date()

    def reset_date(self):

        self.day_menu.configure(
            values=[
                "Day"
            ] + [
                str(day)
                for day in range(
                    1,
                    32
                )
            ]
        )

        self.day_menu.set(
            "Day"
        )

        self.month_menu.set(
            "Month"
        )

        self.year_menu.set(
            "Year"
        )

    def clear_form(self):

        self.selected_task_id = None

        self.clear_entries_only()

        self.save_button.configure(
            text="Add Task"
        )

        self.cancel_button.configure(
            text="Clear"
        )

        self.form_title.configure(
            text="Add Task"
        )

        self.edit_badge.configure(
            text="NEW"
        )

        self.form_message.configure(
            text=""
        )

    # =================================================
    # RESPONSIVE LAYOUT
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

    def apply_responsive_layout(self):

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
            width < 900
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
            # STATS
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

            self.total_card.grid_configure(
                row=0,
                column=0,
                padx=(0, 6),
                pady=(0, 6)
            )

            self.pending_card.grid_configure(
                row=0,
                column=1,
                padx=(6, 0),
                pady=(0, 6)
            )

            self.completed_card.grid_configure(
                row=1,
                column=0,
                columnspan=2,
                padx=0,
                pady=(6, 0)
            )

            # -----------------------------------------
            # FORM STACK
            # -----------------------------------------

            self.form_body.grid_columnconfigure(
                0,
                weight=1
            )

            self.form_body.grid_columnconfigure(
                1,
                weight=0
            )

            self.form_left.grid_configure(
                row=0,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0,
                pady=(0, 12)
            )

            self.form_right.grid_configure(
                row=1,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0
            )

            # -----------------------------------------
            # FILTER STACK
            # -----------------------------------------

            self.filter_menu.grid_configure(
                row=1,
                column=0,
                sticky="ew",
                padx=18,
                pady=(0, 14)
            )

        # =================================================
        # DESKTOP
        # =================================================

        else:

            self.header_badge.grid_configure(
                row=0,
                column=1,
                sticky="e",
                padx=(15, 0),
                pady=0
            )

            for column in range(
                3
            ):

                self.stats_frame.grid_columnconfigure(
                    column,
                    weight=1,
                    uniform="task_stats"
                )

            self.total_card.grid_configure(
                row=0,
                column=0,
                columnspan=1,
                padx=(0, 6),
                pady=0
            )

            self.pending_card.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                padx=6,
                pady=0
            )

            self.completed_card.grid_configure(
                row=0,
                column=2,
                columnspan=1,
                padx=(6, 0),
                pady=0
            )

            self.form_body.grid_columnconfigure(
                0,
                weight=3
            )

            self.form_body.grid_columnconfigure(
                1,
                weight=2
            )

            self.form_left.grid_configure(
                row=0,
                column=0,
                columnspan=1,
                sticky="nsew",
                padx=(0, 8),
                pady=0
            )

            self.form_right.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                sticky="nsew",
                padx=(8, 0),
                pady=0
            )

            self.filter_menu.grid_configure(
                row=0,
                column=1,
                sticky="e",
                padx=18,
                pady=14
            )

        self.after_idle(
            self._refresh_scroll_region
        )

    # =================================================
    # SCROLL REGION
    # =================================================

    def _refresh_scroll_region(self):

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