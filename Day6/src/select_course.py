# /user/bin/env python
__author__ = 'wenchong'

import os
import pickle
from config import setting, templates
from src import init
from src.admin import Teacher, Course, TeacherAdmin, CourseAdmin
from src.student import Student, StudentAdmin
from lib import commons


def admin_run():
    """管理员操作"""

    if os.path.isfile(setting.ADMIN_DB):
        admin_obj = pickle.load(open(setting.ADMIN_DB, 'rb'))
    else:
        commons.log_write("管理员账户不存在，请先创建管理员！！！")
        print("管理员账户不存在，请先创建管理员！！！")
        exit()

    if not admin_obj.get_status():
        commons.log_write("登录失败")
        print("登陆失败")
    else:
        try:
            teachers_obj = pickle.load(open(setting.TEACHER_DB,'rb'))
        except:
            teachers_obj = TeacherAdmin.get_teachers()

        try:
            courses_obj = pickle.load(open(setting.COURSE_DB,'rb'))
        except:
            courses_obj = CourseAdmin.get_courses(teachers_obj)

        menu = """
        1、添加老师
        2、显示老师信息
        3、添加课程
        4、显示课程信息
        5、添加学生
        6、查看学生信息
        q、退出
        """

        action = {
            "1": teachers_obj.add_teacher,
            "2": teachers_obj.show_teachers,
            "3": courses_obj.add_course,
            "4": courses_obj.show_courses,
            "5": student_register,
            "6": student_show,
            "q": exit
        }

        while True:
            print(templates.admin_index)
            print(menu)
            user_input = input('请选择:').strip()
            if user_input in action:
                action[user_input]()
                input("\n按回车键继续")


def student_register():
    """注册学生"""
    try:
        students_obj = pickle.load(open(setting.STUDENT_DB,'rb'))
    except:
        students_obj = StudentAdmin.get_students()

    students_obj.register()


def student_show():
    """显示所有学生信息"""
    try:
        students_obj = pickle.load(open(setting.STUDENT_DB,'rb'))
    except:
        students_obj = StudentAdmin.get_students()

    students_obj.show_students()


def student_run():
    """学生操作"""

    try:
        students_obj = pickle.load(open(setting.STUDENT_DB,'rb'))
    except:
        students_obj = StudentAdmin.get_students()

    try:
        teachers_obj = pickle.load(open(setting.TEACHER_DB,'rb'))
    except:
        teachers_obj = TeacherAdmin.get_teachers()


    try:
        courses_obj = pickle.load(open(setting.COURSE_DB,'rb'))
    except:
        courses_obj = CourseAdmin.get_courses(teachers_obj)

    # 学生登录
    student = students_obj.login()

    if not student:
        print("登陆失败")
    else:
        # 登录成功
        print(templates.student_index)

        menu = """
        1、选课
        2、上课
        3、已选课程
        4、上课记录
        q、退出
        """
        while True:
            print(menu)
            user_input = input("请选择:")

            # 选课
            if user_input == '1':
                print(templates.course_list)
                for index, obj in enumerate(courses_obj.courses, 1):
                    print("%s、课程名称:%s\t授课老师:%s" % (index, obj.name, obj.teacher.name))

                while True:
                    try:
                        user_input = input("请选择:")
                        course = courses_obj.courses[int(user_input) - 1]
                        student.select_course(course)
                        students_obj.write()
                        break
                    except KeyboardInterrupt:
                        break
                    except:
                        continue
                input("按回车键继续")

            # 上课
            elif user_input == '2':
                student.show_course()
                while True:
                    user_input = input("请选择:")
                    try:
                        course = student.courses[int(user_input) - 1]
                        student.learning(course)
                        break
                    except:
                        continue
                while True:
                    user_input = input("[1:好/2:不好]请评价:")
                    if user_input == '1':
                        course.for_good()
                        break
                    elif user_input == '2':
                        course.for_bad()
                        break
                    else:
                        continue

                students_obj.write()
                teachers_obj.update_teacher(course.teacher)

                input("按回车键继续")

            # 已选课程
            elif user_input == '3':
                student.show_course()
                input("按回车键继续")

            # 上课记录
            elif user_input == '4':
                student.show_record()
                input("按回车键继续")

            elif user_input == 'q':
                exit()


def run(args):
    msg = "\n\t{0[0]} init\n\t{0[0]} admin\n\t{0[0]} student\n".format(args)
    if len(args) != 2:
        print(msg)
    else:
        if args[1] == 'init':
            init.run()
        elif args[1] == 'admin':
            admin_run()
        elif args[1] == 'student':
            student_run()
        else:
            print(msg)






