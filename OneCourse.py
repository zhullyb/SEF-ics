import datetime
from OneClass import OneClass


class OneCourseTime:
    """
    用于课程数据存储的类，指代具体某一门课程在周几上第几节课的信息，作为模板方便通过具体的日期进行匹配
    如果同一门课在一周内上多次课，应当实例化为多个 OneCourseTime 对象
    """

    def __init__(self, courseName: str, dayOfTheWeek: int, classTime: tuple[int, int], location="", teacher=""):
        self.courseName = courseName
        self.dayOfTheWeek = dayOfTheWeek
        self.classTime = classTime
        self.location = location
        self.teacher = teacher

    def haveClass(self, date: datetime.date) -> bool:
        """
        判断某一门课程在某一天是否有课
        :param date: 一个 datetime.date 对象，表示日期
        :return: 一个布尔值，表示该门课程在该天是否有课
        """
        if self.dayOfTheWeek == date.weekday() + 1:
            return True
        return False

    def toOneClass(self, date: datetime.date) -> OneClass:
        """
        将 OneCourseTime 对象转换成 OneClass 对象
        :param date: 一个 datetime.date 对象，表示日期
        :return: 一个 OneClass 对象
        """
        if self.haveClass(date):
            return OneClass(self.courseName, date, self.classTime, location=self.location, teacher=self.teacher)
        return None


class OneCourse:
    """
    用于课程数据存储的类，指代具体某一门课程在一周内有哪些课
    """

    def __init__(self, courseName: str, teacher=""):
        self.courseName = courseName
        self.teacher = teacher
        self.courseTimes = []

    def addClassTime(self, dayOfTheWeek: int, classTime: tuple[int, int], location=""):
        self.courseTimes.append(OneCourseTime(
            self.courseName, dayOfTheWeek, classTime, location=location, teacher=self.teacher))

    def toOneClass(self, date: datetime.date) -> OneClass:
        """
        通过遍历，将 OneCourse 对象转换成 OneClass 对象
        :param date: 一个 datetime.date 对象，表示日期
        :return: 一个 OneClass 对象
        """
        for courseTime in self.courseTimes:
            if courseTime.haveClass(date):
                return courseTime.toOneClass(date)
        return None
