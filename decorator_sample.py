import functools


def now():
   print('2025-04-13')



f = now
print(f.__name__)  # now



def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    a = wrapper
    a.__name__ = func.__name__
    return a

@log
def now_date():
   print('2025-04-13')




# @log 相当于是 now = log(now_date)
# now_date()

f = now_date
print("fun name: %s" % f.__name__)  #但是现在函数名字变为了wrapper，而不是now_date2，需要修正: 加入 a.__name__ = func.__name__



def now_date2():
   print('2025-04-13')
now_var2 = log(now_date2)
now_var2()

f = now_var2
print("now_var2 name: %s" % f.__name__)  #但是现在函数名字变为了wrapper，而不是now_date2，需要修正




# 如果decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数，
def log2(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator


@log2("execute")
def now_date2():
   print('2025-04-13')


now_date2()  # now = log('execute')(now) 和两层嵌套的decorator相比，3层嵌套的效果是这样的


def log3(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator


@log3("execute")
def now_date3():
   print('2025-04-13')


f = now_date3
print(f.__name__)