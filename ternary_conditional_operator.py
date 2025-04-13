from typing import List, Optional


# 如果 call 函数的参数类型注解是 List，则传递 None 可能会导致类型检查工具（如 mypy）报错。
# 为了避免这个问题，可以将参数类型注解改为 Optional[List]
def call(input: Optional[List]):
    if input is None:
        print("input is None")
    else:
        print("input is a list")


# 空列表 [] 的布尔值为 False，非空列表的布尔值为 True


a =[]
# call(if a else None)  # 错误！
call(a if a else None)

a=[1,2,3]
call(a if a else None)