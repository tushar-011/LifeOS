import customtkinter as ctk

from datetime import datetime

from database.database import (
    get_today_tasks,
    add_focus_session,
    get_today_focus_stats,
    get_recent_focus_sessions,
)

from ui.theme import (
    COLORS,
    FONT_BODY,
    FONT_DISPLAY,
    module_accent,
    module_accent_hover,
)


class FocusModePage(ctk.CTkScrollableFrame):

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
        # VISUALS
        # =================================================

        self.accent = (
            module_accent(
                "Focus"
            )
        )

        self.accent_hover = (
            module_accent_hover(
                "Focus"
            )
        )

        # =================================================
        # TIMER STATE
        # =================================================

        self.running = False
        self.paused = False
        self.after_id = None

        self.duration_minutes = 25

        self.remaining_seconds = (
            self.duration_minutes
            * 60
        )

        self.task_lookup = {}

        # Lock the active task while focusing.
        self.active_task_id = None
        self.active_task_title = None

        # Responsive state
        self._stacked_layout = False

        # =================================================
        # BUILD
        # =================================================

        self.create_header()

        self.create_main_layout()

        self.load_tasks()
        self.load_statistics()
        self.load_history()

        self.update_timer_display()

        self.after(
            100,
            self.apply_responsive_layout
        )

    # =================================================
    # HEADER
    # =================================================

    def create_header(
        self
    ):

        header = (
            ctk.CTkFrame(
                self,
                fg_color="transparent"
            )
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=28,
            pady=(26, 16)
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        left = (
            ctk.CTkFrame(
                header,
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
            text="Focus Mode",
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
                "Choose one thing and give it "
                "your full attention."
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
                header,
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
            padx=28,
            pady=(0, 28)
        )

        self.main_container.grid_columnconfigure(
            0,
            weight=6
        )

        self.main_container.grid_columnconfigure(
            1,
            weight=4
        )

        self.create_focus_panel()

        self.create_side_panel()

    # =================================================
    # RESPONSIVE LAYOUT
    # =================================================

    def apply_responsive_layout(
        self,
        window_width=None
    ):

        if window_width is None:

            try:

                window_width = (
                    self.winfo_toplevel()
                    .winfo_width()
                )

            except Exception:

                window_width = 1400

        should_stack = (
            window_width < 1160
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
                weight=1
            )

            self.main_container.grid_columnconfigure(
                1,
                weight=0
            )

            self.focus_card.grid_configure(
                row=0,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0,
                pady=(0, 12)
            )

            self.side_container.grid_configure(
                row=1,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0,
                pady=0
            )

        # ---------------------------------------------
        # DESKTOP
        # ---------------------------------------------

        else:

            self.main_container.grid_columnconfigure(
                0,
                weight=6
            )

            self.main_container.grid_columnconfigure(
                1,
                weight=4
            )

            self.focus_card.grid_configure(
                row=0,
                column=0,
                columnspan=1,
                sticky="nsew",
                padx=(0, 9),
                pady=0
            )

            self.side_container.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                sticky="nsew",
                padx=(9, 0),
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

            self._parent_canvas.configure(
                scrollregion=(
                    self._parent_canvas
                    .bbox("all")
                )
            )

        except Exception:

            pass

    # =================================================
    # FOCUS PANEL
    # =================================================

    def create_focus_panel(
        self
    ):

        self.focus_card = (
            ctk.CTkFrame(
                self.main_container,
                corner_radius=20,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=self.accent
            )
        )

        self.focus_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 9)
        )

        self.focus_card.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # TOP LABEL
        # ---------------------------------------------

        ctk.CTkLabel(
            self.focus_card,
            text="DEEP FOCUS SESSION",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold"
            ),
            text_color=self.accent
        ).grid(
            row=0,
            column=0,
            pady=(24, 5)
        )

        # ---------------------------------------------
        # TASK LABEL
        # ---------------------------------------------

        ctk.CTkLabel(
            self.focus_card,
            text="Focus On",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=13,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=1,
            column=0,
            pady=(7, 6)
        )

        self.task_menu = (
            ctk.CTkOptionMenu(
                self.focus_card,
                values=[
                    "General"
                ],
                width=360,
                height=40
            )
        )

        self.task_menu.set(
            "General"
        )

        self.task_menu.grid(
            row=2,
            column=0,
            pady=5
        )

        # ---------------------------------------------
        # DURATION
        # ---------------------------------------------

        ctk.CTkLabel(
            self.focus_card,
            text="Duration",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=13,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=3,
            column=0,
            pady=(15, 6)
        )

        self.duration_menu = (
            ctk.CTkOptionMenu(
                self.focus_card,
                values=[
                    "15 minutes",
                    "25 minutes",
                    "45 minutes",
                    "60 minutes",
                ],
                command=self.change_duration,
                width=180,
                height=38
            )
        )

        self.duration_menu.set(
            "25 minutes"
        )

        self.duration_menu.grid(
            row=4,
            column=0,
            pady=5
        )

        # ---------------------------------------------
        # TIMER SHELL
        # ---------------------------------------------

        timer_shell = (
            ctk.CTkFrame(
                self.focus_card,
                corner_radius=24,
                fg_color=COLORS["surface_alt"],
                border_width=1,
                border_color=COLORS["border_soft"]
            )
        )

        timer_shell.grid(
            row=5,
            column=0,
            padx=40,
            pady=(25, 10),
            sticky="ew"
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
                text="25:00",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=72,
                    weight="bold"
                ),
                text_color=self.accent
            )
        )

        self.timer_label.grid(
            row=0,
            column=0,
            pady=(25, 5)
        )

        # ---------------------------------------------
        # PROGRESS
        # ---------------------------------------------

        self.progress_bar = (
            ctk.CTkProgressBar(
                timer_shell,
                height=8,
                corner_radius=100,
                fg_color=COLORS["surface_soft"],
                progress_color=self.accent
            )
        )

        self.progress_bar.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=45,
            pady=(5, 12)
        )

        self.progress_bar.set(
            0
        )

        self.status_label = (
            ctk.CTkLabel(
                timer_shell,
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
            pady=(0, 22)
        )

        # ---------------------------------------------
        # BUTTONS
        # ---------------------------------------------

        button_frame = (
            ctk.CTkFrame(
                self.focus_card,
                fg_color="transparent"
            )
        )

        button_frame.grid(
            row=6,
            column=0,
            pady=(10, 28)
        )

        self.start_button = (
            ctk.CTkButton(
                button_frame,
                text="Start Focus",
                width=140,
                height=43,
                corner_radius=11,
                fg_color=self.accent,
                hover_color=self.accent_hover,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                command=self.start_focus
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
                width=105,
                height=43,
                corner_radius=11,
                fg_color=COLORS["amber"],
                hover_color=COLORS["amber_hover"],
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                command=self.pause_focus,
                state="disabled"
            )
        )

        self.pause_button.pack(
            side="left",
            padx=5
        )

        self.stop_button = (
            ctk.CTkButton(
                button_frame,
                text="Stop Focus",
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
                command=self.stop_focus_session
            )
        )

        self.stop_button.pack(
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
            padx=(9, 0)
        )

        self.side_container.grid_columnconfigure(
            0,
            weight=1
        )

        self.create_statistics()

        self.create_history()

    # =================================================
    # TASKS
    # =================================================

    def load_tasks(
        self
    ):

        tasks = (
            get_today_tasks(
                limit=100
            )
        )

        current_selection = (
            self.task_menu.get()
        )

        self.task_lookup = {
            "General": {
                "id": None,
                "title": "General"
            }
        }

        values = [
            "General"
        ]

        for task in tasks:

            (
                task_id,
                title,
                due_date,
                priority,
                category,
                completed
            ) = task

            display = (
                f"{title} • {priority}"
            )

            values.append(
                display
            )

            self.task_lookup[
                display
            ] = {
                "id": task_id,
                "title": title
            }

        self.task_menu.configure(
            values=values
        )

        if (
            current_selection
            in values
        ):

            self.task_menu.set(
                current_selection
            )

        else:

            self.task_menu.set(
                "General"
            )

    # =================================================
    # DURATION
    # =================================================

    def change_duration(
        self,
        value
    ):

        if (
            self.running
            or self.paused
        ):

            return

        durations = {
            "15 minutes": 15,
            "25 minutes": 25,
            "45 minutes": 45,
            "60 minutes": 60,
        }

        self.duration_minutes = (
            durations[value]
        )

        self.remaining_seconds = (
            self.duration_minutes
            * 60
        )

        self.update_timer_display()

        self.progress_bar.set(
            0
        )

    # =================================================
    # ACTIVE STATUS
    # =================================================

    def is_session_active(
        self
    ):

        return (
            self.running
            or self.paused
        )

    # =================================================
    # START
    # =================================================

    def start_focus(
        self
    ):

        selected = (
            self.task_menu.get()
        )

        if (
            selected
            not in self.task_lookup
        ):

            self.status_label.configure(
                text=(
                    "Select a focus item first."
                )
            )

            return

        if (
            self.running
            or self.paused
        ):

            return

        # ---------------------------------------------
        # LOCK TASK FOR THIS SESSION
        # ---------------------------------------------

        selected_data = (
            self.task_lookup[
                selected
            ]
        )

        self.active_task_id = (
            selected_data[
                "id"
            ]
        )

        self.active_task_title = (
            selected_data[
                "title"
            ]
        )

        self.running = True
        self.paused = False

        self.start_button.configure(
            state="disabled"
        )

        self.pause_button.configure(
            state="normal"
        )

        self.task_menu.configure(
            state="disabled"
        )

        self.duration_menu.configure(
            state="disabled"
        )

        self.status_label.configure(
            text=(
                f"Focusing on: "
                f"{self.active_task_title}"
            )
        )

        self.set_header_status(
            "Focusing",
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

        self.update_timer_display()

        if (
            self.remaining_seconds
            <= 0
        ):

            self.complete_focus()

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

    def pause_focus(
        self
    ):

        if not self.running:

            return

        self.running = False
        self.paused = True

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
            state="normal",
            command=self.resume_focus
        )

        self.pause_button.configure(
            state="disabled"
        )

        self.status_label.configure(
            text="Focus paused."
        )

        self.set_header_status(
            "Paused",
            COLORS["amber"]
        )

    # =================================================
    # RESUME
    # =================================================

    def resume_focus(
        self
    ):

        if not self.paused:

            return

        self.running = True
        self.paused = False

        self.start_button.configure(
            text="Start Focus",
            state="disabled",
            command=self.start_focus
        )

        self.pause_button.configure(
            state="normal"
        )

        self.status_label.configure(
            text=(
                f"Focusing on: "
                f"{self.active_task_title or 'General'}"
            )
        )

        self.set_header_status(
            "Focusing",
            self.accent
        )

        self.tick()

    # =================================================
    # ELAPSED TIME
    # =================================================

    def get_elapsed_seconds(
        self
    ):

        planned_seconds = (
            self.duration_minutes
            * 60
        )

        elapsed = (
            planned_seconds
            - self.remaining_seconds
        )

        return max(
            0,
            elapsed
        )

    # =================================================
    # SAVE SESSION
    # =================================================

    def save_current_session(
        self,
        status
    ):

        elapsed_seconds = (
            self.get_elapsed_seconds()
        )

        if elapsed_seconds <= 0:

            return False

        add_focus_session(
            self.active_task_id,
            self.active_task_title
            or "General",
            self.duration_minutes,
            actual_seconds=elapsed_seconds,
            status=status
        )

        return True

    # =================================================
    # STOP
    # =================================================

    def stop_focus_session(
        self,
        save=True
    ):

        if (
            not self.running
            and not self.paused
        ):

            self.reset_focus_state()

            return

        if save:

            saved = (
                self.save_current_session(
                    "Stopped"
                )
            )

        else:

            saved = False

        self.reset_focus_state()

        if saved:

            self.status_label.configure(
                text=(
                    "Focus stopped. "
                    "Time saved."
                )
            )

        else:

            self.status_label.configure(
                text="Focus stopped."
            )

        self.load_statistics()

        self.load_history()

    # =================================================
    # COMPLETE
    # =================================================

    def complete_focus(
        self
    ):

        add_focus_session(
            self.active_task_id,
            self.active_task_title
            or "General",
            self.duration_minutes,
            actual_seconds=(
                self.duration_minutes
                * 60
            ),
            status="Completed"
        )

        self.reset_focus_state()

        self.status_label.configure(
            text=(
                "Focus session completed!"
            )
        )

        self.set_header_status(
            "Completed",
            COLORS["emerald"]
        )

        try:

            self.bell()

        except Exception:

            pass

        self.load_statistics()

        self.load_history()

        self.load_tasks()

    # =================================================
    # RESET INTERNAL STATE
    # =================================================

    def reset_focus_state(
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

        self.remaining_seconds = (
            self.duration_minutes
            * 60
        )

        self.active_task_id = None
        self.active_task_title = None

        self.start_button.configure(
            text="Start Focus",
            state="normal",
            command=self.start_focus
        )

        self.pause_button.configure(
            state="disabled"
        )

        self.task_menu.configure(
            state="normal"
        )

        self.duration_menu.configure(
            state="normal"
        )

        self.set_header_status(
            "Ready",
            COLORS["muted"]
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

        planned_seconds = max(
            1,
            self.duration_minutes
            * 60
        )

        elapsed = (
            planned_seconds
            - self.remaining_seconds
        )

        progress = min(
            1,
            max(
                0,
                elapsed
                / planned_seconds
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
        # SESSION CARD
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
            padx=15,
            pady=(14, 4)
        )

        self.session_value = (
            ctk.CTkLabel(
                session_card,
                text="0",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=27,
                    weight="bold"
                ),
                text_color=self.accent
            )
        )

        self.session_value.pack(
            anchor="w",
            padx=15,
            pady=(0, 14)
        )

        # ---------------------------------------------
        # TIME CARD
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
            text="Focused Today",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold"
            ),
            text_color=COLORS["muted"]
        ).pack(
            anchor="w",
            padx=15,
            pady=(14, 4)
        )

        self.time_value = (
            ctk.CTkLabel(
                time_card,
                text="0m",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=24,
                    weight="bold"
                ),
                text_color=COLORS["pink"]
            )
        )

        self.time_value.pack(
            anchor="w",
            padx=15,
            pady=(0, 14)
        )

    # =================================================
    # LOAD STATISTICS
    # =================================================

    def load_statistics(
        self
    ):

        stats = (
            get_today_focus_stats()
        )

        self.session_value.configure(
            text=str(
                stats[
                    "sessions"
                ]
            )
        )

        self.time_value.configure(
            text=self.format_seconds(
                stats[
                    "focus_seconds"
                ]
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

        header = (
            ctk.CTkFrame(
                self.history_card,
                fg_color="transparent"
            )
        )

        header.pack(
            fill="x",
            padx=18,
            pady=(18, 10)
        )

        ctk.CTkLabel(
            header,
            text="Recent Focus Sessions",
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
            text=(
                "Your latest tracked sessions"
            ),
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11
            ),
            text_color=COLORS["muted"]
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

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
            get_recent_focus_sessions()
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
                text="◎",
                font=ctk.CTkFont(
                    size=24,
                    weight="bold"
                ),
                text_color=self.accent
            ).pack(
                pady=(18, 4)
            )

            ctk.CTkLabel(
                empty,
                text="No Focus sessions yet",
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
                    "Your recent sessions "
                    "will appear here."
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
                task_id,
                task_title,
                planned_minutes,
                actual_seconds,
                status,
                completed_at
            ) = session

            if not actual_seconds:

                actual_seconds = (
                    planned_minutes
                    * 60
                )

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
            # TITLE
            # -----------------------------------------

            ctk.CTkLabel(
                row,
                text=task_title,
                anchor="w",
                justify="left",
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
            # DETAILS
            # -----------------------------------------

            status_color = (
                COLORS["emerald"]
                if status
                == "Completed"
                else COLORS["amber"]
            )

            details_frame = (
                ctk.CTkFrame(
                    row,
                    fg_color="transparent"
                )
            )

            details_frame.grid(
                row=1,
                column=0,
                sticky="w",
                padx=13,
                pady=(2, 11)
            )

            ctk.CTkLabel(
                details_frame,
                text=self.format_seconds(
                    actual_seconds
                ),
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10
                ),
                text_color=COLORS["muted"]
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                details_frame,
                text=" • ",
                text_color=COLORS["subtle"]
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                details_frame,
                text=status,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                    weight="bold"
                ),
                text_color=status_color
            ).pack(
                side="left"
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
    # HELPERS
    # =================================================

    def format_seconds(
        self,
        seconds
    ):

        seconds = int(
            seconds
        )

        hours = (
            seconds
            // 3600
        )

        minutes = (
            (
                seconds
                % 3600
            )
            // 60
        )

        remaining_seconds = (
            seconds
            % 60
        )

        if hours:

            return (
                f"{hours}h "
                f"{minutes}m "
                f"{remaining_seconds}s"
            )

        if minutes:

            return (
                f"{minutes}m "
                f"{remaining_seconds}s"
            )

        return (
            f"{remaining_seconds}s"
        )