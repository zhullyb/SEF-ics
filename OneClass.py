import datetime
from ics import Event, Attendee


class OneClass:
    """
    用于课程数据存储的类，指代具体在某一天某一时段的某一节课，可以直接转换成 ics 库中的 Event 对象
    """

    def __init__(self, className: str, date: datetime.date, classTime: tuple[int, int], location="", teacher=""):
        self.className = className
        self.date = date
        self.classTime = classTime
        self.location = location
        self.teacher = teacher

    def toEvent(self):
        """
        将 OneClass 对象转换成 ics 库中的 Event 对象
        :return: ics 库中的 Event 对象
        """
        e = Event()

        e.name = self.className
        e.begin, e.end = OneClass.classTimeToRealTime(
            self.date, self.classTime)
        if self.location:
            e.location = self.location
        if self.teacher:
            e.add_attendee(Attendee('teacher@example.com',
                           common_name=self.teacher))
        return e

    @staticmethod
    def classTimeToRealTime(date: datetime.date, classTime: tuple[datetime.datetime, datetime.datetime]) -> tuple[str, str]:
        """
        将具体的第几节课转换为 ics 库中识读的 str 时间字符串
        :param date: 一个 datetime.date 对象，表示日期
        :param classTime: 一个元组，表示开始是第几节课，结束是第几节课
        :return: 一个包含两个 datetime.datetime 对象的元组，分别表示开始时间和结束时间
        """
        timetable = {
            "1": ["08:00", "08:45"],
            "2": ["08:55", "09:40"],
            "3": ["09:55", "10:40"],
            "4": ["10:50", "11:35"],
            "5": ["11:45", "12:30"],
            "6": ["13:30", "14:15"],
            "7": ["14:25", "15:10"],
            "8": ["15:25", "16:10"],
            "9": ["16:20", "17:05"],
            "10": ["18:30", "19:15"],
            "11": ["19:25", "20:10"],
            "12": ["20:20", "21:05"]
        }

        # 检查 classTime 是否符合预期
        for i in classTime:
            if timetable.get(str(i)) is None:
                raise Exception("classTime is not in timetable")

        # 东八区
        timezone = datetime.timezone(datetime.timedelta(hours=8))

        # 根据日期计算开始时间和结束时间
        startTime = datetime.datetime.combine(
            date,
            datetime.datetime.strptime(
                timetable[str(classTime[0])][0], "%H:%M").time(),
            tzinfo=timezone)
        endTime = datetime.datetime.combine(
            date,
            datetime.datetime.strptime(
                timetable[str(classTime[1])][1], "%H:%M").time(),
            tzinfo=timezone)
        return startTime, endTime


if __name__ == "__main__":
    oneclass = OneClass("课程名称", datetime.date.today(),
                        (1, 2), teacher="上课老师", location="上课地点")
    event = oneclass.toEvent()
    print(event.serialize())
