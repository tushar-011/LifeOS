import customtkinter as ctk

from datetime import datetime

from database.database import (
    get_today_tasks,
    add_focus_session,
    get_today_focus_stats,
    get_recent_focus_sessions
)


class FocusModePage(
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

        # ---------------------------------------------
        # TIMER STATE
        # ---------------------------------------------

        self.running = False
        self.paused = False
        self.after_id = None

        self.duration_minutes = 25

        self.remaining_seconds = (
            self.duration_minutes
            * 60
        )

        # Selected focus item
        self.task_lookup = {}

        self.create_header()
        self.create_focus_card()
        self.create_statistics()
        self.create_history()

        self.load_tasks()
        self.load_statistics()
        self.load_history()

        self.update_timer_display()

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
            text="Focus Mode",
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
                "Choose one thing and give "
                "it your full attention."
            )
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

    # =================================================
    # FOCUS CARD
    # =================================================

    def create_focus_card(self):

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

        # ---------------------------------------------
        # FOCUS ITEM
        # ---------------------------------------------

        ctk.CTkLabel(
            card,
            text="Focus On",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            pady=(25, 5)
        )

        self.task_menu = (
            ctk.CTkOptionMenu(
                card,
                values=[
                    "General"
                ],
                width=340
            )
        )

        self.task_menu.set(
            "General"
        )

        self.task_menu.pack(
            pady=5
        )

        # ---------------------------------------------
        # DURATION
        # ---------------------------------------------

        ctk.CTkLabel(
            card,
            text="Duration",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            pady=(15, 5)
        )

        self.duration_menu = (
            ctk.CTkOptionMenu(
                card,
                values=[
                    "15 minutes",
                    "25 minutes",
                    "45 minutes",
                    "60 minutes"
                ],
                command=self.change_duration,
                width=180
            )
        )

        self.duration_menu.set(
            "25 minutes"
        )

        self.duration_menu.pack(
            pady=5
        )

        # ---------------------------------------------
        # TIMER
        # ---------------------------------------------

        self.timer_label = (
            ctk.CTkLabel(
                card,
                text="25:00",
                font=ctk.CTkFont(
                    size=70,
                    weight="bold"
                )
            )
        )

        self.timer_label.pack(
            pady=(25, 10)
        )

        self.status_label = (
            ctk.CTkLabel(
                card,
                text="Ready to focus."
            )
        )

        self.status_label.pack(
            pady=(0, 15)
        )

        # ---------------------------------------------
        # BUTTONS
        # ---------------------------------------------

        button_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=(5, 30)
        )

        self.start_button = (
            ctk.CTkButton(
                button_frame,
                text="Start Focus",
                width=130,
                height=42,
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
                width=100,
                height=42,
                command=self.pause_focus,
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
                text="Stop Focus",
                width=110,
                height=42,
                command=self.stop_focus_session
            )
        )

        self.reset_button.pack(
            side="left",
            padx=5
        )

    # =================================================
    # TODAY'S TASKS + GENERAL
    # =================================================

    def load_tasks(self):

        tasks = get_today_tasks(
            limit=100
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

        # Don't overwrite selection while focusing
        if (
            current_selection in values
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
            "60 minutes": 60
        }

        self.duration_minutes = (
            durations[value]
        )

        self.remaining_seconds = (
            self.duration_minutes
            * 60
        )

        self.update_timer_display()

    # =================================================
    # ACTIVE STATUS
    # =================================================

    def is_session_active(self):

        return (
            self.running
            or self.paused
        )

    # =================================================
    # START
    # =================================================

    def start_focus(self):

        selected = (
            self.task_menu.get()
        )

        if (
            selected
            not in self.task_lookup
        ):

            self.status_label.configure(
                text="Select a focus item first."
            )

            return

        if (
            self.running
            or self.paused
        ):
            return

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

        focus_title = (
            self.task_lookup[
                selected
            ]["title"]
        )

        self.status_label.configure(
            text=(
                f"Focusing on: "
                f"{focus_title}"
            )
        )

        self.tick()

    # =================================================
    # TIMER LOOP
    # =================================================

    def tick(self):

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

        self.after_id = self.after(
            1000,
            self.tick
        )

    # =================================================
    # PAUSE
    # =================================================

    def pause_focus(self):

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

    # =================================================
    # RESUME
    # =================================================

    def resume_focus(self):

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

        selected = (
            self.task_menu.get()
        )

        title = (
            self.task_lookup.get(
                selected,
                {
                    "title": "General"
                }
            )["title"]
        )

        self.status_label.configure(
            text=(
                f"Focusing on: {title}"
            )
        )

        self.tick()

    # =================================================
    # ELAPSED TIME
    # =================================================

    def get_elapsed_seconds(self):

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

        # Don't create empty sessions
        if elapsed_seconds <= 0:
            return False

        selected = (
            self.task_menu.get()
        )

        task_data = (
            self.task_lookup.get(
                selected,
                {
                    "id": None,
                    "title": "General"
                }
            )
        )

        add_focus_session(
            task_data["id"],
            task_data["title"],
            self.duration_minutes,
            actual_seconds=elapsed_seconds,
            status=status
        )

        return True

    # =================================================
    # MANUAL STOP
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

    def complete_focus(self):

        selected = (
            self.task_menu.get()
        )

        task_data = (
            self.task_lookup.get(
                selected,
                {
                    "id": None,
                    "title": "General"
                }
            )
        )

        add_focus_session(
            task_data["id"],
            task_data["title"],
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

    def reset_focus_state(self):

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

        self.update_timer_display()

    # =================================================
    # TIMER DISPLAY
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

        frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        frame.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        # Session count
        session_card = ctk.CTkFrame(
            frame,
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

        self.session_value = (
            ctk.CTkLabel(
                session_card,
                text="0",
                font=ctk.CTkFont(
                    size=28,
                    weight="bold"
                )
            )
        )

        self.session_value.pack(
            anchor="w",
            padx=18,
            pady=(0, 15)
        )

        # Focus time
        time_card = ctk.CTkFrame(
            frame,
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
            text="Tracked Focus Today",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 3)
        )

        self.time_value = (
            ctk.CTkLabel(
                time_card,
                text="0m",
                font=ctk.CTkFont(
                    size=28,
                    weight="bold"
                )
            )
        )

        self.time_value.pack(
            anchor="w",
            padx=18,
            pady=(0, 15)
        )

    def load_statistics(self):

        stats = (
            get_today_focus_stats()
        )

        self.session_value.configure(
            text=str(
                stats["sessions"]
            )
        )

        self.time_value.configure(
            text=self.format_seconds(
                stats["focus_seconds"]
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
            text="Recent Focus Sessions",
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
            get_recent_focus_sessions()
        )

        if not sessions:

            ctk.CTkLabel(
                self.history_container,
                text=(
                    "No Focus Mode sessions yet."
                )
            ).pack(
                pady=25
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

            # Compatibility with old sessions
            if not actual_seconds:

                actual_seconds = (
                    planned_minutes
                    * 60
                )

            try:

                parsed = datetime.strptime(
                    completed_at,
                    "%Y-%m-%d %H:%M:%S"
                )

                formatted = (
                    parsed.strftime(
                        "%d %b %Y • "
                        "%I:%M %p"
                    )
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
                text=task_title,
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
                    f"{self.format_seconds(actual_seconds)}"
                    f" • {status}"
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
            seconds // 3600
        )

        minutes = (
            (
                seconds % 3600
            )
            // 60
        )

        remaining_seconds = (
            seconds % 60
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