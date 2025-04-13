fruits = ["apple", "banana", "cherry"]

# Create a dictionary with the key as the fruit and the value as the length of the fruit
mydict = {fruit: len(fruit) for fruit in fruits}
print(mydict)

# Filtering Items From Dictionaries
mydict1 = {fruit: len(fruit) for fruit in fruits if len(fruit) ==6}
print(mydict1)


# To make your code memory-efficient,
# you may use a generator expression that
# yields tuples of the form (key, value) instead:
squares_generator = ((x, x * x) for x in range(10))

print(next(squares_generator))
print(next(squares_generator))
print(next(squares_generator))
print(next(squares_generator))



# nested comprehensions with several for clauses or several conditionals
fruits = {"apple": 1.0, "banana": 0.5, "cherry": 2.0, "mango": 2.3}
with_discount = ["apple", "cherry"]
fruits_price={ fruit: price*0.9 if fruit in with_discount else price  for fruit, price in fruits.items()}
print(fruits_price)



# transformations dict
parts = [
    "CPU",
    "GPU",
    "Motherboard",
    "RAM",
    "SSD",
    "Power Supply",
    "Case",
    "Cooling Fan"
]

stocks = [15, 8, 12, 30, 25, 10, 5, 20]

parts_stock={parts[i]:stocks[i] for i in range(len(parts))}
print(parts_stock)

# use the built-in zip() function to create pairs of items.
# This function takes two or more iterables as arguments and
# yields tuples of items by getting one item from each iterable.
parts_stock={ part:stock for part, stock in zip(parts, stocks)}
print(parts_stock)


part_costs = [250, 500, 150, 80, 100, 120, 70, 25]
parts_total_cost = {part: stock * cost for part, stock, cost in zip(parts, stocks, part_costs)}
print(parts_total_cost)





