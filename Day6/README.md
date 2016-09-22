第六天作业

模拟选课系统


blog:http://www.cnblogs.com/wenchong


文件描述:

    1、bin: 程序可执行文件目录
        select_course.py: 程序入口文件
            运行方式:
                python select_course.py init       # 初始化管理员信息
                python select_course.py admin      # 管理员登陆
                python select_course.py student    # 学生登陆
                
    2、config: 程序配置文件目录
            setting.py: 程序配置文件
            templates.py: 模板配置
            
    3、db: 程序数据信息存放目录
            
    4、lib: 程序公共文件目录
            commons.py: 公共函数
            
    5、log: 程序日志文件目录
    
    6、src: 程序逻辑函数目录
            admin.py: 管理员配置模块
            init.py: 管理员初始化模块
            select_course.py: 主模块
            sutdent.py: 学生模块
            
    7、select_course.png: 流程图
    
    
主要的功能:

    1、init
            初始化用户信息，创建管理员账号
    2、admin
            添加、查看老师，学生，课程信息
    3、student
            选课，上课，查看已选课程，查看上课记录

            

运用到的知识：

    1、字典、列表的使用
    2、time，logging，os，pickle 等模块的使用
    3、面向对象
    
    