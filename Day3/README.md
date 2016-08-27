第三天作业

修改 haproxy 配置文件内容


文件描述：
    1、haproxy.py
        程序主文件
    2、conf
        目录下存放 haproxy 配置文件以及 haproxy 的备份文件
    3、haproxy.png
        程序流程图


主要的功能：
    1、添加记录
        输入 json 格式数据
        判断 backend 是否存在
            存在：将 record 记录添加到 backend 之后
            不存在：将 backend 与 record 添加到文件结尾
        备份配置文件，文件后增加时间
        展示添加后的 backend 记录
        
    2、删除记录
        输入 json 格式数据
        判断 backend 是否存在
            存在：
                删除 record 记录后，backend 下是否还有 record 记录
                    有：在新文件中删除输入的 record
                    无：在新文件中删除输入的 record 和 backend 记录
                备份配置文件，文件后增加时间
                展示删除后的 backend 记录
            不存在：退出
    3、获取记录
        输入 backend 域名
        获取 backend 下的记录
        展示 backend 下的记录
        
        
运用到的知识点：
    1、字典，列表、函数的使用
    2、json 模块将字符串转换为 json 数据
    3、with...as... 对单文件以及多文件的操作
    4、format 格式化字符串
    5、循环标记位的使用
    6、try except 异常处理
    7、os 模块重命名文件
    8、while for 循环的使用
    
    