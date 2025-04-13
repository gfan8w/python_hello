

def simple_generator():
    yield 1
    yield 2
    yield 3

# Using the generator
gen = simple_generator()
print(next(gen))  # Output: 1
print(next(gen))  # Output: 2
print(next(gen))  # Output: 3

# infinite sequences
def infinite_counter():
    count = 0
    while True:
        yield count
        count += 1

counter = infinite_counter()
print(next(counter))  # 0
print(next(counter))  # 1
# ... and so on indefinitely


# Pipelining Generators
def squares(nums):
    for n in nums:
        yield n ** 2

def even(nums):
    for n in nums:
        if n % 2 == 0:
            yield n

# Pipeline: even numbers from squares of 0-9
result = even(squares(range(10)))
print(list(result))  # [0, 4, 16, 36, 64]

# send() In Generators
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

acc = accumulator()
print(next(acc))  # Start the generator
print(acc.send(10))  # 10
print(acc.send(20))  # 30


def chain_generators(*iterables):
    for it in iterables:
        yield from it

combined = chain_generators([1, 2], (3, 4), "ab")
print(list(combined))  # [1, 2, 3, 4, 'a', 'b']

# 使用 yield from 会一行一行的输出：
# a
# b
# c
# d
# ...
# 直接使用 yield 会输出一个字符串：
def yield_string(s: str):
    yield s

gen = yield_string("abcdefghijkl")
for s in gen:
    print(s+"\n")









