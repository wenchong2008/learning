# /user/bin/env python
__author__ = 'wenchong'


import time
import getpass
import pickle

from lib import commons
from config import setting, templates
from src.admin import CourseAdmin, Course


class Student(object):
    """学生信息"""

    def __init__(self,username, password, gender, age):
        """初始化学生姓名，密码，性别，年龄，选择的课程，学习记录"""
        self.username = username
        self.password = password
        self.gender = gender
        self.age = age
        self.courses = []
        self.learn_record = []

    def select_course(self,course):
        """选课"""
        # 如果课程已经选择，不再添加
        for obj in self.courses:
            if obj.name == course.name:
                break
        else:
            self.courses.append(course)
            commons.log_write("学生 %s 选择了课程 %s" %(self.username, course.name))

    def show_course(self):
        """输出所有已选课程"""
        print(templates.selected_course)
        for index, course in enumerate(self.courses, 1):
            print("%s、课程名称:%s\t授课老师:%s" %(index, course.name, course.teacher.name))

    def learning(self,course):
        """学生上课"""
        print("--------- 开始上课 ---------\n")
        print("学习内容: %s" % course.content)
        print("\n--------- 上课结束 ---------\n")

        # 添加学习记录
        self.learn_record.append({
            'time': time.strftime("%Y-%m-%d %H:%M:%S"),
            'course': course
        })

        commons.log_write("学生 %s 学习了课程 %s" %(self.username, course.name))

    def show_record(self):
        """输出学习记录"""
        print(templates.learning_record)
        for record in self.learn_record:
            course = record.get('course')
            print("时间:%s\t课程名称:%s\t\t授课老师:%s" %(record['time'], course.name, course.teacher.name))


class StudentAdmin(object):
    """学生管理"""
    __students = None

    def __init__(self):
        self.students = []

    def register(self):
        """学生注册"""
        print(templates.student_add)

        # 姓名
        while True:
            username = input("姓名:")
            for obj in self.students:
                if username == obj.username:
                    print("用户名已存在，请重新输入!!!")
                    break
            else:
                break

        # 密码
        while True:
            password1 = getpass.getpass("密码:")
            password2 = getpass.getpass("再次输入密码:")
            if password2 == password1:
                password = commons.md5(password1)
                break
            else:
                print("两次密码不相同，请重新输入!!!")

        # 性别
        while True:
            user_input = input("[1:男/2:女]请选择:")
            if user_input == '1':
                gender = '男'
                break
            elif user_input == '2':
                gender = '女'
                break
            else:
                continue

        # 年龄
        while True:
            try:
                age = int(input("年龄:"))
                break
            except Exception as e:
                commons.log_write("学生注册-年龄输入错误 %s" % e)
                print()
                continue

        self.students.append(Student(username, password, gender, age))
        self.write()

        commons.log_write("新注册学生 %s" %(username,))

    def login(self):
        """学生登录"""
        username = input('请输入用户名:').strip()
        password = getpass.getpass('请输入密码:').strip()

        for obj in self.students:
            if obj.username == username and obj.password == commons.md5(password):
                commons.log_write("学生 %s 登录成功" % username)
                return obj
        else:
            commons.log_write("学生 %s 登录失败" % username)
            return False

    def write(self):
        """写入文件"""
        pickle.dump(self, open(setting.STUDENT_DB,'wb'))

    def show_students(self):
        """输出所有学习信息"""
        print(templates.student_info)
        for obj in self.students:
            print("姓名: %s\t性别: %s\t年龄: %s" %(obj.username, obj.gender, obj.age))

    @staticmethod
    def get_students():
        """如果实例已经创建，则直接返回，否则创建"""
        if not StudentAdmin.__students:
            StudentAdmin.__students = StudentAdmin()
        return StudentAdmin.__students
