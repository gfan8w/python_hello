
# 如果要定义一个空的tuple，可以写成()：
t = ()
print(t)


# 定义的不是tuple，是1这个数！这是因为括号()既可以表示tuple，
# 又可以表示数学公式中的小括号，这就产生了歧义，
# 因此，Python规定，这种情况下，按小括号进行计算，计算结果自然是1。
t = (1)
print(t)

# 只有1个元素的tuple定义时必须加一个逗号,，来消除歧义
t = (1,)
print(t)


#可变tuple， 可变的不是tuple本身，而是tuple里的list的元素
t = (1, 'a', ["A", "B"])

print(t)

t[2][0]="X"
t[2][1]="Y"

print(t)





