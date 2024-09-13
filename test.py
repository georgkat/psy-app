import random

some_args = {"one": 1, "two": 2}
some_other_args = {'three': 3}

print(some_args)

some_args.update(some_other_args)

print(some_args)

x = [random.randint(1, 9) for n in range(0, 3)]
print(tuple(x))