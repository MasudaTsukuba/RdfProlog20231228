list_x = [1, 2, 3]


def func(list):
    list2 = list.append(4)
    return list2


list2_x = func(list_x)
print(list_x)
print(list2_x)
list_x.append(5)
print(list_x)
print(list2_x)
