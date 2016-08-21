shopping.py
    描述信息：
        入口程序，用于登陆系统并进行购物
        该程序仅适用于 python3.x，如 python 版本为 2.x，请升级至 3.x

        任何界面支持 ctrl+c 退出程序

    执行方法：
        1、chmod +x shopping.py; ./shopping.py
        2、python shopping.py

login.py
    描述信息：
        登陆模块，登陆系统，如果密码3次错误则锁定，登陆成功返回用户名信息

userinfo
    描述信息：
        记录用户名、密码、状态以及配置文件信息，三段数据之间以冒号分隔，如状态信息为“!”，该用户被锁定
    文件内容格式：
        用户名:密码:锁定状态:配置文件
        如用户未被锁定:  username:password::dir/file
        如用户已被锁定:  username:password:!:dir/file
product.json
    描述信息：
        该文件为json 格式，存储商品的分类以及价格信息，文件不存在时会退出程序

userconf
    描述信息：
        用户配置目录，里面存有所有用户的配置文件，配置文件为 json 格式，里面存储用户余额以及购物车信息
        该目录如不存在会自动创建。

shopping-flowchart.png
    描述信息：
        shopping.py 的流程图

