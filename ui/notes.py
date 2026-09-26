import customtkinter as ctk
from datetime import datetime

from database.database import (
    add_note,
    get_notes,
    update_note,
    delete_note,
    get_note_count
)


class NotesPage(ctk.CTkScrollableFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            corner_radius=0
        )

        self.selected_note_id = None

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.create_header()
        self.create_note_form()
        self.create_search_section()
        self.create_notes_list()

        self.load_notes()

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

        header.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            header,
            text="Notes",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            header,
            text="Capture ideas, reminders and information."
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(5, 0)
        )

        self.note_count_label = ctk.CTkLabel(
            header,
            text="0 Notes",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        self.note_count_label.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=10
        )

    # =================================================
    # NOTE FORM
    # =================================================

    def create_note_form(self):

        self.form_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        self.form_card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        self.form_card.grid_columnconfigure(
            0,
            weight=1
        )

        self.form_title = ctk.CTkLabel(
            self.form_card,
            text="Create Note",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        self.form_title.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=20,
            pady=(18, 10)
        )

        # ---------------------------------------------
        # TITLE
        # ---------------------------------------------

        self.title_entry = ctk.CTkEntry(
            self.form_card,
            placeholder_text="Note title"
        )

        self.title_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=8
        )

        # ---------------------------------------------
        # CATEGORY
        # ---------------------------------------------

        self.category_menu = ctk.CTkOptionMenu(
            self.form_card,
            width=180,
            values=[
                "General",
                "Study",
                "College",
                "Personal",
                "Work",
                "Ideas",
                "Other"
            ]
        )

        self.category_menu.set(
            "General"
        )

        self.category_menu.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(10, 20),
            pady=8
        )

        # ---------------------------------------------
        # NOTE CONTENT
        # ---------------------------------------------

        self.content_box = ctk.CTkTextbox(
            self.form_card,
            height=180
        )

        self.content_box.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=8
        )

        # ---------------------------------------------
        # MESSAGE
        # ---------------------------------------------

        self.form_message = ctk.CTkLabel(
            self.form_card,
            text=""
        )

        self.form_message.grid(
            row=3,
            column=0,
            sticky="w",
            padx=20
        )

        # ---------------------------------------------
        # BUTTONS
        # ---------------------------------------------

        button_frame = ctk.CTkFrame(
            self.form_card,
            fg_color="transparent"
        )

        button_frame.grid(
            row=3,
            column=1,
            sticky="e",
            padx=20,
            pady=(5, 18)
        )

        self.save_button = ctk.CTkButton(
            button_frame,
            text="Save Note",
            command=self.save_note
        )

        self.save_button.pack(
            side="left",
            padx=5
        )

        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_form
        )

        self.clear_button.pack(
            side="left",
            padx=5
        )

    # =================================================
    # SEARCH
    # =================================================

    def create_search_section(self):

        search_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        search_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=25,
            pady=(10, 0)
        )

        search_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search notes..."
        )

        self.search_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.load_notes()
        )

        self.filter_category = ctk.CTkOptionMenu(
            search_frame,
            width=170,
            values=[
                "All Categories",
                "General",
                "Study",
                "College",
                "Personal",
                "Work",
                "Ideas",
                "Other"
            ],
            command=lambda _: self.load_notes()
        )

        self.filter_category.set(
            "All Categories"
        )

        self.filter_category.grid(
            row=0,
            column=1
        )

    # =================================================
    # NOTES LIST
    # =================================================

    def create_notes_list(self):

        self.notes_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        self.notes_card.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(10, 25)
        )

        self.notes_container = ctk.CTkFrame(
            self.notes_card,
            fg_color="transparent"
        )

        self.notes_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    # =================================================
    # SAVE
    # =================================================

    def save_note(self):

        title = (
            self.title_entry
            .get()
            .strip()
        )

        content = (
            self.content_box
            .get("1.0", "end")
            .strip()
        )

        category = (
            self.category_menu
            .get()
        )

        if not title:

            self.form_message.configure(
                text="Please enter a note title."
            )

            return

        if not content:

            self.form_message.configure(
                text="Please write something in the note."
            )

            return

        if self.selected_note_id is None:

            add_note(
                title,
                content,
                category
            )

        else:

            update_note(
                self.selected_note_id,
                title,
                content,
                category
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
            category
        )

        total_notes = get_note_count()

        self.note_count_label.configure(
            text=f"{total_notes} Notes"
        )

        if not notes:

            ctk.CTkLabel(
                self.notes_container,
                text="No notes found."
            ).pack(
                pady=35
            )

            return

        for note in notes:

            self.create_note_card(note)

    # =================================================
    # NOTE CARD
    # =================================================

    def create_note_card(self, note):

        (
            note_id,
            title,
            content,
            category,
            created_at,
            updated_at
        ) = note

        card = ctk.CTkFrame(
            self.notes_container,
            corner_radius=12
        )

        card.pack(
            fill="x",
            pady=7
        )

        card.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # TITLE
        # ---------------------------------------------

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=18,
            pady=(14, 3)
        )

        # ---------------------------------------------
        # PREVIEW
        # ---------------------------------------------

        preview = content.replace(
            "\n",
            " "
        )

        if len(preview) > 120:
            preview = preview[:120] + "..."

        ctk.CTkLabel(
            card,
            text=preview,
            anchor="w",
            justify="left",
            wraplength=700
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=18,
            pady=3
        )

        # ---------------------------------------------
        # DETAILS
        # ---------------------------------------------

        formatted_date = updated_at

        try:

            parsed = datetime.strptime(
                updated_at,
                "%Y-%m-%d %H:%M:%S"
            )

            formatted_date = parsed.strftime(
                "%d %b %Y • %I:%M %p"
            )

        except (ValueError, TypeError):
            pass

        details = (
            f"{category}  •  "
            f"Updated {formatted_date}"
        )

        ctk.CTkLabel(
            card,
            text=details,
            font=ctk.CTkFont(
                size=11
            )
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=18,
            pady=(3, 14)
        )

        # ---------------------------------------------
        # EDIT
        # ---------------------------------------------

        ctk.CTkButton(
            card,
            text="Edit",
            width=70,
            command=lambda: self.edit_note(
                note
            )
        ).grid(
            row=0,
            column=1,
            rowspan=3,
            padx=5
        )

        # ---------------------------------------------
        # DELETE
        # ---------------------------------------------

        ctk.CTkButton(
            card,
            text="Delete",
            width=70,
            command=lambda: self.remove_note(
                note_id
            )
        ).grid(
            row=0,
            column=2,
            rowspan=3,
            padx=(5, 15)
        )

    # =================================================
    # EDIT NOTE
    # =================================================

    def edit_note(self, note):

        (
            note_id,
            title,
            content,
            category,
            created_at,
            updated_at
        ) = note

        self.selected_note_id = note_id

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

        self.save_button.configure(
            text="Update Note"
        )

        self.clear_button.configure(
            text="Cancel Edit"
        )

        self.form_message.configure(
            text=""
        )

    # =================================================
    # DELETE NOTE
    # =================================================

    def remove_note(
        self,
        note_id
    ):

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

        self.save_button.configure(
            text="Save Note"
        )

        self.clear_button.configure(
            text="Clear"
        )

        self.form_message.configure(
            text=""
        )