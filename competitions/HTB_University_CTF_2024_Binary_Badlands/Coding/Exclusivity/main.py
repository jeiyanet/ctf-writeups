# take in the number
n = input()

n_list = n.split()

# calculate answer
new_list = []
for i in n_list:
    if i not in new_list:
        new_list.append(i)

# print answer
print(new_list)