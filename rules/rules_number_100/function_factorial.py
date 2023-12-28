"""
factorial
called from exec()
T. Masuda, 2023/12/22
"""

local_bindings = {}

for key1, value1 in bindings.items():
    key_modified = key1.replace(f'http://some.org/_', '').replace(f'http://variable.org/_', '')  # -> x
    value_modified = value1.replace('http://value.org/', '').replace('http://variable.org/', '')
    local_bindings[key_modified] = value_modified  # arguments for exec

x = int(local_bindings['x'])

z = 1
for i in range(1, x+1):
    z *= i

print('z= ', z)

return_bindings = {local_bindings['fact']: z}

results = {}
for key2, value2 in return_bindings.items():  # convert back to uri representations
    key_modified = f'http://variable.org/{key2}'
    value_modified = f'http://value.org/{str(value2)}'
    results[key_modified] = value_modified