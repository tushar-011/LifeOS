from __future__ import annotations

from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk

from database.database import (
    add_note,
    delete_note,
    get_note_count,
    get_notes,
    update_note,
)

from ui.theme import (
    CATEGORY_COLORS,
    COLORS,
    FONT_BODY,
    FONT_DISPLAY,
    module_accent,
    module_accent_hover,
)


class NotesPage(ctk.CTkScrollableFrame):
    """Responsive notes workspace for LifeOS."""

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color=COLORS["app_bg"],
        )

        self.selected_note_id = None

        self.accent = module_accent(
            "Notes"
        )

        self.accent_hover = module_accent_hover(
            "Notes"
        )

        self._compact_layout = None
        self._resize_job = None

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.create_workspace()
        self.create_header()
        self.create_note_form()
        self.create_search_section()
        self.create_notes_list()

        self.workspace.bind(
            "<Configure>",
            self._schedule_layout_check,
            add="+",
        )

        self.after(
            120,
            self.apply_responsive_layout
        )

        self.load_notes()

    # =================================================
    # WORKSPACE
    # =================================================

    def create_workspace(self):

        self.workspace = ctk.CTkFrame(
            self,
            fg_color="transparent",
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

    def create_header(self):

        self.header = ctk.CTkFrame(
            self.workspace,
            fg_color="transparent",
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

        left = ctk.CTkFrame(
            self.header,
            fg_color="transparent",
        )

        left.grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            left,
            text="Notes",
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
                "Capture ideas, reminders and "
                "information without losing context."
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

        self.note_count_badge = ctk.CTkFrame(
            self.header,
            corner_radius=100,
            fg_color=COLORS["surface_soft"],
        )

        self.note_count_badge.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(15, 0),
        )

        self.note_count_label = ctk.CTkLabel(
            self.note_count_badge,
            text="0 Notes",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold",
            ),
            text_color=self.accent,
        )

        self.note_count_label.pack(
            padx=13,
            pady=7,
        )

    # =================================================
    # NOTE FORM
    # =================================================

    def create_note_form(self):

        self.form_card = ctk.CTkFrame(
            self.workspace,
            corner_radius=18,
            fg_color=COLORS["surface"],
            border_width=1,
            border_color=COLORS["border"],
        )

        self.form_card.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 14),
        )

        self.form_card.grid_columnconfigure(
            0,
            weight=1
        )

        header = ctk.CTkFrame(
            self.form_card,
            fg_color="transparent",
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=22,
            pady=(19, 10),
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        left = ctk.CTkFrame(
            header,
            fg_color="transparent",
        )

        left.grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.form_title = ctk.CTkLabel(
            left,
            text="Create Note",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=19,
                weight="bold",
            ),
            text_color=COLORS["text"],
        )

        self.form_title.pack(
            anchor="w"
        )

        ctk.CTkLabel(
            left,
            text=(
                "Give the note a title, category and "
                "enough detail to find it later."
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

        self.form_state_label = ctk.CTkLabel(
            header,
            text="NEW",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=9,
                weight="bold",
            ),
            text_color=self.accent,
        )

        self.form_state_label.grid(
            row=0,
            column=1,
            sticky="e",
        )

        self.form_body = ctk.CTkFrame(
            self.form_card,
            fg_color="transparent",
        )

        self.form_body.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=22,
        )

        self.form_body.grid_columnconfigure(
            0,
            weight=1
        )

        self.form_body.grid_columnconfigure(
            1,
            weight=0,
            minsize=190
        )

        # ---------------------------------------------
        # TITLE
        # ---------------------------------------------

        self.title_holder = ctk.CTkFrame(
            self.form_body,
            fg_color="transparent",
        )

        self.title_holder.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 8),
        )

        self.title_holder.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            self.title_holder,
            text="Title",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold",
            ),
            text_color=COLORS["muted"],
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 5),
        )

        self.title_entry = ctk.CTkEntry(
            self.title_holder,
            placeholder_text="Note title",
            height=42,
        )

        self.title_entry.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        # ---------------------------------------------
        # CATEGORY
        # ---------------------------------------------

        self.category_holder = ctk.CTkFrame(
            self.form_body,
            fg_color="transparent",
        )

        self.category_holder.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(8, 0),
        )

        self.category_holder.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            self.category_holder,
            text="Category",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold",
            ),
            text_color=COLORS["muted"],
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 5),
        )

        self.category_menu = ctk.CTkOptionMenu(
            self.category_holder,
            values=[
                "General",
                "Study",
                "College",
                "Personal",
                "Work",
                "Ideas",
                "Other",
            ],
            height=42,
        )

        self.category_menu.set(
            "General"
        )

        self.category_menu.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        # ---------------------------------------------
        # CONTENT
        # ---------------------------------------------

        ctk.CTkLabel(
            self.form_card,
            text="Content",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold",
            ),
            text_color=COLORS["muted"],
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=22,
            pady=(12, 5),
        )

        self.content_box = ctk.CTkTextbox(
            self.form_card,
            height=180,
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"],
        )

        self.content_box.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=22,
        )

        # ---------------------------------------------
        # FOOTER
        # ---------------------------------------------

        footer = ctk.CTkFrame(
            self.form_card,
            fg_color="transparent",
        )

        footer.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=22,
            pady=(10, 18),
        )

        footer.grid_columnconfigure(
            0,
            weight=1
        )

        self.form_message = ctk.CTkLabel(
            footer,
            text="",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
            ),
            text_color=COLORS["danger"],
        )

        self.form_message.grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.form_buttons = ctk.CTkFrame(
            footer,
            fg_color="transparent",
        )

        self.form_buttons.grid(
            row=0,
            column=1,
            sticky="e",
        )

        self.save_button = ctk.CTkButton(
            self.form_buttons,
            text="Save Note",
            width=120,
            height=40,
            corner_radius=11,
            fg_color=self.accent,
            hover_color=self.accent_hover,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=12,
                weight="bold",
            ),
            command=self.save_note,
        )

        self.save_button.pack(
            side="left",
            padx=(0, 6),
        )

        self.clear_button = ctk.CTkButton(
            self.form_buttons,
            text="Clear",
            width=96,
            height=40,
            corner_radius=11,
            fg_color=COLORS["surface_soft"],
            hover_color=COLORS["border"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=12,
                weight="bold",
            ),
            command=self.clear_form,
        )

        self.clear_button.pack(
            side="left"
        )

    # =================================================
    # SEARCH
    # =================================================

    def create_search_section(self):

        self.search_card = ctk.CTkFrame(
            self.workspace,
            corner_radius=16,
            fg_color=COLORS["surface"],
            border_width=1,
            border_color=COLORS["border"],
        )

        self.search_card.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 12),
        )

        self.search_card.grid_columnconfigure(
            0,
            weight=1
        )

        self.search_holder = ctk.CTkFrame(
            self.search_card,
            fg_color="transparent",
        )

        self.search_holder.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(18, 8),
            pady=14,
        )

        self.search_holder.grid_columnconfigure(
            0,
            weight=1
        )

        self.search_entry = ctk.CTkEntry(
            self.search_holder,
            placeholder_text=(
                "Search title or note content..."
            ),
            height=40,
        )

        self.search_entry.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda _event:
                self.load_notes(),
        )

        self.filter_category = ctk.CTkOptionMenu(
            self.search_card,
            width=180,
            height=40,
            values=[
                "All Categories",
                "General",
                "Study",
                "College",
                "Personal",
                "Work",
                "Ideas",
                "Other",
            ],
            command=lambda _value:
                self.load_notes(),
        )

        self.filter_category.set(
            "All Categories"
        )

        self.filter_category.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(8, 18),
            pady=14,
        )

    # =================================================
    # NOTES LIST
    # =================================================

    def create_notes_list(self):

        self.notes_card = ctk.CTkFrame(
            self.workspace,
            corner_radius=18,
            fg_color=COLORS["surface"],
            border_width=1,
            border_color=COLORS["border"],
        )

        self.notes_card.grid(
            row=3,
            column=0,
            sticky="ew",
        )

        list_header = ctk.CTkFrame(
            self.notes_card,
            fg_color="transparent",
        )

        list_header.pack(
            fill="x",
            padx=20,
            pady=(18, 8),
        )

        list_header.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            list_header,
            text="Your Notes",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=18,
                weight="bold",
            ),
            text_color=COLORS["text"],
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.visible_count_label = ctk.CTkLabel(
            list_header,
            text="0 shown",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold",
            ),
            text_color=self.accent,
        )

        self.visible_count_label.grid(
            row=0,
            column=1,
            sticky="e",
        )

        self.notes_container = ctk.CTkFrame(
            self.notes_card,
            fg_color="transparent",
        )

        self.notes_container.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(2, 14),
        )

        self.notes_container.grid_columnconfigure(
            0,
            weight=1
        )

        self.notes_container.grid_columnconfigure(
            1,
            weight=1
        )

    # =================================================
    # SAVE NOTE
    # =================================================

    def save_note(self):

        title = (
            self.title_entry
            .get()
            .strip()
        )

        content = (
            self.content_box
            .get(
                "1.0",
                "end"
            )
            .strip()
        )

        category = (
            self.category_menu
            .get()
        )

        if not title:

            self.form_message.configure(
                text="Please enter a note title.",
                text_color=COLORS["danger"],
            )

            return

        if not content:

            self.form_message.configure(
                text=(
                    "Please write something "
                    "in the note."
                ),
                text_color=COLORS["danger"],
            )

            return

        if (
            self.selected_note_id
            is None
        ):

            add_note(
                title,
                content,
                category,
            )

        else:

            update_note(
                self.selected_note_id,
                title,
                content,
                category,
            )

        self.clear_form()
        self.load_notes()

    # =================================================
    # LOAD NOTES
    # =================================================

    def load_notes(self):

        for widget in (
            self.notes_container
            .winfo_children()
        ):

            widget.destroy()

        search_text = (
            self.search_entry
            .get()
            .strip()
        )

        category = (
            self.filter_category
            .get()
        )

        notes = get_notes(
            search_text,
            category,
        )

        total_notes = (
            get_note_count()
        )

        self.note_count_label.configure(
            text=(
                f"{total_notes} "
                f"{'Note' if total_notes == 1 else 'Notes'}"
            )
        )

        self.visible_count_label.configure(
            text=(
                f"{len(notes)} shown"
            )
        )

        if not notes:

            empty = ctk.CTkFrame(
                self.notes_container,
                corner_radius=14,
                fg_color=COLORS["surface_alt"],
                border_width=1,
                border_color=COLORS["border_soft"],
            )

            empty.grid(
                row=0,
                column=0,
                columnspan=2,
                sticky="ew",
                pady=4,
            )

            ctk.CTkLabel(
                empty,
                text="▤",
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=28,
                    weight="bold",
                ),
                text_color=self.accent,
            ).pack(
                pady=(22, 5),
            )

            ctk.CTkLabel(
                empty,
                text="No notes found",
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=13,
                    weight="bold",
                ),
                text_color=COLORS["text"],
            ).pack()

            ctk.CTkLabel(
                empty,
                text=(
                    "Create a note or change "
                    "the current search/filter."
                ),
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                ),
                text_color=COLORS["muted"],
            ).pack(
                pady=(4, 22),
            )

            self.after_idle(
                self._refresh_scroll_region
            )

            return

        columns = (
            1
            if self._compact_layout
            else 2
        )

        for index, note in enumerate(
            notes
        ):

            row = (
                index
                // columns
            )

            column = (
                index
                % columns
            )

            self.create_note_card(
                note,
                row=row,
                column=column,
                columns=columns,
            )

        self.after_idle(
            self._refresh_scroll_region
        )

    # =================================================
    # NOTE CARD
    # =================================================

    def create_note_card(
        self,
        note,
        row,
        column,
        columns,
    ):

        (
            note_id,
            title,
            content,
            category,
            created_at,
            updated_at,
        ) = note

        category_color = (
            CATEGORY_COLORS.get(
                category,
                self.accent,
            )
        )

        card = ctk.CTkFrame(
            self.notes_container,
            corner_radius=14,
            fg_color=COLORS["surface_alt"],
            border_width=1,
            border_color=COLORS["border_soft"],
        )

        if columns == 1:

            padx = 0

        elif column == 0:

            padx = (
                0,
                6
            )

        else:

            padx = (
                6,
                0
            )

        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=padx,
            pady=6,
        )

        card.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # CLICKING CARD OPENS NOTE
        # ---------------------------------------------

        self.bind_note_open(
            card,
            note
        )

        # ---------------------------------------------
        # TOP
        # ---------------------------------------------

        top = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )

        top.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=16,
            pady=(14, 5),
        )

        top.grid_columnconfigure(
            0,
            weight=1
        )

        title_label = ctk.CTkLabel(
            top,
            text=title,
            anchor="w",
            justify="left",
            wraplength=430,
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=16,
                weight="bold",
            ),
            text_color=COLORS["text"],
            cursor="hand2",
        )

        title_label.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 8),
        )

        self.bind_note_open(
            title_label,
            note
        )

        badge = ctk.CTkFrame(
            top,
            corner_radius=100,
            fg_color=category_color,
        )

        badge.grid(
            row=0,
            column=1,
            sticky="e",
        )

        ctk.CTkLabel(
            badge,
            text=category,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=9,
                weight="bold",
            ),
            text_color=COLORS["white"],
        ).pack(
            padx=8,
            pady=3,
        )

        # ---------------------------------------------
        # CONTENT PREVIEW
        # ---------------------------------------------

        preview = (
            " ".join(
                content.split()
            )
        )

        if len(preview) > 230:

            preview = (
                preview[:230]
                .rstrip()
                + "..."
            )

        preview_label = ctk.CTkLabel(
            card,
            text=preview,
            anchor="w",
            justify="left",
            wraplength=520,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
            ),
            text_color=COLORS["muted"],
            cursor="hand2",
        )

        preview_label.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=16,
            pady=(3, 9),
        )

        self.bind_note_open(
            preview_label,
            note
        )

        # ---------------------------------------------
        # FOOTER
        # ---------------------------------------------

        footer = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )

        footer.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=16,
            pady=(3, 14),
        )

        footer.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            footer,
            text=(
                "Updated "
                + self.format_timestamp(
                    updated_at
                )
            ),
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=9,
            ),
            text_color=COLORS["subtle"],
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        # ---------------------------------------------
        # ACTIONS
        # ---------------------------------------------

        actions = ctk.CTkFrame(
            footer,
            fg_color="transparent",
        )

        actions.grid(
            row=0,
            column=1,
            sticky="e",
        )

        ctk.CTkButton(
            actions,
            text="View",
            width=64,
            height=34,
            corner_radius=9,
            fg_color=self.accent,
            hover_color=self.accent_hover,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold",
            ),
            command=lambda:
                self.open_note_popup(
                    note
                ),
        ).pack(
            side="left",
            padx=(0, 5),
        )

        ctk.CTkButton(
            actions,
            text="Edit",
            width=64,
            height=34,
            corner_radius=9,
            fg_color=COLORS["indigo"],
            hover_color=COLORS["indigo_hover"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold",
            ),
            command=lambda:
                self.edit_note(
                    note
                ),
        ).pack(
            side="left",
            padx=(0, 5),
        )

        ctk.CTkButton(
            actions,
            text="Delete",
            width=70,
            height=34,
            corner_radius=9,
            fg_color=COLORS["danger"],
            hover_color=COLORS["danger_hover"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold",
            ),
            command=lambda:
                self.remove_note(
                    note_id
                ),
        ).pack(
            side="left"
        )

    # =================================================
    # BIND CARD CLICK
    # =================================================

    def bind_note_open(
        self,
        widget,
        note
    ):

        widget.bind(
            "<Button-1>",
            lambda _event:
                self.open_note_popup(
                    note
                ),
            add="+",
        )

        try:

            widget.configure(
                cursor="hand2"
            )

        except Exception:

            pass

    # =================================================
    # NOTE POPUP
    # =================================================

    def open_note_popup(
        self,
        note
    ):

        (
            note_id,
            title,
            content,
            category,
            created_at,
            updated_at,
        ) = note

        popup = ctk.CTkToplevel(
            self
        )

        popup.title(
            f"LifeOS Note • {title}"
        )

        popup.geometry(
            "760x650"
        )

        popup.minsize(
            620,
            520
        )

        popup.configure(
            fg_color=COLORS["app_bg"]
        )

        popup.transient(
            self.winfo_toplevel()
        )

        popup.grab_set()

        self.after(
            50,
            lambda:
                self.center_popup(
                    popup,
                    760,
                    650
                )
        )

        popup.grid_columnconfigure(
            0,
            weight=1
        )

        popup.grid_rowconfigure(
            0,
            weight=1
        )

        # =================================================
        # MAIN POPUP CARD
        # =================================================

        container = ctk.CTkFrame(
            popup,
            corner_radius=20,
            fg_color=COLORS["surface"],
            border_width=1,
            border_color=COLORS["border"],
        )

        container.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=20,
            pady=20,
        )

        container.grid_columnconfigure(
            0,
            weight=1
        )

        container.grid_rowconfigure(
            3,
            weight=1
        )

        # =================================================
        # POPUP HEADER
        # =================================================

        header = ctk.CTkFrame(
            container,
            fg_color="transparent",
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=24,
            pady=(22, 12),
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        title_area = ctk.CTkFrame(
            header,
            fg_color="transparent",
        )

        title_area.grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            title_area,
            text="NOTE",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=9,
                weight="bold",
            ),
            text_color=self.accent,
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            title_area,
            text="View & Edit",
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=24,
                weight="bold",
            ),
            text_color=COLORS["text"],
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        category_color = (
            CATEGORY_COLORS.get(
                category,
                self.accent,
            )
        )

        category_badge = ctk.CTkFrame(
            header,
            corner_radius=100,
            fg_color=category_color,
        )

        category_badge.grid(
            row=0,
            column=1,
            sticky="e",
        )

        ctk.CTkLabel(
            category_badge,
            text=category,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold",
            ),
            text_color=COLORS["white"],
        ).pack(
            padx=10,
            pady=5,
        )

        # =================================================
        # TITLE + CATEGORY EDIT
        # =================================================

        fields = ctk.CTkFrame(
            container,
            fg_color="transparent",
        )

        fields.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=24,
            pady=(0, 10),
        )

        fields.grid_columnconfigure(
            0,
            weight=1
        )

        fields.grid_columnconfigure(
            1,
            weight=0,
            minsize=180
        )

        title_holder = ctk.CTkFrame(
            fields,
            fg_color="transparent",
        )

        title_holder.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 8),
        )

        title_holder.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            title_holder,
            text="Title",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold",
            ),
            text_color=COLORS["muted"],
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 5),
        )

        popup_title_entry = ctk.CTkEntry(
            title_holder,
            height=42,
        )

        popup_title_entry.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        popup_title_entry.insert(
            0,
            title
        )

        category_holder = ctk.CTkFrame(
            fields,
            fg_color="transparent",
        )

        category_holder.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(8, 0),
        )

        category_holder.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            category_holder,
            text="Category",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold",
            ),
            text_color=COLORS["muted"],
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 5),
        )

        popup_category_menu = ctk.CTkOptionMenu(
            category_holder,
            values=[
                "General",
                "Study",
                "College",
                "Personal",
                "Work",
                "Ideas",
                "Other",
            ],
            height=42,
        )

        popup_category_menu.set(
            category
        )

        popup_category_menu.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        # =================================================
        # CONTENT LABEL
        # =================================================

        ctk.CTkLabel(
            container,
            text="Full Note",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
                weight="bold",
            ),
            text_color=COLORS["muted"],
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=24,
            pady=(4, 5),
        )

        # =================================================
        # FULL CONTENT
        # =================================================

        popup_content_box = ctk.CTkTextbox(
            container,
            corner_radius=13,
            border_width=1,
            border_color=COLORS["border"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=13,
            ),
            wrap="word",
        )

        popup_content_box.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=24,
            pady=(0, 10),
        )

        popup_content_box.insert(
            "1.0",
            content
        )

        # =================================================
        # META INFORMATION
        # =================================================

        meta_text = (
            f"Created: "
            f"{self.format_timestamp(created_at)}"
            f"    •    "
            f"Updated: "
            f"{self.format_timestamp(updated_at)}"
        )

        ctk.CTkLabel(
            container,
            text=meta_text,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=9,
            ),
            text_color=COLORS["subtle"],
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=24,
            pady=(0, 9),
        )

        # =================================================
        # MESSAGE
        # =================================================

        popup_message = ctk.CTkLabel(
            container,
            text="",
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=10,
            ),
            text_color=COLORS["danger"],
        )

        popup_message.grid(
            row=5,
            column=0,
            sticky="w",
            padx=24,
        )

        # =================================================
        # ACTIONS
        # =================================================

        actions = ctk.CTkFrame(
            container,
            fg_color="transparent",
        )

        actions.grid(
            row=6,
            column=0,
            sticky="ew",
            padx=24,
            pady=(10, 22),
        )

        actions.grid_columnconfigure(
            0,
            weight=1
        )

        left_actions = ctk.CTkFrame(
            actions,
            fg_color="transparent",
        )

        left_actions.grid(
            row=0,
            column=0,
            sticky="w",
        )

        right_actions = ctk.CTkFrame(
            actions,
            fg_color="transparent",
        )

        right_actions.grid(
            row=0,
            column=1,
            sticky="e",
        )

        # =================================================
        # DELETE FROM POPUP
        # =================================================

        def delete_from_popup():

            confirm = messagebox.askyesno(
                "Delete Note",
                (
                    "Are you sure you want to "
                    "delete this note?"
                ),
                parent=popup,
            )

            if not confirm:

                return

            delete_note(
                note_id
            )

            popup.destroy()

            if (
                self.selected_note_id
                == note_id
            ):

                self.clear_form()

            self.load_notes()

        ctk.CTkButton(
            left_actions,
            text="Delete Note",
            width=115,
            height=40,
            corner_radius=11,
            fg_color=COLORS["danger"],
            hover_color=COLORS["danger_hover"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold",
            ),
            command=delete_from_popup,
        ).pack(
            side="left"
        )

        # =================================================
        # SAVE FROM POPUP
        # =================================================

        def save_popup_changes():

            new_title = (
                popup_title_entry
                .get()
                .strip()
            )

            new_content = (
                popup_content_box
                .get(
                    "1.0",
                    "end"
                )
                .strip()
            )

            new_category = (
                popup_category_menu
                .get()
            )

            if not new_title:

                popup_message.configure(
                    text="Title cannot be empty.",
                    text_color=COLORS["danger"],
                )

                return

            if not new_content:

                popup_message.configure(
                    text="Note content cannot be empty.",
                    text_color=COLORS["danger"],
                )

                return

            update_note(
                note_id,
                new_title,
                new_content,
                new_category,
            )

            popup_message.configure(
                text="Changes saved.",
                text_color=COLORS["emerald"],
            )

            popup.title(
                f"LifeOS Note • {new_title}"
            )

            self.load_notes()

        ctk.CTkButton(
            right_actions,
            text="Close",
            width=90,
            height=40,
            corner_radius=11,
            fg_color=COLORS["surface_soft"],
            hover_color=COLORS["border"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold",
            ),
            command=popup.destroy,
        ).pack(
            side="left",
            padx=(0, 6),
        )

        ctk.CTkButton(
            right_actions,
            text="Save Changes",
            width=130,
            height=40,
            corner_radius=11,
            fg_color=self.accent,
            hover_color=self.accent_hover,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=11,
                weight="bold",
            ),
            command=save_popup_changes,
        ).pack(
            side="left"
        )

    # =================================================
    # POPUP CENTERING
    # =================================================

    def center_popup(
        self,
        popup,
        width,
        height
    ):

        try:

            root = (
                self.winfo_toplevel()
            )

            root.update_idletasks()

            actual_width = min(
                width,
                max(
                    620,
                    root.winfo_width() - 100
                )
            )

            actual_height = min(
                height,
                max(
                    520,
                    root.winfo_height() - 80
                )
            )

            x = (
                root.winfo_rootx()
                + (
                    root.winfo_width()
                    - actual_width
                )
                // 2
            )

            y = (
                root.winfo_rooty()
                + (
                    root.winfo_height()
                    - actual_height
                )
                // 2
            )

            popup.geometry(
                f"{actual_width}x{actual_height}"
                f"+{x}+{y}"
            )

        except Exception:

            pass

    # =================================================
    # EDIT NOTE IN MAIN FORM
    # =================================================

    def edit_note(
        self,
        note
    ):

        (
            note_id,
            title,
            content,
            category,
            created_at,
            updated_at,
        ) = note

        self.selected_note_id = (
            note_id
        )

        self.title_entry.delete(
            0,
            "end"
        )

        self.content_box.delete(
            "1.0",
            "end"
        )

        self.title_entry.insert(
            0,
            title
        )

        self.content_box.insert(
            "1.0",
            content
        )

        self.category_menu.set(
            category
        )

        self.form_title.configure(
            text="Edit Note"
        )

        self.form_state_label.configure(
            text="EDITING"
        )

        self.save_button.configure(
            text="Update Note"
        )

        self.clear_button.configure(
            text="Cancel Edit"
        )

        self.form_message.configure(
            text=""
        )

        try:

            self._parent_canvas.yview_moveto(
                0
            )

        except Exception:

            pass

        self.title_entry.focus()

    # =================================================
    # DELETE NOTE
    # =================================================

    def remove_note(
        self,
        note_id
    ):

        confirm = messagebox.askyesno(
            "Delete Note",
            "Are you sure you want to delete this note?",
            parent=self.winfo_toplevel(),
        )

        if not confirm:

            return

        delete_note(
            note_id
        )

        if (
            self.selected_note_id
            == note_id
        ):

            self.clear_form()

        self.load_notes()

    # =================================================
    # CLEAR FORM
    # =================================================

    def clear_form(self):

        self.selected_note_id = None

        self.title_entry.delete(
            0,
            "end"
        )

        self.content_box.delete(
            "1.0",
            "end"
        )

        self.category_menu.set(
            "General"
        )

        self.form_title.configure(
            text="Create Note"
        )

        self.form_state_label.configure(
            text="NEW"
        )

        self.save_button.configure(
            text="Save Note"
        )

        self.clear_button.configure(
            text="Clear"
        )

        self.form_message.configure(
            text=""
        )

    # =================================================
    # FORMAT TIMESTAMP
    # =================================================

    def format_timestamp(
        self,
        value
    ):

        if not value:

            return "Unknown"

        try:

            parsed = datetime.strptime(
                value,
                "%Y-%m-%d %H:%M:%S",
            )

            return parsed.strftime(
                "%d %b %Y • %I:%M %p"
            )

        except (
            ValueError,
            TypeError
        ):

            return str(
                value
            )

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

    def apply_responsive_layout(self):

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
            width < 900
        )

        if (
            compact
            == self._compact_layout
        ):

            return

        self._compact_layout = (
            compact
        )

        if compact:

            self.note_count_badge.grid_configure(
                row=1,
                column=0,
                sticky="w",
                padx=0,
                pady=(12, 0),
            )

            self.form_body.grid_columnconfigure(
                0,
                weight=1
            )

            self.form_body.grid_columnconfigure(
                1,
                weight=0,
                minsize=0
            )

            self.category_holder.grid_configure(
                row=1,
                column=0,
                sticky="ew",
                padx=0,
                pady=(12, 0),
            )

            self.filter_category.grid_configure(
                row=1,
                column=0,
                sticky="ew",
                padx=18,
                pady=(0, 14),
            )

            self.notes_container.grid_columnconfigure(
                0,
                weight=1
            )

            self.notes_container.grid_columnconfigure(
                1,
                weight=0
            )

        else:

            self.note_count_badge.grid_configure(
                row=0,
                column=1,
                sticky="e",
                padx=(15, 0),
                pady=0,
            )

            self.form_body.grid_columnconfigure(
                0,
                weight=1
            )

            self.form_body.grid_columnconfigure(
                1,
                weight=0,
                minsize=190
            )

            self.category_holder.grid_configure(
                row=0,
                column=1,
                sticky="ew",
                padx=(8, 0),
                pady=0,
            )

            self.filter_category.grid_configure(
                row=0,
                column=1,
                sticky="e",
                padx=(8, 18),
                pady=14,
            )

            self.notes_container.grid_columnconfigure(
                0,
                weight=1
            )

            self.notes_container.grid_columnconfigure(
                1,
                weight=1
            )

        self.load_notes()

        self.after_idle(
            self._refresh_scroll_region
        )

    # =================================================
    # SCROLL REGION
    # =================================================

    def _refresh_scroll_region(self):

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