l = [0, 0, 1, 1, 0]
doc_method = []
for index, x in enumerate(l):
    print(index, x)
    if x:
        doc_method.append(index)
print(doc_method)