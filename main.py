# This is a sample Python script.
import sys


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    int
    i1 = 1 + \
         2
    print(i1)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
if True:
    print("123123123")
else:
    print("else")

str = "12345678"
# str[1:2:3]3个参数，第一个表示开始位置从开始，第二个参数表示结束位置（不包含下标本身，含头不含尾），三个参数表示截取步长，每次截取间隔多长
# 输出第一个字符
print(str[0])
# 输出第一个到最后一个 （下表从0开始，不包含结尾）
print(str[0:-1])

# print默认是换行输出 添加end=""表示不换行
print(str[0:-1:2], end="")
print(str[0::7])

print("导入模块")
# sys.argv获得一个数组，第一个元素表示当前程序文件
for i in sys.argv:
    print(i)
print("python path", sys.path)

# type()函数可以查询变量类型 不会认为子类是父类类型
a, b, c, d = 1, 1.0, False, 4 + 3j
print(type(a), type(b), type(c), type(d))


# 对象A
class A:
    pass


# 对象B
class B(A):
    pass


# isinstance()函数同样是查询变量类型，但是会认子类是一种父类类型
print(type(A()) == A)
print(isinstance(A(), A))
print(type(B()) == A)
print(isinstance(B(), A))
# 类型比较
print(issubclass(bool, int))

print(2**31-1)
print(2**31)
num = 2**31
print(type(num))
