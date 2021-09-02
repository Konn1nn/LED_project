def return_tuple():
    a = 1
    b = 2
    c = 3
    return (a, b, c)

plumb = return_tuple()
k, l, m = plumb

print(k)
print(l)
print(m)
print(plumb)