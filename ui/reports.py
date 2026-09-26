import customtkinter as ctk

from datetime import datetime
from pathlib import Path

from tkinter import (
    filedialog,
    messagebox
)

from database.database import (
    get_report_summary,
    get_report_completed_tasks,
    get_report_category_summary
)

from utils.settings_manager import (
    get_setting,
    get_default_export_path
)


class ReportsPage(
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
            (0, 1, 2),
            weight=1
        )

        self.report_type = (
            "Daily"
        )

        self.create_header()
        self.create_period_selector()
        self.create_summary_cards()
        self.create_tasks_section()
        self.create_category_section()

        self.refresh_reports()

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
            columnspan=3,
            sticky="ew",
            padx=25,
            pady=(25, 10)
        )

        left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            fill="x",
            expand=True
        )

        ctk.CTkLabel(
            left,
            text="Reports",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            left,
            text=(
                "Review completed tasks and "
                "category performance."
            )
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        ctk.CTkButton(
            header,
            text="Export .txt",
            width=130,
            height=40,
            command=self.export_report
        ).pack(
            side="right"
        )

    # =================================================
    # REPORT PERIOD
    # =================================================

    def create_period_selector(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=25,
            pady=10
        )

        ctk.CTkLabel(
            card,
            text="Report Period",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            side="left",
            padx=(20, 15),
            pady=18
        )

        self.period_selector = (
            ctk.CTkSegmentedButton(
                card,
                values=[
                    "Daily",
                    "Weekly",
                    "Monthly"
                ],
                command=self.change_report_type
            )
        )

        self.period_selector.set(
            "Daily"
        )

        self.period_selector.pack(
            side="left"
        )

        self.range_label = (
            ctk.CTkLabel(
                card,
                text=""
            )
        )

        self.range_label.pack(
            side="right",
            padx=20
        )

    # =================================================
    # SUMMARY CARDS
    # =================================================

    def create_summary_cards(self):

        self.tasks_value = (
            self.create_summary_card(
                0,
                "Tasks Completed",
                "0"
            )
        )

        self.categories_value = (
            self.create_summary_card(
                1,
                "Categories Used",
                "0"
            )
        )

        self.top_category_value = (
            self.create_summary_card(
                2,
                "Top Category",
                "None"
            )
        )

    def create_summary_card(
        self,
        column,
        title,
        value
    ):

        card = ctk.CTkFrame(
            self,
            corner_radius=15,
            height=120
        )

        card.grid(
            row=2,
            column=column,
            sticky="nsew",
            padx=10,
            pady=10
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
            pady=(18, 4)
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

        return value_label

    # =================================================
    # TASK SECTION
    # =================================================

    def create_tasks_section(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            card,
            text="Completed Tasks",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        self.tasks_container = (
            ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
        )

        self.tasks_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

    # =================================================
    # CATEGORY SECTION
    # =================================================

    def create_category_section(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.grid(
            row=3,
            column=2,
            sticky="nsew",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            card,
            text="Category Summary",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        self.category_container = (
            ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
        )

        self.category_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
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

    def refresh_reports(self):

        self.load_summary()

        self.load_completed_tasks()

        self.load_category_summary()

    # =================================================
    # SUMMARY
    # =================================================

    def load_summary(self):

        summary = (
            get_report_summary(
                self.report_type
            )
        )

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
            summary["start_date"]
            == summary["end_date"]
        ):

            range_text = start

        else:

            range_text = (
                f"{start} - {end}"
            )

        self.range_label.configure(
            text=range_text
        )

    # =================================================
    # COMPLETED TASKS
    # =================================================

    def load_completed_tasks(self):

        for widget in (
            self.tasks_container
            .winfo_children()
        ):

            widget.destroy()

        tasks = (
            get_report_completed_tasks(
                self.report_type
            )
        )

        if not tasks:

            ctk.CTkLabel(
                self.tasks_container,
                text=(
                    "No completed tasks "
                    "for this report period."
                )
            ).pack(
                anchor="w",
                padx=5,
                pady=25
            )

            return

        for task in tasks:

            (
                task_id,
                title,
                priority,
                category,
                due_date,
                completed_at,
                created_at
            ) = task

            row = ctk.CTkFrame(
                self.tasks_container,
                corner_radius=10
            )

            row.pack(
                fill="x",
                pady=5
            )

            left = ctk.CTkFrame(
                row,
                fg_color="transparent"
            )

            left.pack(
                side="left",
                fill="x",
                expand=True,
                padx=15,
                pady=12
            )

            ctk.CTkLabel(
                left,
                text=title,
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                )
            ).pack(
                anchor="w"
            )

            details = (
                f"{category} • "
                f"{priority} priority"
            )

            if due_date:

                details += (
                    f" • Due {due_date}"
                )

            ctk.CTkLabel(
                left,
                text=details,
                font=ctk.CTkFont(
                    size=11
                )
            ).pack(
                anchor="w",
                pady=(3, 0)
            )

            history_date = (
                completed_at
                or created_at
            )

            ctk.CTkLabel(
                row,
                text=self.format_datetime(
                    history_date
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
    # CATEGORY SUMMARY
    # =================================================

    def load_category_summary(self):

        for widget in (
            self.category_container
            .winfo_children()
        ):

            widget.destroy()

        categories = (
            get_report_category_summary(
                self.report_type
            )
        )

        if not categories:

            ctk.CTkLabel(
                self.category_container,
                text=(
                    "No category data "
                    "for this period."
                )
            ).pack(
                anchor="w",
                padx=5,
                pady=25
            )

            return

        total = sum(
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

            row = ctk.CTkFrame(
                self.category_container,
                corner_radius=10
            )

            row.pack(
                fill="x",
                pady=5
            )

            ctk.CTkLabel(
                row,
                text=category,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                )
            ).pack(
                side="left",
                padx=15,
                pady=12
            )

            percentage = 0

            if total:

                percentage = round(
                    (
                        count
                        / total
                    )
                    * 100
                )

            ctk.CTkLabel(
                row,
                text=(
                    f"{count} tasks "
                    f"• {percentage}%"
                )
            ).pack(
                side="right",
                padx=15
            )

    # =================================================
    # EXPORT TXT
    # =================================================

    def export_report(self):

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

        export_folder = (
            get_setting(
                "export_folder",
                get_default_export_path()
            )
        )

        Path(
            export_folder
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        filename = (
            f"LifeOS_"
            f"{self.report_type}_Report_"
            f"{datetime.now().strftime('%Y-%m-%d')}"
            f".txt"
        )

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
                        "*.txt"
                    )
                ]
            )
        )

        if not file_path:

            return

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
                start=1
            ):

                (
                    task_id,
                    title,
                    priority,
                    category,
                    due_date,
                    completed_at,
                    created_at
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

        try:

            with open(
                file_path,
                "w",
                encoding="utf-8"
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
                parent=self
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                (
                    "The report could not "
                    "be exported.\n\n"
                    f"{error}"
                ),
                parent=self
            )

    # =================================================
    # HELPERS
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
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            return parsed.strftime(
                "%d %b %Y\n"
                "%I:%M %p"
            )

        except ValueError:

            return value

    def format_date_only(
        self,
        value
    ):

        try:

            parsed = (
                datetime.strptime(
                    value,
                    "%Y-%m-%d"
                )
            )

            return parsed.strftime(
                "%d %b %Y"
            )

        except ValueError:

            return value