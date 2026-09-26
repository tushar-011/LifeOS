import calendar

from datetime import date, datetime

import customtkinter as ctk

from database.database import (
    add_planner_activity,
    delete_planner_activity,
    get_planner_activities,
    toggle_planner_activity,
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
# PLANNER PAGE
# =================================================

class PlannerPage(ctk.CTkScrollableFrame):

    def __init__(
        self,
        parent
    ):

        super().__init__(
            parent,
            corner_radius=0,
            fg_color=COLORS["app_bg"]
        )

        # ---------------------------------------------
        # DATE STATE
        # ---------------------------------------------

        today = date.today()

        self.current_year = today.year
        self.current_month = today.month
        self.selected_date = today

        # ---------------------------------------------
        # COLORS
        # ---------------------------------------------

        self.accent = (
            module_accent(
                "Planner"
            )
        )

        self.accent_hover = (
            module_accent_hover(
                "Planner"
            )
        )

        # ---------------------------------------------
        # RESPONSIVE STATE
        # ---------------------------------------------

        self._stacked_layout = None
        self._resize_job = None

        # ---------------------------------------------
        # PAGE GRID
        # ---------------------------------------------

        self.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # BUILD
        # ---------------------------------------------

        self.create_header()

        self.create_main_layout()

        self.build_calendar()

        self.load_selected_day()

        # ---------------------------------------------
        # RESPONSIVE EVENTS
        # ---------------------------------------------

        self.main_container.bind(
            "<Configure>",
            self._schedule_layout_check,
            add="+"
        )

        self.after(
            150,
            self.apply_responsive_layout
        )

    # =================================================
    # HEADER
    # =================================================

    def create_header(
        self
    ):

        self.header = (
            ctk.CTkFrame(
                self,
                fg_color="transparent"
            )
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=30,
            pady=(26, 16)
        )

        self.header.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # LEFT SIDE
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
            text="Planner",
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
                "Plan your day, organize activities "
                "and keep your schedule visible."
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
        # TODAY
        # ---------------------------------------------

        self.today_button = (
            ctk.CTkButton(
                self.header,
                text="Today",
                width=100,
                height=38,
                corner_radius=11,
                fg_color=self.accent,
                hover_color=self.accent_hover,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                command=self.go_to_today
            )
        )

        self.today_button.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(18, 0)
        )

    # =================================================
    # MAIN LAYOUT
    # =================================================

    def create_main_layout(
        self
    ):

        self.main_container = (
            ctk.CTkFrame(
                self,
                fg_color="transparent"
            )
        )

        self.main_container.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=30,
            pady=(0, 30)
        )

        # ---------------------------------------------
        # IMPORTANT:
        #
        # Schedule gets a genuine minimum width.
        # This prevents it being squeezed into
        # the tiny column seen in the screenshot.
        # ---------------------------------------------

        self.main_container.grid_columnconfigure(
            0,
            weight=1,
            minsize=620
        )

        self.main_container.grid_columnconfigure(
            1,
            weight=0,
            minsize=330
        )

        # ---------------------------------------------
        # CALENDAR
        # ---------------------------------------------

        self.calendar_card = (
            ctk.CTkFrame(
                self.main_container,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        self.calendar_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        # ---------------------------------------------
        # SCHEDULE
        # ---------------------------------------------

        self.schedule_card = (
            ctk.CTkFrame(
                self.main_container,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=self.accent
            )
        )

        self.schedule_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        self.create_calendar_header()

        self.create_schedule_panel()

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
        self,
        window_width=None
    ):

        self._resize_job = None

        try:

            self.update_idletasks()

            available_width = (
                self.main_container
                .winfo_width()
            )

        except Exception:

            available_width = 1200

        # ---------------------------------------------
        # FALLBACK
        # ---------------------------------------------

        if (
            available_width
            <= 1
        ):

            try:

                available_width = (
                    self.winfo_width()
                    - 60
                )

            except Exception:

                available_width = 1200

        # ---------------------------------------------
        # STACK IF THE CALENDAR + 330PX SIDE PANEL
        # CANNOT FIT COMFORTABLY.
        # ---------------------------------------------

        should_stack = (
            available_width
            < 1040
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
        # STACKED
        # =================================================

        if should_stack:

            self.main_container.grid_columnconfigure(
                0,
                weight=1,
                minsize=0
            )

            self.main_container.grid_columnconfigure(
                1,
                weight=0,
                minsize=0
            )

            self.calendar_card.grid_configure(
                row=0,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0,
                pady=(0, 14)
            )

            self.schedule_card.grid_configure(
                row=1,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0,
                pady=(0, 8)
            )

        # =================================================
        # SIDE BY SIDE
        # =================================================

        else:

            self.main_container.grid_columnconfigure(
                0,
                weight=1,
                minsize=620
            )

            self.main_container.grid_columnconfigure(
                1,
                weight=0,
                minsize=330
            )

            self.calendar_card.grid_configure(
                row=0,
                column=0,
                columnspan=1,
                sticky="nsew",
                padx=(0, 10),
                pady=0
            )

            self.schedule_card.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                sticky="nsew",
                padx=(10, 0),
                pady=0
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
    # CALENDAR HEADER
    # =================================================

    def create_calendar_header(
        self
    ):

        self.calendar_header = (
            ctk.CTkFrame(
                self.calendar_card,
                fg_color="transparent"
            )
        )

        self.calendar_header.pack(
            fill="x",
            padx=20,
            pady=(20, 12)
        )

        self.calendar_header.grid_columnconfigure(
            1,
            weight=1
        )

        # ---------------------------------------------
        # PREVIOUS
        # ---------------------------------------------

        ctk.CTkButton(
            self.calendar_header,
            text="‹",
            width=42,
            height=38,
            corner_radius=10,
            fg_color=COLORS["surface_soft"],
            hover_color=self.accent,
            text_color=COLORS["text"],
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=20,
                weight="bold"
            ),
            command=self.previous_month
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        # ---------------------------------------------
        # MONTH
        # ---------------------------------------------

        self.month_label = (
            ctk.CTkLabel(
                self.calendar_header,
                text="",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=22,
                    weight="bold"
                ),
                text_color=COLORS["text"]
            )
        )

        self.month_label.grid(
            row=0,
            column=1
        )

        # ---------------------------------------------
        # NEXT
        # ---------------------------------------------

        ctk.CTkButton(
            self.calendar_header,
            text="›",
            width=42,
            height=38,
            corner_radius=10,
            fg_color=COLORS["surface_soft"],
            hover_color=self.accent,
            text_color=COLORS["text"],
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=20,
                weight="bold"
            ),
            command=self.next_month
        ).grid(
            row=0,
            column=2,
            sticky="e"
        )

        # ---------------------------------------------
        # CALENDAR GRID
        # ---------------------------------------------

        self.calendar_grid = (
            ctk.CTkFrame(
                self.calendar_card,
                fg_color="transparent"
            )
        )

        self.calendar_grid.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=(4, 18)
        )

    # =================================================
    # BUILD CALENDAR
    # =================================================

    def build_calendar(
        self
    ):

        # ---------------------------------------------
        # CLEAR
        # ---------------------------------------------

        for widget in (
            self.calendar_grid
            .winfo_children()
        ):

            widget.destroy()

        # ---------------------------------------------
        # TITLE
        # ---------------------------------------------

        month_name = (
            calendar.month_name[
                self.current_month
            ]
        )

        self.month_label.configure(
            text=(
                f"{month_name} "
                f"{self.current_year}"
            )
        )

        # ---------------------------------------------
        # COLUMN SETUP
        # ---------------------------------------------

        for column in range(
            7
        ):

            self.calendar_grid.grid_columnconfigure(
                column,
                weight=1,
                uniform="calendar_columns"
            )

        # ---------------------------------------------
        # DAY HEADERS
        # ---------------------------------------------

        day_names = [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun",
        ]

        for (
            column,
            name
        ) in enumerate(
            day_names
        ):

            ctk.CTkLabel(
                self.calendar_grid,
                text=name,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=11,
                    weight="bold"
                ),
                text_color=COLORS["muted"]
            ).grid(
                row=0,
                column=column,
                sticky="ew",
                padx=3,
                pady=(5, 9)
            )

        # ---------------------------------------------
        # MONTH
        # ---------------------------------------------

        month_data = (
            calendar.monthcalendar(
                self.current_year,
                self.current_month
            )
        )

        today = date.today()

        for (
            row_index,
            week
        ) in enumerate(
            month_data,
            start=1
        ):

            self.calendar_grid.grid_rowconfigure(
                row_index,
                weight=1,
                minsize=74
            )

            for (
                column,
                day_number
            ) in enumerate(
                week
            ):

                # -------------------------------------
                # EMPTY DAY
                # -------------------------------------

                if (
                    day_number
                    == 0
                ):

                    ctk.CTkFrame(
                        self.calendar_grid,
                        fg_color="transparent",
                        height=74
                    ).grid(
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

                activities = (
                    get_planner_activities(
                        current_date.isoformat()
                    )
                )

                is_today = (
                    current_date
                    == today
                )

                is_selected = (
                    current_date
                    == self.selected_date
                )

                # -------------------------------------
                # CELL TEXT
                # -------------------------------------

                text = str(
                    day_number
                )

                if is_today:

                    text += "\nToday"

                elif activities:

                    text += (
                        f"\n{len(activities)} planned"
                    )

                # -------------------------------------
                # CELL COLORS
                # -------------------------------------

                if is_selected:

                    fg_color = (
                        self.accent
                    )

                    hover_color = (
                        self.accent_hover
                    )

                    text_color = (
                        COLORS["white"]
                    )

                    border_width = 0

                elif is_today:

                    fg_color = (
                        COLORS[
                            "surface_soft"
                        ]
                    )

                    hover_color = (
                        COLORS[
                            "surface_hover"
                        ]
                    )

                    text_color = (
                        self.accent
                    )

                    border_width = 2

                else:

                    fg_color = (
                        COLORS[
                            "surface_alt"
                        ]
                    )

                    hover_color = (
                        COLORS[
                            "surface_soft"
                        ]
                    )

                    text_color = (
                        COLORS[
                            "text"
                        ]
                    )

                    border_width = 1

                # -------------------------------------
                # CELL
                # -------------------------------------

                button = (
                    ctk.CTkButton(
                        self.calendar_grid,
                        text=text,
                        height=74,
                        corner_radius=11,
                        fg_color=fg_color,
                        hover_color=hover_color,
                        text_color=text_color,
                        border_width=border_width,
                        border_color=self.accent,
                        font=ctk.CTkFont(
                            family=FONT_BODY,
                            size=11,
                            weight="bold"
                        ),
                        command=(
                            lambda selected=current_date:
                            self.select_date(
                                selected
                            )
                        )
                    )
                )

                button.grid(
                    row=row_index,
                    column=column,
                    sticky="nsew",
                    padx=3,
                    pady=3
                )

        self.after_idle(
            self._refresh_scroll_region
        )

    # =================================================
    # SELECT DATE
    # =================================================

    def select_date(
        self,
        selected_date
    ):

        self.selected_date = (
            selected_date
        )

        self.build_calendar()

        self.load_selected_day()

    # =================================================
    # PREVIOUS MONTH
    # =================================================

    def previous_month(
        self
    ):

        self.current_month -= 1

        if (
            self.current_month
            == 0
        ):

            self.current_month = 12
            self.current_year -= 1

        self.build_calendar()

    # =================================================
    # NEXT MONTH
    # =================================================

    def next_month(
        self
    ):

        self.current_month += 1

        if (
            self.current_month
            == 13
        ):

            self.current_month = 1
            self.current_year += 1

        self.build_calendar()

    # =================================================
    # TODAY
    # =================================================

    def go_to_today(
        self
    ):

        today = date.today()

        self.current_year = today.year
        self.current_month = today.month
        self.selected_date = today

        self.build_calendar()

        self.load_selected_day()

    # =================================================
    # SCHEDULE PANEL
    # =================================================

    def create_schedule_panel(
        self
    ):

        # ---------------------------------------------
        # HEADER WRAPPER
        # ---------------------------------------------

        header = (
            ctk.CTkFrame(
                self.schedule_card,
                fg_color="transparent"
            )
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(20, 4)
        )

        # ---------------------------------------------
        # DATE
        # ---------------------------------------------

        self.selected_date_label = (
            ctk.CTkLabel(
                header,
                text="",
                anchor="w",
                justify="left",
                wraplength=285,
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=20,
                    weight="bold"
                ),
                text_color=COLORS["text"]
            )
        )

        self.selected_date_label.pack(
            anchor="w",
            fill="x"
        )

        # ---------------------------------------------
        # WEEKDAY
        # ---------------------------------------------

        self.selected_day_label = (
            ctk.CTkLabel(
                header,
                text="",
                anchor="w",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12
                ),
                text_color=COLORS["muted"]
            )
        )

        self.selected_day_label.pack(
            anchor="w",
            pady=(4, 0)
        )

        # ---------------------------------------------
        # DIVIDER
        # ---------------------------------------------

        ctk.CTkFrame(
            self.schedule_card,
            height=1,
            fg_color=COLORS["border_soft"]
        ).pack(
            fill="x",
            padx=20,
            pady=14
        )

        # ---------------------------------------------
        # ADD
        # ---------------------------------------------

        self.add_activity_button = (
            ctk.CTkButton(
                self.schedule_card,
                text="+ Add Activity",
                height=40,
                corner_radius=11,
                fg_color=self.accent,
                hover_color=self.accent_hover,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                command=self.open_activity_popup
            )
        )

        self.add_activity_button.pack(
            fill="x",
            padx=20,
            pady=(0, 14)
        )

        # ---------------------------------------------
        # ACTIVITY LIST
        # ---------------------------------------------

        self.activity_container = (
            ctk.CTkFrame(
                self.schedule_card,
                fg_color="transparent"
            )
        )

        self.activity_container.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(0, 16)
        )

    # =================================================
    # LOAD DAY
    # =================================================

    def load_selected_day(
        self
    ):

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

        # ---------------------------------------------
        # CLEAR
        # ---------------------------------------------

        for widget in (
            self.activity_container
            .winfo_children()
        ):

            widget.destroy()

        # ---------------------------------------------
        # LOAD
        # ---------------------------------------------

        activities = (
            get_planner_activities(
                self.selected_date
                .isoformat()
            )
        )

        # ---------------------------------------------
        # EMPTY
        # ---------------------------------------------

        if not activities:

            empty = (
                ctk.CTkFrame(
                    self.activity_container,
                    corner_radius=13,
                    fg_color=COLORS[
                        "surface_alt"
                    ],
                    border_width=1,
                    border_color=COLORS[
                        "border_soft"
                    ]
                )
            )

            empty.pack(
                fill="x",
                pady=5
            )

            ctk.CTkLabel(
                empty,
                text="◇",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=26,
                    weight="bold"
                ),
                text_color=self.accent
            ).pack(
                pady=(20, 5)
            )

            ctk.CTkLabel(
                empty,
                text="Nothing planned",
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
                    "Add an activity for "
                    "this date."
                ),
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=11
                ),
                text_color=COLORS["muted"]
            ).pack(
                pady=(4, 20)
            )

        else:

            for activity in activities:

                self.create_activity_card(
                    activity
                )

        self.after_idle(
            self._refresh_scroll_region
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
            completed,
        ) = activity

        category_color = (
            CATEGORY_COLORS.get(
                category,
                self.accent
            )
        )

        card = (
            ctk.CTkFrame(
                self.activity_container,
                corner_radius=13,
                fg_color=COLORS[
                    "surface_alt"
                ],
                border_width=1,
                border_color=COLORS[
                    "border_soft"
                ]
            )
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
        # COMPLETE
        # ---------------------------------------------

        checkbox = (
            ctk.CTkCheckBox(
                card,
                text="",
                width=24,
                fg_color=category_color,
                hover_color=category_color,
                command=(
                    lambda:
                    self.change_status(
                        activity_id,
                        checkbox.get()
                    )
                )
            )
        )

        checkbox.grid(
            row=0,
            column=0,
            rowspan=3,
            padx=(13, 8),
            pady=14
        )

        if completed:

            checkbox.select()

        # ---------------------------------------------
        # TIME
        # ---------------------------------------------

        time_text = (
            f"{self.format_time(start_time)}"
            f" – "
            f"{self.format_time(end_time)}"
        )

        ctk.CTkLabel(
            card,
            text=time_text,
            anchor="w",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold"
            ),
            text_color=COLORS["muted"]
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(2, 8),
            pady=(12, 2)
        )

        # ---------------------------------------------
        # TITLE
        # ---------------------------------------------

        ctk.CTkLabel(
            card,
            text=title,
            anchor="w",
            justify="left",
            wraplength=205,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=13,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(2, 8),
            pady=2
        )

        # ---------------------------------------------
        # CATEGORY
        # ---------------------------------------------

        category_badge = (
            ctk.CTkFrame(
                card,
                corner_radius=100,
                fg_color=category_color
            )
        )

        category_badge.grid(
            row=2,
            column=1,
            sticky="w",
            padx=(2, 8),
            pady=(5, 12)
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

        # ---------------------------------------------
        # DELETE
        # ---------------------------------------------

        ctk.CTkButton(
            card,
            text="×",
            width=36,
            height=36,
            corner_radius=10,
            fg_color=COLORS["danger"],
            hover_color=COLORS["danger_hover"],
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=15,
                weight="bold"
            ),
            command=(
                lambda:
                self.remove_activity(
                    activity_id
                )
            )
        ).grid(
            row=0,
            column=2,
            rowspan=3,
            padx=(5, 12),
            pady=12
        )

    # =================================================
    # ADD ACTIVITY POPUP
    # =================================================

    def open_activity_popup(
        self
    ):

        popup = (
            ctk.CTkToplevel(
                self
            )
        )

        popup.title(
            "Add Planner Activity"
        )

        popup.geometry(
            "480x525"
        )

        popup.resizable(
            False,
            False
        )

        popup.configure(
            fg_color=COLORS[
                "app_bg"
            ]
        )

        popup.transient(
            self.winfo_toplevel()
        )

        popup.grab_set()

        self.after(
            50,
            lambda:
            self.center_popup(
                popup,
                480,
                525
            )
        )

        container = (
            ctk.CTkFrame(
                popup,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        container.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=18
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        ctk.CTkLabel(
            container,
            text="Add Activity",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=24,
                weight="bold"
            ),
            text_color=self.accent
        ).pack(
            anchor="w",
            padx=22,
            pady=(22, 4)
        )

        ctk.CTkLabel(
            container,
            text=(
                self.selected_date
                .strftime(
                    "%A, %d %B %Y"
                )
            ),
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=12
            ),
            text_color=COLORS["muted"]
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 15)
        )

        # ---------------------------------------------
        # TITLE
        # ---------------------------------------------

        title_entry = (
            ctk.CTkEntry(
                container,
                placeholder_text=(
                    "What are you planning?"
                ),
                height=42
            )
        )

        title_entry.pack(
            fill="x",
            padx=22,
            pady=7
        )

        # ---------------------------------------------
        # CATEGORY
        # ---------------------------------------------

        category_menu = (
            ctk.CTkOptionMenu(
                container,
                values=[
                    "General",
                    "Study",
                    "College",
                    "Personal",
                    "Work",
                    "Fitness",
                    "Other",
                ],
                height=40
            )
        )

        category_menu.set(
            "General"
        )

        category_menu.pack(
            fill="x",
            padx=22,
            pady=7
        )

        # ---------------------------------------------
        # TIME
        # ---------------------------------------------

        ctk.CTkLabel(
            container,
            text="Time",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=13,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).pack(
            anchor="w",
            padx=22,
            pady=(12, 5)
        )

        time_frame = (
            ctk.CTkFrame(
                container,
                fg_color="transparent"
            )
        )

        time_frame.pack(
            fill="x",
            padx=22,
            pady=5
        )

        time_frame.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        time_values = (
            self.generate_times()
        )

        start_menu = (
            ctk.CTkOptionMenu(
                time_frame,
                values=time_values
            )
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

        end_menu = (
            ctk.CTkOptionMenu(
                time_frame,
                values=time_values
            )
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

        # ---------------------------------------------
        # ERROR MESSAGE
        # ---------------------------------------------

        message_label = (
            ctk.CTkLabel(
                container,
                text="",
                text_color=COLORS["danger"],
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=11
                )
            )
        )

        message_label.pack(
            anchor="w",
            padx=22,
            pady=(8, 0)
        )

        # =================================================
        # SAVE
        # =================================================

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

            if (
                end_time
                <= start_time
            ):

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

        # ---------------------------------------------
        # SAVE BUTTON
        # ---------------------------------------------

        ctk.CTkButton(
            container,
            text="Add to Planner",
            height=42,
            corner_radius=11,
            fg_color=self.accent,
            hover_color=self.accent_hover,
            command=save
        ).pack(
            fill="x",
            padx=22,
            pady=(18, 7)
        )

        # ---------------------------------------------
        # CANCEL
        # ---------------------------------------------

        ctk.CTkButton(
            container,
            text="Cancel",
            height=40,
            corner_radius=11,
            fg_color=COLORS["surface_soft"],
            hover_color=COLORS["border"],
            text_color=COLORS["text"],
            command=popup.destroy
        ).pack(
            fill="x",
            padx=22,
            pady=(0, 18)
        )

        title_entry.focus()

    # =================================================
    # POPUP CENTERING
    # =================================================

    def center_popup(
        self,
        popup,
        width,
        height
    ):

        try:

            root = (
                self.winfo_toplevel()
            )

            root.update_idletasks()

            x = (
                root.winfo_rootx()
                + (
                    root.winfo_width()
                    - width
                )
                // 2
            )

            y = (
                root.winfo_rooty()
                + (
                    root.winfo_height()
                    - height
                )
                // 2
            )

            popup.geometry(
                f"{width}x{height}"
                f"+{x}+{y}"
            )

        except Exception:

            pass

    # =================================================
    # TIMES
    # =================================================

    def generate_times(
        self
    ):

        values = []

        for hour in range(
            24
        ):

            for minute in (
                0,
                30
            ):

                values.append(
                    f"{hour:02d}:"
                    f"{minute:02d}"
                )

        return values

    # =================================================
    # FORMAT TIME
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
    # COMPLETE
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

        self.build_calendar()

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