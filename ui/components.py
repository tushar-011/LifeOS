from __future__ import annotations

import customtkinter as ctk

from ui.theme import (
    COLORS,
    FONT_BODY,
    FONT_DISPLAY,
    module_accent,
    module_accent_hover,
    module_secondary,
)


# =================================================
# APP CARD
# =================================================

class AppCard(ctk.CTkFrame):
    """
    Standard LifeOS card.

    Compatible with older calls like:

        AppCard(parent, title="Something")

    and newer module-aware cards.
    """

    def __init__(
        self,
        parent,
        title=None,
        subtitle=None,
        module="Dashboard",
        accent=False,
        corner_radius=18,
        **kwargs
    ):

        kwargs.setdefault(
            "fg_color",
            COLORS["surface"]
        )

        kwargs.setdefault(
            "border_width",
            1
        )

        kwargs.setdefault(
            "border_color",
            COLORS["border"]
        )

        super().__init__(
            parent,
            corner_radius=corner_radius,
            **kwargs
        )

        self.module = module
        self.accent_color = (
            module_accent(
                module
            )
        )

        # ---------------------------------------------
        # OPTIONAL ACCENT STRIP
        # ---------------------------------------------

        if accent:
            self.accent_strip = (
                ctk.CTkFrame(
                    self,
                    width=5,
                    corner_radius=100,
                    fg_color=self.accent_color
                )
            )

            self.accent_strip.pack(
                side="left",
                fill="y",
                padx=(0, 0),
                pady=14
            )

        # ---------------------------------------------
        # OPTIONAL HEADER
        # ---------------------------------------------

        if title:
            self.header_frame = (
                ctk.CTkFrame(
                    self,
                    fg_color="transparent"
                )
            )

            self.header_frame.pack(
                fill="x",
                padx=22,
                pady=(18, 10)
            )

            self.title_label = (
                ctk.CTkLabel(
                    self.header_frame,
                    text=title,
                    font=ctk.CTkFont(
                        family=FONT_DISPLAY,
                        size=19,
                        weight="bold"
                    ),
                    text_color=COLORS["text"]
                )
            )

            self.title_label.pack(
                anchor="w"
            )

            if subtitle:
                self.subtitle_label = (
                    ctk.CTkLabel(
                        self.header_frame,
                        text=subtitle,
                        font=ctk.CTkFont(
                            family=FONT_BODY,
                            size=12
                        ),
                        text_color=COLORS["muted"],
                        justify="left",
                        wraplength=760
                    )
                )

                self.subtitle_label.pack(
                    anchor="w",
                    pady=(4, 0)
                )


# =================================================
# NAV BUTTON
# =================================================

class NavButton(ctk.CTkButton):
    """
    Sidebar button with active state support.

    Supports both:
        module="Tasks"
    and
        page_name="Tasks"

    so it stays compatible with older and newer main.py.
    """

    def __init__(
        self,
        parent,
        text,
        icon,
        command,
        module=None,
        page_name=None,
        **kwargs
    ):

        self.page_text = text
        self.icon_text = icon

        self.page_name = (
            page_name
            or module
            or text
        )

        self.accent = (
            module_accent(
                self.page_name
            )
        )

        self.accent_hover = (
            module_accent_hover(
                self.page_name
            )
        )

        super().__init__(
            parent,
            text=f"{icon}   {text}",
            height=44,
            anchor="w",
            corner_radius=12,
            fg_color="transparent",
            hover_color=COLORS["surface_soft"],
            text_color=COLORS["muted"],
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=13,
                weight="bold"
            ),
            command=command,
            **kwargs
        )

        self.is_active = False
        self.is_collapsed = False

        try:
            self.configure(
                cursor="hand2"
            )
        except Exception:
            pass

    # =================================================
    # ACTIVE STATE
    # =================================================

    def set_active(
        self,
        active=True
    ):

        self.is_active = active

        if active:
            self.configure(
                fg_color=self.accent,
                hover_color=self.accent_hover,
                text_color=COLORS["white"]
            )

        else:
            self.configure(
                fg_color="transparent",
                hover_color=COLORS["surface_soft"],
                text_color=COLORS["muted"]
            )

    # =================================================
    # COLLAPSE
    # =================================================

    def collapse(self):

        self.is_collapsed = True

        self.configure(
            text=self.icon_text,
            width=48,
            anchor="center"
        )

    # =================================================
    # EXPAND
    # =================================================

    def expand(self):

        self.is_collapsed = False

        self.configure(
            text=(
                f"{self.icon_text}   "
                f"{self.page_text}"
            ),
            anchor="w"
        )


# =================================================
# PAGE HEADER
# =================================================

class PageHeader(ctk.CTkFrame):
    """
    Reusable large page heading.
    """

    def __init__(
        self,
        parent,
        title,
        subtitle="",
        module="Dashboard",
        eyebrow=None,
        **kwargs
    ):

        kwargs.setdefault(
            "fg_color",
            "transparent"
        )

        super().__init__(
            parent,
            **kwargs
        )

        accent = (
            module_accent(
                module
            )
        )

        if eyebrow:
            badge = (
                ctk.CTkFrame(
                    self,
                    fg_color=accent,
                    corner_radius=100
                )
            )

            badge.pack(
                anchor="w",
                pady=(0, 8)
            )

            ctk.CTkLabel(
                badge,
                text=eyebrow.upper(),
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                    weight="bold"
                ),
                text_color=COLORS["white"]
            ).pack(
                padx=10,
                pady=4
            )

        ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=31,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).pack(
            anchor="w"
        )

        if subtitle:
            ctk.CTkLabel(
                self,
                text=subtitle,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=14
                ),
                text_color=COLORS["muted"],
                justify="left",
                wraplength=900
            ).pack(
                anchor="w",
                pady=(5, 0)
            )

        ctk.CTkFrame(
            self,
            width=64,
            height=4,
            corner_radius=100,
            fg_color=accent
        ).pack(
            anchor="w",
            pady=(12, 0)
        )


# =================================================
# SECTION HEADER
# =================================================

class SectionHeader(ctk.CTkFrame):
    """
    Compact section heading.
    """

    def __init__(
        self,
        parent,
        title,
        subtitle=None,
        module="Dashboard",
        action_text=None,
        action_command=None,
        **kwargs
    ):

        kwargs.setdefault(
            "fg_color",
            "transparent"
        )

        super().__init__(
            parent,
            **kwargs
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        left = (
            ctk.CTkFrame(
                self,
                fg_color="transparent"
            )
        )

        left.grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            left,
            text=title,
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=19,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).pack(
            anchor="w"
        )

        if subtitle:
            ctk.CTkLabel(
                left,
                text=subtitle,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12
                ),
                text_color=COLORS["muted"],
                justify="left",
                wraplength=700
            ).pack(
                anchor="w",
                pady=(3, 0)
            )

        if (
            action_text
            and action_command
        ):

            ctk.CTkButton(
                self,
                text=action_text,
                width=110,
                height=34,
                corner_radius=10,
                fg_color=module_accent(
                    module
                ),
                hover_color=module_accent_hover(
                    module
                ),
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=12,
                    weight="bold"
                ),
                command=action_command
            ).grid(
                row=0,
                column=1,
                sticky="e",
                padx=(15, 0)
            )


# =================================================
# STAT CARD
# =================================================

class StatCard(ctk.CTkFrame):
    """
    Reusable statistics card.
    """

    def __init__(
        self,
        parent,
        title,
        value="0",
        icon="",
        module="Dashboard",
        subtitle=None,
        **kwargs
    ):

        kwargs.setdefault(
            "fg_color",
            COLORS["surface"]
        )

        kwargs.setdefault(
            "border_width",
            1
        )

        kwargs.setdefault(
            "border_color",
            COLORS["border"]
        )

        super().__init__(
            parent,
            corner_radius=18,
            **kwargs
        )

        self.accent = (
            module_accent(
                module
            )
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------
        # TOP AREA
        # ---------------------------------------------

        top = (
            ctk.CTkFrame(
                self,
                fg_color="transparent"
            )
        )

        top.pack(
            fill="x",
            padx=18,
            pady=(16, 6)
        )

        ctk.CTkLabel(
            top,
            text=title,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=12,
                weight="bold"
            ),
            text_color=COLORS["muted"]
        ).pack(
            side="left"
        )

        if icon:
            icon_box = (
                ctk.CTkFrame(
                    top,
                    width=34,
                    height=34,
                    corner_radius=10,
                    fg_color=self.accent
                )
            )

            icon_box.pack(
                side="right"
            )

            icon_box.pack_propagate(
                False
            )

            ctk.CTkLabel(
                icon_box,
                text=icon,
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=15,
                    weight="bold"
                ),
                text_color=COLORS["white"]
            ).pack(
                expand=True
            )

        # ---------------------------------------------
        # VALUE
        # ---------------------------------------------

        self.value_label = (
            ctk.CTkLabel(
                self,
                text=str(value),
                font=ctk.CTkFont(
                    family=FONT_DISPLAY,
                    size=28,
                    weight="bold"
                ),
                text_color=COLORS["text"]
            )
        )

        self.value_label.pack(
            anchor="w",
            padx=18,
            pady=(2, 2)
        )

        # ---------------------------------------------
        # SUBTITLE
        # ---------------------------------------------

        self.subtitle_label = None

        if subtitle:
            self.subtitle_label = (
                ctk.CTkLabel(
                    self,
                    text=subtitle,
                    font=ctk.CTkFont(
                        family=FONT_BODY,
                        size=11
                    ),
                    text_color=COLORS["subtle"],
                    justify="left",
                    wraplength=240
                )
            )

            self.subtitle_label.pack(
                anchor="w",
                padx=18,
                pady=(0, 8)
            )

        # ---------------------------------------------
        # ACCENT LINE
        # ---------------------------------------------

        ctk.CTkFrame(
            self,
            height=4,
            corner_radius=100,
            fg_color=self.accent
        ).pack(
            fill="x",
            padx=18,
            pady=(10, 15)
        )

    def set_value(
        self,
        value
    ):

        self.value_label.configure(
            text=str(value)
        )

    def set_subtitle(
        self,
        value
    ):

        if self.subtitle_label:
            self.subtitle_label.configure(
                text=str(value)
            )


# =================================================
# BADGE
# =================================================

class Badge(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        text,
        color="#6366F1",
        **kwargs
    ):

        kwargs.setdefault(
            "fg_color",
            color
        )

        super().__init__(
            parent,
            corner_radius=100,
            **kwargs
        )

        self.label = (
            ctk.CTkLabel(
                self,
                text=text,
                font=ctk.CTkFont(
                    family=FONT_BODY,
                    size=10,
                    weight="bold"
                ),
                text_color=COLORS["white"]
            )
        )

        self.label.pack(
            padx=9,
            pady=4
        )

    def set_text(
        self,
        text
    ):

        self.label.configure(
            text=text
        )


# =================================================
# ACCENT BUTTON
# =================================================

class AccentButton(ctk.CTkButton):

    def __init__(
        self,
        parent,
        text,
        command=None,
        module="Dashboard",
        **kwargs
    ):

        kwargs.setdefault(
            "height",
            40
        )

        kwargs.setdefault(
            "corner_radius",
            11
        )

        kwargs.setdefault(
            "fg_color",
            module_accent(
                module
            )
        )

        kwargs.setdefault(
            "hover_color",
            module_accent_hover(
                module
            )
        )

        kwargs.setdefault(
            "text_color",
            COLORS["white"]
        )

        kwargs.setdefault(
            "font",
            ctk.CTkFont(
                family=FONT_BODY,
                size=13,
                weight="bold"
            )
        )

        super().__init__(
            parent,
            text=text,
            command=command,
            **kwargs
        )


# =================================================
# SECONDARY BUTTON
# =================================================

class SecondaryButton(ctk.CTkButton):

    def __init__(
        self,
        parent,
        text,
        command=None,
        **kwargs
    ):

        kwargs.setdefault(
            "height",
            38
        )

        kwargs.setdefault(
            "corner_radius",
            10
        )

        kwargs.setdefault(
            "fg_color",
            COLORS["surface_soft"]
        )

        kwargs.setdefault(
            "hover_color",
            COLORS["border"]
        )

        kwargs.setdefault(
            "text_color",
            COLORS["text"]
        )

        kwargs.setdefault(
            "border_width",
            1
        )

        kwargs.setdefault(
            "border_color",
            COLORS["border"]
        )

        kwargs.setdefault(
            "font",
            ctk.CTkFont(
                family=FONT_BODY,
                size=12,
                weight="bold"
            )
        )

        super().__init__(
            parent,
            text=text,
            command=command,
            **kwargs
        )


# =================================================
# DANGER BUTTON
# =================================================

class DangerButton(ctk.CTkButton):

    def __init__(
        self,
        parent,
        text,
        command=None,
        **kwargs
    ):

        kwargs.setdefault(
            "height",
            38
        )

        kwargs.setdefault(
            "corner_radius",
            10
        )

        kwargs.setdefault(
            "fg_color",
            COLORS["danger"]
        )

        kwargs.setdefault(
            "hover_color",
            COLORS["danger_hover"]
        )

        kwargs.setdefault(
            "text_color",
            COLORS["white"]
        )

        kwargs.setdefault(
            "font",
            ctk.CTkFont(
                family=FONT_BODY,
                size=12,
                weight="bold"
            )
        )

        super().__init__(
            parent,
            text=text,
            command=command,
            **kwargs
        )


# =================================================
# DIVIDER
# =================================================

class Divider(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        **kwargs
    ):

        kwargs.setdefault(
            "height",
            1
        )

        kwargs.setdefault(
            "fg_color",
            COLORS["border_soft"]
        )

        super().__init__(
            parent,
            **kwargs
        )


# =================================================
# EMPTY STATE
# =================================================

class EmptyState(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        title="Nothing here yet",
        message="Your activity will appear here.",
        icon="◇",
        module="Dashboard",
        **kwargs
    ):

        kwargs.setdefault(
            "fg_color",
            COLORS["surface_alt"]
        )

        kwargs.setdefault(
            "border_width",
            1
        )

        kwargs.setdefault(
            "border_color",
            COLORS["border_soft"]
        )

        super().__init__(
            parent,
            corner_radius=15,
            **kwargs
        )

        accent = (
            module_accent(
                module
            )
        )

        ctk.CTkLabel(
            self,
            text=icon,
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=28,
                weight="bold"
            ),
            text_color=accent
        ).pack(
            pady=(22, 7)
        )

        ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(
                family=FONT_DISPLAY,
                size=15,
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).pack()

        ctk.CTkLabel(
            self,
            text=message,
            font=ctk.CTkFont(
                family=FONT_BODY,
                size=12
            ),
            text_color=COLORS["muted"],
            wraplength=420,
            justify="center"
        ).pack(
            padx=20,
            pady=(5, 22)
        )