
# input()返回的数据类型是str，str不能直接和整数比较，
# 必须先把str转换成整数。Python提供了int()函数来完成这件事情

birth = "2" #input("birth:")
if int(birth) < 2000:
    print("00前")
else:
    print("00后")



# match 模式匹配
age = 15
match age:
    case x if x<10:
        print(f'< 10 years old: {x}')
    case 10:
        print('10 years old')
    case 11 | 12 | 13 |14 | 15:
        print('11-15 years old')
    case _:
        print('15+ years old')


# 第二个case ['gcc', file1, *files]表示列表第一个字符串是'gcc'，
# 第二个字符串绑定到变量file1，后面的任意个字符串绑定到*files（
# 符号*的作用将在函数的参数中讲解），它实际上表示至少指定一个文件
args = ["gcc", 'hello.c', 'world.c', 'test.c']
# args = ["gcc"]
match args:
    case ['gcc']:
        print("gcc miss source file(s).")
    case ['gcc', file1, *files]:
        print(f"gcc {file1} {' '.join(files)}")
    case ["clean"]:
        print("clean source file(s).")
    case _:
        print("unknown command.")






