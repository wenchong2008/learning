第四天作业

模拟 ATM 操作


blog:http://www.cnblogs.com/wenchong


文件描述:

    1、bin: 程序可执行文件目录
        creditcard.py: 程序入口文件
            运行方式:
                python creditcard.py init       # 初始化用户信息
                python creditcard.py admin      # 管理员登陆
                python creditcard.py client     # 普通用户登陆
                python creditcard.py crontab    # 生成账单与计算利息
                
    2、config: 程序配置文件目录
            setting.py: 程序配置文件
            templates.py: 模板配置
            
    3、db: 程序数据信息存放目录
            credit_user.json: 用户信息文件
            
    4、lib: 程序公共文件目录
            common.py: 公共函数
            
    5、log: 程序日志文件目录
    
    6、src: 程序逻辑函数目录
            admin.py： 管理员配置模块
            client.py: 客户端管理模块
            creditcard.py: 主模块
            crontab.py: 账单与利息模块
            init.py: 初始化模块
            
    7、creditcard.png: 流程图
    
    
主要的功能:

    1、init
            初始化用户信息，创建管理员账号
    2、admin
            添加、删除、冻结、解冻、查询账户
    3、client
            提现、转账、还款、查看信用卡，查看账单、查看交易
    4、crontab
            生成账单，产生利息
            

运用到的知识：

    1、字典、列表的使用
    2、time，logging，os，json 等模块的使用
    
    