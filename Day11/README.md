第十一天作业

类 RPC

blog:http://www.cnblogs.com/wenchong


文件描述：

    1、Client
            a、bin
                    client.py: 客户端程序
                        python client.py 10.211.55.5
                        python client.py
            b、config
                    setting.py: 配置文件，执行 RabbitMQ 服务器地址
            c、src
                    Client.py: 客户端逻辑程序文件
    2、Server
            a、bin
                    server.py: 服务端程序
                        python server.py -H 10.211.55.5 "ls -l"
                        python server.py -G group1 "ls -l"
            b、config
                    setting.py: 配置文件，执行 RabbitMQ 服务器地址
                    groups: 配置组
            c、src
                    Server.py: 服务端逻辑程序文件
    
            
            
主要功能

    1、在运行了客户端程序的服务器上远程执行命令并返回结果
    
运用到的知识

    1、字典、列表的使用
    2、argparse，paramiko, pika 等模块的使用
    3、面向对象
    4、RabbitMQ 生产者消费者模型

实例

    1、在客户端服务器运行客户端程序
            python client.py
            python client.py 10.211.55.5
    2、配置主机组
            修改 config/groups.py 文件
            格式： group = ['10.211.5.5', '10.211.55.6']
    3、执行命令
            python server.py -H 10.211.55.5 "ls -l"
            python server.py -G group "ls -l"
    
            
           
    