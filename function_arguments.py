


def add_end(L=[]):
    L.append("end")
    return L

l=[1,2,3]
add_end(l)
print(l)   #[1, 2, 3, 'end']  正常调用不会出错

add_end()
print(l)   #使用默认参数一开始也是对的

l=add_end()
print(l) #['end', 'end'] 使用默认参数，会出错

# Python函数在定义的时候，默认参数L的值就被计算出来了，即[]，
# 因为默认参数L也是一个变量，它指向对象[]，
# 每次调用该函数，如果改变了L的内容，
# 则下次调用时，默认参数的内容就变了，不再是函数定义时的[]了


print("the correct to use the default parameter is:")


def add_end(L=None):
    if L is None:
        L = []
    L.append('END')
    return L

l=add_end()
print(l)

l=add_end()
print(l)


print("可变参数")

# 可变参数
def calc(numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum

a=calc([1, 2, 3])
print(a)

# 定义可变参数和定义一个list或tuple参数相比，仅仅在参数前面加了一个*号。
# 在函数内部，参数numbers接收到的是一个tuple
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum


a=calc(1, 2, 3)
print(a)

nums = [1, 2, 3]
a=calc(nums[0], nums[1], nums[2])
print(a)

# Python允许你在list或tuple前面加一个*号，把list或tuple的元素变成可变参数传进去
a=calc(*[1, 2, 3])
print(a)


print("关键字参数")
# 关键字参数
# 可变参数允许你传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple。
# 而关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict


def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)


person('Michael', 30)

person('Adam', 45, gender='M', job='Engineer')


extra = {'city': 'Beijing', 'job': 'Engineer'}

person('Jack', 24, city=extra['city'], job=extra['job'])
# 上面复杂的调用可以用简化的写法
person('Jack', 24, **extra)

# **extra表示把extra这个dict的所有key-value用关键字参数传入到函数的**kw参数，
# kw将获得一个dict，注意kw获得的dict是extra的一份拷贝，对kw的改动不会影响到函数外的extra


def person(name, age, **kw):
    """
    对于关键字参数，函数的调用者可以传入任意不受限制的关键字参数。至于到底传入了哪些，就需要在函数内部通过kw检查
    :param name:
    :param age:
    :param kw:
    :return:
    """
    if 'city' in kw:
        # 有city参数
        pass
    if 'job' in kw:
        # 有job参数
        pass
    print('name:', name, 'age:', age, 'other:', kw)

person('Adam', 45, job='M', city="aa")


print("命名关键字")
# 命名关键字
# 和关键字参数**kw不同，命名关键字参数需要一个特殊分隔符*，*后面的参数被视为命名关键字参数
def engineer(name, age, *, city, job):
    """
    和关键字参数**kw不同，命名关键字参数需要一个特殊分隔符*，*后面的参数被视为命名关键字参数
    :param name:
    :param age:
    :param city:
    :param job:
    :return:
    """
    print(name, age, city, job)

engineer('Jack', 24, city='Beijing', job='Engineer')

# engineer('Jack', 24, 'Beijing', job='Engineer')    # 命名关键字参数必须传入参数名,这里没传city，会报错
# engineer('Jack', 24, city2='Beijing', job='Engineer')  # 报错, city2不在命名关键词参数里

# 如果函数定义中已经有了一个可变参数，后面跟着的命名关键字参数就不再需要一个特殊分隔符*了
def person1(name, age, *args, city, job):
    print(name, age, args, city, job)


# 在Python中定义函数，可以用必选参数、默认参数、可变参数、关键字参数和命名关键字参数，
# 这5种参数都可以组合使用。但是请注意，
# 参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数
def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)

def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)


f1(1,2)
f1(1, 2, c=3)
f1(1, 2, 3, 'a', 'b')
f1(1, 2, 3, 'a', 'b', x=99)
f2(1, 2, d=99, ext=None)

args = (5, 6, 7, 8)
kw = {'x': 99, 'y': '#'}
f1(*args, **kw)

args = (20, 30, 40)
kw = {'d': 100, 'J': 'good'}
f2(*args, **kw)   #只支持3个位置参数，必须要有命名参数d

# 对于任意函数，都可以通过类似func(*args, **kw)的形式调用它，无论它的参数是如何定义的






