"""LifeOS shared visual system."""

from __future__ import annotations

import customtkinter as ctk


COLORS = {
    "app_bg": ("#F4F6FB", "#090B12"),
    "sidebar": ("#FFFFFF", "#10131E"),
    "topbar": ("#FFFFFF", "#0E111B"),
    "surface": ("#FFFFFF", "#151927"),
    "surface_alt": ("#F8FAFE", "#1B2031"),
    "surface_soft": ("#EEF2FA", "#20263A"),
    "surface_hover": ("#F0F3FA", "#1F2537"),
    "border": ("#DEE4F0", "#2B3248"),
    "border_soft": ("#E8ECF4", "#242A3C"),
    "text": ("#172033", "#F7F8FC"),
    "muted": ("#697386", "#9DA7BC"),
    "subtle": ("#8D96A8", "#7F8AA3"),
    "white": "#FFFFFF",
    "black": "#0B0D13",
    "violet": "#8B5CF6",
    "violet_hover": "#7C3AED",
    "indigo": "#6366F1",
    "indigo_hover": "#4F46E5",
    "cyan": "#06B6D4",
    "cyan_hover": "#0891B2",
    "emerald": "#10B981",
    "emerald_hover": "#059669",
    "amber": "#F59E0B",
    "amber_hover": "#D97706",
    "coral": "#F97370",
    "coral_hover": "#EF4444",
    "pink": "#EC4899",
    "pink_hover": "#DB2777",
    "sky": "#3B82F6",
    "sky_hover": "#2563EB",
    "lime": "#84CC16",
    "danger": "#EF4444",
    "danger_hover": "#DC2626",
    "success": "#10B981",
    "warning": "#F59E0B",
}

MODULES = {
    "Dashboard": {
        "accent": "violet",
        "accent2": "cyan",
        "icon": "⌂",
    },

    "Tasks": {
        "accent": "emerald",
        "accent2": "lime",
        "icon": "✓",
    },

    "Planner": {
        "accent": "indigo",
        "accent2": "sky",
        "icon": "▦",
    },

    "Focus": {
        "accent": "violet",
        "accent2": "pink",
        "icon": "◎",
    },

    "Pomodoro": {
        "accent": "coral",
        "accent2": "amber",
        "icon": "◷",
    },

    "Stopwatch": {
        "accent": "cyan",
        "accent2": "sky",
        "icon": "◴",
    },

    "Notes": {
        "accent": "amber",
        "accent2": "coral",
        "icon": "▤",
    },

    "Analytics": {
        "accent": "pink",
        "accent2": "violet",
        "icon": "▥",
    },

    "History": {
        "accent": "sky",
        "accent2": "cyan",
        "icon": "↺",
    },

    "Reports": {
        "accent": "emerald",
        "accent2": "amber",
        "icon": "▧",
    },

    "Settings": {
        "accent": "indigo",
        "accent2": "violet",
        "icon": "⚙",
    },
}


CATEGORY_COLORS = {
    "General": "#64748B",
    "Study": "#8B5CF6",
    "College": "#6366F1",
    "Personal": "#EC4899",
    "Work": "#06B6D4",
    "Fitness": "#10B981",
    "Ideas": "#F59E0B",
    "Other": "#94A3B8",
}


# =================================================
# FONT SYSTEM
# =================================================

FONT_DISPLAY = "Segoe UI Variable Display"
FONT_BODY = "Segoe UI Variable Text"
FONT_MONO = "Cascadia Code"


# =================================================
# MODULE HELPERS
# =================================================

def module_accent(
    page_name: str
) -> str:

    spec = MODULES.get(
        page_name,
        MODULES["Dashboard"]
    )

    return COLORS[
        spec["accent"]
    ]


def module_accent_hover(
    page_name: str
) -> str:

    spec = MODULES.get(
        page_name,
        MODULES["Dashboard"]
    )

    return COLORS.get(
        f"{spec['accent']}_hover",
        COLORS[
            spec["accent"]
        ]
    )


def module_secondary(
    page_name: str
) -> str:

    spec = MODULES.get(
        page_name,
        MODULES["Dashboard"]
    )

    return COLORS[
        spec["accent2"]
    ]


# =================================================
# FONT HELPERS
# =================================================

def _font_size(
    widget
):

    try:
        font = widget.cget(
            "font"
        )

        if isinstance(
            font,
            ctk.CTkFont
        ):

            return abs(
                int(
                    font.cget(
                        "size"
                    )
                )
            )

    except Exception:
        pass

    return None


def _restyle_font(
    widget
):

    try:
        font = widget.cget(
            "font"
        )

        if not isinstance(
            font,
            ctk.CTkFont
        ):
            return

        size = abs(
            int(
                font.cget(
                    "size"
                )
            )
        )

        font.configure(
            family=(
                FONT_DISPLAY
                if size >= 18
                else FONT_BODY
            )
        )

    except Exception:
        pass


# =================================================
# BUTTON COLOR LOGIC
# =================================================

def _semantic_button_colour(
    text,
    accent,
    hover
):

    value = (
        text
        or ""
    ).lower()

    # ---------------------------------------------
    # DANGER
    # ---------------------------------------------

    if any(
        word in value
        for word in (
            "delete",
            "stop",
            "remove",
            "reset",
        )
    ):

        return (
            COLORS["danger"],
            COLORS["danger_hover"],
        )

    # ---------------------------------------------
    # WARNING
    # ---------------------------------------------

    if any(
        word in value
        for word in (
            "pause",
            "break",
        )
    ):

        return (
            COLORS["amber"],
            COLORS["amber_hover"],
        )

    # ---------------------------------------------
    # SECONDARY
    # ---------------------------------------------

    if any(
        word in value
        for word in (
            "restore",
            "edit",
            "choose",
        )
    ):

        return (
            COLORS["indigo"],
            COLORS["indigo_hover"],
        )

    return (
        accent,
        hover,
    )


# =================================================
# PAGE STYLE ENGINE
# =================================================

def style_page(
    page,
    page_name
):

    """
    Apply shared styling without changing layout geometry.

    Frame borders deliberately stay static.

    The older hover-border effect looked nice on large cards
    but on tightly packed cards it could look clipped by the
    parent canvas. Buttons and navigation now provide the
    visual hover feedback instead.
    """

    accent = module_accent(
        page_name
    )

    hover = module_accent_hover(
        page_name
    )

    secondary = module_secondary(
        page_name
    )

    # ---------------------------------------------
    # PAGE BACKGROUND
    # ---------------------------------------------

    try:
        page.configure(
            fg_color=COLORS[
                "app_bg"
            ]
        )

    except Exception:
        pass

    # =================================================
    # WALK ALL PAGE WIDGETS
    # =================================================

    def walk(
        widget,
        depth=0
    ):

        for child in (
            widget.winfo_children()
        ):

            _restyle_font(
                child
            )

            try:
                # =====================================
                # FRAMES / CARDS
                # =====================================

                if isinstance(
                    child,
                    ctk.CTkFrame
                ):

                    current = child.cget(
                        "fg_color"
                    )

                    if (
                        current
                        != "transparent"
                    ):

                        child.configure(
                            fg_color=(
                                COLORS["surface"]
                                if depth <= 1
                                else COLORS["surface_alt"]
                            ),

                            border_width=1,

                            border_color=COLORS[
                                "border"
                            ],
                        )

                # =====================================
                # BUTTONS
                # =====================================

                elif isinstance(
                    child,
                    ctk.CTkButton
                ):

                    text = str(
                        child.cget(
                            "text"
                        )
                        or ""
                    )

                    (
                        foreground,
                        hover_color,
                    ) = (
                        _semantic_button_colour(
                            text,
                            accent,
                            hover,
                        )
                    )

                    child.configure(
                        fg_color=foreground,
                        hover_color=hover_color,
                        text_color=COLORS[
                            "white"
                        ],
                        corner_radius=10,
                        border_width=0,
                        font=ctk.CTkFont(
                            family=FONT_BODY,
                            size=13,
                            weight="bold",
                        ),
                    )

                # =====================================
                # ENTRY
                # =====================================

                elif isinstance(
                    child,
                    ctk.CTkEntry
                ):

                    child.configure(
                        fg_color=COLORS[
                            "surface_alt"
                        ],
                        border_color=COLORS[
                            "border"
                        ],
                        text_color=COLORS[
                            "text"
                        ],
                        placeholder_text_color=COLORS[
                            "muted"
                        ],
                        corner_radius=10,
                    )

                # =====================================
                # TEXTBOX
                # =====================================

                elif isinstance(
                    child,
                    ctk.CTkTextbox
                ):

                    child.configure(
                        fg_color=COLORS[
                            "surface_alt"
                        ],
                        border_width=1,
                        border_color=COLORS[
                            "border"
                        ],
                        text_color=COLORS[
                            "text"
                        ],
                        corner_radius=12,
                    )

                # =====================================
                # OPTION MENU
                # =====================================

                elif isinstance(
                    child,
                    ctk.CTkOptionMenu
                ):

                    child.configure(
                        fg_color=COLORS[
                            "surface_soft"
                        ],
                        button_color=accent,
                        button_hover_color=hover,
                        text_color=COLORS[
                            "text"
                        ],
                        dropdown_fg_color=COLORS[
                            "surface"
                        ],
                        dropdown_hover_color=COLORS[
                            "surface_soft"
                        ],
                        dropdown_text_color=COLORS[
                            "text"
                        ],
                        corner_radius=10,
                    )

                # =====================================
                # SEGMENTED BUTTON
                # =====================================

                elif isinstance(
                    child,
                    ctk.CTkSegmentedButton
                ):

                    child.configure(
                        fg_color=COLORS[
                            "surface_soft"
                        ],
                        selected_color=accent,
                        selected_hover_color=hover,
                        unselected_color=COLORS[
                            "surface_soft"
                        ],
                        unselected_hover_color=COLORS[
                            "border"
                        ],
                        text_color=COLORS[
                            "text"
                        ],
                        corner_radius=10,
                    )

                # =====================================
                # CHECKBOX
                # =====================================

                elif isinstance(
                    child,
                    ctk.CTkCheckBox
                ):

                    child.configure(
                        fg_color=accent,
                        hover_color=hover,
                        border_color=COLORS[
                            "border"
                        ],
                        text_color=COLORS[
                            "text"
                        ],
                        corner_radius=6,
                    )

                # =====================================
                # SWITCH
                # =====================================

                elif isinstance(
                    child,
                    ctk.CTkSwitch
                ):

                    child.configure(
                        progress_color=accent,
                        button_hover_color=secondary,
                        text_color=COLORS[
                            "text"
                        ],
                    )

                # =====================================
                # PROGRESS BAR
                # =====================================

                elif isinstance(
                    child,
                    ctk.CTkProgressBar
                ):

                    child.configure(
                        fg_color=COLORS[
                            "surface_soft"
                        ],
                        progress_color=accent,
                    )

                # =====================================
                # LABEL
                # =====================================

                elif isinstance(
                    child,
                    ctk.CTkLabel
                ):

                    text = str(
                        child.cget(
                            "text"
                        )
                        or ""
                    )

                    size = (
                        _font_size(
                            child
                        )
                        or 13
                    )

                    color = (
                        COLORS["text"]
                        if size >= 13
                        else COLORS["muted"]
                    )

                    lower = text.lower()

                    # ---------------------------------
                    # PRIORITY COLORS
                    # ---------------------------------

                    if (
                        "high" in lower
                        and
                        "priority" in lower
                    ):

                        color = COLORS[
                            "danger"
                        ]

                    elif (
                        "medium" in lower
                        and
                        "priority" in lower
                    ):

                        color = COLORS[
                            "amber"
                        ]

                    elif (
                        "low" in lower
                        and
                        "priority" in lower
                    ):

                        color = COLORS[
                            "emerald"
                        ]

                    # ---------------------------------
                    # STATUS COLORS
                    # ---------------------------------

                    elif (
                        lower.strip()
                        in (
                            "completed",
                            "complete",
                        )
                    ):

                        color = COLORS[
                            "success"
                        ]

                    elif (
                        lower.strip()
                        in (
                            "stopped",
                            "overdue",
                        )
                    ):

                        color = COLORS[
                            "danger"
                        ]

                    # ---------------------------------
                    # LARGE PAGE TITLES
                    # ---------------------------------

                    elif size >= 28:

                        color = accent

                    child.configure(
                        text_color=color
                    )

            except Exception:
                pass

            walk(
                child,
                depth + 1
            )

    walk(
        page
    )


# =================================================
# CHART PALETTE
# =================================================

def chart_palette(
    page_name
):

    return [
        module_accent(
            page_name
        ),

        module_secondary(
            page_name
        ),

        COLORS[
            "emerald"
        ],

        COLORS[
            "amber"
        ],

        COLORS[
            "coral"
        ],

        COLORS[
            "cyan"
        ],

        COLORS[
            "pink"
        ],
    ]


# =================================================
# CHART THEME
# =================================================

def chart_theme_values():

    dark = (
        ctk.get_appearance_mode()
        .lower()
        == "dark"
    )

    if dark:

        return {
            "figure": "#151927",
            "axes": "#151927",
            "text": "#F7F8FC",
            "muted": "#9DA7BC",
            "grid": "#343C55",
        }

    return {
        "figure": "#FFFFFF",
        "axes": "#FFFFFF",
        "text": "#172033",
        "muted": "#697386",
        "grid": "#DFE5F0",
    }


# =================================================
# MATPLOTLIB / SEABORN STYLING
# =================================================

def style_matplotlib_figure(
    figure,
    axes,
    page_name
):

    """
    Match Matplotlib / Seaborn charts
    to the current LifeOS appearance.
    """

    theme = (
        chart_theme_values()
    )

    figure.patch.set_facecolor(
        theme[
            "figure"
        ]
    )

    # ---------------------------------------------
    # ONE OR MULTIPLE AXES
    # ---------------------------------------------

    axes_list = (
        list(
            axes
        )
        if isinstance(
            axes,
            (
                list,
                tuple,
            )
        )
        else [
            axes
        ]
    )

    for axis in axes_list:

        axis.set_facecolor(
            theme[
                "axes"
            ]
        )

        axis.tick_params(
            colors=theme[
                "muted"
            ],
            labelsize=9,
        )

        axis.xaxis.label.set_color(
            theme[
                "muted"
            ]
        )

        axis.yaxis.label.set_color(
            theme[
                "muted"
            ]
        )

        axis.title.set_color(
            theme[
                "text"
            ]
        )

        axis.grid(
            True,
            color=theme[
                "grid"
            ],
            alpha=0.28,
            linewidth=0.8,
        )

        axis.set_axisbelow(
            True
        )

        # -----------------------------------------
        # CLEAN MODERN AXES
        # -----------------------------------------

        for spine in (
            axis.spines.values()
        ):

            spine.set_visible(
                False
            )

        # -----------------------------------------
        # LEGEND
        # -----------------------------------------

        legend = (
            axis.get_legend()
        )

        if legend:

            legend.get_frame().set_facecolor(
                theme[
                    "figure"
                ]
            )

            legend.get_frame().set_edgecolor(
                theme[
                    "grid"
                ]
            )

            for label in (
                legend.get_texts()
            ):

                label.set_color(
                    theme[
                        "text"
                    ]
                )