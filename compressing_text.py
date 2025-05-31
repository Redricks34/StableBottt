f = open("24.txt")
x = f.read()
count = count_old = m = 0
for i in x:
	if i == "A":
		m = max(m, count + count_old + 1)
		count_old = count
		count = 0
	else:
                count += 1
m = max(m, count + count_old + 1)
print(m)