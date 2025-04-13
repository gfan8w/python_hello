
a = 10

def updateGlobal():
    a = 5
    print(a) # 5

updateGlobal()
print(a)  # 10, not changed to 5


def updateGlobal1():
    global a
    a = 3

updateGlobal1()
print(a)    # changed to 3

