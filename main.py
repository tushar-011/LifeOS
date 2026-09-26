import customtkinter as ctk

from datetime import datetime

from ui.dashboard import DashboardPage
from ui.tasks import TasksPage
from ui.notes import NotesPage
from ui.planner import PlannerPage
from ui.pomodoro import PomodoroPage
from ui.components import NavButton

from database.database import initialize_database


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LifeOSApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        initialize_database()

        self.title("LifeOS")
        self.geometry("1400x820")
        self.minsize(1050, 650)

        self.sidebar_open = True

        self.sidebar_width = 220
        self.sidebar_collapsed_width = 72

        # Stores already-created pages
        self.pages = {}

        # Stores current visible page name
        self.current_page = None

        self.grid_rowconfigure(
            1,
            weight=1
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.create_topbar()
        self.create_sidebar()
        self.create_content_area()

        # Global mouse wheel / trackpad support
        self.bind_all(
            "<MouseWheel>",
            self.handle_mousewheel
        )

        self.show_dashboard()

    # =================================================
    # TRACKPAD / MOUSE WHEEL
    # =================================================

    def handle_mousewheel(
        self,
        event
    ):

        try:

            widget = self.winfo_containing(
                event.x_root,
                event.y_root
            )

            current_widget = widget

            while current_widget is not None:

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
                        abs(event.delta) // 120
                    )

                    canvas.yview_scroll(
                        direction * magnitude,
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

        self.topbar = ctk.CTkFrame(
            self,
            height=60,
            corner_radius=0
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

        self.menu_button = ctk.CTkButton(
            self.topbar,
            text="☰",
            width=42,
            height=38,
            corner_radius=10,
            command=self.toggle_sidebar
        )

        self.menu_button.grid(
            row=0,
            column=0,
            padx=(15, 10),
            pady=10
        )

        self.app_title = ctk.CTkLabel(
            self.topbar,
            text="LifeOS",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        self.app_title.grid(
            row=0,
            column=1,
            sticky="w"
        )

        date_text = datetime.now().strftime(
            "%A, %d %B"
        )

        self.date_label = ctk.CTkLabel(
            self.topbar,
            text=date_text,
            font=ctk.CTkFont(
                size=14
            )
        )

        self.date_label.grid(
            row=0,
            column=3,
            padx=15
        )

        self.theme_switch = ctk.CTkSwitch(
            self.topbar,
            text="Dark",
            command=self.toggle_theme
        )

        self.theme_switch.select()

        self.theme_switch.grid(
            row=0,
            column=4,
            padx=(5, 20)
        )

    # =================================================
    # SIDEBAR
    # =================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=self.sidebar_width,
            corner_radius=0
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
                lambda:
                self.show_placeholder(
                    "Focus Mode"
                )
            ),

            (
                "Pomodoro",
                "◷",
                self.show_pomodoro
            ),

            (
                "Stopwatch",
                "◴",
                lambda:
                self.show_placeholder(
                    "Stopwatch"
                )
            ),

            (
                "Notes",
                "▤",
                self.show_notes
            ),

            (
                "Analytics",
                "▥",
                lambda:
                self.show_placeholder(
                    "Analytics"
                )
            ),

            (
                "History",
                "↺",
                lambda:
                self.show_placeholder(
                    "History"
                )
            ),

            (
                "Reports",
                "▧",
                lambda:
                self.show_placeholder(
                    "Reports"
                )
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

        self.sidebar.grid_rowconfigure(
            row,
            weight=1
        )

        self.settings_button = NavButton(
            self.sidebar,
            text="Settings",
            icon="⚙",
            command=lambda:
            self.show_placeholder(
                "Settings"
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

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
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
    # PAGE MANAGEMENT
    # =================================================

    def hide_all_pages(self):

        for page in self.pages.values():

            page.grid_remove()

    def show_page(
        self,
        page_name,
        page_class
    ):

        self.hide_all_pages()

        # Create page only once
        if page_name not in self.pages:

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

            page = self.pages[
                page_name
            ]

            page.grid()

        self.current_page = page_name

        # Refresh page data when needed
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

            if page_name == "Dashboard":

                page.refresh_dashboard()

            elif page_name == "Tasks":

                page.load_tasks()

            elif page_name == "Notes":

                page.load_notes()

            elif page_name == "Planner":

                page.build_calendar()
                page.load_selected_day()

            elif page_name == "Pomodoro":

                page.load_statistics()
                page.load_history()

        except Exception:

            pass

    # =================================================
    # DASHBOARD
    # =================================================

    def show_dashboard(self):

        self.show_page(
            "Dashboard",
            DashboardPage
        )

    # =================================================
    # TASKS
    # =================================================

    def show_tasks(self):

        self.show_page(
            "Tasks",
            TasksPage
        )

    # =================================================
    # NOTES
    # =================================================

    def show_notes(self):

        self.show_page(
            "Notes",
            NotesPage
        )

    # =================================================
    # PLANNER
    # =================================================

    def show_planner(self):

        self.show_page(
            "Planner",
            PlannerPage
        )

    # =================================================
    # POMODORO
    # =================================================

    def show_pomodoro(self):

        self.show_page(
            "Pomodoro",
            PomodoroPage
        )

    # =================================================
    # PLACEHOLDER
    # =================================================

    def show_placeholder(
        self,
        title
    ):

        page_name = (
            f"placeholder_"
            f"{title}"
        )

        self.hide_all_pages()

        if page_name not in self.pages:

            page = ctk.CTkFrame(
                self.content,
                corner_radius=0,
                fg_color="transparent"
            )

            page.grid(
                row=0,
                column=0,
                sticky="nsew"
            )

            heading = ctk.CTkLabel(
                page,
                text=title,
                font=ctk.CTkFont(
                    size=32,
                    weight="bold"
                )
            )

            heading.pack(
                anchor="nw",
                padx=35,
                pady=(30, 10)
            )

            subtitle = ctk.CTkLabel(
                page,
                text=(
                    f"{title} module "
                    f"coming next."
                ),
                font=ctk.CTkFont(
                    size=15
                )
            )

            subtitle.pack(
                anchor="nw",
                padx=35
            )

            self.pages[
                page_name
            ] = page

        else:

            page = self.pages[
                page_name
            ]

            page.grid()

        self.current_page = (
            page_name
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
                width=(
                    self.sidebar_width
                )
            )

            for button in (
                self.nav_buttons
            ):

                button.expand()

            self.sidebar_open = True

    # =================================================
    # THEME
    # =================================================

    def toggle_theme(self):

        if self.theme_switch.get():

            ctk.set_appearance_mode(
                "dark"
            )

            self.theme_switch.configure(
                text="Dark"
            )

        else:

            ctk.set_appearance_mode(
                "light"
            )

            self.theme_switch.configure(
                text="Light"
            )


if __name__ == "__main__":

    app = LifeOSApp()

    app.mainloop()