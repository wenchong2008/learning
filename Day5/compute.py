# /user/bin/env python
__author__ = 'wenchong'


import re


def compute_mul_div(expression):
    """
    处理乘除法
    """
    # 两个数乘除表达式
    mul_div_expression = re.compile('\d+\.?\d*[\*/]{1}[\+\-]?\d+\.?\d*')

    while True:
        # 匹配表达式中的两数乘除
        mul_div = mul_div_expression.search(expression)
        # 如果不存在则返回表达式
        if not mul_div:
            return expression

        else:
            # 获取两数乘除表达式
            mul_div = mul_div.group()
            # 获取数字与运算符
            num1, operator, num2 = re.split('([\*/]{1})',mul_div)

            if operator == '*':
                value = float(num1) * float(num2)
            else:
                value = float(num1) / float(num2)

            # 将乘除之后的结果与前后表达式拼接，生成新的表达式
            before, after = mul_div_expression.split(expression,1)
            expression = '%s%s%s' % (before,value,after)


def compute_add_sub(expression):
    """
    处理加减法
    """

    # 生成两个数加减的正则表达式
    add_sub_expression = re.compile('[\+\-]?\d+\.?\d*[\+\-]{1}\d+\.?\d*')
    while True:
        # 将 +-,-+,++,-- 符号替换
        while True:
            if re.search('\+\-|\-\+|\+\+|\-\-', expression):
                expression = re.sub('\+\-|\-\+', '-', expression)
                expression = re.sub('\+\+|\-\-', '+', expression)
            else:
                break

        # 匹配两个数的加减法
        add_sub = add_sub_expression.search(expression)

        # 如果表达式不为两个数的加减法，则返回表达式
        if not add_sub:
            return expression
        else:
            # 获取两个数加减法的表达式
            add_sub = add_sub.group()

            # 如果表达式以 - 开头，
            if add_sub.startswith('-'):
                # 删除开头的 -
                add_sub = re.sub('^\-', '', add_sub)

                # 获取运算符与前后的数字，如果运算符位 +，则两个数字相减，如果运算符位 -，则两个数字相加,并被 0 减，取负值
                num1,operator,num2 = re.split('([\+\-]{1})', add_sub)
                if operator == '+':
                    value = float(num1) - float(num2)
                else:
                    value = float(num1) + float(num2)
                value *= -1
            else:
                # 删除开头的 +
                add_sub = re.sub('^\+', '', add_sub)
                # 获取运算符与前后的数字，如果运算符位 +，则两个数字相加，如果运算符位 -，则两个数字相减
                num1, operator, num2 = re.split('([\+\-]{1})', add_sub)
                if operator == '+':
                    value = float(num1) + float(num2)
                else:
                    value = float(num1) - float(num2)

            # 使用表达式计算后的值与表达式前后拼出新的表达式
            before, after = add_sub_expression.split(expression, 1)
            expression = '%s%s%s' % (before, value, after)


def compute(expression):
    """
    依次处理乘除法，加减法，并返回运算值
    """
    expression = compute_mul_div(expression)
    value = compute_add_sub(expression)

    return value


def remove_bracket(expression):
    """
    去除括号
    """

    # 去除表达式中的所有括号
    while True:
        if not re.search('\([^\(\)]+\)', expression):
            return expression
        else:
            before, someting, after = re.split('\(([^\(\)]+)\)', expression, 1)
            value = compute(someting)
            expression = "%s%s%s" % (before, value, after)


def main():
    """
    主函数，获取表达式，并计算，返回值
    """
    expression = input("请输入表达式:")
    # 删除表达式中的空白
    expression = re.sub('\s*', '', expression)
    # 去括号
    expression = remove_bracket(expression)
    # 计算值
    value = compute(expression)
    print(value)


if __name__ == '__main__':
    main()