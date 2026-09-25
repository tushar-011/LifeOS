import customtkinter as ctk


class AppCard(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        title=None,
        corner_radius=16,
        **kwargs
    ):
        super().__init__(
            parent,
            corner_radius=corner_radius,
            **kwargs
        )

        if title:
            self.title_label = ctk.CTkLabel(
                self,
                text=title,
                font=ctk.CTkFont(
                    size=19,
                    weight="bold"
                )
            )

            self.title_label.pack(
                anchor="w",
                padx=20,
                pady=(18, 10)
            )


class NavButton(ctk.CTkButton):
    def __init__(
        self,
        parent,
        text,
        icon,
        command
    ):
        super().__init__(
            parent,
            text=f"{icon}   {text}",
            height=42,
            anchor="w",
            corner_radius=10,
            command=command
        )

        self.page_text = text
        self.icon_text = icon

    def collapse(self):
        self.configure(
            text=self.icon_text,
            width=48,
            anchor="center"
        )

    def expand(self):
        self.configure(
            text=f"{self.icon_text}   {self.page_text}",
            anchor="w"
        )