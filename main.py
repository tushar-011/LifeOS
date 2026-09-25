import customtkinter as ctk

from ui.dashboard import DashboardPage


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LifeOSApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("LifeOS")
        self.geometry("1350x780")
        self.minsize(1100, 650)

        self.sidebar_open = True

        # Main window grid
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

        self.topbar.grid_columnconfigure(1, weight=1)

        # Menu button
        self.menu_button = ctk.CTkButton(
            self.topbar,
            text="☰",
            width=45,
            height=40,
            command=self.toggle_sidebar
        )

        self.menu_button.grid(
            row=0,
            column=0,
            padx=(15, 10),
            pady=10
        )

        # App title
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

        # Theme switch
        self.theme_switch = ctk.CTkSwitch(
            self.topbar,
            text="Dark Mode",
            command=self.toggle_theme
        )

        self.theme_switch.select()

        self.theme_switch.grid(
            row=0,
            column=2,
            padx=20
        )

    # -------------------------------------------------
    # SIDEBAR
    # -------------------------------------------------

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )

        self.sidebar.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        self.sidebar.grid_columnconfigure(0, weight=1)

        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Tasks", lambda: self.show_placeholder("Tasks")),
            ("Planner", lambda: self.show_placeholder("Planner")),
            ("Focus", lambda: self.show_placeholder("Focus Mode")),
            ("Pomodoro", lambda: self.show_placeholder("Pomodoro")),
            ("Stopwatch", lambda: self.show_placeholder("Stopwatch")),
            ("Notes", lambda: self.show_placeholder("Notes")),
            ("Analytics", lambda: self.show_placeholder("Analytics")),
            ("History", lambda: self.show_placeholder("History")),
            ("Reports", lambda: self.show_placeholder("Reports")),
            ("Settings", lambda: self.show_placeholder("Settings"))
        ]

        row = 0

        for text, command in nav_items:

            button = ctk.CTkButton(
                self.sidebar,
                text=text,
                height=42,
                anchor="w",
                corner_radius=8,
                command=command
            )

            button.grid(
                row=row,
                column=0,
                padx=15,
                pady=5,
                sticky="ew"
            )

            row += 1

    # -------------------------------------------------
    # CONTENT AREA
    # -------------------------------------------------

    def create_content_area(self):

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0
        )

        self.content.grid(
            row=1,
            column=1,
            sticky="nsew"
        )

        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

    # -------------------------------------------------
    # PAGE MANAGEMENT
    # -------------------------------------------------

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):

        self.clear_content()

        dashboard = DashboardPage(self.content)

        dashboard.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    def show_placeholder(self, title):

        self.clear_content()

        frame = ctk.CTkFrame(
            self.content,
            corner_radius=0
        )

        frame.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        label = ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        )

        label.pack(
            anchor="nw",
            padx=30,
            pady=30
        )

        message = ctk.CTkLabel(
            frame,
            text=f"{title} module will be built here.",
            font=ctk.CTkFont(size=16)
        )

        message.pack(
            anchor="nw",
            padx=30
        )

    # -------------------------------------------------
    # SIDEBAR TOGGLE
    # -------------------------------------------------

    def toggle_sidebar(self):

        if self.sidebar_open:

            self.sidebar.grid_remove()
            self.sidebar_open = False

        else:

            self.sidebar.grid()
            self.sidebar_open = True

    # -------------------------------------------------
    # THEME
    # -------------------------------------------------

    def toggle_theme(self):

        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")


if __name__ == "__main__":
    app = LifeOSApp()
    app.mainloop()