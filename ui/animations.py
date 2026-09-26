"""Small, dependency-free UI animations for LifeOS."""

from __future__ import annotations


# =================================================
# EASING
# =================================================

def ease_out_cubic(
    t: float
) -> float:

    return (
        1
        - pow(
            1 - t,
            3
        )
    )


# =================================================
# SIDEBAR ANIMATION
# =================================================

def animate_sidebar(
    widget,
    start: int,
    end: int,
    duration_ms: int = 180,
    steps: int = 12,
    on_done=None
):

    delta = (
        end
        - start
    )

    interval = max(
        8,
        duration_ms // steps
    )

    def tick(
        index=0
    ):

        t = min(
            1.0,
            index / steps
        )

        value = round(
            start
            + delta
            * ease_out_cubic(
                t
            )
        )

        try:

            widget.configure(
                width=value
            )

        except Exception:

            return

        if index < steps:

            widget.after(
                interval,
                lambda:
                tick(
                    index + 1
                )
            )

        elif on_done:

            on_done()

    tick()


# =================================================
# PAGE SLIDE-IN
# =================================================

def slide_in(
    page,
    container,
    offset: int = 28,
    duration_ms: int = 150,
    steps: int = 10
):

    """
    Slide a cached page in from the right.

    After the animation finishes, the page is
    returned to normal grid geometry management.
    """

    interval = max(
        8,
        duration_ms // steps
    )

    # ---------------------------------------------
    # TEMPORARILY SWITCH TO PLACE()
    # ---------------------------------------------

    try:

        page.grid_remove()

        page.place(
            x=offset,
            y=0,
            relwidth=1,
            relheight=1
        )

        page.lift()

    except Exception:

        # Fall back to ordinary grid if the
        # animation cannot be started.

        try:

            page.grid(
                row=0,
                column=0,
                sticky="nsew"
            )

        except Exception:

            pass

        return

    # ---------------------------------------------
    # ANIMATION LOOP
    # ---------------------------------------------

    def tick(
        index=0
    ):

        t = min(
            1.0,
            index / steps
        )

        x = round(
            offset
            * (
                1
                - ease_out_cubic(
                    t
                )
            )
        )

        try:

            page.place_configure(
                x=x
            )

        except Exception:

            return

        if index < steps:

            container.after(
                interval,
                lambda:
                tick(
                    index + 1
                )
            )

        else:

            # -------------------------------------
            # RESTORE GRID MANAGEMENT
            # -------------------------------------

            try:

                page.place_forget()

                page.grid(
                    row=0,
                    column=0,
                    sticky="nsew"
                )

            except Exception:

                pass

    tick()