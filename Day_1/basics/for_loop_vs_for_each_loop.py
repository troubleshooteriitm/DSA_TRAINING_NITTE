x=[10,20,30,40]

for i in x: # for each loop
    print(i,end=" ")
print()
#  1 2 3 4

for i in range(len(x)): # for loop
    print(i,x[i],end=" ")

# 0 1 2 3

marks={
    "rajawat":87,
    "neelima":50,
    "pranjali":89
}

for i in marks:
    print(marks[i],i)