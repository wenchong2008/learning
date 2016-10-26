##描述
第十二天作业：`类堡垒机`


##文件说明

    ├── bin
    │    ├── hostAdmin.py: 用户管理程序
    │    ├── jump.py: 跳转程序
    ├── config
    │    ├── setting.py: 数据库连接信息
    ├── src
    │    ├── Models.py: 数据表创建以及管理逻辑程序文件
    │    ├── HostAdmin.py: 用户管理逻辑程序文件
    │    ├── Jump.py: 跳转程序文件
    ├── HostUserAdmin.png
    ├── Jump.png
         
            
##主要功能

* 登陆到登陆到跳转机,通过堡垒机系统账号登陆并选择有权限的账号进行登陆到远程服务器
    
##运用到的知识
* 字典、列表的使用
* `argparse`，`paramiko`, `pika` 等模块的使用
* 面向对象
* `RabbitMQ` 生产者消费者模型

##使用方法：
1. 在跳转机上安装 `sqlalchemy`, `pymysql` 模块
2. 在跳转机上创建跳转账号

        useradd audit
        passwd audit
3. 上传代码到跳转机目录 `/home/audit/{name}`
4. 分配权限

        chown audit:audit /home/audit/{name}
5. 在 `/home/audit/.bashrc` 文件中添加

        python /home/audit/{name}/bin/jump.py
        logout
6. 添加管理信息

        python /home/audit/{name}/bin/hostAdmin.py
        python /home/audit/{name}/bin/hostAdmin.py host  #添加远程主机信息
        python /home/audit/{name}/bin/hostAdmin.py group  #添加group
        python /home/audit/{name}/bin/hostAdmin.py user  #添加堡垒机账号信息
        python /home/audit/{name}/bin/hostAdmin.py info  #查看堡垒机账号信息
            
            
            
       
    
            
           
    