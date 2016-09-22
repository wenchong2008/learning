# /user/bin/env python
__author__ = 'wenchong'


import time
import pickle
import getpass

from config import setting, templates
from lib import commons


class AdminUser(object):
    """管理员账号管理，包含创建，登陆"""

    def __init__(self):
        self.logintime = None
        self.username = None
        self.password = None
        self.timeout = None

    def create(self):
        """创建管理员账号"""
        username = input('请输入用户名:').strip()
        password1 = getpass.getpass('请输入密码:').strip()
        password2 = getpass.getpass('再次输入密码:').strip()

        # 获取超时时间，如不输入则使用默认值，默认值在配置文件中
        while True:
            try:
                timeout = input('请输入超时时间(%ss):' % setting.TIMEOUT).strip()
                if timeout:
                    self.timeout = int(timeout)
                else:
                    self.timeout = setting.TIMEOUT
                break
            except Exception as e:
                commons.log_write("创建管理员-超时时间配置错误 %s" % e, level = 'warning')
                continue

        # 如果两次密码一样，则将密码进行 md5 加密
        if password1 == password2:
            password = commons.md5(password1)
            self.username = username
            self.password = password
            commons.log_write("管理员创建成功")
            self.write()
            return True
        else:
            print('两次密码不一致，请重新操作')
            return False

    def write(self):
        """将数据保存到文件"""
        pickle.dump(self,open(setting.ADMIN_DB,'wb'))

    def login(self):
        """管理员登陆"""
        username = input('请输入用户名:').strip()
        password = getpass.getpass('请输入密码:').strip()

        # 登陆成功后重置登陆时间，并写入文件，返回 True
        if self.username == username and self.password == commons.md5(password):
            self.logintime = time.time()
            self.write()
            commons.log_write("管理员成功登陆")
            return True
        else:
            return False

    def logout(self):
        """注销"""
        self.logintime = None
        commons.log_write("管理员注销")

    def get_status(self):
        """获取用户状态"""

        # 如果最后登陆时间 + 超时时间大于现在的时间，则直接返回 True,否则重新登陆
        if self.logintime and self.timeout:
            if self.logintime + self.timeout > time.time():
                self.logintime = time.time()
                self.write()
                commons.log_write("缓存登陆")
                return True
            else:
                print("会话超时，请重新登陆")

        return self.login()


class Teacher(object):
    """授课教师信息"""

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age
        self.asset = 0

    def teaching(self, for_pay):
        """课时费"""
        self.asset += for_pay

    def teaching_for_bad(self, forfeit):
        """授课被评价为不好时，扣课时费"""
        self.asset -= forfeit


class TeacherAdmin(object):
    """授课教师管理"""

    __teachers = None

    def __init__(self):
        # 所有授课教师列表
        self.teachers = []

    def __fetch_name(self):
        """获取授课教师姓名"""
        self.name = input("姓名:").strip()

    def __fetch_age(self):
        """获取授课教师年龄"""
        while True:
            try:
                self.age = int(input("年龄:").strip())
                break
            except:
                continue

    def __fetch_gender(self):
        """获取授课教师性别"""
        while True:
            user_input = input("[1:男性/2:女性]:").strip()
            if user_input == '1':
                self.gender = '男'
                break
            elif user_input == '2':
                self.gender = '女'
                break
            else:
                continue

    def add_teacher(self):
        """新增授课教师"""
        print(templates.teacher_add)
        self.__fetch_name()
        self.__fetch_age()
        self.__fetch_gender()
        teacher = Teacher(self.name, self.gender, self.age)
        self.teachers.append(teacher)
        self.write()
        commons.log_write("新增授课教师 %s" % self.name)

    def show_teachers(self):
        """输出所有授课教师"""
        print(templates.teacher_info)
        commons.log_write('输出所有授课教师')
        for teacher in self.teachers:
            print('姓名: %s\t性别: %s\t年龄: %s\t资产: %s' %(teacher.name, teacher.gender, teacher.age, teacher.asset))

    def update_teacher(self,teacher):
        """更新授课教师资产，并写入文件"""
        for obj in self.teachers:
            if obj.name == teacher.name:
                obj.asset = teacher.asset
                commons.log_write("更新授课教师 %s 的资产" % obj.name)

        self.write()

    def write(self):
        """写入文件"""
        pickle.dump(self, open(setting.TEACHER_DB,'wb'))

    @staticmethod
    def get_teachers():
        """如果实例已经创建，则直接返回，否则创建"""
        if not TeacherAdmin.__teachers:
            TeacherAdmin.__teachers = TeacherAdmin()
        return TeacherAdmin.__teachers


class Course(object):
    """课程信息"""
    def __init__(self, name, for_pay, forfeit, content, teacher):
        """定义课程名称，课时费，罚款，以及授课教师"""
        self.name = name
        self.for_pay = for_pay
        self.forfeit = forfeit
        self.content = content
        self.teacher = teacher

    def for_good(self):
        """课程被评价为好"""
        self.teacher.teaching(self.for_pay)

    def for_bad(self):
        """课程被评价为不好"""
        self.teacher.teaching(self.for_pay)
        self.teacher.teaching_for_bad(self.forfeit)


class CourseAdmin(object):
    """课程信息管理"""
    __courses = None

    def __init__(self, teachers):
        self.courses = []
        self.teachers = teachers

    def __fetch_name(self):
        """课程名称"""
        self.name = input('课程名称:').strip()

    def __fetch_for_pay(self):
        """课程课时费"""
        while True:
            try:
                self.for_pay = int(input("课时费:").strip())
                break
            except Exception as e:
                commons.log_write("创建课程-课时费输入错误 %s" % e, level = 'warning')
                continue

    def __fetch_forfeit(self):
        """罚金"""
        while True:
            try:
                self.forfeit = int(input("罚金:").strip())
                break
            except Exception as e:
                commons.log_write('创建课程-罚金输入错误 %s' % e, level = 'warning')
                continue

    def __fetch_content(self):
        """课程内容"""
        self.content = input("课程内容:").strip()

    def __fetch_teacher(self):
        """课程授课教师"""
        print("--------- 老师列表 ---------")
        for index,obj in enumerate(self.teachers.teachers,1):
            print("%s、姓名: %s\t性别: %s\t年龄: %s" %(index, obj.name, obj.gender, obj.age))

        while True:
            try:
                user_input = input("\n[ctrl+c = 退出]请选择老师:").strip()
                teacher = self.teachers.teachers[int(user_input) - 1]
                return teacher
            except KeyboardInterrupt:
                break
            except Exception as e:
                commons.log_write("创建课程-授课教师选择错误 %s" % e, level = 'warning')
                continue

    def add_course(self):
        print(templates.course_add)
        self.__fetch_name()
        self.__fetch_for_pay()
        self.__fetch_forfeit()
        self.__fetch_content()
        teacher = self.__fetch_teacher()
        self.courses.append(Course(self.name, self.for_pay, self.forfeit, self.content, teacher))
        self.write()
        commons.log_write("新增课程 %s 授课教师 %s" %(self.name, teacher.name))

    def show_courses(self):
        """输出所有课程"""
        print(templates.course_info)
        for obj in self.courses:
            print('名称: %s\t课时费: %s\t罚金: %s\t授课老师: %s\t内容: %s' %(obj.name, obj.for_pay, obj.forfeit, obj.teacher.name, obj.content ))

    def write(self):
        """写入文件"""
        pickle.dump(self, open(setting.COURSE_DB,'wb'))

    @staticmethod
    def get_courses(teachers):
        """如果实例已经创建，则直接返回，否则创建"""
        if not CourseAdmin.__courses:
            CourseAdmin.__courses = CourseAdmin(teachers)
        return CourseAdmin.__courses




