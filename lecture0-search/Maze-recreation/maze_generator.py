import random

width = int(input('enter the width of the desired maze:\n>>'))
height = int(input('enter the height of the desired maze:\n>>'))

debut = (random.randint(0,width),random.randint(0,height))
fin = (random.randint(0,width),random.randint(0,height))

while debut == fin:
    debut = (random.randint(0, width), random.randint(0, height))


init = ['#' * width] * height

for i,row in enumerate(init):
    for j,col in enumerate(row):
        if (i,j) == debut:
            init[i] = init[i][:j] + 'A' +init[i][j + 1:]
        elif (i,j) == fin:
            init[i] = init[i][:j] + 'B' +init[i][j + 1:]





for a in init:
    print(a)
























