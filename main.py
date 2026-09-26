import customtkinter as ctk

from datetime import datetime
from tkinter import messagebox

from ui.dashboard import DashboardPage
from ui.tasks import TasksPage
from ui.notes import NotesPage
from ui.planner import PlannerPage
from ui.focus_mode import FocusModePage
from ui.pomodoro import PomodoroPage
from ui.stopwatch import StopwatchPage
from ui.analytics import AnalyticsPage
from ui.history import HistoryPage
from ui.reports import ReportsPage
from ui.settings import SettingsPage
from ui.components import NavButton

from database.database import (
    initialize_database
)

from utils.settings_manager import (
    load_settings,
    update_setting
)


# =================================================
# LOAD APPLICATION SETTINGS
# =================================================

APP_SETTINGS = (
    load_settings()
)

INITIAL_THEME = (
    APP_SETTINGS.get(
        "appearance_mode",
        "Dark"
    )
)


# =================================================
# CUSTOMTKINTER
# =================================================

ctk.set_appearance_mode(
    INITIAL_THEME.lower()
)

ctk.set_default_color_theme(
    "blue"
)


# =================================================
# APPLICATION
# =================================================

class LifeOSApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        # ---------------------------------------------
        # DATABASE
        # ---------------------------------------------

        initialize_database()

        # ---------------------------------------------
        # WINDOW
        # ---------------------------------------------

        self.title(
            "LifeOS"
        )

        self.geometry(
            "1400x820"
        )

        self.minsize(
            1050,
            650
        )

        # ---------------------------------------------
        # SIDEBAR
        # ---------------------------------------------

        self.sidebar_open = True

        self.sidebar_width = 220
        self.sidebar_collapsed_width = 72

        # ---------------------------------------------
        # PAGE CACHE
        # ---------------------------------------------

        self.pages = {}

        self.current_page = None

        # ---------------------------------------------
        # GRID
        # ---------------------------------------------

        self.grid_rowconfigure(
            1,
            weight=1
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        # ---------------------------------------------
        # UI
        # ---------------------------------------------

        self.create_topbar()
        self.create_sidebar()
        self.create_content_area()

        # ---------------------------------------------
        # SCROLLING
        # ---------------------------------------------

        self.bind_all(
            "<MouseWheel>",
            self.handle_mousewheel
        )

        # ---------------------------------------------
        # CLOSE
        # ---------------------------------------------

        self.protocol(
            "WM_DELETE_WINDOW",
            self.handle_close
        )

        # ---------------------------------------------
        # START
        # ---------------------------------------------

        self.show_dashboard()

    # =================================================
    # FOCUS SESSION CHECK
    # =================================================

    def focus_session_is_active(self):

        focus_page = (
            self.pages.get(
                "Focus"
            )
        )

        if focus_page is None:

            return False

        try:

            return (
                focus_page
                .is_session_active()
            )

        except Exception:

            return False

    # =================================================
    # FOCUS LEAVE CONFIRMATION
    # =================================================

    def request_stop_focus(self):

        if not self.focus_session_is_active():

            return True

        answer = (
            messagebox.askyesno(
                "Focus session active",
                (
                    "A Focus Mode session is "
                    "currently active.\n\n"

                    "Do you want to stop focus?\n\n"

                    "Your focused time so far "
                    "will be saved."
                ),
                parent=self
            )
        )

        if not answer:

            return False

        focus_page = (
            self.pages.get(
                "Focus"
            )
        )

        if focus_page:

            focus_page.stop_focus_session(
                save=True
            )

        return True

    # =================================================
    # CLOSE
    # =================================================

    def handle_close(self):

        if not self.request_stop_focus():

            return

        self.destroy()

    # =================================================
    # MOUSE / TRACKPAD
    # =================================================

    def handle_mousewheel(
        self,
        event
    ):

        try:

            widget = (
                self.winfo_containing(
                    event.x_root,
                    event.y_root
                )
            )

            current_widget = widget

            while (
                current_widget
                is not None
            ):

                if isinstance(
                    current_widget,
                    ctk.CTkScrollableFrame
                ):

                    canvas = (
                        current_widget
                        ._parent_canvas
                    )

                    if event.delta == 0:

                        return

                    direction = (
                        -1
                        if event.delta > 0
                        else 1
                    )

                    magnitude = max(
                        1,
                        abs(event.delta)
                        // 120
                    )

                    canvas.yview_scroll(
                        direction
                        * magnitude,
                        "units"
                    )

                    return

                try:

                    current_widget = (
                        current_widget.master
                    )

                except AttributeError:

                    break

        except Exception:

            pass

    # =================================================
    # TOP BAR
    # =================================================

    def create_topbar(self):

        self.topbar = (
            ctk.CTkFrame(
                self,
                height=60,
                corner_radius=0
            )
        )

        self.topbar.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        self.topbar.grid_columnconfigure(
            2,
            weight=1
        )

        # ---------------------------------------------
        # MENU
        # ---------------------------------------------

        self.menu_button = (
            ctk.CTkButton(
                self.topbar,
                text="☰",
                width=42,
                height=38,
                corner_radius=10,
                command=self.toggle_sidebar
            )
        )

        self.menu_button.grid(
            row=0,
            column=0,
            padx=(15, 10),
            pady=10
        )

        # ---------------------------------------------
        # APP NAME
        # ---------------------------------------------

        self.app_title = (
            ctk.CTkLabel(
                self.topbar,
                text="LifeOS",
                font=ctk.CTkFont(
                    size=24,
                    weight="bold"
                )
            )
        )

        self.app_title.grid(
            row=0,
            column=1,
            sticky="w"
        )

        # ---------------------------------------------
        # DATE
        # ---------------------------------------------

        date_text = (
            datetime.now()
            .strftime(
                "%A, %d %B"
            )
        )

        self.date_label = (
            ctk.CTkLabel(
                self.topbar,
                text=date_text,
                font=ctk.CTkFont(
                    size=14
                )
            )
        )

        self.date_label.grid(
            row=0,
            column=3,
            padx=15
        )

        # ---------------------------------------------
        # THEME SWITCH
        # ---------------------------------------------

        self.theme_switch = (
            ctk.CTkSwitch(
                self.topbar,
                text="Dark",
                command=self.toggle_theme
            )
        )

        self.theme_switch.grid(
            row=0,
            column=4,
            padx=(5, 20)
        )

        self.sync_theme_controls()

    # =================================================
    # SYNC THEME CONTROL
    # =================================================

    def sync_theme_controls(self):

        settings = (
            load_settings()
        )

        theme = (
            settings.get(
                "appearance_mode",
                "Dark"
            )
        )

        if theme == "Light":

            self.theme_switch.deselect()

            self.theme_switch.configure(
                text="Light"
            )

        elif theme == "Dark":

            self.theme_switch.select()

            self.theme_switch.configure(
                text="Dark"
            )

        else:

            self.theme_switch.configure(
                text="System"
            )

    # =================================================
    # SIDEBAR
    # =================================================

    def create_sidebar(self):

        self.sidebar = (
            ctk.CTkFrame(
                self,
                width=self.sidebar_width,
                corner_radius=0
            )
        )

        self.sidebar.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(
            False
        )

        self.sidebar.grid_columnconfigure(
            0,
            weight=1
        )

        self.nav_buttons = []

        navigation = [

            (
                "Dashboard",
                "⌂",
                self.show_dashboard
            ),

            (
                "Tasks",
                "✓",
                self.show_tasks
            ),

            (
                "Planner",
                "▦",
                self.show_planner
            ),

            (
                "Focus",
                "◎",
                self.show_focus
            ),

            (
                "Pomodoro",
                "◷",
                self.show_pomodoro
            ),

            (
                "Stopwatch",
                "◴",
                self.show_stopwatch
            ),

            (
                "Notes",
                "▤",
                self.show_notes
            ),

            (
                "Analytics",
                "▥",
                self.show_analytics
            ),

            (
                "History",
                "↺",
                self.show_history
            ),

            (
                "Reports",
                "▧",
                self.show_reports
            ),
        ]

        row = 0

        for (
            text,
            icon,
            command
        ) in navigation:

            button = NavButton(
                self.sidebar,
                text=text,
                icon=icon,
                command=command
            )

            button.grid(
                row=row,
                column=0,
                padx=12,
                pady=4,
                sticky="ew"
            )

            self.nav_buttons.append(
                button
            )

            row += 1

        # ---------------------------------------------
        # SETTINGS AT BOTTOM
        # ---------------------------------------------

        self.sidebar.grid_rowconfigure(
            row,
            weight=1
        )

        self.settings_button = (
            NavButton(
                self.sidebar,
                text="Settings",
                icon="⚙",
                command=self.show_settings
            )
        )

        self.settings_button.grid(
            row=row + 1,
            column=0,
            padx=12,
            pady=(4, 15),
            sticky="ew"
        )

        self.nav_buttons.append(
            self.settings_button
        )

    # =================================================
    # CONTENT
    # =================================================

    def create_content_area(self):

        self.content = (
            ctk.CTkFrame(
                self,
                corner_radius=0,
                fg_color="transparent"
            )
        )

        self.content.grid(
            row=1,
            column=1,
            sticky="nsew"
        )

        self.content.grid_rowconfigure(
            0,
            weight=1
        )

        self.content.grid_columnconfigure(
            0,
            weight=1
        )

    # =================================================
    # PAGE CACHE
    # =================================================

    def hide_all_pages(self):

        for page in (
            self.pages.values()
        ):

            page.grid_remove()

    # =================================================
    # SHOW PAGE
    # =================================================

    def show_page(
        self,
        page_name,
        page_class
    ):

        # ---------------------------------------------
        # FOCUS LOCK
        # ---------------------------------------------

        if (
            self.current_page == "Focus"
            and page_name != "Focus"
            and self.focus_session_is_active()
        ):

            if not self.request_stop_focus():

                return

        self.hide_all_pages()

        # ---------------------------------------------
        # CREATE PAGE ONCE
        # ---------------------------------------------

        if (
            page_name
            not in self.pages
        ):

            page = page_class(
                self.content
            )

            page.grid(
                row=0,
                column=0,
                sticky="nsew"
            )

            self.pages[
                page_name
            ] = page

        else:

            page = (
                self.pages[
                    page_name
                ]
            )

            page.grid()

        self.current_page = (
            page_name
        )

        self.refresh_page(
            page_name,
            page
        )

    # =================================================
    # REFRESH PAGE
    # =================================================

    def refresh_page(
        self,
        page_name,
        page
    ):

        try:

            if (
                page_name
                == "Dashboard"
            ):

                page.refresh_dashboard()

            elif (
                page_name
                == "Tasks"
            ):

                page.load_tasks()

            elif (
                page_name
                == "Notes"
            ):

                page.load_notes()

            elif (
                page_name
                == "Planner"
            ):

                page.build_calendar()

                page.load_selected_day()

            elif (
                page_name
                == "Focus"
            ):

                if not (
                    page.is_session_active()
                ):

                    page.load_tasks()

                page.load_statistics()
                page.load_history()

            elif (
                page_name
                == "Pomodoro"
            ):

                page.load_statistics()
                page.load_history()

            elif (
                page_name
                == "Stopwatch"
            ):

                page.load_statistics()
                page.load_history()

            elif (
                page_name
                == "Analytics"
            ):

                page.refresh_analytics()

            elif (
                page_name
                == "History"
            ):

                page.refresh_history()

            elif (
                page_name
                == "Reports"
            ):

                page.refresh_reports()

            elif (
                page_name
                == "Settings"
            ):

                page.refresh_settings()

        except Exception as error:

            print(
                f"Error refreshing "
                f"{page_name}: "
                f"{error}"
            )

    # =================================================
    # PAGE METHODS
    # =================================================

    def show_dashboard(self):

        self.show_page(
            "Dashboard",
            DashboardPage
        )

    def show_tasks(self):

        self.show_page(
            "Tasks",
            TasksPage
        )

    def show_planner(self):

        self.show_page(
            "Planner",
            PlannerPage
        )

    def show_focus(self):

        self.show_page(
            "Focus",
            FocusModePage
        )

    def show_pomodoro(self):

        self.show_page(
            "Pomodoro",
            PomodoroPage
        )

    def show_stopwatch(self):

        self.show_page(
            "Stopwatch",
            StopwatchPage
        )

    def show_notes(self):

        self.show_page(
            "Notes",
            NotesPage
        )

    def show_analytics(self):

        self.show_page(
            "Analytics",
            AnalyticsPage
        )

    def show_history(self):

        self.show_page(
            "History",
            HistoryPage
        )

    def show_reports(self):

        self.show_page(
            "Reports",
            ReportsPage
        )

    def show_settings(self):

        self.show_page(
            "Settings",
            SettingsPage
        )

    # =================================================
    # SIDEBAR TOGGLE
    # =================================================

    def toggle_sidebar(self):

        if self.sidebar_open:

            self.sidebar.configure(
                width=(
                    self
                    .sidebar_collapsed_width
                )
            )

            for button in (
                self.nav_buttons
            ):

                button.collapse()

            self.sidebar_open = False

        else:

            self.sidebar.configure(
                width=self.sidebar_width
            )

            for button in (
                self.nav_buttons
            ):

                button.expand()

            self.sidebar_open = True

    # =================================================
    # TOPBAR THEME SWITCH
    # =================================================

    def toggle_theme(self):

        # The topbar only provides quick
        # Dark / Light switching.

        if (
            self.theme_switch.get()
        ):

            theme = "Dark"

        else:

            theme = "Light"

        ctk.set_appearance_mode(
            theme.lower()
        )

        update_setting(
            "appearance_mode",
            theme
        )

        self.theme_switch.configure(
            text=theme
        )

        # Sync Settings page if created
        settings_page = (
            self.pages.get(
                "Settings"
            )
        )

        if settings_page:

            settings_page.refresh_settings()


# =================================================
# START APPLICATION
# =================================================

if __name__ == "__main__":

    app = LifeOSApp()

    app.mainloop()