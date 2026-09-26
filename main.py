import customtkinter as ctk
from datetime import datetime

from ui.dashboard import DashboardPage
from ui.tasks import TasksPage
from ui.components import NavButton

from database.database import initialize_database

from ui.notes import NotesPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LifeOSApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Initialize database before loading UI
        initialize_database()

        self.title("LifeOS")
        self.geometry("1400x820")
        self.minsize(1050, 650)

        self.sidebar_open = True
        self.sidebar_width = 220
        self.sidebar_collapsed_width = 72

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_topbar()
        self.create_sidebar()
        self.create_content_area()

        self.show_dashboard()

    # -------------------------------------------------
    # TOP BAR
    # -------------------------------------------------

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

        self.topbar.grid_columnconfigure(2, weight=1)

        # Menu Button
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

        # App Name
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

        # Date
        date_text = datetime.now().strftime(
            "%A, %d %B"
        )

        self.date_label = ctk.CTkLabel(
            self.topbar,
            text=date_text,
            font=ctk.CTkFont(size=14)
        )

        self.date_label.grid(
            row=0,
            column=3,
            padx=15
        )

        # Theme Toggle
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

    # -------------------------------------------------
    # SIDEBAR
    # -------------------------------------------------

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

        self.sidebar.grid_propagate(False)
        self.sidebar.grid_columnconfigure(0, weight=1)

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
                lambda: self.show_placeholder("Planner")
            ),

            (
                "Focus",
                "◎",
                lambda: self.show_placeholder("Focus Mode")
            ),

            (
                "Pomodoro",
                "◷",
                lambda: self.show_placeholder("Pomodoro")
            ),

            (
                "Stopwatch",
                "◴",
                lambda: self.show_placeholder("Stopwatch")
            ),

            (
                "Notes",
                "▤",
                self.show_notes
            ),

            (
                "Analytics",
                "▥",
                lambda: self.show_placeholder("Analytics")
            ),

            (
                "History",
                "↺",
                lambda: self.show_placeholder("History")
            ),

            (
                "Reports",
                "▧",
                lambda: self.show_placeholder("Reports")
            ),
        ]

        row = 0

        for text, icon, command in navigation:

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

            self.nav_buttons.append(button)

            row += 1

        # Push Settings to bottom
        self.sidebar.grid_rowconfigure(
            row,
            weight=1
        )

        self.settings_button = NavButton(
            self.sidebar,
            text="Settings",
            icon="⚙",
            command=lambda: self.show_placeholder(
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

    # -------------------------------------------------
    # CONTENT AREA
    # -------------------------------------------------

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

    # -------------------------------------------------
    # PAGE MANAGEMENT
    # -------------------------------------------------

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):

        self.clear_content()

        page = DashboardPage(
            self.content
        )

        page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    def show_tasks(self):

        self.clear_content()

        page = TasksPage(
            self.content
        )

        page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        
    def show_notes(self):
        self.clear_content()

        page = NotesPage(
            self.content
        )

        page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    def show_placeholder(self, title):

        self.clear_content()

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
            text=f"{title} module coming next.",
            font=ctk.CTkFont(size=15)
        )

        subtitle.pack(
            anchor="nw",
            padx=35
        )

    # -------------------------------------------------
    # COLLAPSIBLE SIDEBAR
    # -------------------------------------------------

    def toggle_sidebar(self):

        if self.sidebar_open:

            self.sidebar.configure(
                width=self.sidebar_collapsed_width
            )

            for button in self.nav_buttons:
                button.collapse()

            self.sidebar_open = False

        else:

            self.sidebar.configure(
                width=self.sidebar_width
            )

            for button in self.nav_buttons:
                button.expand()

            self.sidebar_open = True

    # -------------------------------------------------
    # THEME
    # -------------------------------------------------

    def toggle_theme(self):

        if self.theme_switch.get():

            ctk.set_appearance_mode("dark")

            self.theme_switch.configure(
                text="Dark"
            )

        else:

            ctk.set_appearance_mode("light")

            self.theme_switch.configure(
                text="Light"
            )


if __name__ == "__main__":

    app = LifeOSApp()
    app.mainloop()