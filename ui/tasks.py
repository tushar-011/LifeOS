import customtkinter as ctk

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

        self.grid_columnconfigure(0, weight=1)

        self.create_header()
        self.create_stats()
        self.create_form()
        self.create_task_list()

        self.load_tasks()

    # ---------------------------------------
    # HEADER
    # ---------------------------------------

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
            text="Manage your daily tasks and priorities."
        )

        subtitle.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(5, 0)
        )

    # ---------------------------------------
    # STATS
    # ---------------------------------------

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

    # ---------------------------------------
    # FORM
    # ---------------------------------------

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

        ctk.CTkLabel(
            self.form_card,
            text="Add Task",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=20,
            pady=(18, 10)
        )

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

        self.date_entry = ctk.CTkEntry(
            self.form_card,
            placeholder_text="Due date (YYYY-MM-DD)"
        )

        self.date_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(10, 20),
            pady=8
        )

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

        self.priority_menu = ctk.CTkOptionMenu(
            self.form_card,
            values=[
                "Low",
                "Medium",
                "High"
            ]
        )

        self.priority_menu.set("Medium")

        self.priority_menu.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=8
        )

        self.category_entry = ctk.CTkEntry(
            self.form_card,
            placeholder_text="Category"
        )

        self.category_entry.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=(10, 20),
            pady=8
        )

        button_frame = ctk.CTkFrame(
            self.form_card,
            fg_color="transparent"
        )

        button_frame.grid(
            row=4,
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
            text="Cancel Edit",
            command=self.clear_form
        )

        self.cancel_button.pack(
            side="left",
            padx=5
        )

    # ---------------------------------------
    # TASK LIST
    # ---------------------------------------

    def create_task_list(self):

        self.list_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        self.list_card.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(10, 25)
        )

        ctk.CTkLabel(
            self.list_card,
            text="Your Tasks",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        self.tasks_container = ctk.CTkFrame(
            self.list_card,
            fg_color="transparent"
        )

        self.tasks_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

    # ---------------------------------------
    # DATABASE ACTIONS
    # ---------------------------------------

    def save_task(self):

        title = self.title_entry.get().strip()

        if not title:
            return

        description = (
            self.description_entry
            .get()
            .strip()
        )

        due_date = (
            self.date_entry
            .get()
            .strip()
        )

        priority = (
            self.priority_menu
            .get()
        )

        category = (
            self.category_entry
            .get()
            .strip()
        )

        if not category:
            category = "General"

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

    def load_tasks(self):

        for widget in (
            self.tasks_container
            .winfo_children()
        ):
            widget.destroy()

        tasks = get_tasks()

        total = len(tasks)

        completed_count = sum(
            1
            for task in tasks
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

        if not tasks:

            ctk.CTkLabel(
                self.tasks_container,
                text="No tasks yet."
            ).pack(
                pady=30
            )

            return

        for task in tasks:
            self.create_task_card(task)

    # ---------------------------------------
    # TASK CARD
    # ---------------------------------------

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

        details = (
            f"{category}  •  "
            f"{priority}"
        )

        if due_date:
            details += (
                f"  •  Due {due_date}"
            )

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

    # ---------------------------------------
    # TASK CONTROLS
    # ---------------------------------------

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

    def remove_task(self, task_id):

        delete_task(task_id)
        self.load_tasks()

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

        self.date_entry.insert(
            0,
            due_date or ""
        )

        self.priority_menu.set(
            priority
        )

        self.category_entry.insert(
            0,
            category
        )

        self.save_button.configure(
            text="Update Task"
        )

    def clear_entries_only(self):

        self.title_entry.delete(
            0,
            "end"
        )

        self.description_entry.delete(
            0,
            "end"
        )

        self.date_entry.delete(
            0,
            "end"
        )

        self.category_entry.delete(
            0,
            "end"
        )

    def clear_form(self):

        self.selected_task_id = None

        self.clear_entries_only()

        self.priority_menu.set(
            "Medium"
        )

        self.save_button.configure(
            text="Add Task"
        )