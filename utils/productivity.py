def calculate_productivity_score(
    tasks_completed,
    tasks_total,
    focus_minutes,
    planner_completed,
    planner_total
):
    """
    Productivity Score:

    Tasks   = 50 points
    Focus   = 30 points
    Planner = 20 points

    Maximum = 100
    """

    # =================================================
    # TASK SCORE
    # =================================================

    if tasks_total > 0:

        task_ratio = (
            tasks_completed
            / tasks_total
        )

        task_score = (
            task_ratio
            * 50
        )

    else:

        task_score = 0

    # =================================================
    # FOCUS SCORE
    # =================================================

    focus_target_minutes = 120

    focus_ratio = min(
        focus_minutes
        / focus_target_minutes,
        1
    )

    focus_score = (
        focus_ratio
        * 30
    )

    # =================================================
    # PLANNER SCORE
    # =================================================

    if planner_total > 0:

        planner_ratio = (
            planner_completed
            / planner_total
        )

        planner_score = (
            planner_ratio
            * 20
        )

    else:

        planner_score = 0

    # =================================================
    # TOTAL
    # =================================================

    total_score = (
        task_score
        + focus_score
        + planner_score
    )

    return round(
        min(
            total_score,
            100
        )
    )


def score_label(
    score
):

    if score >= 80:
        return "Excellent"

    if score >= 60:
        return "Productive"

    if score >= 40:
        return "Moderate"

    if score > 0:
        return "Getting Started"

    return "No Activity"