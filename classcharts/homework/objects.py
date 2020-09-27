from datetime import datetime


class Homework:
    def __init__(self, data, description):
        self.title = data["title"] if data["title"] else "No Title Given."
        self.description = (
            description if description else "No Description Given."
        )
        self.issue_date = datetime.fromisoformat(data["issue_date"])
        self.due_date = datetime.fromisoformat(data["due_date"])
        self.teacher = Teacher(data["teacher"])
        self.lesson = Lesson(data["lesson"])

        self.attachments = []

        for i in data["homework_attachments"]:
            self.attachments.append(Attachment(i))

    def __repr__(self):
        return (
            f"<Homework title={self.title!r}"
            + f" issue_date={self.issue_date!r} due_date={self.due_date!r}"
            + f" teacher={self.teacher!r} lesson={self.lesson!r}"
            + f" attachments={self.attachments!r}>"
        )


class Teacher:
    def __init__(self, data):
        self.title = data["title"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]

        self.name = f"{self.title} {self.first_name[0]} {self.last_name}"

    def __repr__(self):
        return f"<Teacher name={self.name!r}>"


class Lesson:
    def __init__(self, data):
        self.name = data["name"]
        try:
            self.subject = data["subject"]["name"]
        except TypeError:
            self.subject = None

    def __repr__(self):
        return f"<Lesson name={self.name!r} subject={self.subject!r}>"


class Attachment:
    def __init__(self, data):
        self.file = data["file"]
        self.file_name = data["file_name"]

    def __repr__(self):
        return f"<Attachment file_name={self.file_name!r}>"
