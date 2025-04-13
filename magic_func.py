
# __call__
# 在Python中，__call__是一个特殊方法，赋予了对象可被直接调用的能力 ，
# 就像函数一样。当一个类实例被当作函数调用时，
# 实际上就是在调用这个类的__call__方法。这为设计灵活、行为动态的对象提供了强大手段，
# 使得对象可以模仿函数行为，实现更高级的面向对象编程模式。

class Counter:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return self.count

# 创建Counter实例
my_counter = Counter()
print(my_counter())  # 输出: 1




