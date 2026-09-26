import customtkinter as ctk

from datetime import datetime

from database.database import (
    add_pomodoro_session,
    get_today_pomodoro_stats,
    get_recent_pomodoro_sessions
)


class PomodoroPage(ctk.CTkScrollableFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            corner_radius=0
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.timer_running = False
        self.timer_paused = False

        self.after_id = None

        self.session_type = "Focus"

        self.duration_minutes = 25
        self.remaining_seconds = 25 * 60

        self.create_header()
        self.create_timer_card()
        self.create_statistics()
        self.create_history()

        self.update_timer_display()
        self.load_statistics()
        self.load_history()

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

        ctk.CTkLabel(
            header,
            text="Pomodoro",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            header,
            text=(
                "Focus deeply, then take "
                "a short break."
            )
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

    # =================================================
    # TIMER CARD
    # =================================================

    def create_timer_card(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        # Session type
        self.session_menu = ctk.CTkOptionMenu(
            card,
            width=180,
            values=[
                "Focus",
                "Short Break",
                "Long Break"
            ],
            command=self.change_session
        )

        self.session_menu.set(
            "Focus"
        )

        self.session_menu.pack(
            pady=(25, 15)
        )

        # Timer
        self.timer_label = ctk.CTkLabel(
            card,
            text="25:00",
            font=ctk.CTkFont(
                size=70,
                weight="bold"
            )
        )

        self.timer_label.pack(
            pady=15
        )

        self.status_label = ctk.CTkLabel(
            card,
            text="Ready to focus"
        )

        self.status_label.pack(
            pady=(0, 15)
        )

        # Buttons
        button_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=10
        )

        self.start_button = ctk.CTkButton(
            button_frame,
            text="Start",
            width=110,
            height=42,
            command=self.start_timer
        )

        self.start_button.pack(
            side="left",
            padx=5
        )

        self.pause_button = ctk.CTkButton(
            button_frame,
            text="Pause",
            width=110,
            height=42,
            command=self.pause_timer,
            state="disabled"
        )

        self.pause_button.pack(
            side="left",
            padx=5
        )

        self.reset_button = ctk.CTkButton(
            button_frame,
            text="Reset",
            width=110,
            height=42,
            command=self.reset_timer
        )

        self.reset_button.pack(
            side="left",
            padx=5
        )

        # Custom duration
        custom_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        custom_frame.pack(
            pady=(15, 25)
        )

        self.custom_entry = ctk.CTkEntry(
            custom_frame,
            width=130,
            placeholder_text="Minutes"
        )

        self.custom_entry.pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            custom_frame,
            text="Set Custom",
            width=100,
            command=self.set_custom_duration
        ).pack(
            side="left",
            padx=5
        )

    # =================================================
    # SESSION TYPE
    # =================================================

    def change_session(
        self,
        value
    ):

        if self.timer_running:
            return

        self.session_type = value

        durations = {
            "Focus": 25,
            "Short Break": 5,
            "Long Break": 15
        }

        self.duration_minutes = (
            durations[value]
        )

        self.remaining_seconds = (
            self.duration_minutes
            * 60
        )

        self.update_timer_display()

        if value == "Focus":

            self.status_label.configure(
                text="Ready to focus"
            )

        else:

            self.status_label.configure(
                text="Break time"
            )

    # =================================================
    # CUSTOM
    # =================================================

    def set_custom_duration(self):

        if self.timer_running:
            return

        try:

            minutes = int(
                self.custom_entry
                .get()
                .strip()
            )

            if minutes <= 0:
                raise ValueError

            if minutes > 180:

                self.status_label.configure(
                    text=(
                        "Maximum custom "
                        "duration is 180 minutes."
                    )
                )

                return

            self.duration_minutes = minutes

            self.remaining_seconds = (
                minutes * 60
            )

            self.update_timer_display()

            self.status_label.configure(
                text=(
                    f"Custom timer: "
                    f"{minutes} minutes"
                )
            )

        except ValueError:

            self.status_label.configure(
                text="Enter a valid number of minutes."
            )

    # =================================================
    # START
    # =================================================

    def start_timer(self):

        if self.timer_running:

            if self.timer_paused:

                self.timer_paused = False

                self.status_label.configure(
                    text="Timer resumed"
                )

                self.start_button.configure(
                    text="Start",
                    state="disabled"
                )

                self.pause_button.configure(
                    state="normal"
                )

                self.tick()

            return

        self.timer_running = True
        self.timer_paused = False

        self.start_button.configure(
            state="disabled"
        )

        self.pause_button.configure(
            state="normal"
        )

        self.session_menu.configure(
            state="disabled"
        )

        self.status_label.configure(
            text=(
                "Focus session running"
                if self.session_type == "Focus"
                else "Break running"
            )
        )

        self.tick()

    # =================================================
    # TICK
    # =================================================

    def tick(self):

        if (
            not self.timer_running
            or self.timer_paused
        ):
            return

        self.update_timer_display()

        if self.remaining_seconds <= 0:

            self.complete_session()
            return

        self.remaining_seconds -= 1

        self.after_id = self.after(
            1000,
            self.tick
        )

    # =================================================
    # PAUSE
    # =================================================

    def pause_timer(self):

        if not self.timer_running:
            return

        if self.timer_paused:
            return

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
            text="Timer paused"
        )

    # =================================================
    # RESET
    # =================================================

    def reset_timer(self):

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

        self.status_label.configure(
            text="Timer reset"
        )

        self.update_timer_display()

    # =================================================
    # COMPLETE
    # =================================================

    def complete_session(self):

        self.timer_running = False
        self.timer_paused = False
        self.after_id = None

        add_pomodoro_session(
            self.session_type,
            self.duration_minutes
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

        self.status_label.configure(
            text=(
                f"{self.session_type} "
                f"session completed!"
            )
        )

        try:
            self.bell()
        except Exception:
            pass

        self.load_statistics()
        self.load_history()

        self.remaining_seconds = (
            self.duration_minutes
            * 60
        )

        self.update_timer_display()

    # =================================================
    # DISPLAY
    # =================================================

    def update_timer_display(self):

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

    # =================================================
    # STATISTICS
    # =================================================

    def create_statistics(self):

        stats_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        stats_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        stats_frame.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        sessions_card = ctk.CTkFrame(
            stats_frame,
            corner_radius=15
        )

        sessions_card.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 7)
        )

        ctk.CTkLabel(
            sessions_card,
            text="Focus Sessions Today",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 3)
        )

        self.session_count_label = (
            ctk.CTkLabel(
                sessions_card,
                text="0",
                font=ctk.CTkFont(
                    size=28,
                    weight="bold"
                )
            )
        )

        self.session_count_label.pack(
            anchor="w",
            padx=18,
            pady=(0, 15)
        )

        time_card = ctk.CTkFrame(
            stats_frame,
            corner_radius=15
        )

        time_card.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(7, 0)
        )

        ctk.CTkLabel(
            time_card,
            text="Focus Time Today",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 3)
        )

        self.focus_time_label = (
            ctk.CTkLabel(
                time_card,
                text="0m",
                font=ctk.CTkFont(
                    size=28,
                    weight="bold"
                )
            )
        )

        self.focus_time_label.pack(
            anchor="w",
            padx=18,
            pady=(0, 15)
        )

    def load_statistics(self):

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

    def create_history(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=25,
            pady=(10, 25)
        )

        ctk.CTkLabel(
            card,
            text="Recent Sessions",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        self.history_container = (
            ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
        )

        self.history_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

    def load_history(self):

        for widget in (
            self.history_container
            .winfo_children()
        ):

            widget.destroy()

        sessions = (
            get_recent_pomodoro_sessions()
        )

        if not sessions:

            ctk.CTkLabel(
                self.history_container,
                text="No Pomodoro sessions yet."
            ).pack(
                pady=25
            )

            return

        for session in sessions:

            (
                session_id,
                session_type,
                duration,
                completed_at
            ) = session

            try:

                parsed = datetime.strptime(
                    completed_at,
                    "%Y-%m-%d %H:%M:%S"
                )

                formatted = parsed.strftime(
                    "%d %b %Y • %I:%M %p"
                )

            except ValueError:

                formatted = completed_at

            row = ctk.CTkFrame(
                self.history_container,
                corner_radius=10
            )

            row.pack(
                fill="x",
                pady=4
            )

            ctk.CTkLabel(
                row,
                text=session_type,
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                )
            ).pack(
                side="left",
                padx=15,
                pady=12
            )

            ctk.CTkLabel(
                row,
                text=(
                    f"{duration} min"
                )
            ).pack(
                side="left",
                padx=10
            )

            ctk.CTkLabel(
                row,
                text=formatted,
                font=ctk.CTkFont(
                    size=11
                )
            ).pack(
                side="right",
                padx=15
            )

    # =================================================
    # MINUTES FORMAT
    # =================================================

    def format_minutes(
        self,
        minutes
    ):

        if minutes < 60:

            return f"{minutes}m"

        hours = minutes // 60
        remaining = minutes % 60

        if remaining == 0:

            return f"{hours}h"

        return (
            f"{hours}h {remaining}m"
        )