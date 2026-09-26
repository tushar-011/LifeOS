from __future__ import annotations

import os

import customtkinter as ctk

from tkinter import (
    filedialog,
    messagebox,
)

from utils.settings_manager import (
    load_settings,
    update_setting,
    reset_settings,
    backup_database,
    restore_database,
    get_database_path,
    get_settings_path,
    get_default_export_path,
)

from ui.theme import (
    COLORS,
    FONT_BODY,
    FONT_DISPLAY,
    module_accent,
    module_accent_hover,
)


# =================================================
# SETTINGS PAGE
# =================================================

class SettingsPage(ctk.CTkScrollableFrame):

    def __init__(
        self,
        parent
    ):

        super().__init__(
            parent,
            corner_radius=0,
            fg_color=COLORS["app_bg"],
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        # =================================================
        # SETTINGS
        # =================================================

        self.settings = (
            load_settings()
        )

        self.accent = (
            module_accent(
                "Settings"
            )
        )

        self.accent_hover = (
            module_accent_hover(
                "Settings"
            )
        )

        # =================================================
        # RESPONSIVE STATE
        # =================================================

        self._compact_layout = None
        self._resize_job = None

        # =================================================
        # BUILD
        # =================================================

        self.create_workspace()

        self.create_header()

        self.create_preferences_area()

        self.create_data_section()

        self.create_about_section()

        # =================================================
        # RESPONSIVE
        # =================================================

        self.workspace.bind(
            "<Configure>",
            self._schedule_layout_check,
            add="+",
        )

        self.after(
            120,
            self.apply_responsive_layout
        )

    # =================================================
    # WORKSPACE
    # =================================================

    def create_workspace(
        self
    ):

        self.workspace = (
            ctk.CTkFrame(
                self,
                fg_color="transparent",
            )
        )

        self.workspace.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=30,
            pady=(0, 32),
        )

        self.workspace.grid_columnconfigure(
            0,
            weight=1
        )

    # =================================================
    # HEADER
    # =================================================

    def create_header(
        self
    ):

        self.header = (
            ctk.CTkFrame(
                self.workspace,
                fg_color="transparent",
            )
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(26, 18),
        )

        self.header.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # LEFT
        # ---------------------------------------------

        left = (
            ctk.CTkFrame(
                self.header,
                fg_color="transparent",
            )
        )

        left.grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            left,
            text="Settings",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=31,
                weight="bold",
            ),
            text_color=self.accent,
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            left,
            text=(
                "Customize LifeOS and manage "
                "your local application data."
            ),
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=13,
            ),
            text_color=COLORS["muted"],
        ).pack(
            anchor="w",
            pady=(5, 0),
        )

        # ---------------------------------------------
        # OFFLINE BADGE
        # ---------------------------------------------

        badge = (
            ctk.CTkFrame(
                self.header,
                corner_radius=100,
                fg_color=COLORS["surface_soft"],
            )
        )

        badge.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(15, 0),
        )

        dot = (
            ctk.CTkFrame(
                badge,
                width=8,
                height=8,
                corner_radius=100,
                fg_color=COLORS["emerald"],
            )
        )

        dot.pack(
            side="left",
            padx=(11, 6),
            pady=9,
        )

        ctk.CTkLabel(
            badge,
            text="Local & Offline",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold",
            ),
            text_color=COLORS["text"],
        ).pack(
            side="left",
            padx=(0, 11),
            pady=7,
        )

    # =================================================
    # PREFERENCES AREA
    # =================================================

    def create_preferences_area(
        self
    ):

        self.preferences_area = (
            ctk.CTkFrame(
                self.workspace,
                fg_color="transparent",
            )
        )

        self.preferences_area.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 14),
        )

        self.preferences_area.grid_columnconfigure(
            0,
            weight=1
        )

        self.preferences_area.grid_columnconfigure(
            1,
            weight=1
        )

        self.create_appearance_section()

        self.create_export_section()

    # =================================================
    # APPEARANCE
    # =================================================

    def create_appearance_section(
        self
    ):

        self.appearance_card = (
            ctk.CTkFrame(
                self.preferences_area,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"],
            )
        )

        self.appearance_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 7),
        )

        self.appearance_card.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        header = (
            ctk.CTkFrame(
                self.appearance_card,
                fg_color="transparent",
            )
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(19, 8),
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        left = (
            ctk.CTkFrame(
                header,
                fg_color="transparent",
            )
        )

        left.grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            left,
            text="Appearance",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=19,
                weight="bold",
            ),
            text_color=COLORS["text"],
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            left,
            text="Choose how LifeOS looks.",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
            ),
            text_color=COLORS["muted"],
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        icon_box = (
            ctk.CTkFrame(
                header,
                width=38,
                height=38,
                corner_radius=11,
                fg_color=self.accent,
            )
        )

        icon_box.grid(
            row=0,
            column=1,
            sticky="e",
        )

        icon_box.grid_propagate(
            False
        )

        ctk.CTkLabel(
            icon_box,
            text="◐",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=17,
                weight="bold",
            ),
            text_color=COLORS["white"],
        ).place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

        # ---------------------------------------------
        # CONTROL
        # ---------------------------------------------

        control = (
            ctk.CTkFrame(
                self.appearance_card,
                corner_radius=13,
                fg_color=COLORS["surface_alt"],
                border_width=1,
                border_color=COLORS["border_soft"],
            )
        )

        control.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=(7, 20),
        )

        control.grid_columnconfigure(
            0,
            weight=1
        )

        text_area = (
            ctk.CTkFrame(
                control,
                fg_color="transparent",
            )
        )

        text_area.grid(
            row=0,
            column=0,
            sticky="w",
            padx=14,
            pady=14,
        )

        ctk.CTkLabel(
            text_area,
            text="Application Theme",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold",
            ),
            text_color=COLORS["text"],
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            text_area,
            text="Dark, Light or system default",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=9,
            ),
            text_color=COLORS["muted"],
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        self.theme_menu = (
            ctk.CTkOptionMenu(
                control,
                values=[
                    "Dark",
                    "Light",
                    "System",
                ],
                width=150,
                height=38,
                command=self.change_theme,
            )
        )

        self.theme_menu.set(
            self.settings.get(
                "appearance_mode",
                "Dark",
            )
        )

        self.theme_menu.grid(
            row=0,
            column=1,
            sticky="e",
            padx=14,
            pady=14,
        )

    # =================================================
    # CHANGE THEME
    # =================================================

    def change_theme(
        self,
        value
    ):

        update_setting(
            "appearance_mode",
            value,
        )

        self.settings[
            "appearance_mode"
        ] = value

        ctk.set_appearance_mode(
            value.lower()
        )

        app = (
            self.winfo_toplevel()
        )

        if hasattr(
            app,
            "sync_theme_controls"
        ):

            app.sync_theme_controls()

    # =================================================
    # EXPORTS
    # =================================================

    def create_export_section(
        self
    ):

        self.export_card = (
            ctk.CTkFrame(
                self.preferences_area,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"],
            )
        )

        self.export_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(7, 0),
        )

        self.export_card.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        header = (
            ctk.CTkFrame(
                self.export_card,
                fg_color="transparent",
            )
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(19, 8),
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        left = (
            ctk.CTkFrame(
                header,
                fg_color="transparent",
            )
        )

        left.grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            left,
            text="Exports",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=19,
                weight="bold",
            ),
            text_color=COLORS["text"],
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            left,
            text="Default report export location.",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
            ),
            text_color=COLORS["muted"],
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        icon_box = (
            ctk.CTkFrame(
                header,
                width=38,
                height=38,
                corner_radius=11,
                fg_color=COLORS["amber"],
            )
        )

        icon_box.grid(
            row=0,
            column=1,
            sticky="e",
        )

        icon_box.grid_propagate(
            False
        )

        ctk.CTkLabel(
            icon_box,
            text="↗",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=17,
                weight="bold",
            ),
            text_color=COLORS["white"],
        ).place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

        # ---------------------------------------------
        # PATH
        # ---------------------------------------------

        path_frame = (
            ctk.CTkFrame(
                self.export_card,
                corner_radius=13,
                fg_color=COLORS["surface_alt"],
                border_width=1,
                border_color=COLORS["border_soft"],
            )
        )

        path_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=(7, 10),
        )

        path_frame.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            path_frame,
            text="EXPORT FOLDER",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=8,
                weight="bold",
            ),
            text_color=COLORS["amber"],
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=14,
            pady=(11, 2),
        )

        self.export_path_label = (
            ctk.CTkLabel(
                path_frame,
                text=self.settings.get(
                    "export_folder",
                    get_default_export_path(),
                ),
                anchor="w",
                justify="left",
                wraplength=420,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                ),
                text_color=COLORS["text"],
            )
        )

        self.export_path_label.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=14,
            pady=(0, 11),
        )

        # ---------------------------------------------
        # ACTIONS
        # ---------------------------------------------

        actions = (
            ctk.CTkFrame(
                self.export_card,
                fg_color="transparent",
            )
        )

        actions.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 20),
        )

        actions.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkButton(
            actions,
            text="Choose Folder",
            height=38,
            corner_radius=10,
            fg_color=COLORS["amber"],
            hover_color=COLORS["amber_hover"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold",
            ),
            command=self.choose_export_folder,
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5),
        )

        ctk.CTkButton(
            actions,
            text="Open Folder",
            width=110,
            height=38,
            corner_radius=10,
            fg_color=COLORS["surface_soft"],
            hover_color=COLORS["border"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold",
            ),
            command=self.open_export_folder,
        ).grid(
            row=0,
            column=1,
            sticky="e",
            padx=(5, 0),
        )

    # =================================================
    # CHOOSE EXPORT FOLDER
    # =================================================

    def choose_export_folder(
        self
    ):

        current_folder = (
            self.settings.get(
                "export_folder",
                get_default_export_path(),
            )
        )

        folder = (
            filedialog.askdirectory(
                parent=self,
                title="Choose LifeOS Export Folder",
                initialdir=current_folder,
            )
        )

        if not folder:

            return

        update_setting(
            "export_folder",
            folder,
        )

        self.settings[
            "export_folder"
        ] = folder

        self.export_path_label.configure(
            text=folder
        )

        self.refresh_storage_info()

    # =================================================
    # OPEN EXPORT FOLDER
    # =================================================

    def open_export_folder(
        self
    ):

        folder = (
            self.settings.get(
                "export_folder",
                get_default_export_path(),
            )
        )

        try:

            os.makedirs(
                folder,
                exist_ok=True,
            )

            if os.name == "nt":

                os.startfile(
                    folder
                )

            else:

                messagebox.showinfo(
                    "Export Folder",
                    folder,
                    parent=self,
                )

        except Exception as error:

            messagebox.showerror(
                "Folder Error",
                (
                    "The export folder could "
                    "not be opened.\n\n"
                    f"{error}"
                ),
                parent=self,
            )

    # =================================================
    # DATA MANAGEMENT
    # =================================================

    def create_data_section(
        self
    ):

        self.data_card = (
            ctk.CTkFrame(
                self.workspace,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"],
            )
        )

        self.data_card.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 14),
        )

        self.data_card.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        header = (
            ctk.CTkFrame(
                self.data_card,
                fg_color="transparent",
            )
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=22,
            pady=(20, 10),
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        left = (
            ctk.CTkFrame(
                header,
                fg_color="transparent",
            )
        )

        left.grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            left,
            text="Data Management",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=20,
                weight="bold",
            ),
            text_color=COLORS["text"],
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            left,
            text=(
                "Back up, restore and manage "
                "your locally stored LifeOS data."
            ),
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
            ),
            text_color=COLORS["muted"],
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        database_badge = (
            ctk.CTkFrame(
                header,
                corner_radius=100,
                fg_color=COLORS["surface_soft"],
            )
        )

        database_badge.grid(
            row=0,
            column=1,
            sticky="e",
        )

        ctk.CTkLabel(
            database_badge,
            text="SQLite Database",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=9,
                weight="bold",
            ),
            text_color=COLORS["emerald"],
        ).pack(
            padx=11,
            pady=6,
        )

        # =================================================
        # STORAGE PATHS
        # =================================================

        self.storage_area = (
            ctk.CTkFrame(
                self.data_card,
                fg_color="transparent",
            )
        )

        self.storage_area.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=22,
            pady=(5, 12),
        )

        self.storage_area.grid_columnconfigure(
            0,
            weight=1
        )

        self.storage_area.grid_columnconfigure(
            1,
            weight=1
        )

        # ---------------------------------------------
        # DATABASE PATH
        # ---------------------------------------------

        self.database_path_card = (
            self.create_path_card(
                self.storage_area,
                column=0,
                title="DATABASE",
                value=get_database_path(),
                accent=COLORS["emerald"],
                padx=(0, 6),
            )
        )

        # ---------------------------------------------
        # SETTINGS PATH
        # ---------------------------------------------

        self.settings_path_card = (
            self.create_path_card(
                self.storage_area,
                column=1,
                title="SETTINGS",
                value=get_settings_path(),
                accent=COLORS["indigo"],
                padx=(6, 0),
            )
        )

        # =================================================
        # ACTIONS
        # =================================================

        actions = (
            ctk.CTkFrame(
                self.data_card,
                fg_color="transparent",
            )
        )

        actions.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=22,
            pady=(2, 21),
        )

        actions.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # LEFT ACTIONS
        # ---------------------------------------------

        left_actions = (
            ctk.CTkFrame(
                actions,
                fg_color="transparent",
            )
        )

        left_actions.grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkButton(
            left_actions,
            text="Backup Database",
            width=150,
            height=40,
            corner_radius=11,
            fg_color=COLORS["emerald"],
            hover_color=COLORS["emerald_hover"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold",
            ),
            command=self.backup_data,
        ).pack(
            side="left",
            padx=(0, 7),
        )

        ctk.CTkButton(
            left_actions,
            text="Restore Database",
            width=150,
            height=40,
            corner_radius=11,
            fg_color=COLORS["indigo"],
            hover_color=COLORS["indigo_hover"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold",
            ),
            command=self.restore_data,
        ).pack(
            side="left",
        )

        # ---------------------------------------------
        # RESET
        # ---------------------------------------------

        self.reset_button = (
            ctk.CTkButton(
                actions,
                text="Reset Settings",
                width=130,
                height=40,
                corner_radius=11,
                fg_color=COLORS["surface_soft"],
                hover_color=COLORS["border"],
                border_width=1,
                border_color=COLORS["danger"],
                text_color=COLORS["danger"],
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=11,
                    weight="bold",
                ),
                command=self.reset_app_settings,
            )
        )

        self.reset_button.grid(
            row=0,
            column=1,
            sticky="e",
        )

    # =================================================
    # PATH CARD
    # =================================================

    def create_path_card(
        self,
        parent,
        column,
        title,
        value,
        accent,
        padx,
    ):

        card = (
            ctk.CTkFrame(
                parent,
                corner_radius=13,
                fg_color=COLORS["surface_alt"],
                border_width=1,
                border_color=COLORS["border_soft"],
            )
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=padx,
        )

        card.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=8,
                weight="bold",
            ),
            text_color=accent,
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=14,
            pady=(12, 3),
        )

        label = (
            ctk.CTkLabel(
                card,
                text=value,
                anchor="w",
                justify="left",
                wraplength=470,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                ),
                text_color=COLORS["text"],
            )
        )

        label.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=14,
            pady=(0, 13),
        )

        card.path_label = label

        return card

    # =================================================
    # BACKUP
    # =================================================

    def backup_data(
        self
    ):

        filename = (
            "LifeOS_Backup.db"
        )

        file_path = (
            filedialog.asksaveasfilename(
                parent=self,
                title="Backup LifeOS Database",
                defaultextension=".db",
                initialfile=filename,
                filetypes=[
                    (
                        "SQLite Database",
                        "*.db",
                    )
                ],
            )
        )

        if not file_path:

            return

        try:

            backup_database(
                file_path
            )

            messagebox.showinfo(
                "Backup Complete",
                (
                    "Your LifeOS database was "
                    "backed up successfully."
                ),
                parent=self,
            )

        except Exception as error:

            messagebox.showerror(
                "Backup Error",
                (
                    "The database could not "
                    "be backed up.\n\n"
                    f"{error}"
                ),
                parent=self,
            )

    # =================================================
    # RESTORE
    # =================================================

    def restore_data(
        self
    ):

        file_path = (
            filedialog.askopenfilename(
                parent=self,
                title="Restore LifeOS Database",
                filetypes=[
                    (
                        "SQLite Database",
                        "*.db",
                    )
                ],
            )
        )

        if not file_path:

            return

        confirm = (
            messagebox.askyesno(
                "Restore Database",
                (
                    "Restoring a database will "
                    "replace the current LifeOS data.\n\n"
                    "A safety backup of the current "
                    "database will be created automatically.\n\n"
                    "Continue?"
                ),
                parent=self,
            )
        )

        if not confirm:

            return

        try:

            restore_database(
                file_path
            )

            messagebox.showinfo(
                "Restore Complete",
                (
                    "The database was restored "
                    "successfully.\n\n"
                    "Restart LifeOS to ensure all "
                    "pages reload the restored data."
                ),
                parent=self,
            )

        except Exception as error:

            messagebox.showerror(
                "Restore Error",
                (
                    "The database could not "
                    "be restored.\n\n"
                    f"{error}"
                ),
                parent=self,
            )

    # =================================================
    # RESET SETTINGS
    # =================================================

    def reset_app_settings(
        self
    ):

        confirm = (
            messagebox.askyesno(
                "Reset Settings",
                (
                    "Reset LifeOS settings "
                    "to their default values?"
                ),
                parent=self,
            )
        )

        if not confirm:

            return

        self.settings = (
            reset_settings()
        )

        theme = (
            self.settings[
                "appearance_mode"
            ]
        )

        ctk.set_appearance_mode(
            theme.lower()
        )

        self.theme_menu.set(
            theme
        )

        self.export_path_label.configure(
            text=self.settings[
                "export_folder"
            ]
        )

        self.refresh_storage_info()

        app = (
            self.winfo_toplevel()
        )

        if hasattr(
            app,
            "sync_theme_controls"
        ):

            app.sync_theme_controls()

        messagebox.showinfo(
            "Settings Reset",
            (
                "LifeOS settings were "
                "restored to defaults."
            ),
            parent=self,
        )

    # =================================================
    # ABOUT
    # =================================================

    def create_about_section(
        self
    ):

        self.about_card = (
            ctk.CTkFrame(
                self.workspace,
                corner_radius=18,
                fg_color=COLORS["surface"],
                border_width=1,
                border_color=COLORS["border"],
            )
        )

        self.about_card.grid(
            row=3,
            column=0,
            sticky="ew",
        )

        self.about_card.grid_columnconfigure(
            0,
            weight=1
        )

        # =================================================
        # ABOUT HEADER
        # =================================================

        header = (
            ctk.CTkFrame(
                self.about_card,
                fg_color="transparent",
            )
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=24,
            pady=(22, 15),
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        left = (
            ctk.CTkFrame(
                header,
                fg_color="transparent",
            )
        )

        left.grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            left,
            text="About LifeOS",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=23,
                weight="bold",
            ),
            text_color=COLORS["text"],
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            left,
            text="Personal Productivity Management System",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold",
            ),
            text_color=self.accent,
        ).pack(
            anchor="w",
            pady=(3, 0),
        )

        version = (
            self.settings.get(
                "app_version",
                "1.0.0",
            )
        )

        version_badge = (
            ctk.CTkFrame(
                header,
                corner_radius=100,
                fg_color=self.accent,
            )
        )

        version_badge.grid(
            row=0,
            column=1,
            sticky="e",
        )

        ctk.CTkLabel(
            version_badge,
            text=f"Version {version}",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=9,
                weight="bold",
            ),
            text_color=COLORS["white"],
        ).pack(
            padx=12,
            pady=6,
        )

        # =================================================
        # ABOUT GRID
        # =================================================

        self.about_grid = (
            ctk.CTkFrame(
                self.about_card,
                fg_color="transparent",
            )
        )

        self.about_grid.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 14),
        )

        self.about_grid.grid_columnconfigure(
            0,
            weight=1
        )

        self.about_grid.grid_columnconfigure(
            1,
            weight=1
        )

        # ---------------------------------------------
        # OVERVIEW
        # ---------------------------------------------

        self.about_overview = (
            self.create_about_panel(
                self.about_grid,
                row=0,
                column=0,
                title="Overview",
                accent=COLORS["violet"],
                content=(
                    "LifeOS is an offline desktop productivity "
                    "application that combines task management, "
                    "planning, focus tracking, time management, "
                    "notes, analytics, history and reporting.\n\n"
                    "The core application works locally without "
                    "requiring an internet connection, cloud "
                    "service or LifeOS account."
                ),
                padx=(0, 6),
            )
        )

        # ---------------------------------------------
        # PRODUCTIVITY
        # ---------------------------------------------

        self.about_productivity = (
            self.create_about_panel(
                self.about_grid,
                row=0,
                column=1,
                title="Productivity Score",
                accent=COLORS["cyan"],
                content=(
                    "The LifeOS productivity score is based on "
                    "measurable application activity rather than "
                    "an unexplained rating.\n\n"
                    "Tasks contribute 50%, tracked Focus time "
                    "contributes 30%, and Planner completion "
                    "contributes 20%."
                ),
                padx=(6, 0),
            )
        )

        # ---------------------------------------------
        # MODULES
        # ---------------------------------------------

        self.about_modules = (
            self.create_about_panel(
                self.about_grid,
                row=1,
                column=0,
                title="Core Modules",
                accent=COLORS["emerald"],
                content=(
                    "Dashboard • Task Manager • Notes • Planner\n\n"
                    "Focus Mode • Pomodoro • Stopwatch\n\n"
                    "Analytics • History • Reports • Settings"
                ),
                padx=(0, 6),
                pady=(12, 0),
            )
        )

        # ---------------------------------------------
        # STACK
        # ---------------------------------------------

        self.about_stack = (
            self.create_about_panel(
                self.about_grid,
                row=1,
                column=1,
                title="Technology Stack",
                accent=COLORS["amber"],
                content=(
                    "Python 3\n"
                    "CustomTkinter / Tkinter\n"
                    "SQLite\n"
                    "Matplotlib & Seaborn\n"
                    "Pillow\n"
                    "JSON configuration\n"
                    "PyInstaller packaging target"
                ),
                padx=(6, 0),
                pady=(12, 0),
            )
        )

        # ---------------------------------------------
        # PRIVACY
        # ---------------------------------------------

        self.about_privacy = (
            self.create_about_panel(
                self.about_grid,
                row=2,
                column=0,
                title="Offline Data & Privacy",
                accent=COLORS["indigo"],
                content=(
                    "Tasks, planner activities, notes, Focus "
                    "sessions, Pomodoro sessions, Stopwatch "
                    "sessions and related history are stored "
                    "inside a local SQLite database.\n\n"
                    "Core LifeOS functionality does not require "
                    "remote storage or cloud synchronization."
                ),
                padx=(0, 6),
                pady=(12, 0),
            )
        )

        # ---------------------------------------------
        # PURPOSE
        # ---------------------------------------------

        self.about_purpose = (
            self.create_about_panel(
                self.about_grid,
                row=2,
                column=1,
                title="Project Purpose",
                accent=COLORS["coral"],
                content=(
                    "LifeOS demonstrates practical Python GUI "
                    "development, object-oriented programming, "
                    "functions, conditionals, loops, collections, "
                    "modules, exception handling, file handling, "
                    "SQLite operations and data visualization "
                    "inside one usable desktop application."
                ),
                padx=(6, 0),
                pady=(12, 0),
            )
        )

        # =================================================
        # STORAGE DETAILS
        # =================================================

        storage = (
            ctk.CTkFrame(
                self.about_card,
                corner_radius=14,
                fg_color=COLORS["surface_alt"],
                border_width=1,
                border_color=COLORS["border_soft"],
            )
        )

        storage.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15),
        )

        storage.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            storage,
            text="LOCAL STORAGE",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=8,
                weight="bold",
            ),
            text_color=self.accent,
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=16,
            pady=(13, 5),
        )

        self.storage_info_label = (
            ctk.CTkLabel(
                storage,
                text="",
                anchor="w",
                justify="left",
                wraplength=1000,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                ),
                text_color=COLORS["muted"],
            )
        )

        self.storage_info_label.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=16,
            pady=(0, 14),
        )

        # =================================================
        # FOOTER
        # =================================================

        footer = (
            ctk.CTkFrame(
                self.about_card,
                fg_color="transparent",
            )
        )

        footer.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=24,
            pady=(0, 22),
        )

        ctk.CTkLabel(
            footer,
            text=(
                "LifeOS • Local productivity, planning "
                "and focus in one place."
            ),
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold",
            ),
            text_color=self.accent,
        ).pack(
            anchor="center"
        )

        self.refresh_storage_info()

    # =================================================
    # ABOUT PANEL
    # =================================================

    def create_about_panel(
        self,
        parent,
        row,
        column,
        title,
        accent,
        content,
        padx,
        pady=0,
    ):

        panel = (
            ctk.CTkFrame(
                parent,
                corner_radius=14,
                fg_color=COLORS["surface_alt"],
                border_width=1,
                border_color=COLORS["border_soft"],
            )
        )

        panel.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=padx,
            pady=pady,
        )

        panel.grid_columnconfigure(
            1,
            weight=1
        )

        # ---------------------------------------------
        # ACCENT STRIP
        # ---------------------------------------------

        strip = (
            ctk.CTkFrame(
                panel,
                width=5,
                corner_radius=100,
                fg_color=accent,
            )
        )

        strip.grid(
            row=0,
            column=0,
            rowspan=2,
            sticky="ns",
            padx=(10, 11),
            pady=13,
        )

        # ---------------------------------------------
        # TITLE
        # ---------------------------------------------

        ctk.CTkLabel(
            panel,
            text=title,
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=15,
                weight="bold",
            ),
            text_color=COLORS["text"],
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(0, 14),
            pady=(13, 5),
        )

        # ---------------------------------------------
        # CONTENT
        # ---------------------------------------------

        ctk.CTkLabel(
            panel,
            text=content,
            justify="left",
            anchor="nw",
            wraplength=500,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
            ),
            text_color=COLORS["muted"],
        ).grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(0, 14),
            pady=(0, 14),
        )

        return panel

    # =================================================
    # REFRESH STORAGE INFO
    # =================================================

    def refresh_storage_info(
        self
    ):

        try:

            self.database_path_card.path_label.configure(
                text=get_database_path()
            )

            self.settings_path_card.path_label.configure(
                text=get_settings_path()
            )

        except Exception:

            pass

        if hasattr(
            self,
            "storage_info_label"
        ):

            export_folder = (
                self.settings.get(
                    "export_folder",
                    get_default_export_path(),
                )
            )

            self.storage_info_label.configure(
                text=(
                    f"Database: {get_database_path()}\n\n"
                    f"Settings: {get_settings_path()}\n\n"
                    f"Export Folder: {export_folder}"
                )
            )

    # =================================================
    # REFRESH SETTINGS
    # =================================================

    def refresh_settings(
        self
    ):

        self.settings = (
            load_settings()
        )

        self.theme_menu.set(
            self.settings.get(
                "appearance_mode",
                "Dark",
            )
        )

        self.export_path_label.configure(
            text=self.settings.get(
                "export_folder",
                get_default_export_path(),
            )
        )

        self.refresh_storage_info()

    # =================================================
    # RESPONSIVE
    # =================================================

    def _schedule_layout_check(
        self,
        _event=None
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
    # APPLY RESPONSIVE
    # =================================================

    def apply_responsive_layout(
        self
    ):

        self._resize_job = None

        try:

            self.update_idletasks()

            width = (
                self.workspace
                .winfo_width()
            )

        except Exception:

            width = 1200

        if width <= 1:

            return

        compact = (
            width < 950
        )

        if (
            compact
            == self._compact_layout
        ):

            return

        self._compact_layout = (
            compact
        )

        # =================================================
        # COMPACT
        # =================================================

        if compact:

            # -----------------------------------------
            # PREFERENCES STACK
            # -----------------------------------------

            self.preferences_area.grid_columnconfigure(
                0,
                weight=1
            )

            self.preferences_area.grid_columnconfigure(
                1,
                weight=0
            )

            self.appearance_card.grid_configure(
                row=0,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0,
                pady=(0, 14),
            )

            self.export_card.grid_configure(
                row=1,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0,
                pady=0,
            )

            # -----------------------------------------
            # STORAGE PATHS STACK
            # -----------------------------------------

            self.storage_area.grid_columnconfigure(
                0,
                weight=1
            )

            self.storage_area.grid_columnconfigure(
                1,
                weight=0
            )

            self.database_path_card.grid_configure(
                row=0,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0,
                pady=(0, 10),
            )

            self.settings_path_card.grid_configure(
                row=1,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=0,
                pady=0,
            )

            # -----------------------------------------
            # ABOUT STACK
            # -----------------------------------------

            self.about_grid.grid_columnconfigure(
                0,
                weight=1
            )

            self.about_grid.grid_columnconfigure(
                1,
                weight=0
            )

            panels = [
                self.about_overview,
                self.about_productivity,
                self.about_modules,
                self.about_stack,
                self.about_privacy,
                self.about_purpose,
            ]

            for (
                index,
                panel
            ) in enumerate(
                panels
            ):

                panel.grid_configure(
                    row=index,
                    column=0,
                    columnspan=2,
                    sticky="ew",
                    padx=0,
                    pady=(
                        (0, 10)
                        if index < len(panels) - 1
                        else 0
                    ),
                )

        # =================================================
        # DESKTOP
        # =================================================

        else:

            # -----------------------------------------
            # PREFERENCES
            # -----------------------------------------

            self.preferences_area.grid_columnconfigure(
                0,
                weight=1
            )

            self.preferences_area.grid_columnconfigure(
                1,
                weight=1
            )

            self.appearance_card.grid_configure(
                row=0,
                column=0,
                columnspan=1,
                sticky="nsew",
                padx=(0, 7),
                pady=0,
            )

            self.export_card.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                sticky="nsew",
                padx=(7, 0),
                pady=0,
            )

            # -----------------------------------------
            # STORAGE PATHS
            # -----------------------------------------

            self.storage_area.grid_columnconfigure(
                0,
                weight=1
            )

            self.storage_area.grid_columnconfigure(
                1,
                weight=1
            )

            self.database_path_card.grid_configure(
                row=0,
                column=0,
                columnspan=1,
                sticky="nsew",
                padx=(0, 6),
                pady=0,
            )

            self.settings_path_card.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                sticky="nsew",
                padx=(6, 0),
                pady=0,
            )

            # -----------------------------------------
            # ABOUT GRID
            # -----------------------------------------

            self.about_grid.grid_columnconfigure(
                0,
                weight=1
            )

            self.about_grid.grid_columnconfigure(
                1,
                weight=1
            )

            self.about_overview.grid_configure(
                row=0,
                column=0,
                columnspan=1,
                padx=(0, 6),
                pady=0,
            )

            self.about_productivity.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                padx=(6, 0),
                pady=0,
            )

            self.about_modules.grid_configure(
                row=1,
                column=0,
                columnspan=1,
                padx=(0, 6),
                pady=(12, 0),
            )

            self.about_stack.grid_configure(
                row=1,
                column=1,
                columnspan=1,
                padx=(6, 0),
                pady=(12, 0),
            )

            self.about_privacy.grid_configure(
                row=2,
                column=0,
                columnspan=1,
                padx=(0, 6),
                pady=(12, 0),
            )

            self.about_purpose.grid_configure(
                row=2,
                column=1,
                columnspan=1,
                padx=(6, 0),
                pady=(12, 0),
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