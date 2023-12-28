"""function for solving simultaneous linear equation
function_solve_simultaneous_linear_equation.py
T. Masuda, 2023/12/25
"""

local_bindings = {}

for key1, value1 in bindings.items():
    key_modified = key1.replace(f'http://some.org/_', '').replace(f'http://variable.org/_', '')  # -> x
    value_modified = value1.replace('http://value.org/', '').replace('http://variable.org/', '')
    local_bindings[key_modified] = value_modified  # arguments for exec

a11 = int(local_bindings['a11'])
a12 = int(local_bindings['a12'])
a21 = int(local_bindings['a21'])
a22 = int(local_bindings['a22'])
b1 = int(local_bindings['b1'])
b2 = int(local_bindings['b2'])

div = a11*a22-a12*a21
v1 = (a22*b1-a12*b2)/div
v2 = (-a21*b1+a11*b2)/div

v1 = int(v1)
v2 = int(v2)
return_bindings = {local_bindings['x1']: v1, local_bindings['x2']: v2}

results = {}
for key2, value2 in return_bindings.items():  # convert back to uri representations
    key_modified = f'http://variable.org/{key2}'
    value_modified = f'http://value.org/{str(value2)}'
    results[key_modified] = value_modified
