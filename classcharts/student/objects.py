from datetime import datetime
from enum import Enum
from .utils import sanitise


class ActivityPoint:
    def __repr__(self):
        return (
            f"<{self.__class__.__name__} id={self.id!r}"
            + f" point_type={self.point_type!r} score={self.score!r}"
            + f" reason={self.reason!r}>"
        )


class Positive(ActivityPoint):
    def __init__(self, data):
        self._data = data
        self.id = data["id"]
        self.point_type = data["type"]
        self.score = data["score"]
        self.reason = data["reason"]
        self.timestamp = datetime.fromisoformat(data["timestamp"])
        self.lesson = data["lesson_name"]
        self.teacher = data["teacher_name"]
        self.note = data["note"]


class Negative(ActivityPoint):
    def __init__(self, data):
        self._data = data
        self.id = data["id"]
        self.point_type = data["type"]
        self.score = data["score"]
        self.reason = data["reason"]
        self.timestamp = datetime.fromisoformat(data["timestamp"])
        self.lesson = data["lesson_name"]
        self.teacher = data["teacher_name"]
        self.note = data["note"]


class DetentionPoint(ActivityPoint):
    def __init__(self, data):
        self._data = data
        self.id = data["id"]
        self.point_type = data["type"]
        self.score = data["score"]
        self.reason = data["reason"]
        self.date_set = datetime.fromisoformat(data["timestamp"])
        self.lesson = data["lesson_name"]
        self.teacher = data["teacher_name"]
        self.note = data["note"]
        self.date = datetime.fromisoformat(data["detention_date"])
        self.time = datetime.strptime(data["detention_time"], "%H:%M")
        self.location = data["detention_location"]
        self.type = data["detention_type"]


class Announcement:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.description = sanitise(data["description"])
        self.viewed = True if data["state"] == "viewed" else False
        self.timestamp = datetime.fromisoformat(data["timestamp"])
        self.school_name = data["school_name"]

    def __repr__(self):
        return (
            f"<Announcement id={self.id!r} title={self.title!r}"
            + f" timestamp={self.timestamp!r}"
            + f" school_name={self.school_name!r}>"
        )


class DisplayDate(Enum):
    due = "due_date"
    issue = "issue_date"


class Homework:  # different from homework.Homework
    def __init__(self, data):
        self.lesson = data["lesson"]
        self.subject = data["subject"]
        self.teacher = data["teacher"]
        self.id = data["id"]
        self.title = sanitise(data["title"])
        self.description = sanitise(data["description"])
        self.issue_date = datetime.strptime(data["issue_date"], "%Y-%m-%d")
        self.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d")
        self.validated_attachments = [
            Attachment(d) for d in data["validated_attachments"]
        ]
        self.completion_time = (
            int(data["completion_time_value"] or "0"),
            data["completion_time_unit"],
        )
        self.status = HomeworkStatus(data["status"])

    def __repr__(self):
        return (
            f"<Homework id={self.id!r} lesson={self.lesson!r}"
            + f" teacher={self.teacher!r} title={self.title!r}"
            + f" issue_date={self.issue_date!r} due_date={self.due_date!r}"
            + f" status={self.status!r}>"
        )


class Attachment:
    def __init__(self, data):
        self.id = data["id"]
        self.filename = data["file_name"]
        self.file = data["file"]
        self.validated_file = data.get("validated_attachment")

    def __repr__(self):
        return f"<Attachment id={self.id!r} filename={self.filename!r}>"


class HomeworkStatus:
    def __init__(self, data):
        self.id = data["id"]
        self.ticked = True if data["ticked"] == "yes" else False
        self.submitted_attachments = [
            Attachment(d) for d in data["attachments"]
        ]

    def __repr__(self):
        return (
            f"<HomeworkStatus id={self.id!r} ticked={self.ticked!r}"
            + f" submitted_attachments={self.submitted_attachments!r}>"
        )


class Teacher:
    def __init__(self, data):
        self.title = data["title"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]

        self.name = f"{self.title} {self.first_name[0]} {self.last_name}"

    def __repr__(self):
        return f"<Teacher name={self.name!r}>"


class BasicLesson:
    def __init__(self, data):
        self.name = data["name"]
        try:
            self.subject = data["subject"]["name"]
        except TypeError:
            self.subject = None

    def __repr__(self):
        return f"<BasicLesson name={self.name!r} subject={self.subject!r}>"


class Detention:
    def __init__(self, data):
        self.id = data["id"]
        self.attended = True if data["attended"] == "yes" else False
        time = datetime.strptime(data["time"], "%H:%M")
        self.date = datetime.fromisoformat(data["date"]).replace(
            minute=time.minute, hour=time.hour
        )
        self.length = int(data["length"])
        self.location = data["location"]
        self.lesson = BasicLesson(data["lesson"])
        self.teacher = Teacher(data["teacher"])
        self.lesson_pupil_behaviour = data["lesson_pupil_behaviour"]["reason"]
        self.detention_type = data["detention_type"]["name"]

    def __repr__(self):
        return (
            f"<Detention id={self.id!r} attended={self.attended!r}"
            + f" date={self.date!r} length={self.length!r}"
            + f" lesson={self.lesson!r} teacher={self.teacher!r}"
            + f" detention_type={self.detention_type!r}>"
        )


class Lesson(BasicLesson):
    def __init__(self, data):
        super().__init__(
            {
                "name": data["lesson_name"],
                "subject": {"name": data["subject_name"]},
            }
        )
        title, first_name, last_name = data["teacher_name"].split(" ")
        self.teacher = Teacher(
            {"title": title, "first_name": first_name, "last_name": last_name}
        )
        self.room = data["room_name"]
        self.date = datetime.strptime(data["date"], "%Y-%m-%d")
        self.period = {
            "name": data["period_name"],
            "number": data["period_number"],
        }
        self.start = datetime.fromisoformat(data["start_time"])
        self.end = datetime.fromisoformat(data["end_time"])
        self.note = data["note"] or None
        self._key = data["key"]

    def __repr__(self):
        return (
            f"<Lesson name={self.name!r} subject={self.subject!r}"
            + f" room={self.room!r}>"
        )


class Timetable:
    def __init__(self, data):
        self.lessons = [Lesson(data) for data in data["data"]]
        self.date = datetime.fromisoformat(data["meta"]["dates"][0])
        self.start = datetime.fromisoformat(data["meta"]["start_time"])
        self.end = datetime.fromisoformat(data["meta"]["end_time"])

    def __repr__(self):
        return f"<Timetable date={self.date!r}>"


class AttendanceLesson(BasicLesson):
    def __init__(self, name, data):
        super().__init__({"name": name, "subject": {"name": None}})
        self.code = data["code"] or None
        self.late_minutes = int(data["late_minutes"] or "0")
        self.status = data["status"]

    def __repr__(self):
        return f"<AttendanceLesson name={self.name!r} code={self.code!r}>"


class Attendance:
    def __init__(self, data):
        self.percentage = int(data["meta"]["percentage"])
        self.percentage_singe_august = int(
            data["meta"]["percentage_singe_august"]
        )
        self.dates = [
            datetime.fromisoformat(date) for date in data["meta"]["dates"]
        ]
        self.days = {}

        for date, day in data["data"].items():
            self.days[datetime.fromisoformat(date)] = [
                AttendanceLesson(name, lesson) for name, lesson in day.items()
            ]

        self.sessions = data["meta"]["sessions"]
        self.start = datetime.fromisoformat(data["meta"]["start_date"])
        self.end = datetime.fromisoformat(data["meta"]["end_date"])

    def __repr__(self):
        return f"<Attendance percentage={self.percentage!r}>"
