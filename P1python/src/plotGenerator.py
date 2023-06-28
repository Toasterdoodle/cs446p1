import matplotlib.pyplot as plt

x = []
y = []

with open("mySAS-heaps.txt", "rt") as file:
    # count = 0
    for line in file:
        # count = count + 1
        # if count % 10 == 0:
        line = line.split()
        x.append(line[0])
        y.append(line[1])

plt.tick_params(left = False, right = False , labelleft = False ,
                labelbottom = False, bottom = False)
# print(x)
plt.plot(x, y)
# plt.axis([])
plt.ylabel('Unique words from 0 to 5627')
plt.xlabel('Words counter from 0 to 86142')
plt.show()