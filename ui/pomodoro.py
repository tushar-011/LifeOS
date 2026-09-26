import customtkinter as ctk

from datetime import datetime

from database.database import (
    add_pomodoro_session,
    get_today_pomodoro_stats,
    get_recent_pomodoro_sessions
)

from ui.theme import (
    COLORS,
    FONT_BODY,
    FONT_DISPLAY,
    module_accent,
    module_accent_hover,
)


# =================================================
# POMODORO PAGE
# =================================================

class PomodoroPage(ctk.CTkScrollableFrame):

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

        # =================================================
        # COLORS
        # =================================================

        self.accent = (
            module_accent(
                "Pomodoro"
            )
        )

        self.accent_hover = (
            module_accent_hover(
                "Pomodoro"
            )
        )

        # =================================================
        # TIMER STATE
        # =================================================

        self.timer_running = False
        self.timer_paused = False

        self.after_id = None

        self.session_type = "Focus"

        self.duration_minutes = 25

        self.remaining_seconds = (
            self.duration_minutes
            * 60
        )

        # =================================================
        # RESPONSIVE STATE
        # =================================================

        self._stacked_layout = None
        self._resize_job = None

        # =================================================
        # BUILD
        # =================================================

        self.create_header()

        self.create_main_layout()

        self.update_timer_display()

        self.load_statistics()

        self.load_history()

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
        # LEFT
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
            text="Pomodoro",
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
                "Focus deeply, then recharge "
                "with a deliberate break."
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
        # STATUS PILL
        # ---------------------------------------------

        self.header_status = (
            ctk.CTkFrame(
                self.header,
                corner_radius=100,
                fg_color=COLORS["surface_soft"]
            )
        )

        self.header_status.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(15, 0)
        )

        self.header_status_dot = (
            ctk.CTkFrame(
                self.header_status,
                width=8,
                height=8,
                corner_radius=100,
                fg_color=COLORS["muted"]
            )
        )

        self.header_status_dot.pack(
            side="left",
            padx=(11, 6),
            pady=9
        )

        self.header_status_label = (
            ctk.CTkLabel(
                self.header_status,
                text="Ready",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                    weight="bold"
                ),
                text_color=COLORS["text"]
            )
        )

        self.header_status_label.pack(
            side="left",
            padx=(0, 11),
            pady=6
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

        self.main_container.grid_columnconfigure(
            0,
            weight=6,
            minsize=520
        )

        self.main_container.grid_columnconfigure(
            1,
            weight=4,
            minsize=360
        )

        self.create_timer_card()

        self.create_side_panel()

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

        if (
            available_width
            <= 1
        ):

            available_width = (
                self.winfo_width()
                - 60
            )

        should_stack = (
            available_width
            < 950
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

            self.timer_card.grid_configure(
                row=0,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0,
                pady=(0, 14)
            )

            self.side_container.grid_configure(
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

            self.main_container.grid_columnconfigure(
                0,
                weight=6,
                minsize=520
            )

            self.main_container.grid_columnconfigure(
                1,
                weight=4,
                minsize=360
            )

            self.timer_card.grid_configure(
                row=0,
                column=0,
                columnspan=1,
                sticky="nsew",
                padx=(0, 10),
                pady=0
            )

            self.side_container.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                sticky="nsew",
                padx=(10, 0)
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
    # TIMER CARD
    # =================================================

    def create_timer_card(
        self
    ):

        self.timer_card = (
            ctk.CTkFrame(
                self.main_container,
                corner_radius=20,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=self.accent
            )
        )

        self.timer_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        self.timer_card.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # SECTION LABEL
        # ---------------------------------------------

        ctk.CTkLabel(
            self.timer_card,
            text="POMODORO TIMER",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold"
            ),
            text_color=self.accent
        ).grid(
            row=0,
            column=0,
            pady=(25, 8)
        )

        # =================================================
        # MODE SELECTOR
        # =================================================

        self.session_menu = (
            ctk.CTkSegmentedButton(
                self.timer_card,
                values=[
                    "Focus",
                    "Short Break",
                    "Long Break"
                ],
                command=self.change_session,
                selected_color=self.accent,
                selected_hover_color=self.accent_hover,
                unselected_color=COLORS["surface_soft"],
                unselected_hover_color=COLORS["border"],
                height=38
            )
        )

        self.session_menu.set(
            "Focus"
        )

        self.session_menu.grid(
            row=1,
            column=0,
            padx=35,
            pady=(3, 20),
            sticky="ew"
        )

        # =================================================
        # TIMER SHELL
        # =================================================

        self.timer_shell = (
            ctk.CTkFrame(
                self.timer_card,
                corner_radius=24,
                fg_color=COLORS["surface_alt"],
                border_width=1,
                border_color=COLORS["border_soft"]
            )
        )

        self.timer_shell.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=38,
            pady=(0, 18)
        )

        self.timer_shell.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # TIMER
        # ---------------------------------------------

        self.timer_label = (
            ctk.CTkLabel(
                self.timer_shell,
                text="25:00",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=76,
                    weight="bold"
                ),
                text_color=self.accent
            )
        )

        self.timer_label.grid(
            row=0,
            column=0,
            pady=(30, 10)
        )

        # ---------------------------------------------
        # PROGRESS
        # ---------------------------------------------

        self.progress_bar = (
            ctk.CTkProgressBar(
                self.timer_shell,
                height=9,
                corner_radius=100,
                fg_color=COLORS["surface_soft"],
                progress_color=self.accent
            )
        )

        self.progress_bar.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=50,
            pady=(0, 13)
        )

        self.progress_bar.set(
            0
        )

        # ---------------------------------------------
        # STATUS
        # ---------------------------------------------

        self.status_label = (
            ctk.CTkLabel(
                self.timer_shell,
                text="Ready to focus.",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12
                ),
                text_color=COLORS["muted"]
            )
        )

        self.status_label.grid(
            row=2,
            column=0,
            pady=(0, 26)
        )

        # =================================================
        # BUTTONS
        # =================================================

        button_frame = (
            ctk.CTkFrame(
                self.timer_card,
                fg_color="transparent"
            )
        )

        button_frame.grid(
            row=3,
            column=0,
            pady=(5, 14)
        )

        self.start_button = (
            ctk.CTkButton(
                button_frame,
                text="Start",
                width=130,
                height=43,
                corner_radius=11,
                fg_color=self.accent,
                hover_color=self.accent_hover,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                command=self.start_timer
            )
        )

        self.start_button.pack(
            side="left",
            padx=5
        )

        self.pause_button = (
            ctk.CTkButton(
                button_frame,
                text="Pause",
                width=115,
                height=43,
                corner_radius=11,
                fg_color=COLORS["amber"],
                hover_color=COLORS["amber_hover"],
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                command=self.pause_timer,
                state="disabled"
            )
        )

        self.pause_button.pack(
            side="left",
            padx=5
        )

        self.reset_button = (
            ctk.CTkButton(
                button_frame,
                text="Reset",
                width=115,
                height=43,
                corner_radius=11,
                fg_color=COLORS["danger"],
                hover_color=COLORS["danger_hover"],
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                command=self.reset_timer
            )
        )

        self.reset_button.pack(
            side="left",
            padx=5
        )

        # =================================================
        # CUSTOM TIMER
        # =================================================

        custom_box = (
            ctk.CTkFrame(
                self.timer_card,
                corner_radius=14,
                fg_color=COLORS["surface_alt"],
                border_width=1,
                border_color=COLORS["border_soft"]
            )
        )

        custom_box.grid(
            row=4,
            column=0,
            padx=38,
            pady=(7, 28),
            sticky="ew"
        )

        custom_box.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            custom_box,
            text="Custom duration",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold"
            ),
            text_color=COLORS["muted"]
        ).grid(
            row=0,
            column=0,
            padx=(16, 10),
            pady=14
        )

        self.custom_entry = (
            ctk.CTkEntry(
                custom_box,
                placeholder_text="Minutes",
                height=37
            )
        )

        self.custom_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5,
            pady=10
        )

        self.custom_button = (
            ctk.CTkButton(
                custom_box,
                text="Set Custom",
                width=105,
                height=37,
                corner_radius=10,
                fg_color=self.accent,
                hover_color=self.accent_hover,
                command=self.set_custom_duration
            )
        )

        self.custom_button.grid(
            row=0,
            column=2,
            padx=(5, 12),
            pady=10
        )

    # =================================================
    # SIDE PANEL
    # =================================================

    def create_side_panel(
        self
    ):

        self.side_container = (
            ctk.CTkFrame(
                self.main_container,
                fg_color="transparent"
            )
        )

        self.side_container.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        self.side_container.grid_columnconfigure(
            0,
            weight=1
        )

        self.create_statistics()

        self.create_history()

    # =================================================
    # STATISTICS
    # =================================================

    def create_statistics(
        self
    ):

        stats_frame = (
            ctk.CTkFrame(
                self.side_container,
                fg_color="transparent"
            )
        )

        stats_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        stats_frame.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        # ---------------------------------------------
        # SESSIONS
        # ---------------------------------------------

        sessions_card = (
            ctk.CTkFrame(
                stats_frame,
                corner_radius=16,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        sessions_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 6)
        )

        ctk.CTkLabel(
            sessions_card,
            text="Focus Sessions",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold"
            ),
            text_color=COLORS["muted"]
        ).pack(
            anchor="w",
            padx=16,
            pady=(15, 4)
        )

        self.session_count_label = (
            ctk.CTkLabel(
                sessions_card,
                text="0",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=28,
                    weight="bold"
                ),
                text_color=self.accent
            )
        )

        self.session_count_label.pack(
            anchor="w",
            padx=16,
            pady=(0, 15)
        )

        # ---------------------------------------------
        # FOCUS TIME
        # ---------------------------------------------

        time_card = (
            ctk.CTkFrame(
                stats_frame,
                corner_radius=16,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        time_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(6, 0)
        )

        ctk.CTkLabel(
            time_card,
            text="Focus Time",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold"
            ),
            text_color=COLORS["muted"]
        ).pack(
            anchor="w",
            padx=16,
            pady=(15, 4)
        )

        self.focus_time_label = (
            ctk.CTkLabel(
                time_card,
                text="0m",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=26,
                    weight="bold"
                ),
                text_color=COLORS["amber"]
            )
        )

        self.focus_time_label.pack(
            anchor="w",
            padx=16,
            pady=(0, 15)
        )

    # =================================================
    # LOAD STATISTICS
    # =================================================

    def load_statistics(
        self
    ):

        stats = (
            get_today_pomodoro_stats()
        )

        self.session_count_label.configure(
            text=str(
                stats["sessions"]
            )
        )

        self.focus_time_label.configure(
            text=self.format_minutes(
                stats["focus_minutes"]
            )
        )

    # =================================================
    # HISTORY
    # =================================================

    def create_history(
        self
    ):

        self.history_card = (
            ctk.CTkFrame(
                self.side_container,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        self.history_card.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.side_container.grid_rowconfigure(
            1,
            weight=1
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        history_header = (
            ctk.CTkFrame(
                self.history_card,
                fg_color="transparent"
            )
        )

        history_header.pack(
            fill="x",
            padx=18,
            pady=(18, 10)
        )

        ctk.CTkLabel(
            history_header,
            text="Recent Sessions",
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
            history_header,
            text="Your latest Pomodoro activity",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11
            ),
            text_color=COLORS["muted"]
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # ---------------------------------------------
        # CONTAINER
        # ---------------------------------------------

        self.history_container = (
            ctk.CTkFrame(
                self.history_card,
                fg_color="transparent"
            )
        )

        self.history_container.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(0, 14)
        )

    # =================================================
    # LOAD HISTORY
    # =================================================

    def load_history(
        self
    ):

        for widget in (
            self.history_container
            .winfo_children()
        ):

            widget.destroy()

        sessions = (
            get_recent_pomodoro_sessions()
        )

        if not sessions:

            empty = (
                ctk.CTkFrame(
                    self.history_container,
                    corner_radius=12,
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
                text="◷",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=25,
                    weight="bold"
                ),
                text_color=self.accent
            ).pack(
                pady=(20, 5)
            )

            ctk.CTkLabel(
                empty,
                text="No Pomodoro sessions yet",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                text_color=COLORS["text"]
            ).pack()

            ctk.CTkLabel(
                empty,
                text=(
                    "Completed Focus sessions "
                    "will appear here."
                ),
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10
                ),
                text_color=COLORS["muted"]
            ).pack(
                pady=(3, 20)
            )

            return

        for session in sessions:

            (
                session_id,
                session_type,
                duration,
                completed_at
            ) = session

            # -----------------------------------------
            # DATE
            # -----------------------------------------

            try:

                parsed = (
                    datetime.strptime(
                        completed_at,
                        "%Y-%m-%d %H:%M:%S"
                    )
                )

                formatted = (
                    parsed.strftime(
                        "%d %b • %I:%M %p"
                    )
                )

            except ValueError:

                formatted = (
                    completed_at
                )

            # -----------------------------------------
            # ROW
            # -----------------------------------------

            row = (
                ctk.CTkFrame(
                    self.history_container,
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
                0,
                weight=1
            )

            # -----------------------------------------
            # SESSION TYPE
            # -----------------------------------------

            ctk.CTkLabel(
                row,
                text=session_type,
                anchor="w",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                text_color=COLORS["text"]
            ).grid(
                row=0,
                column=0,
                sticky="ew",
                padx=(13, 8),
                pady=(11, 2)
            )

            # -----------------------------------------
            # DURATION
            # -----------------------------------------

            ctk.CTkLabel(
                row,
                text=f"{duration} minutes",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10
                ),
                text_color=COLORS["muted"]
            ).grid(
                row=1,
                column=0,
                sticky="w",
                padx=(13, 8),
                pady=(2, 11)
            )

            # -----------------------------------------
            # DATE
            # -----------------------------------------

            ctk.CTkLabel(
                row,
                text=formatted,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10
                ),
                text_color=COLORS["muted"]
            ).grid(
                row=0,
                column=1,
                rowspan=2,
                sticky="e",
                padx=(8, 13),
                pady=10
            )

        self.after_idle(
            self._refresh_scroll_region
        )

    # =================================================
    # SESSION TYPE
    # =================================================

    def change_session(
        self,
        value
    ):

        if (
            self.timer_running
            or self.timer_paused
        ):

            return

        self.session_type = value

        durations = {
            "Focus": 25,
            "Short Break": 5,
            "Long Break": 15
        }

        self.duration_minutes = (
            durations[
                value
            ]
        )

        self.remaining_seconds = (
            self.duration_minutes
            * 60
        )

        self.progress_bar.set(
            0
        )

        self.update_timer_display()

        if value == "Focus":

            self.status_label.configure(
                text="Ready to focus."
            )

        elif value == "Short Break":

            self.status_label.configure(
                text="Take a short break."
            )

        else:

            self.status_label.configure(
                text="Take a longer break."
            )

        self.set_header_status(
            "Ready",
            COLORS["muted"]
        )

    # =================================================
    # CUSTOM DURATION
    # =================================================

    def set_custom_duration(
        self
    ):

        if (
            self.timer_running
            or self.timer_paused
        ):

            self.status_label.configure(
                text=(
                    "Reset the timer before "
                    "changing duration."
                )
            )

            return

        try:

            minutes = int(
                self.custom_entry
                .get()
                .strip()
            )

            if (
                minutes <= 0
            ):

                raise ValueError

            if (
                minutes > 180
            ):

                self.status_label.configure(
                    text=(
                        "Maximum custom duration "
                        "is 180 minutes."
                    )
                )

                return

            self.duration_minutes = minutes

            self.remaining_seconds = (
                minutes
                * 60
            )

            self.progress_bar.set(
                0
            )

            self.update_timer_display()

            self.status_label.configure(
                text=(
                    f"Custom timer set to "
                    f"{minutes} minutes."
                )
            )

        except ValueError:

            self.status_label.configure(
                text=(
                    "Enter a valid number "
                    "of minutes."
                )
            )

    # =================================================
    # START TIMER
    # =================================================

    def start_timer(
        self
    ):

        # ---------------------------------------------
        # RESUME
        # ---------------------------------------------

        if self.timer_paused:

            self.timer_paused = False
            self.timer_running = True

            self.start_button.configure(
                text="Start",
                state="disabled"
            )

            self.pause_button.configure(
                state="normal"
            )

            self.status_label.configure(
                text="Timer resumed."
            )

            self.set_header_status(
                "Running",
                self.accent
            )

            self.tick()

            return

        # ---------------------------------------------
        # ALREADY RUNNING
        # ---------------------------------------------

        if self.timer_running:

            return

        # ---------------------------------------------
        # START NEW
        # ---------------------------------------------

        self.timer_running = True
        self.timer_paused = False

        self.start_button.configure(
            text="Start",
            state="disabled"
        )

        self.pause_button.configure(
            state="normal"
        )

        self.session_menu.configure(
            state="disabled"
        )

        self.custom_entry.configure(
            state="disabled"
        )

        self.custom_button.configure(
            state="disabled"
        )

        if (
            self.session_type
            == "Focus"
        ):

            text = (
                "Focus session running."
            )

        else:

            text = (
                "Break timer running."
            )

        self.status_label.configure(
            text=text
        )

        self.set_header_status(
            "Running",
            self.accent
        )

        self.tick()

    # =================================================
    # TIMER LOOP
    # =================================================

    def tick(
        self
    ):

        if (
            not self.timer_running
            or self.timer_paused
        ):

            return

        self.update_timer_display()

        if (
            self.remaining_seconds
            <= 0
        ):

            self.complete_session()

            return

        self.remaining_seconds -= 1

        self.after_id = (
            self.after(
                1000,
                self.tick
            )
        )

    # =================================================
    # PAUSE
    # =================================================

    def pause_timer(
        self
    ):

        if (
            not self.timer_running
            or self.timer_paused
        ):

            return

        self.timer_running = False
        self.timer_paused = True

        if self.after_id:

            try:

                self.after_cancel(
                    self.after_id
                )

            except Exception:

                pass

            self.after_id = None

        self.start_button.configure(
            text="Resume",
            state="normal"
        )

        self.pause_button.configure(
            state="disabled"
        )

        self.status_label.configure(
            text="Timer paused."
        )

        self.set_header_status(
            "Paused",
            COLORS["amber"]
        )

    # =================================================
    # RESET
    # =================================================

    def reset_timer(
        self
    ):

        if self.after_id:

            try:

                self.after_cancel(
                    self.after_id
                )

            except Exception:

                pass

            self.after_id = None

        self.timer_running = False
        self.timer_paused = False

        self.remaining_seconds = (
            self.duration_minutes
            * 60
        )

        self.start_button.configure(
            text="Start",
            state="normal"
        )

        self.pause_button.configure(
            state="disabled"
        )

        self.session_menu.configure(
            state="normal"
        )

        self.custom_entry.configure(
            state="normal"
        )

        self.custom_button.configure(
            state="normal"
        )

        self.status_label.configure(
            text="Timer reset."
        )

        self.set_header_status(
            "Ready",
            COLORS["muted"]
        )

        self.progress_bar.set(
            0
        )

        self.update_timer_display()

    # =================================================
    # COMPLETE SESSION
    # =================================================

    def complete_session(
        self
    ):

        self.timer_running = False
        self.timer_paused = False

        self.after_id = None

        # ---------------------------------------------
        # DATABASE
        # ---------------------------------------------

        add_pomodoro_session(
            self.session_type,
            self.duration_minutes
        )

        # ---------------------------------------------
        # CONTROLS
        # ---------------------------------------------

        self.start_button.configure(
            text="Start",
            state="normal"
        )

        self.pause_button.configure(
            state="disabled"
        )

        self.session_menu.configure(
            state="normal"
        )

        self.custom_entry.configure(
            state="normal"
        )

        self.custom_button.configure(
            state="normal"
        )

        self.status_label.configure(
            text=(
                f"{self.session_type} "
                f"session completed!"
            )
        )

        self.set_header_status(
            "Completed",
            COLORS["emerald"]
        )

        self.progress_bar.set(
            1
        )

        try:

            self.bell()

        except Exception:

            pass

        self.load_statistics()

        self.load_history()

        # ---------------------------------------------
        # RESET TIMER DISPLAY AFTER SHORT DELAY
        # ---------------------------------------------

        self.remaining_seconds = (
            self.duration_minutes
            * 60
        )

        self.after(
            800,
            self._reset_after_completion
        )

    # =================================================
    # RESET AFTER COMPLETION
    # =================================================

    def _reset_after_completion(
        self
    ):

        if not self.timer_running:

            self.progress_bar.set(
                0
            )

            self.update_timer_display()

    # =================================================
    # TIMER DISPLAY
    # =================================================

    def update_timer_display(
        self
    ):

        minutes = (
            self.remaining_seconds
            // 60
        )

        seconds = (
            self.remaining_seconds
            % 60
        )

        self.timer_label.configure(
            text=(
                f"{minutes:02d}:"
                f"{seconds:02d}"
            )
        )

        total_seconds = max(
            1,
            self.duration_minutes
            * 60
        )

        elapsed_seconds = (
            total_seconds
            - self.remaining_seconds
        )

        progress = (
            elapsed_seconds
            / total_seconds
        )

        progress = max(
            0,
            min(
                1,
                progress
            )
        )

        self.progress_bar.set(
            progress
        )

    # =================================================
    # HEADER STATUS
    # =================================================

    def set_header_status(
        self,
        text,
        color
    ):

        self.header_status_label.configure(
            text=text
        )

        self.header_status_dot.configure(
            fg_color=color
        )

    # =================================================
    # FORMAT MINUTES
    # =================================================

    def format_minutes(
        self,
        minutes
    ):

        minutes = int(
            minutes
        )

        if (
            minutes < 60
        ):

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

        if (
            remaining
            == 0
        ):

            return (
                f"{hours}h"
            )

        return (
            f"{hours}h "
            f"{remaining}m"
        )