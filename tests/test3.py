resultat = [('class', 'card-title m-t-0 m-b-10'), ('style', 'color:white')]

print(resultat)
for cl, classes in filter(lambda x: x[0] == "class", resultat):
    if "card-title" in classes:
        print(cl, classes)

print("debut")
for i in [1, 2, 3, 4]:
    print(i)
    break
else:
    print("else")

print("fin")
