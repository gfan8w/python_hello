add = lambda x, y: x+y

a = add(1,4)
print(a)

#无参lambda
a=(lambda : 1)()  # 1
print(a)

#可变参数 *args
fn1 = lambda *args: args
print(fn1(10, 20, 30))  # 【输出结果为：（10，20，30）】

# 可变参数：**kwargs
fn1 = lambda **kwargs: kwargs
print(fn1(name='python', age=20))

#条件判断
a= (lambda x,y : x if x>y else y)(3,4)  # 4
print(a)

#字典结合
d = {"+": lambda x,y: x+y, "-": lambda x,y: x-y}
a=d['+'](3,8)
print(a)


#作为 map的迭代方法
m = [1,2,3,4,5,6]
result = map(lambda x: x+1, m)
print(list(result))


#作为 filter的迭代方法
result = filter(lambda x: x % 2==1, m)
print(list(result))

#作为sorted的key方法
s=[{'name':'tom', 'age':18}, {'name':'lily', 'age':20}, {'name':'lucy', 'age':15}]
s_l=sorted(s, key=lambda x:x['age'], reverse=True)
print(s_l)

s.sort(key=lambda x: -x['age']) #逆序 ，前面加 -
print(s)


# 在lambda表达式中，我们使用(x['field1'], x['field2'])作为排序的key。
# 这样可以先按field1进行排序，如果field1相同，则按field2进行逆序排序。
data = [
    {'field1': 3, 'field2': 2},
    {'field1': 1, 'field2': 5},
    {'field1': 2, 'field2': 1},
    {'field1': 2, 'field2': 5},
    {'field1': 4, 'field2': 4}
]

sorted_data = sorted(data, key=lambda x: (x['field1'], -x['field2']))

for d in sorted_data:
    print(d)


#reduce
from functools import reduce
result = reduce(lambda x,y: x+y, m)
print(result)


#iter迭代器
# 根本原因：迭代器是可变对象，且默认参数在函数定义时仅初始化一次。
# 输出 a b c：每次调用 n() 时，next(y) 从同一个迭代器中按顺序返回值。
# 关键结论：
# 迭代器会记住状态。
# 默认参数如果是可变对象（如迭代器、列表、字典），会在多次调用中共享状态。
# 这种特性可以用于需要记忆状态的场景，但也需注意默认参数的共享可能引发意外的副作用
# y=iter('abcdefg') 是 lambda 函数的默认参数，仅在函数定义时初始化一次。
n = lambda x,y=iter('abcdefg'): next(y)

print(n(None))  # 输出 'a'
print(n(None))  # 输出 'b'
print(n(None))  # 输出 'c'


n = lambda x, y=iter('abcdefg'): (next(y), id(y))

print(n(None))  # 输出 ('a', 140000000)
print(n(None))  # 输出 ('b', 140000000) → 相同的内存地址


def foo(x, y=0):
    y += 1
    return y

print(foo(None))  # 输出 1
print(foo(None))  # 输出 1（每次调用 y 重新初始化为 0）





# 示例1：对 args 中的每个元素加 1，返回新元组
fn2 = lambda *args: tuple(x + 1 for x in args)
print(fn2(10, 20, 30))  # 输出: (11, 21, 31)

# 过滤出 args 中的偶数
fn5 = lambda *args: tuple(x for x in args if x % 2 == 0)
print(fn5(10, 21, 30, 40))  # 输出: (10, 30, 40)

# 示例2：计算 args 的和
fn3 = lambda *args: sum(x for x in args)
print(fn3(10, 20, 30))  # 输出: 60

# 示例3：打印 args 中的每个元素（需用函数包裹，因为 lambda 不能直接包含语句）
def print_args(*args):
    for x in args:
        print(x)

fn4 = lambda *args: print_args(*args)
fn4(10, 20, 30)  # 输出: 10, 20, 30（每行一个）

