from __future__ import annotations

from datetime import datetime
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk

from database.database import initialize_database
from ui.analytics import AnalyticsPage
from ui.animations import animate_sidebar
from ui.components import NavButton
from ui.dashboard import DashboardPage
from ui.focus_mode import FocusModePage
from ui.history import HistoryPage
from ui.notes import NotesPage
from ui.planner import PlannerPage
from ui.pomodoro import PomodoroPage
from ui.reports import ReportsPage
from ui.settings import SettingsPage
from ui.stopwatch import StopwatchPage
from ui.tasks import TasksPage
from ui.theme import COLORS, FONT_BODY, FONT_DISPLAY, module_accent, style_page
from utils.settings_manager import load_settings, update_setting


BASE_DIR = Path(__file__).resolve().parent
THEME_FILE = BASE_DIR / "ui" / "lifeos_theme.json"
APP_SETTINGS = load_settings()
INITIAL_THEME = APP_SETTINGS.get("appearance_mode", "Dark")

ctk.set_appearance_mode(INITIAL_THEME.lower())
ctk.set_default_color_theme(str(THEME_FILE))


class LifeOSApp(ctk.CTk):
    """Main LifeOS desktop shell.

    Important layout rule: pages always stay under grid geometry management.
    Using place() on CTkScrollableFrame can leave its internal canvas at the
    requested width instead of the available width and can also break its
    scroll region. Keeping pages gridded fixes both full-width layouts and
    native scrollbar dragging.
    """

    def __init__(self):
        super().__init__()
        initialize_database()

        self.title("LifeOS • Personal Productivity System")
        self.geometry("1450x860")
        self.minsize(980, 640)
        self.configure(fg_color=COLORS["app_bg"])

        self.sidebar_open = True
        self.sidebar_animating = False
        self.sidebar_width = 236
        self.sidebar_collapsed_width = 76
        self.sidebar_auto_collapsed = False

        self.pages = {}
        self.current_page = None
        self.nav_buttons = {}
        self._wheel_remainders = {}
        self._resize_job = None
        self._clock_job = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_topbar()
        self.create_sidebar()
        self.create_content_area()

        self.bind_all("<MouseWheel>", self.handle_mousewheel, add="+")
        self.bind_all("<Button-4>", self.handle_mousewheel, add="+")
        self.bind_all("<Button-5>", self.handle_mousewheel, add="+")
        self.bind("<Configure>", self._schedule_responsive_layout, add="+")
        self.protocol("WM_DELETE_WINDOW", self.handle_close)

        self.update_clock()
        self.after(40, self.show_dashboard)

    # ------------------------------------------------------------------
    # Focus protection
    # ------------------------------------------------------------------
    def focus_session_is_active(self):
        page = self.pages.get("Focus")
        if page is None:
            return False
        try:
            return bool(page.is_session_active())
        except Exception as error:
            print(f"Focus state error: {error}")
            return False

    def request_stop_focus(self):
        if not self.focus_session_is_active():
            return True

        answer = messagebox.askyesno(
            "Focus session active",
            "A Focus Mode session is still active.\n\n"
            "Do you want to stop focus and save the time tracked so far?",
            parent=self,
        )
        if not answer:
            return False

        page = self.pages.get("Focus")
        if page:
            try:
                page.stop_focus_session(save=True)
            except Exception as error:
                messagebox.showerror(
                    "Focus Error",
                    f"LifeOS could not stop the focus session.\n\n{error}",
                    parent=self,
                )
                return False
        return True

    def handle_close(self):
        if not self.request_stop_focus():
            return
        if self._clock_job:
            try:
                self.after_cancel(self._clock_job)
            except Exception:
                pass
        self.destroy()

    # ------------------------------------------------------------------
    # Global mouse / trackpad scrolling
    # ------------------------------------------------------------------
    def _nearest_scrollable(self, widget):
        current = widget
        while current is not None:
            if isinstance(current, ctk.CTkScrollableFrame):
                return current
            try:
                current = current.master
            except Exception:
                break
        return None

    def handle_mousewheel(self, event):
        """Route wheel/trackpad movement to the scrollable frame under cursor.

        The physical scrollbar remains fully usable even when a trackpad does
        not emit useful wheel events on a particular Windows driver.
        """
        try:
            hovered = self.winfo_containing(event.x_root, event.y_root)
            scrollable = self._nearest_scrollable(hovered)
            if scrollable is None:
                return None

            canvas = scrollable._parent_canvas

            if getattr(event, "num", None) == 4:
                units = -2
            elif getattr(event, "num", None) == 5:
                units = 2
            else:
                delta = getattr(event, "delta", 0)
                if not delta:
                    return None

                key = str(canvas)
                remainder = self._wheel_remainders.get(key, 0.0)
                remainder += (-delta / 48.0)
                units = int(remainder)
                self._wheel_remainders[key] = remainder - units

                if units == 0:
                    return "break"

            canvas.yview_scroll(
                units,
                "units"
            )

            return "break"

        except Exception as error:
            print(f"Scrolling error: {error}")
            return None

    # ------------------------------------------------------------------
    # Top bar
    # ------------------------------------------------------------------
    def create_topbar(self):
        self.topbar = ctk.CTkFrame(
            self,
            height=70,
            corner_radius=0,
            fg_color=COLORS["topbar"],
        )
        self.topbar.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew"
        )
        self.topbar.grid_propagate(False)
        self.topbar.grid_columnconfigure(
            3,
            weight=1
        )

        self.menu_button = ctk.CTkButton(
            self.topbar,
            text="☰",
            width=42,
            height=42,
            corner_radius=12,
            fg_color=COLORS["surface_soft"],
            hover_color=COLORS["border"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=19,
                weight="bold"
            ),
            command=self.toggle_sidebar,
        )
        self.menu_button.grid(
            row=0,
            column=0,
            padx=(16, 10),
            pady=14
        )

        brand = ctk.CTkFrame(
            self.topbar,
            fg_color="transparent"
        )
        brand.grid(
            row=0,
            column=1,
            sticky="w"
        )

        self.brand_mark = ctk.CTkFrame(
            brand,
            width=8,
            height=38,
            corner_radius=100,
            fg_color=module_accent("Dashboard"),
        )
        self.brand_mark.pack(
            side="left",
            padx=(0, 10)
        )

        brand_text = ctk.CTkFrame(
            brand,
            fg_color="transparent"
        )
        brand_text.pack(
            side="left"
        )

        ctk.CTkLabel(
            brand_text,
            text="LifeOS",
            text_color=COLORS["text"],
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=22,
                weight="bold"
            ),
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            brand_text,
            text="Productivity Workspace",
            text_color=COLORS["muted"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10
            ),
        ).pack(
            anchor="w"
        )

        self.page_pill = ctk.CTkFrame(
            self.topbar,
            corner_radius=100,
            fg_color=COLORS["surface_soft"],
        )
        self.page_pill.grid(
            row=0,
            column=2,
            padx=(26, 10),
            pady=18
        )

        self.page_dot = ctk.CTkFrame(
            self.page_pill,
            width=8,
            height=8,
            corner_radius=100,
            fg_color=module_accent("Dashboard"),
        )
        self.page_dot.pack(
            side="left",
            padx=(11, 6),
            pady=8
        )

        self.page_hint = ctk.CTkLabel(
            self.page_pill,
            text="Dashboard",
            text_color=COLORS["text"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold"
            ),
        )
        self.page_hint.pack(
            side="left",
            padx=(0, 11),
            pady=6
        )

        clock_area = ctk.CTkFrame(
            self.topbar,
            fg_color="transparent"
        )
        clock_area.grid(
            row=0,
            column=4,
            sticky="e",
            padx=(8, 12)
        )

        self.clock_label = ctk.CTkLabel(
            clock_area,
            text="",
            text_color=COLORS["text"],
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=14,
                weight="bold"
            ),
        )
        self.clock_label.pack(
            anchor="e"
        )

        self.date_label = ctk.CTkLabel(
            clock_area,
            text="",
            text_color=COLORS["muted"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10
            ),
        )
        self.date_label.pack(
            anchor="e"
        )

        self.theme_switch = ctk.CTkSwitch(
            self.topbar,
            text="Dark",
            width=80,
            command=self.toggle_theme,
            progress_color=COLORS["violet"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold"
            ),
        )
        self.theme_switch.grid(
            row=0,
            column=5,
            padx=(4, 18)
        )

        self.sync_theme_controls()

    def update_clock(self):
        now = datetime.now()

        try:
            self.clock_label.configure(
                text=now.strftime("%I:%M %p")
            )

            self.date_label.configure(
                text=now.strftime("%A, %d %B %Y")
            )

        except Exception:
            return

        self._clock_job = self.after(
            1000,
            self.update_clock
        )

    # ------------------------------------------------------------------
    # Sidebar
    # ------------------------------------------------------------------
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=self.sidebar_width,
            corner_radius=0,
            fg_color=COLORS["sidebar"],
        )

        self.sidebar.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        self.sidebar.grid_columnconfigure(
            0,
            weight=1
        )

        self.sidebar_header = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        self.sidebar_header.grid(
            row=0,
            column=0,
            padx=14,
            pady=(18, 12),
            sticky="ew"
        )

        self.sidebar_logo = ctk.CTkFrame(
            self.sidebar_header,
            width=42,
            height=42,
            corner_radius=13,
            fg_color=COLORS["violet"],
        )

        self.sidebar_logo.pack(
            side="left"
        )

        self.sidebar_logo.pack_propagate(
            False
        )

        ctk.CTkLabel(
            self.sidebar_logo,
            text="L",
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=18,
                weight="bold"
            ),
        ).pack(
            expand=True
        )

        self.sidebar_header_text = ctk.CTkFrame(
            self.sidebar_header,
            fg_color="transparent"
        )

        self.sidebar_header_text.pack(
            side="left",
            padx=(10, 0)
        )

        ctk.CTkLabel(
            self.sidebar_header_text,
            text="Workspace",
            text_color=COLORS["text"],
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=15,
                weight="bold"
            ),
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            self.sidebar_header_text,
            text="Stay organized",
            text_color=COLORS["muted"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10
            ),
        ).pack(
            anchor="w"
        )

        self.nav_label = ctk.CTkLabel(
            self.sidebar,
            text="NAVIGATION",
            anchor="w",
            text_color=COLORS["subtle"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=9,
                weight="bold"
            ),
        )

        self.nav_label.grid(
            row=1,
            column=0,
            padx=22,
            pady=(3, 8),
            sticky="ew"
        )

        navigation = [
            ("Dashboard", "⌂", self.show_dashboard),
            ("Tasks", "✓", self.show_tasks),
            ("Planner", "▦", self.show_planner),
            ("Focus", "◎", self.show_focus),
            ("Pomodoro", "◷", self.show_pomodoro),
            ("Stopwatch", "◴", self.show_stopwatch),
            ("Notes", "▤", self.show_notes),
            ("Analytics", "▥", self.show_analytics),
            ("History", "↺", self.show_history),
            ("Reports", "▧", self.show_reports),
        ]

        row = 2

        for name, icon, command in navigation:
            button = NavButton(
                self.sidebar,
                text=name,
                icon=icon,
                command=command,
                page_name=name,
            )

            button.grid(
                row=row,
                column=0,
                padx=12,
                pady=3,
                sticky="ew"
            )

            self.nav_buttons[name] = button

            row += 1

        self.sidebar.grid_rowconfigure(
            row,
            weight=1
        )

        self.sidebar_status = ctk.CTkFrame(
            self.sidebar,
            corner_radius=14,
            fg_color=COLORS["surface_alt"],
            border_width=1,
            border_color=COLORS["border_soft"],
        )

        self.sidebar_status.grid(
            row=row + 1,
            column=0,
            padx=12,
            pady=(8, 8),
            sticky="ew"
        )

        ctk.CTkLabel(
            self.sidebar_status,
            text="●  Offline • Local Data",
            text_color=COLORS["emerald"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold"
            ),
        ).pack(
            anchor="w",
            padx=12,
            pady=10
        )

        self.settings_button = NavButton(
            self.sidebar,
            text="Settings",
            icon="⚙",
            command=self.show_settings,
            page_name="Settings",
        )

        self.settings_button.grid(
            row=row + 2,
            column=0,
            padx=12,
            pady=(0, 14),
            sticky="ew"
        )

        self.nav_buttons["Settings"] = (
            self.settings_button
        )

    # ------------------------------------------------------------------
    # Content / page management
    # ------------------------------------------------------------------
    def create_content_area(self):
        self.content = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=COLORS["app_bg"],
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

    def hide_all_pages(self):
        for page in self.pages.values():
            try:
                page.grid_remove()
            except Exception:
                pass

    def update_active_navigation(
        self,
        page_name
    ):
        for name, button in self.nav_buttons.items():
            button.set_active(
                name == page_name
            )

        accent = module_accent(
            page_name
        )

        self.brand_mark.configure(
            fg_color=accent
        )

        self.page_dot.configure(
            fg_color=accent
        )

        self.page_hint.configure(
            text=page_name
        )

    def show_page(
        self,
        page_name,
        page_class
    ):
        if (
            self.current_page == "Focus"
            and page_name != "Focus"
            and self.focus_session_is_active()
            and not self.request_stop_focus()
        ):
            return

        self.hide_all_pages()

        if page_name not in self.pages:
            page = page_class(
                self.content
            )

            # Keep scrollable pages under grid management permanently.
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

            page.grid(
                row=0,
                column=0,
                sticky="nsew"
            )

        self.current_page = (
            page_name
        )

        self.update_active_navigation(
            page_name
        )

        self.refresh_page(
            page_name,
            page
        )

        try:
            style_page(
                page,
                page_name
            )

        except Exception as error:
            print(
                f"Styling error on {page_name}: {error}"
            )

        # Force CTkScrollableFrame to recalculate its canvas scroll region
        # and width after navigation or a sidebar resize.
        self.after_idle(
            lambda p=page:
            self._refresh_page_geometry(
                p
            )
        )

    def _refresh_page_geometry(
        self,
        page
    ):
        try:
            page.update_idletasks()

            if isinstance(
                page,
                ctk.CTkScrollableFrame
            ):
                page._parent_canvas.configure(
                    scrollregion=(
                        page._parent_canvas.bbox(
                            "all"
                        )
                    )
                )

        except Exception:
            pass

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

            elif page_name == "Focus":
                if not page.is_session_active():
                    page.load_tasks()

                page.load_statistics()
                page.load_history()

            elif page_name == "Pomodoro":
                page.load_statistics()
                page.load_history()

            elif page_name == "Stopwatch":
                page.load_statistics()
                page.load_history()

            elif page_name == "Analytics":
                page.refresh_analytics()

            elif page_name == "History":
                page.refresh_history()

            elif page_name == "Reports":
                page.refresh_reports()

            elif page_name == "Settings":
                page.refresh_settings()

        except Exception as error:
            print(
                f"Error refreshing {page_name}: {error}"
            )

    # ------------------------------------------------------------------
    # Public navigation methods
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Sidebar animation / responsive shell
    # ------------------------------------------------------------------
    def toggle_sidebar(
        self,
        automatic=False
    ):
        if self.sidebar_animating:
            return

        self.sidebar_animating = True

        opening = not self.sidebar_open

        start = (
            self.sidebar_collapsed_width
            if opening
            else self.sidebar_width
        )

        end = (
            self.sidebar_width
            if opening
            else self.sidebar_collapsed_width
        )

        if not opening:
            self._hide_sidebar_text()

        def done():
            self.sidebar_open = opening
            self.sidebar_animating = False

            if opening:
                self._show_sidebar_text()

            if not automatic:
                self.sidebar_auto_collapsed = False

            if self.current_page in self.pages:
                self.after_idle(
                    lambda:
                    self._refresh_page_geometry(
                        self.pages[
                            self.current_page
                        ]
                    )
                )

        animate_sidebar(
            self.sidebar,
            start=start,
            end=end,
            duration_ms=180,
            steps=12,
            on_done=done,
        )

    def _hide_sidebar_text(self):
        for button in self.nav_buttons.values():
            button.collapse()

        try:
            self.sidebar_header_text.pack_forget()
            self.nav_label.grid_remove()
            self.sidebar_status.grid_remove()

        except Exception:
            pass

    def _show_sidebar_text(self):
        for button in self.nav_buttons.values():
            button.expand()

        try:
            if not self.sidebar_header_text.winfo_manager():
                self.sidebar_header_text.pack(
                    side="left",
                    padx=(10, 0)
                )

            self.nav_label.grid()
            self.sidebar_status.grid()

        except Exception:
            pass

    def _schedule_responsive_layout(
        self,
        event
    ):
        if event.widget is not self:
            return

        if self._resize_job:
            try:
                self.after_cancel(
                    self._resize_job
                )
            except Exception:
                pass

        self._resize_job = self.after(
            120,
            self._apply_responsive_layout
        )

    def _apply_responsive_layout(self):
        self._resize_job = None

        width = self.winfo_width()

        # Keep enough horizontal room for Planner
        # and two-column timer pages.
        if (
            width < 1220
            and self.sidebar_open
            and not self.sidebar_animating
        ):
            self.sidebar_auto_collapsed = True
            self.toggle_sidebar(
                automatic=True
            )

        elif (
            width > 1380
            and not self.sidebar_open
            and self.sidebar_auto_collapsed
            and not self.sidebar_animating
        ):
            self.toggle_sidebar(
                automatic=True
            )

        planner = self.pages.get(
            "Planner"
        )

        if (
            planner
            and hasattr(
                planner,
                "apply_responsive_layout"
            )
        ):
            planner.apply_responsive_layout(
                width
            )

    # ------------------------------------------------------------------
    # Theme
    # ------------------------------------------------------------------
    def sync_theme_controls(self):
        theme = (
            load_settings()
            .get(
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
            if (
                ctk.get_appearance_mode()
                == "Dark"
            ):
                self.theme_switch.select()
            else:
                self.theme_switch.deselect()

            self.theme_switch.configure(
                text="System"
            )

    def toggle_theme(self):
        theme = (
            "Dark"
            if self.theme_switch.get()
            else "Light"
        )

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

        for (
            page_name,
            page
        ) in self.pages.items():
            try:
                style_page(
                    page,
                    page_name
                )
            except Exception:
                pass

        settings_page = (
            self.pages.get(
                "Settings"
            )
        )

        if settings_page:
            try:
                settings_page.refresh_settings()
            except Exception:
                pass


if __name__ == "__main__":
    app = LifeOSApp()
    app.mainloop()