with open("matrs.txt", "r") as f:

    matrix1 = f.readline().strip()
    matrix2 = f.readline().strip()

f.close()


spisok = []
spisok_1 = []
spisok_2 = []
spisok_3 = []
spisok_4 = []
spp = []


for i in matrix1:
    if i.isdigit() == True:
        if len(spisok_1) < 2:
            spisok_1.append(int(i))
        else:
            spisok_2.append(int(i))

spisok.append(spisok_1)
spisok.append(spisok_2)

for i in matrix2:
    if i.isdigit() == True:
        if len(spisok_3) < 2:
            spisok_3.append(int(i))
        else:
            spisok_4.append(int(i))

spp.append(spisok_3)
spp.append(spisok_4)

mat1 = spisok
mat2 = spp


