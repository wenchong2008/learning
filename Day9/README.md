第九天作业

FTP工具-扩展

blog:http://www.cnblogs.com/wenchong


文件描述：

    1、ftp_server
        a、bin
            FTPServer.py    FTP Server程序，启动 FTP Server
            UserAdmin.py    FTP 用户管理程序，用于添加账号
            
        b、config
            setting.py      FTP Server 配置文件
                
        c、database          
                程序数据信息存放目录
                
        d、homedir
                用户家目录所在路径
                
        e、lib
            commons.py      公共函数
            
        f、log
                日志文件
                
        g、src   
            程序逻辑函数目录
            FTPServer.py    FTP Server程序逻辑文件
            UserAdmin.py    FTP 用户管理逻辑文件
        
        h、FTPServer.png
            FTP Server 流程图
            
        i、UserAdmin.png
            用户管理流程图
            
    2、ftp_client
        a、bin
            FTPClient.py    FTP 客户端程序，连接 FTP Server
            
        b、src
            FTPClient.py    FTP 客户端逻辑文件
           
        c、lib
            commons.py      公共函数
        
        d、FTPClient.png
            流程图
            
            
主要功能

    1、显示服务器文件信息【ls】
    2、切换目录【cd】
    3、获取当前目录【pwd】           
    4、上传文件【put】
    5、下载文件【get】
    6、创建目录【mkdir】
    7、删除文件或目录【rm】
    8、磁盘配额
    9、上传现在文件进度条
    10、用户加密认证
    11、断点续传
    12、用户只能查看自己的家目录
    
运用到的知识

    1、字典、列表的使用
    2、time，logging，os，pickle 等模块的使用
    3、面向对象
    4、socket 网络编程
    5、多线程
           
    