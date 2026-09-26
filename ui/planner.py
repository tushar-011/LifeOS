import customtkinter as ctk
import calendar

from datetime import date, datetime

from database.database import (
    add_planner_activity,
    get_planner_activities,
    toggle_planner_activity,
    delete_planner_activity
)


class PlannerPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        today = date.today()

        self.current_year = today.year
        self.current_month = today.month

        self.selected_date = today

        self.grid_rowconfigure(
            1,
            weight=1
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.create_header()
        self.create_main_layout()

        self.build_calendar()
        self.load_selected_day()

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

        ctk.CTkLabel(
            header,
            text="Planner",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            header,
            text="Click a date to plan your day."
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(5, 0)
        )

        today_button = ctk.CTkButton(
            header,
            text="Today",
            width=90,
            command=self.go_to_today
        )

        today_button.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=5
        )

    # =================================================
    # MAIN LAYOUT
    # =================================================

    def create_main_layout(self):

        self.main_container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.main_container.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(0, 25)
        )

        self.main_container.grid_columnconfigure(
            0,
            weight=3
        )

        self.main_container.grid_columnconfigure(
            1,
            weight=2
        )

        self.main_container.grid_rowconfigure(
            0,
            weight=1
        )

        # Calendar card
        self.calendar_card = ctk.CTkFrame(
            self.main_container,
            corner_radius=15
        )

        self.calendar_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        # Selected day schedule
        self.schedule_card = ctk.CTkFrame(
            self.main_container,
            corner_radius=15
        )

        self.schedule_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        self.create_calendar_header()
        self.create_schedule_panel()

    # =================================================
    # CALENDAR HEADER
    # =================================================

    def create_calendar_header(self):

        header = ctk.CTkFrame(
            self.calendar_card,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        header.grid_columnconfigure(
            1,
            weight=1
        )

        previous_button = ctk.CTkButton(
            header,
            text="‹",
            width=40,
            command=self.previous_month
        )

        previous_button.grid(
            row=0,
            column=0
        )

        self.month_label = ctk.CTkLabel(
            header,
            text="",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        self.month_label.grid(
            row=0,
            column=1
        )

        next_button = ctk.CTkButton(
            header,
            text="›",
            width=40,
            command=self.next_month
        )

        next_button.grid(
            row=0,
            column=2
        )

        # Calendar grid container
        self.calendar_grid = ctk.CTkFrame(
            self.calendar_card,
            fg_color="transparent"
        )

        self.calendar_grid.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(5, 20)
        )

    # =================================================
    # BUILD CALENDAR
    # =================================================

    def build_calendar(self):

        for widget in (
            self.calendar_grid
            .winfo_children()
        ):
            widget.destroy()

        month_name = calendar.month_name[
            self.current_month
        ]

        self.month_label.configure(
            text=(
                f"{month_name} "
                f"{self.current_year}"
            )
        )

        # Monday -> Sunday
        day_names = [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun"
        ]

        for column, day_name in enumerate(
            day_names
        ):

            self.calendar_grid.grid_columnconfigure(
                column,
                weight=1
            )

            label = ctk.CTkLabel(
                self.calendar_grid,
                text=day_name,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                )
            )

            label.grid(
                row=0,
                column=column,
                sticky="ew",
                padx=3,
                pady=5
            )

        month_data = calendar.monthcalendar(
            self.current_year,
            self.current_month
        )

        today = date.today()

        for row_index, week in enumerate(
            month_data,
            start=1
        ):

            self.calendar_grid.grid_rowconfigure(
                row_index,
                weight=1
            )

            for column, day_number in enumerate(
                week
            ):

                if day_number == 0:

                    empty = ctk.CTkLabel(
                        self.calendar_grid,
                        text=""
                    )

                    empty.grid(
                        row=row_index,
                        column=column,
                        sticky="nsew",
                        padx=3,
                        pady=3
                    )

                    continue

                current_date = date(
                    self.current_year,
                    self.current_month,
                    day_number
                )

                text = str(day_number)

                # Show number of activities
                activities = (
                    get_planner_activities(
                        current_date.isoformat()
                    )
                )

                if activities:
                    text += f"\n• {len(activities)}"

                button = ctk.CTkButton(
                    self.calendar_grid,
                    text=text,
                    height=65,
                    corner_radius=10,
                    command=(
                        lambda selected=current_date:
                        self.select_date(
                            selected
                        )
                    )
                )

                # Highlight selected date
                if (
                    current_date
                    == self.selected_date
                ):

                    button.configure(
                        border_width=2
                    )

                # Today's date also gets text indicator
                if current_date == today:

                    if activities:
                        button.configure(
                            text=(
                                f"{day_number}\n"
                                f"Today • {len(activities)}"
                            )
                        )

                    else:

                        button.configure(
                            text=(
                                f"{day_number}\nToday"
                            )
                        )

                button.grid(
                    row=row_index,
                    column=column,
                    sticky="nsew",
                    padx=3,
                    pady=3
                )

    # =================================================
    # SELECT DATE
    # =================================================

    def select_date(self, selected_date):

        self.selected_date = (
            selected_date
        )

        self.build_calendar()
        self.load_selected_day()

        # Clicking a date opens activity popup
        self.open_activity_popup()

    # =================================================
    # MONTH NAVIGATION
    # =================================================

    def previous_month(self):

        self.current_month -= 1

        if self.current_month == 0:

            self.current_month = 12
            self.current_year -= 1

        self.build_calendar()

    def next_month(self):

        self.current_month += 1

        if self.current_month == 13:

            self.current_month = 1
            self.current_year += 1

        self.build_calendar()

    def go_to_today(self):

        today = date.today()

        self.current_year = today.year
        self.current_month = today.month
        self.selected_date = today

        self.build_calendar()
        self.load_selected_day()

    # =================================================
    # ACTIVITY POPUP
    # =================================================

    def open_activity_popup(self):

        popup = ctk.CTkToplevel(
            self
        )

        popup.title(
            "Add Planner Activity"
        )

        popup.geometry(
            "480x520"
        )

        popup.resizable(
            False,
            False
        )

        popup.transient(
            self.winfo_toplevel()
        )

        popup.grab_set()

        selected_text = (
            self.selected_date
            .strftime(
                "%A, %d %B %Y"
            )
        )

        ctk.CTkLabel(
            popup,
            text="Add Activity",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        ctk.CTkLabel(
            popup,
            text=selected_text,
            font=ctk.CTkFont(
                size=14
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        # Title
        title_entry = ctk.CTkEntry(
            popup,
            placeholder_text="What are you planning?",
            height=42
        )

        title_entry.pack(
            fill="x",
            padx=25,
            pady=8
        )

        # Category
        category_menu = ctk.CTkOptionMenu(
            popup,
            values=[
                "General",
                "Study",
                "College",
                "Personal",
                "Work",
                "Fitness",
                "Other"
            ],
            height=40
        )

        category_menu.set(
            "General"
        )

        category_menu.pack(
            fill="x",
            padx=25,
            pady=8
        )

        # Time heading
        ctk.CTkLabel(
            popup,
            text="Time",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(15, 5)
        )

        time_frame = ctk.CTkFrame(
            popup,
            fg_color="transparent"
        )

        time_frame.pack(
            fill="x",
            padx=25,
            pady=5
        )

        time_frame.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        time_values = (
            self.generate_times()
        )

        start_menu = ctk.CTkOptionMenu(
            time_frame,
            values=time_values
        )

        start_menu.set(
            "09:00"
        )

        start_menu.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5)
        )

        end_menu = ctk.CTkOptionMenu(
            time_frame,
            values=time_values
        )

        end_menu.set(
            "10:00"
        )

        end_menu.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(5, 0)
        )

        message_label = ctk.CTkLabel(
            popup,
            text=""
        )

        message_label.pack(
            anchor="w",
            padx=25,
            pady=10
        )

        def save():

            title = (
                title_entry
                .get()
                .strip()
            )

            if not title:

                message_label.configure(
                    text=(
                        "Enter an activity title."
                    )
                )

                return

            start_time = (
                start_menu.get()
            )

            end_time = (
                end_menu.get()
            )

            if end_time <= start_time:

                message_label.configure(
                    text=(
                        "End time must be "
                        "after start time."
                    )
                )

                return

            add_planner_activity(
                title,
                self.selected_date.isoformat(),
                start_time,
                end_time,
                category_menu.get()
            )

            popup.destroy()

            self.build_calendar()
            self.load_selected_day()

        save_button = ctk.CTkButton(
            popup,
            text="Add to Planner",
            height=42,
            command=save
        )

        save_button.pack(
            fill="x",
            padx=25,
            pady=(20, 8)
        )

        cancel_button = ctk.CTkButton(
            popup,
            text="Cancel",
            height=40,
            command=popup.destroy
        )

        cancel_button.pack(
            fill="x",
            padx=25,
            pady=5
        )

    # =================================================
    # TIME VALUES
    # =================================================

    def generate_times(self):

        times = []

        for hour in range(24):

            for minute in (
                0,
                30
            ):

                times.append(
                    f"{hour:02d}:{minute:02d}"
                )

        return times

    # =================================================
    # SCHEDULE PANEL
    # =================================================

    def create_schedule_panel(self):

        self.selected_date_label = (
            ctk.CTkLabel(
                self.schedule_card,
                text="",
                font=ctk.CTkFont(
                    size=21,
                    weight="bold"
                )
            )
        )

        self.selected_date_label.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        self.selected_day_label = (
            ctk.CTkLabel(
                self.schedule_card,
                text=""
            )
        )

        self.selected_day_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        add_button = ctk.CTkButton(
            self.schedule_card,
            text="+ Add Activity",
            command=self.open_activity_popup
        )

        add_button.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        self.activity_container = (
            ctk.CTkScrollableFrame(
                self.schedule_card,
                fg_color="transparent"
            )
        )

        self.activity_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

    # =================================================
    # LOAD SELECTED DAY
    # =================================================

    def load_selected_day(self):

        self.selected_date_label.configure(
            text=(
                self.selected_date
                .strftime(
                    "%d %B %Y"
                )
            )
        )

        self.selected_day_label.configure(
            text=(
                self.selected_date
                .strftime(
                    "%A"
                )
            )
        )

        for widget in (
            self.activity_container
            .winfo_children()
        ):
            widget.destroy()

        activities = get_planner_activities(
            self.selected_date.isoformat()
        )

        if not activities:

            ctk.CTkLabel(
                self.activity_container,
                text="Nothing planned."
            ).pack(
                anchor="w",
                padx=5,
                pady=20
            )

            return

        for activity in activities:

            self.create_activity_card(
                activity
            )

    # =================================================
    # ACTIVITY CARD
    # =================================================

    def create_activity_card(
        self,
        activity
    ):

        (
            activity_id,
            title,
            activity_date,
            start_time,
            end_time,
            category,
            completed
        ) = activity

        card = ctk.CTkFrame(
            self.activity_container,
            corner_radius=10
        )

        card.pack(
            fill="x",
            pady=5
        )

        card.grid_columnconfigure(
            1,
            weight=1
        )

        checkbox = ctk.CTkCheckBox(
            card,
            text="",
            width=25,
            command=(
                lambda:
                self.change_status(
                    activity_id,
                    checkbox.get()
                )
            )
        )

        checkbox.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(12, 3),
            pady=12
        )

        if completed:
            checkbox.select()

        time_text = (
            f"{self.format_time(start_time)}"
            f" - "
            f"{self.format_time(end_time)}"
        )

        ctk.CTkLabel(
            card,
            text=time_text,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=5,
            pady=(10, 1)
        )

        ctk.CTkLabel(
            card,
            text=(
                f"{title}  •  {category}"
            )
        ).grid(
            row=1,
            column=1,
            sticky="w",
            padx=5,
            pady=(1, 10)
        )

        delete_button = ctk.CTkButton(
            card,
            text="×",
            width=35,
            command=(
                lambda:
                self.remove_activity(
                    activity_id
                )
            )
        )

        delete_button.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=10
        )

    # =================================================
    # FORMAT TIME
    # =================================================

    def format_time(self, value):

        try:

            parsed = datetime.strptime(
                value,
                "%H:%M"
            )

            return parsed.strftime(
                "%I:%M %p"
            ).lstrip("0")

        except (
            ValueError,
            TypeError
        ):

            return value

    # =================================================
    # STATUS
    # =================================================

    def change_status(
        self,
        activity_id,
        completed
    ):

        toggle_planner_activity(
            activity_id,
            completed
        )

        self.load_selected_day()

    # =================================================
    # DELETE
    # =================================================

    def remove_activity(
        self,
        activity_id
    ):

        delete_planner_activity(
            activity_id
        )

        self.build_calendar()
        self.load_selected_day()