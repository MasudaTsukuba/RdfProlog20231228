# factorial
# called from exec()
# T. Masuda, 2023/12/22

x = int(x)

z = 1
for i in range(1, x+1):
    z *= i

print('z= ', z)

result = {fact: z}
