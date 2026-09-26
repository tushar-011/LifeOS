import customtkinter as ctk
import calendar

from datetime import datetime, date

from database.database import (
    add_task,
    get_tasks,
    update_task,
    delete_task,
    toggle_task
)


class TasksPage(ctk.CTkScrollableFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            corner_radius=0
        )

        self.selected_task_id = None

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.create_header()
        self.create_stats()
        self.create_form()
        self.create_filter_section()
        self.create_task_list()

        self.load_tasks()

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

        header.grid_columnconfigure(
            0,
            weight=1
        )

        title = ctk.CTkLabel(
            header,
            text="Task Manager",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            sticky="w"
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Manage your tasks, deadlines and priorities."
        )

        subtitle.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(5, 0)
        )

    # =================================================
    # STATISTICS
    # =================================================

    def create_stats(self):

        self.stats_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.stats_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        self.stats_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        self.total_label = self.create_stat_card(
            0,
            "Total",
            "0"
        )

        self.pending_label = self.create_stat_card(
            1,
            "Pending",
            "0"
        )

        self.completed_label = self.create_stat_card(
            2,
            "Completed",
            "0"
        )

    def create_stat_card(
        self,
        column,
        title,
        value
    ):

        card = ctk.CTkFrame(
            self.stats_frame,
            corner_radius=14
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=7
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
            pady=(15, 2)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        )

        value_label.pack(
            anchor="w",
            padx=18,
            pady=(0, 15)
        )

        return value_label

    # =================================================
    # ADD / EDIT TASK FORM
    # =================================================

    def create_form(self):

        self.form_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        self.form_card.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        self.form_card.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        self.form_title = ctk.CTkLabel(
            self.form_card,
            text="Add Task",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        self.form_title.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=20,
            pady=(18, 10)
        )

        # ---------------------------------------------
        # TASK TITLE
        # ---------------------------------------------

        self.title_entry = ctk.CTkEntry(
            self.form_card,
            placeholder_text="Task title"
        )

        self.title_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=8
        )

        # ---------------------------------------------
        # DATE SELECTOR
        # ---------------------------------------------

        date_frame = ctk.CTkFrame(
            self.form_card,
            fg_color="transparent"
        )

        date_frame.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(10, 20),
            pady=8
        )

        date_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        current_year = date.today().year

        # Day
        self.day_menu = ctk.CTkOptionMenu(
            date_frame,
            values=[
                "Day"
            ] + [
                str(day)
                for day in range(1, 32)
            ]
        )

        self.day_menu.set("Day")

        self.day_menu.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5)
        )

        # Month
        month_values = [
            calendar.month_abbr[i]
            for i in range(1, 13)
        ]

        self.month_menu = ctk.CTkOptionMenu(
            date_frame,
            values=[
                "Month"
            ] + month_values,
            command=self.update_day_values
        )

        self.month_menu.set("Month")

        self.month_menu.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5
        )

        # Year
        self.year_menu = ctk.CTkOptionMenu(
            date_frame,
            values=[
                "Year"
            ] + [
                str(year)
                for year in range(
                    current_year,
                    current_year + 6
                )
            ],
            command=self.update_day_values
        )

        self.year_menu.set("Year")

        self.year_menu.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=(5, 0)
        )

        # ---------------------------------------------
        # DESCRIPTION
        # ---------------------------------------------

        self.description_entry = ctk.CTkEntry(
            self.form_card,
            placeholder_text="Short description"
        )

        self.description_entry.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=8
        )

        # ---------------------------------------------
        # PRIORITY DROPDOWN
        # ---------------------------------------------

        self.priority_menu = ctk.CTkOptionMenu(
            self.form_card,
            values=[
                "Low",
                "Medium",
                "High"
            ]
        )

        self.priority_menu.set(
            "Medium"
        )

        self.priority_menu.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=8
        )

        # ---------------------------------------------
        # CATEGORY DROPDOWN
        # ---------------------------------------------

        self.category_menu = ctk.CTkOptionMenu(
            self.form_card,
            values=[
                "General",
                "Study",
                "College",
                "Personal",
                "Work",
                "Fitness",
                "Other"
            ]
        )

        self.category_menu.set(
            "General"
        )

        self.category_menu.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=(10, 20),
            pady=8
        )

        # ---------------------------------------------
        # MESSAGE
        # ---------------------------------------------

        self.form_message = ctk.CTkLabel(
            self.form_card,
            text=""
        )

        self.form_message.grid(
            row=4,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 0)
        )

        # ---------------------------------------------
        # BUTTONS
        # ---------------------------------------------

        button_frame = ctk.CTkFrame(
            self.form_card,
            fg_color="transparent"
        )

        button_frame.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="e",
            padx=20,
            pady=(8, 18)
        )

        self.save_button = ctk.CTkButton(
            button_frame,
            text="Add Task",
            command=self.save_task
        )

        self.save_button.pack(
            side="left",
            padx=5
        )

        self.cancel_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_form
        )

        self.cancel_button.pack(
            side="left",
            padx=5
        )

    # =================================================
    # DATE FUNCTIONS
    # =================================================

    def update_day_values(self, _=None):

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
            ).index(month)

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

            current_day = self.day_menu.get()

            self.day_menu.configure(
                values=values
            )

            if (
                current_day != "Day"
                and int(current_day) > days_in_month
            ):
                self.day_menu.set("Day")

        except (
            ValueError,
            IndexError
        ):
            pass

    def get_selected_date(self):

        day = self.day_menu.get()
        month = self.month_menu.get()
        year = self.year_menu.get()

        # No date selected at all
        if (
            day == "Day"
            and month == "Month"
            and year == "Year"
        ):
            return ""

        # Partially selected date
        if (
            day == "Day"
            or month == "Month"
            or year == "Year"
        ):
            return None

        try:

            month_number = list(
                calendar.month_abbr
            ).index(month)

            selected_date = date(
                int(year),
                month_number,
                int(day)
            )

            return selected_date.isoformat()

        except (
            ValueError,
            IndexError
        ):
            return None

    # =================================================
    # FILTER SECTION
    # =================================================

    def create_filter_section(self):

        filter_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        filter_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=25,
            pady=(10, 0)
        )

        filter_frame.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            filter_frame,
            text="Tasks",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.filter_menu = ctk.CTkOptionMenu(
            filter_frame,
            width=160,
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
            sticky="e"
        )

    # =================================================
    # TASK LIST
    # =================================================

    def create_task_list(self):

        self.list_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        self.list_card.grid(
            row=4,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(10, 25)
        )

        self.tasks_container = ctk.CTkFrame(
            self.list_card,
            fg_color="transparent"
        )

        self.tasks_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
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
                text="Please enter a task title."
            )

            return

        description = (
            self.description_entry
            .get()
            .strip()
        )

        due_date = self.get_selected_date()

        if due_date is None:

            self.form_message.configure(
                text="Please select a complete valid date."
            )

            return

        priority = (
            self.priority_menu
            .get()
        )

        category = (
            self.category_menu
            .get()
        )

        if self.selected_task_id is None:

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

        all_tasks = get_tasks()

        total = len(all_tasks)

        completed_count = sum(
            1
            for task in all_tasks
            if task[6]
        )

        pending_count = (
            total - completed_count
        )

        self.total_label.configure(
            text=str(total)
        )

        self.pending_label.configure(
            text=str(pending_count)
        )

        self.completed_label.configure(
            text=str(completed_count)
        )

        tasks = self.apply_filter(
            all_tasks
        )

        if not tasks:

            ctk.CTkLabel(
                self.tasks_container,
                text="No tasks found."
            ).pack(
                pady=35
            )

            return

        for task in tasks:
            self.create_task_card(task)

    # =================================================
    # FILTER TASKS
    # =================================================

    def apply_filter(self, tasks):

        selected_filter = (
            self.filter_menu.get()
        )

        today = date.today()

        filtered = []

        for task in tasks:

            due_date = task[3]
            completed = bool(task[6])

            task_date = None

            if due_date:

                try:

                    task_date = datetime.strptime(
                        due_date,
                        "%Y-%m-%d"
                    ).date()

                except ValueError:
                    pass

            if selected_filter == "All Tasks":

                filtered.append(task)

            elif selected_filter == "Pending":

                if not completed:
                    filtered.append(task)

            elif selected_filter == "Completed":

                if completed:
                    filtered.append(task)

            elif selected_filter == "Today":

                if (
                    not completed
                    and task_date == today
                ):
                    filtered.append(task)

            elif selected_filter == "Upcoming":

                if (
                    not completed
                    and task_date is not None
                    and task_date > today
                ):
                    filtered.append(task)

            elif selected_filter == "Overdue":

                if (
                    not completed
                    and task_date is not None
                    and task_date < today
                ):
                    filtered.append(task)

        return filtered

    # =================================================
    # TASK CARD
    # =================================================

    def create_task_card(self, task):

        (
            task_id,
            title,
            description,
            due_date,
            priority,
            category,
            completed
        ) = task

        card = ctk.CTkFrame(
            self.tasks_container,
            corner_radius=12
        )

        card.pack(
            fill="x",
            pady=6
        )

        card.grid_columnconfigure(
            1,
            weight=1
        )

        check = ctk.CTkCheckBox(
            card,
            text="",
            width=25,
            command=lambda: self.change_status(
                task_id,
                check.get()
            )
        )

        check.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(15, 5),
            pady=15
        )

        if completed:
            check.select()

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        title_label.grid(
            row=0,
            column=1,
            sticky="w",
            padx=5,
            pady=(12, 2)
        )

        # ---------------------------------------------
        # DETAILS
        # ---------------------------------------------

        details = (
            f"{category}  •  {priority}"
        )

        if due_date:

            try:

                parsed_date = datetime.strptime(
                    due_date,
                    "%Y-%m-%d"
                )

                formatted_date = parsed_date.strftime(
                    "%d %b %Y"
                )

                task_date = parsed_date.date()

                if (
                    task_date < date.today()
                    and not completed
                ):

                    details += (
                        f"  •  Overdue"
                        f"  •  {formatted_date}"
                    )

                elif (
                    task_date == date.today()
                    and not completed
                ):

                    details += (
                        f"  •  Due Today"
                    )

                else:

                    details += (
                        f"  •  Due {formatted_date}"
                    )

            except ValueError:

                details += (
                    f"  •  Due {due_date}"
                )

        else:

            details += "  •  No Due Date"

        detail_label = ctk.CTkLabel(
            card,
            text=details,
            font=ctk.CTkFont(
                size=12
            )
        )

        detail_label.grid(
            row=1,
            column=1,
            sticky="w",
            padx=5,
            pady=(0, 12)
        )

        # ---------------------------------------------
        # EDIT
        # ---------------------------------------------

        edit_button = ctk.CTkButton(
            card,
            text="Edit",
            width=70,
            command=lambda: self.edit_task(
                task
            )
        )

        edit_button.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=5,
            pady=12
        )

        # ---------------------------------------------
        # DELETE
        # ---------------------------------------------

        delete_button = ctk.CTkButton(
            card,
            text="Delete",
            width=70,
            command=lambda: self.remove_task(
                task_id
            )
        )

        delete_button.grid(
            row=0,
            column=3,
            rowspan=2,
            padx=(5, 15),
            pady=12
        )

    # =================================================
    # CHANGE STATUS
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

    # =================================================
    # DELETE
    # =================================================

    def remove_task(self, task_id):

        delete_task(task_id)

        if self.selected_task_id == task_id:
            self.clear_form()

        self.load_tasks()

    # =================================================
    # EDIT
    # =================================================

    def edit_task(self, task):

        (
            task_id,
            title,
            description,
            due_date,
            priority,
            category,
            completed
        ) = task

        self.selected_task_id = task_id

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

        # Restore date
        if due_date:

            try:

                parsed_date = datetime.strptime(
                    due_date,
                    "%Y-%m-%d"
                )

                self.year_menu.set(
                    str(parsed_date.year)
                )

                self.month_menu.set(
                    calendar.month_abbr[
                        parsed_date.month
                    ]
                )

                self.update_day_values()

                self.day_menu.set(
                    str(parsed_date.day)
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

        self.form_message.configure(
            text=""
        )

    # =================================================
    # CLEAR ENTRIES
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

    # =================================================
    # RESET DATE
    # =================================================

    def reset_date(self):

        self.day_menu.configure(
            values=[
                "Day"
            ] + [
                str(day)
                for day in range(1, 32)
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

    # =================================================
    # CLEAR FORM
    # =================================================

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

        self.form_message.configure(
            text=""
        )