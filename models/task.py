class Task:
    def __init__(
        self,
        task_id,
        title,
        description="",
        due_date="",
        priority="Medium",
        category="General",
        completed=False
    ):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.category = category
        self.completed = completed