模拟账号登陆
===

### 文件描述信息
* loginauth.py
    描述：
        入口程序，用于模拟账号登陆
        该程序仅适用于 python3.x，如 python 版本为 2.x，请升级至 3.x
    执行方法：
        1、chmod +x login.py; ./login.py
        2、python login.py

* userinfo
    描述信息：
        记录用户名、密码以及状态信息，三段数据之间以冒号分隔，如状态信息为“!”，该用户被锁定
    文件内容格式：
        用户名:密码:锁定状态
        如用户未被锁定:  username:password:
        如用户已被锁定:  username:password:!


* loginauth.png
    描述信息：
        login.py 程序的处理逻辑图