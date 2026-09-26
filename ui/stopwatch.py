import time
from datetime import datetime

import customtkinter as ctk

from database.database import (
    add_stopwatch_session,
    get_today_stopwatch_stats,
    get_recent_stopwatch_sessions,
)

from ui.theme import (
    COLORS,
    FONT_BODY,
    FONT_DISPLAY,
    module_accent,
    module_accent_hover,
)


class StopwatchPage(ctk.CTkScrollableFrame):

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
                "Stopwatch"
            )
        )

        self.accent_hover = (
            module_accent_hover(
                "Stopwatch"
            )
        )

        # =================================================
        # STOPWATCH STATE
        # =================================================

        self.running = False
        self.paused = False

        self.start_mark = None
        self.saved_elapsed = 0.0

        self.after_id = None

        # =================================================
        # LAPS
        # =================================================

        self.laps = []
        self.last_lap_time = 0.0

        # =================================================
        # RESPONSIVE
        # =================================================

        self._stacked_layout = None
        self._resize_job = None

        # =================================================
        # BUILD
        # =================================================

        self.create_header()

        self.create_main_layout()

        self.update_display()

        self.load_statistics()

        self.load_laps()

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
            text="Stopwatch",
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
                "Track open-ended work, "
                "record laps and save sessions."
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

        self.create_stopwatch_card()

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

        if available_width <= 1:

            try:

                available_width = (
                    self.winfo_width()
                    - 60
                )

            except Exception:

                available_width = 1200

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

        # ---------------------------------------------
        # STACKED
        # ---------------------------------------------

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

            self.stopwatch_card.grid_configure(
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

        # ---------------------------------------------
        # DESKTOP
        # ---------------------------------------------

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

            self.stopwatch_card.grid_configure(
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
    # STOPWATCH CARD
    # =================================================

    def create_stopwatch_card(
        self
    ):

        self.stopwatch_card = (
            ctk.CTkFrame(
                self.main_container,
                corner_radius=20,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=self.accent
            )
        )

        self.stopwatch_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        self.stopwatch_card.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # LABEL
        # ---------------------------------------------

        ctk.CTkLabel(
            self.stopwatch_card,
            text="OPEN-ENDED SESSION",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold"
            ),
            text_color=self.accent
        ).grid(
            row=0,
            column=0,
            pady=(26, 8)
        )

        # ---------------------------------------------
        # TIMER SHELL
        # ---------------------------------------------

        timer_shell = (
            ctk.CTkFrame(
                self.stopwatch_card,
                corner_radius=24,
                fg_color=COLORS["surface_alt"],
                border_width=1,
                border_color=COLORS["border_soft"]
            )
        )

        timer_shell.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=38,
            pady=(5, 20)
        )

        timer_shell.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # TIMER
        # ---------------------------------------------

        self.timer_label = (
            ctk.CTkLabel(
                timer_shell,
                text="00:00:00.0",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=62,
                    weight="bold"
                ),
                text_color=self.accent
            )
        )

        self.timer_label.grid(
            row=0,
            column=0,
            pady=(32, 10)
        )

        # ---------------------------------------------
        # STATUS
        # ---------------------------------------------

        self.status_label = (
            ctk.CTkLabel(
                timer_shell,
                text="Ready",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12
                ),
                text_color=COLORS["muted"]
            )
        )

        self.status_label.grid(
            row=1,
            column=0,
            pady=(0, 28)
        )

        # =================================================
        # PRIMARY CONTROLS
        # =================================================

        primary_buttons = (
            ctk.CTkFrame(
                self.stopwatch_card,
                fg_color="transparent"
            )
        )

        primary_buttons.grid(
            row=2,
            column=0,
            pady=(8, 8)
        )

        self.start_button = (
            ctk.CTkButton(
                primary_buttons,
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
                command=self.start_stopwatch
            )
        )

        self.start_button.pack(
            side="left",
            padx=5
        )

        self.pause_button = (
            ctk.CTkButton(
                primary_buttons,
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
                primary_buttons,
                text="Lap",
                width=115,
                height=43,
                corner_radius=11,
                fg_color=self.accent,
                hover_color=self.accent_hover,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                command=self.record_lap,
                state="disabled"
            )
        )

        self.lap_button.pack(
            side="left",
            padx=5
        )

        # =================================================
        # SECONDARY CONTROLS
        # =================================================

        secondary_buttons = (
            ctk.CTkFrame(
                self.stopwatch_card,
                fg_color="transparent"
            )
        )

        secondary_buttons.grid(
            row=3,
            column=0,
            pady=(5, 28)
        )

        self.reset_button = (
            ctk.CTkButton(
                secondary_buttons,
                text="Reset",
                width=130,
                height=40,
                corner_radius=11,
                fg_color=COLORS["danger"],
                hover_color=COLORS["danger_hover"],
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                command=self.reset_stopwatch
            )
        )

        self.reset_button.pack(
            side="left",
            padx=5
        )

        self.save_button = (
            ctk.CTkButton(
                secondary_buttons,
                text="Save Session",
                width=150,
                height=40,
                corner_radius=11,
                fg_color=self.accent,
                hover_color=self.accent_hover,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                command=self.save_session
            )
        )

        self.save_button.pack(
            side="left",
            padx=5
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

        self.create_laps_section()

        self.create_history()

    # =================================================
    # CURRENT ELAPSED
    # =================================================

    def get_elapsed(
        self
    ):

        if (
            self.running
            and
            self.start_mark is not None
        ):

            return (
                self.saved_elapsed
                +
                (
                    time.perf_counter()
                    - self.start_mark
                )
            )

        return self.saved_elapsed

    # =================================================
    # START / RESUME
    # =================================================

    def start_stopwatch(
        self
    ):

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

        if not self.running:

            return

        self.update_display()

        self.after_id = (
            self.after(
                100,
                self.tick
            )
        )

    # =================================================
    # PAUSE
    # =================================================

    def pause_stopwatch(
        self
    ):

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

        self.set_header_status(
            "Paused",
            COLORS["amber"]
        )

        self.update_display()

    # =================================================
    # RESET
    # =================================================

    def reset_stopwatch(
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

        self.set_header_status(
            "Ready",
            COLORS["muted"]
        )

        self.update_display()

        self.load_laps()

    # =================================================
    # LAP
    # =================================================

    def record_lap(
        self
    ):

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
                "number": (
                    len(self.laps)
                    + 1
                ),

                "lap_time": lap_duration,

                "total_time": total_elapsed,
            }
        )

        self.load_laps()

    # =================================================
    # SAVE SESSION
    # =================================================

    def save_session(
        self
    ):

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

        # ---------------------------------------------
        # PAUSE CURRENT RUN
        # ---------------------------------------------

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
            round(
                elapsed
            )
        )

        # ---------------------------------------------
        # DATABASE
        # ---------------------------------------------

        add_stopwatch_session(
            duration_seconds,
            len(
                self.laps
            )
        )

        self.status_label.configure(
            text="Session saved."
        )

        self.set_header_status(
            "Saved",
            COLORS["emerald"]
        )

        # ---------------------------------------------
        # REFRESH STATS / HISTORY
        # ---------------------------------------------

        self.load_statistics()

        self.load_history()

        # ---------------------------------------------
        # RESET SESSION
        # ---------------------------------------------

        self.saved_elapsed = 0.0

        self.paused = False
        self.running = False

        self.start_mark = None

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
    # DISPLAY
    # =================================================

    def update_display(
        self
    ):

        elapsed = (
            self.get_elapsed()
        )

        hours = int(
            elapsed
            // 3600
        )

        minutes = int(
            (
                elapsed
                % 3600
            )
            // 60
        )

        seconds = int(
            elapsed
            % 60
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
    # STATISTICS
    # =================================================

    def create_statistics(
        self
    ):

        self.statistics_frame = (
            ctk.CTkFrame(
                self.side_container,
                fg_color="transparent"
            )
        )

        self.statistics_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        self.statistics_frame.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        # ---------------------------------------------
        # SESSIONS
        # ---------------------------------------------

        session_card = (
            ctk.CTkFrame(
                self.statistics_frame,
                corner_radius=16,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        session_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 6)
        )

        ctk.CTkLabel(
            session_card,
            text="Sessions Today",
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

        self.sessions_value = (
            ctk.CTkLabel(
                session_card,
                text="0",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=28,
                    weight="bold"
                ),
                text_color=self.accent
            )
        )

        self.sessions_value.pack(
            anchor="w",
            padx=16,
            pady=(0, 15)
        )

        # ---------------------------------------------
        # TIME TODAY
        # ---------------------------------------------

        time_card = (
            ctk.CTkFrame(
                self.statistics_frame,
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
            text="Tracked Today",
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

        self.total_time_value = (
            ctk.CTkLabel(
                time_card,
                text="0s",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=26,
                    weight="bold"
                ),
                text_color=COLORS["sky"]
            )
        )

        self.total_time_value.pack(
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
            get_today_stopwatch_stats()
        )

        self.sessions_value.configure(
            text=str(
                stats[
                    "sessions"
                ]
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
    # LAPS
    # =================================================

    def create_laps_section(
        self
    ):

        self.laps_card = (
            ctk.CTkFrame(
                self.side_container,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"]
            )
        )

        self.laps_card.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        header = (
            ctk.CTkFrame(
                self.laps_card,
                fg_color="transparent"
            )
        )

        header.pack(
            fill="x",
            padx=18,
            pady=(18, 8)
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            header,
            text="Laps",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=18,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.lap_count_label = (
            ctk.CTkLabel(
                header,
                text="0 laps",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                    weight="bold"
                ),
                text_color=self.accent
            )
        )

        self.lap_count_label.grid(
            row=0,
            column=1,
            sticky="e"
        )

        self.lap_container = (
            ctk.CTkFrame(
                self.laps_card,
                fg_color="transparent"
            )
        )

        self.lap_container.pack(
            fill="x",
            padx=14,
            pady=(0, 14)
        )

    # =================================================
    # LOAD LAPS
    # =================================================

    def load_laps(
        self
    ):

        for widget in (
            self.lap_container
            .winfo_children()
        ):

            widget.destroy()

        self.lap_count_label.configure(
            text=(
                f"{len(self.laps)} "
                f"{'lap' if len(self.laps) == 1 else 'laps'}"
            )
        )

        if not self.laps:

            empty = (
                ctk.CTkFrame(
                    self.lap_container,
                    corner_radius=12,
                    fg_color=COLORS["surface_alt"],
                    border_width=1,
                    border_color=COLORS["border_soft"]
                )
            )

            empty.pack(
                fill="x",
                pady=4
            )

            ctk.CTkLabel(
                empty,
                text="No laps recorded yet.",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=11
                ),
                text_color=COLORS["muted"]
            ).pack(
                pady=18
            )

            return

        # Newest first
        for lap in reversed(
            self.laps
        ):

            row = (
                ctk.CTkFrame(
                    self.lap_container,
                    corner_radius=12,
                    fg_color=COLORS["surface_alt"],
                    border_width=1,
                    border_color=COLORS["border_soft"]
                )
            )

            row.pack(
                fill="x",
                pady=4
            )

            row.grid_columnconfigure(
                1,
                weight=1
            )

            # -----------------------------------------
            # NUMBER
            # -----------------------------------------

            number_box = (
                ctk.CTkFrame(
                    row,
                    width=38,
                    height=38,
                    corner_radius=10,
                    fg_color=self.accent
                )
            )

            number_box.grid(
                row=0,
                column=0,
                rowspan=2,
                padx=(11, 10),
                pady=10
            )

            number_box.grid_propagate(
                False
            )

            ctk.CTkLabel(
                number_box,
                text=str(
                    lap["number"]
                ),
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=11,
                    weight="bold"
                ),
                text_color=COLORS["white"]
            ).place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )

            # -----------------------------------------
            # LAP TIME
            # -----------------------------------------

            ctk.CTkLabel(
                row,
                text=(
                    "Lap "
                    f"{self.format_precise_time(lap['lap_time'])}"
                ),
                anchor="w",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=11,
                    weight="bold"
                ),
                text_color=COLORS["text"]
            ).grid(
                row=0,
                column=1,
                sticky="ew",
                pady=(10, 1)
            )

            # -----------------------------------------
            # TOTAL
            # -----------------------------------------

            ctk.CTkLabel(
                row,
                text=(
                    "Total "
                    f"{self.format_precise_time(lap['total_time'])}"
                ),
                anchor="w",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10
                ),
                text_color=COLORS["muted"]
            ).grid(
                row=1,
                column=1,
                sticky="ew",
                pady=(1, 10)
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
            row=2,
            column=0,
            sticky="nsew"
        )

        self.side_container.grid_rowconfigure(
            2,
            weight=1
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        header = (
            ctk.CTkFrame(
                self.history_card,
                fg_color="transparent"
            )
        )

        header.pack(
            fill="x",
            padx=18,
            pady=(18, 9)
        )

        ctk.CTkLabel(
            header,
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
            header,
            text="Recently saved stopwatch sessions",
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
            get_recent_stopwatch_sessions()
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
                pady=4
            )

            ctk.CTkLabel(
                empty,
                text="◴",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=25,
                    weight="bold"
                ),
                text_color=self.accent
            ).pack(
                pady=(18, 4)
            )

            ctk.CTkLabel(
                empty,
                text="No saved sessions yet",
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
                    "Save a stopwatch session "
                    "to see it here."
                ),
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10
                ),
                text_color=COLORS["muted"]
            ).pack(
                pady=(3, 18)
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

                parsed = (
                    datetime.strptime(
                        completed_at,
                        "%Y-%m-%d %H:%M:%S"
                    )
                )

                formatted_date = (
                    parsed.strftime(
                        "%d %b • %I:%M %p"
                    )
                )

            except ValueError:

                formatted_date = (
                    completed_at
                )

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
            # DURATION
            # -----------------------------------------

            ctk.CTkLabel(
                row,
                text=self.format_duration(
                    duration_seconds
                ),
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
            # LAP COUNT
            # -----------------------------------------

            ctk.CTkLabel(
                row,
                text=(
                    f"{lap_count} "
                    f"{'lap' if lap_count == 1 else 'laps'}"
                ),
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
                text=formatted_date,
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
    # FORMAT PRECISE TIME
    # =================================================

    def format_precise_time(
        self,
        seconds_value
    ):

        minutes = int(
            seconds_value
            // 60
        )

        seconds = int(
            seconds_value
            % 60
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

    # =================================================
    # FORMAT DURATION
    # =================================================

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

        return (
            f"{seconds}s"
        )