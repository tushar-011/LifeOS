import customtkinter as ctk

import time

from datetime import datetime

from database.database import (
    add_stopwatch_session,
    get_today_stopwatch_stats,
    get_recent_stopwatch_sessions
)


class StopwatchPage(
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
            0,
            weight=1
        )

        # Timer state
        self.running = False
        self.paused = False

        self.start_mark = None
        self.saved_elapsed = 0.0

        self.after_id = None

        # Lap information
        self.laps = []
        self.last_lap_time = 0.0

        self.create_header()
        self.create_stopwatch_card()
        self.create_statistics()
        self.create_laps_section()
        self.create_history()

        self.update_display()
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
            text="Stopwatch",
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
                "Track open-ended work "
                "and record laps."
            )
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

    # =================================================
    # STOPWATCH CARD
    # =================================================

    def create_stopwatch_card(self):

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

        self.timer_label = (
            ctk.CTkLabel(
                card,
                text="00:00:00.0",
                font=ctk.CTkFont(
                    size=60,
                    weight="bold"
                )
            )
        )

        self.timer_label.pack(
            pady=(35, 10)
        )

        self.status_label = (
            ctk.CTkLabel(
                card,
                text="Ready"
            )
        )

        self.status_label.pack(
            pady=(0, 15)
        )

        # -------------------------------------------------
        # PRIMARY BUTTONS
        # -------------------------------------------------

        button_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=10
        )

        self.start_button = (
            ctk.CTkButton(
                button_frame,
                text="Start",
                width=110,
                height=42,
                command=self.start_stopwatch
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
                width=110,
                height=42,
                command=self.pause_stopwatch,
                state="disabled"
            )
        )

        self.pause_button.pack(
            side="left",
            padx=5
        )

        self.lap_button = (
            ctk.CTkButton(
                button_frame,
                text="Lap",
                width=110,
                height=42,
                command=self.record_lap,
                state="disabled"
            )
        )

        self.lap_button.pack(
            side="left",
            padx=5
        )

        # -------------------------------------------------
        # SECONDARY BUTTONS
        # -------------------------------------------------

        secondary_frame = (
            ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
        )

        secondary_frame.pack(
            pady=(5, 30)
        )

        self.reset_button = (
            ctk.CTkButton(
                secondary_frame,
                text="Reset",
                width=120,
                command=self.reset_stopwatch
            )
        )

        self.reset_button.pack(
            side="left",
            padx=5
        )

        self.save_button = (
            ctk.CTkButton(
                secondary_frame,
                text="Save Session",
                width=140,
                command=self.save_session
            )
        )

        self.save_button.pack(
            side="left",
            padx=5
        )

    # =================================================
    # GET CURRENT ELAPSED TIME
    # =================================================

    def get_elapsed(self):

        if (
            self.running
            and self.start_mark is not None
        ):

            return (
                self.saved_elapsed
                + (
                    time.perf_counter()
                    - self.start_mark
                )
            )

        return self.saved_elapsed

    # =================================================
    # START / RESUME
    # =================================================

    def start_stopwatch(self):

        if self.running:
            return

        self.start_mark = (
            time.perf_counter()
        )

        self.running = True
        self.paused = False

        self.start_button.configure(
            text="Start",
            state="disabled"
        )

        self.pause_button.configure(
            state="normal"
        )

        self.lap_button.configure(
            state="normal"
        )

        self.status_label.configure(
            text="Running"
        )

        self.tick()

    # =================================================
    # TIMER LOOP
    # =================================================

    def tick(self):

        if not self.running:
            return

        self.update_display()

        self.after_id = self.after(
            100,
            self.tick
        )

    # =================================================
    # PAUSE
    # =================================================

    def pause_stopwatch(self):

        if not self.running:
            return

        self.saved_elapsed = (
            self.get_elapsed()
        )

        self.running = False
        self.paused = True
        self.start_mark = None

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

        self.lap_button.configure(
            state="disabled"
        )

        self.status_label.configure(
            text="Paused"
        )

        self.update_display()

    # =================================================
    # RESET
    # =================================================

    def reset_stopwatch(self):

        if self.after_id:

            try:

                self.after_cancel(
                    self.after_id
                )

            except Exception:
                pass

            self.after_id = None

        self.running = False
        self.paused = False

        self.start_mark = None
        self.saved_elapsed = 0.0

        self.laps = []
        self.last_lap_time = 0.0

        self.start_button.configure(
            text="Start",
            state="normal"
        )

        self.pause_button.configure(
            state="disabled"
        )

        self.lap_button.configure(
            state="disabled"
        )

        self.status_label.configure(
            text="Ready"
        )

        self.update_display()
        self.load_laps()

    # =================================================
    # LAP
    # =================================================

    def record_lap(self):

        if not self.running:
            return

        total_elapsed = (
            self.get_elapsed()
        )

        lap_duration = (
            total_elapsed
            - self.last_lap_time
        )

        self.last_lap_time = (
            total_elapsed
        )

        self.laps.append(
            {
                "number": len(self.laps) + 1,
                "lap_time": lap_duration,
                "total_time": total_elapsed
            }
        )

        self.load_laps()

    # =================================================
    # SAVE SESSION
    # =================================================

    def save_session(self):

        elapsed = (
            self.get_elapsed()
        )

        if elapsed < 1:

            self.status_label.configure(
                text=(
                    "Run the stopwatch "
                    "before saving."
                )
            )

            return

        # Pause current run before saving
        if self.running:

            self.saved_elapsed = elapsed

            self.running = False
            self.start_mark = None

            if self.after_id:

                try:

                    self.after_cancel(
                        self.after_id
                    )

                except Exception:
                    pass

                self.after_id = None

        duration_seconds = int(
            round(elapsed)
        )

        add_stopwatch_session(
            duration_seconds,
            len(self.laps)
        )

        self.status_label.configure(
            text="Session saved."
        )

        self.load_statistics()
        self.load_history()

        # Start fresh after saving
        self.saved_elapsed = 0.0
        self.paused = False

        self.laps = []
        self.last_lap_time = 0.0

        self.start_button.configure(
            text="Start",
            state="normal"
        )

        self.pause_button.configure(
            state="disabled"
        )

        self.lap_button.configure(
            state="disabled"
        )

        self.update_display()
        self.load_laps()

    # =================================================
    # TIMER DISPLAY
    # =================================================

    def update_display(self):

        elapsed = (
            self.get_elapsed()
        )

        hours = int(
            elapsed // 3600
        )

        minutes = int(
            (
                elapsed % 3600
            )
            // 60
        )

        seconds = int(
            elapsed % 60
        )

        tenths = int(
            (
                elapsed
                - int(elapsed)
            )
            * 10
        )

        self.timer_label.configure(
            text=(
                f"{hours:02d}:"
                f"{minutes:02d}:"
                f"{seconds:02d}."
                f"{tenths}"
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

        # Sessions
        session_card = ctk.CTkFrame(
            stats_frame,
            corner_radius=15
        )

        session_card.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 7)
        )

        ctk.CTkLabel(
            session_card,
            text="Sessions Today",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 3)
        )

        self.sessions_value = (
            ctk.CTkLabel(
                session_card,
                text="0",
                font=ctk.CTkFont(
                    size=28,
                    weight="bold"
                )
            )
        )

        self.sessions_value.pack(
            anchor="w",
            padx=18,
            pady=(0, 15)
        )

        # Total time
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
            text="Stopwatch Time Today",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 3)
        )

        self.total_time_value = (
            ctk.CTkLabel(
                time_card,
                text="0m",
                font=ctk.CTkFont(
                    size=28,
                    weight="bold"
                )
            )
        )

        self.total_time_value.pack(
            anchor="w",
            padx=18,
            pady=(0, 15)
        )

    def load_statistics(self):

        stats = (
            get_today_stopwatch_stats()
        )

        self.sessions_value.configure(
            text=str(
                stats["sessions"]
            )
        )

        self.total_time_value.configure(
            text=self.format_duration(
                stats[
                    "total_seconds"
                ]
            )
        )

    # =================================================
    # LAPS SECTION
    # =================================================

    def create_laps_section(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        ctk.CTkLabel(
            card,
            text="Laps",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        self.lap_container = (
            ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
        )

        self.lap_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.load_laps()

    def load_laps(self):

        for widget in (
            self.lap_container
            .winfo_children()
        ):

            widget.destroy()

        if not self.laps:

            ctk.CTkLabel(
                self.lap_container,
                text="No laps recorded."
            ).pack(
                pady=20
            )

            return

        # Newest lap first
        for lap in reversed(
            self.laps
        ):

            row = ctk.CTkFrame(
                self.lap_container,
                corner_radius=10
            )

            row.pack(
                fill="x",
                pady=4
            )

            ctk.CTkLabel(
                row,
                text=(
                    f"Lap {lap['number']}"
                ),
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
                    "Lap: "
                    f"{self.format_precise_time(lap['lap_time'])}"
                )
            ).pack(
                side="left",
                padx=15
            )

            ctk.CTkLabel(
                row,
                text=(
                    "Total: "
                    f"{self.format_precise_time(lap['total_time'])}"
                )
            ).pack(
                side="right",
                padx=15
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
            row=4,
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
            get_recent_stopwatch_sessions()
        )

        if not sessions:

            ctk.CTkLabel(
                self.history_container,
                text=(
                    "No saved stopwatch "
                    "sessions yet."
                )
            ).pack(
                pady=25
            )

            return

        for session in sessions:

            (
                session_id,
                duration_seconds,
                lap_count,
                completed_at
            ) = session

            try:

                parsed = datetime.strptime(
                    completed_at,
                    "%Y-%m-%d %H:%M:%S"
                )

                formatted_date = (
                    parsed.strftime(
                        "%d %b %Y • "
                        "%I:%M %p"
                    )
                )

            except ValueError:

                formatted_date = (
                    completed_at
                )

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
                text=self.format_duration(
                    duration_seconds
                ),
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
                    f"{lap_count} laps"
                )
            ).pack(
                side="left",
                padx=10
            )

            ctk.CTkLabel(
                row,
                text=formatted_date,
                font=ctk.CTkFont(
                    size=11
                )
            ).pack(
                side="right",
                padx=15
            )

    # =================================================
    # FORMAT HELPERS
    # =================================================

    def format_precise_time(
        self,
        seconds_value
    ):

        minutes = int(
            seconds_value // 60
        )

        seconds = int(
            seconds_value % 60
        )

        tenths = int(
            (
                seconds_value
                - int(seconds_value)
            )
            * 10
        )

        return (
            f"{minutes:02d}:"
            f"{seconds:02d}."
            f"{tenths}"
        )

    def format_duration(
        self,
        seconds_value
    ):

        seconds_value = int(
            seconds_value
        )

        hours = (
            seconds_value
            // 3600
        )

        minutes = (
            (
                seconds_value
                % 3600
            )
            // 60
        )

        seconds = (
            seconds_value
            % 60
        )

        if hours:

            return (
                f"{hours}h "
                f"{minutes}m "
                f"{seconds}s"
            )

        if minutes:

            return (
                f"{minutes}m "
                f"{seconds}s"
            )

        return f"{seconds}s"