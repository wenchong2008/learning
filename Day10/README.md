第十天作业

类 Fabric

blog:http://www.cnblogs.com/wenchong


文件描述：

    1、bin: 程序可执行文件目录
            hostAdmin.py:   主机管理入口
            myFabric.py:    远程主机操作入口
    2、config: 程序配置文件目录
            setting.py:     程序配置文件
            groups.py:      主机组配置管理文件
    3、database: 程序数据信息存放目录
            hosts:          所有主机的保存文件目录
    4、lib: 程序公共文件目录
            commons.py: 公共函数
    5、src: 程序逻辑函数目录
            HostAdmin.py:   主机管理逻辑程序
            MyFabirc.py:    远程主机操作逻辑程序
    6、hostAdmin.png:       主机管理流程图
    7、myFabric.png:        远程主机操作流程图
    
            
            
主要功能

    1、添加需要管理的远程主机
    2、查看所有已经添加的管理主机
    3、查看所有的主机组
    4、在远程主机或主机组执行命令
    5、上传文件的主机或主机组中的所有主机
    6、从远程主机下载文件，或将远程主机组中的文件下载到本地
    
运用到的知识

    1、字典、列表的使用
    2、os，pickle，argparse，paramiko 等模块的使用
    3、面向对象

实例

    1、添加主机
            python3.5 bin/hostAdmin.py add -H 10.211.55.5 -u root -p password
            python3.5 bin/hostAdmin.py add -H 10.211.55.5
    2、查看主机或主机组
            python3.5 bin/hostAdmin.py list -G
            python3.5 bin/hostAdmin.py list -H
    3、执行命令
            python3.5 bin/myFabric.py -H 10.211.55.5 run "ls"
            python3.5 bin/myFabric.py -G group1 run "ls"
    4、上传文件
            python3.5 bin/myFabric.py -H 10.211.55.5 upload localpath remotepath
            python3.5 bin/myFabric.py -G group1 upload localpath remotepath
    5、下载文件
            python3.5 bin/myFabric.py -H 10.211.55.5 download remotepath localpath
            python3.5 bin/myFabric.py -G group1 download remotepath localpath
            
           
    