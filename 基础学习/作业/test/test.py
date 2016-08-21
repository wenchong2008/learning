# /user/bin/env python
__author__ = 'wenchong'

print('#'*100)
print('测试项目 1：')
# 一、元素分类
# 有如下值集合 [11,22,33,44,55,66,77,88,99,90...]，将所有大于 66 的值保存至字典的第一个key中，将小于 66 的值保存至第二个key的值中。
# 即： {'k1': 大于66的所有值, 'k2': 小于66的所有值}

li = [11,22,33,44,55,66,77,88,99,90]
more_than_66 = []
less_than_66 = []
for i in li:

    if i > 66:
        more_than_66.append(i)
    else:
        less_than_66.append(i)
dict = {
    'more_than_66':more_than_66,
    'less_than_66':less_than_66,
}
print(dict)


print('#'*100)
print('测试项目 2：')
# 二、查找
# 查找列表中元素，移除每个元素的空格，并查找以 a或A开头 并且以 c 结尾的所有元素。
#     li = ["alec", " aric", "Alex", "Tony", "rain"]
#     tu = ("alec", " aric", "Alex", "Tony", "rain")
#     dic = {'k1': "alex", 'k2': ' aric',  "k3": "Alex", "k4": "Tony"}

li = ["alec", " aric", "Alex", "Tony", "rain"]
for i in li:
    # i.strip() 去除掉左右的空格
    # i.split() 以空格分割为列表
    i = i.strip().split()
    # "".join(i) 以空字符串连接列表 i 的每一个元素
    i = "".join(i)
    # 当 i 以 A 或 a 开头，并且以 c 结尾时，输出 i
    if i.startswith(('a','A')) and i.endswith('c'):
        print(i)

print('#'*100)
print('测试项目 3：')
# 三、输出商品列表，用户输入序号，显示用户选中的商品
#     商品 li = ["手机", "电脑", '鼠标垫', '游艇']

li = ["手机", "电脑", '鼠标垫', '游艇']
for k,v in enumerate(li,1):
    print(k,v)

user_input = input("请输入商品对应的序号: ")
for k,v in enumerate(li,1):
    if int(user_input) == k:
        print('您选择的商品为：',v)

print('您选择的商品为：',li[int(user_input)-1])



a = {'a':'a','b':'b'}


import json
json.load()