import math
import copy

#istnieje juz w swiss
def isOdd(num):
    if (num % 2) == 0:
        return False
    else:
        return True


#istnieje juz w swiss
def getPlayerByPN(group, pn):
    for k in group:
        if(k['pairing_no'] == pn):
            return k

def pairGroup(no):
    group = lista[no]

    if (no >= center):
        dir = +1
    else:
        dir = -1

    if((len(group)<2)):
        for i in group:
            lista[no+dir].append(group[i])

        if(no!=center):
            pairGroup(no+dir)

    prefW = {}
    prefB = {}
    prefN = {}
    drop = set()

    for k in group:
        suma = sum(k['color_hist'])
        if(suma>0):
            prefB[k['pairing_no']] = suma
        if(suma<0):
            prefW[k['pairing_no']] = suma
        if(suma==0):
            prefN[k['pairing_no']] = suma

    #sorted(prefW, key=lambda i: i['pairing_no'], reverse=True)
    #sorted(prefB, key=lambda i: i['pairing_no'], reverse=True)
    #sorted(prefN, key=lambda i: i['pairing_no'], reverse=True)

    print(prefW)
    print(prefB)
    print(prefN)

    print("----------------")



    whiteToDel = set()
    tmpPairs = list()

    for k in prefW:
        if(len(prefB)>0):
            pair = (k, next(iter(prefB.keys())))
            tmpPairs.append(pair)
            del prefB[next(iter(prefB.keys()))]
            whiteToDel.add(k)
        else:
            if(len(prefN)>0):
                pair = (k, next(iter(prefN.keys())))
                tmpPairs.append(pair)
                del prefN[next(iter(prefN.keys()))]
                whiteToDel.add(k)
            else:
                break

    for k in whiteToDel:
        del prefW[k]

    print(prefW)
    print(prefB)
    print(prefN)


    if(len(prefW)>0):
        print("Czarne i None wykorzystane. Zostaly same biale. Parujemy tylko biale")

        if (len(prefW) % 2 != 0):
            drop.add(list(prefW)[-1],)
            del prefW[list(prefW)[-1]]

        for v, w in zip(list(prefW)[::2], list(prefW)[1::2]):
            pair = (v, w)
            tmpPairs.append(pair)
            del prefW[v]
            del prefW[w]


    else:
        print("Wszystkie biale wykorzystane. Sprawdzam czy sa czarne")

        blackToDel = set()
        for k in prefB:
            if (len(prefN) > 0):
                pair = (k, next(iter(prefN.keys())))
                tmpPairs.append(pair)
                del prefN[next(iter(prefN.keys()))]
                blackToDel.add(k)
            else:
                break

        for k in blackToDel:
            del prefB[k]

        print(prefW)
        print(prefB)
        print(prefN)

        if (len(prefB) > 0):
            print("Nie ma juz bialych. Wszystkie None wykorzystane. Zostaly jeszcze czarne. Parujemy tylko czarne")

            if (len(prefB) % 2 != 0):
                drop.add(list(prefB)[-1],)
                del prefB[list(prefB)[-1]]

            for v, w in zip(list(prefB)[::2], list(prefB)[1::2]):
                pair = (v, w)
                tmpPairs.append(pair)
                del prefB[v]
                del prefB[w]

        else:
            if(len(prefN)>0):
                print("Nie ma juz bialy i czarnych. Zostaly same Noney. Paruje Nony")

                if (len(prefN) % 2 != 0):
                    drop.add(list(prefN)[-1],)
                    del prefN[list(prefN)[-1]]

                for v, w in zip(list(prefN)[::2], list(prefN)[1::2]):
                    pair = (v, w)
                    tmpPairs.append(pair)
                    del prefN[v]
                    del prefN[w]


    print("Pierwotne pary")
    print(tmpPairs)
    print(prefW)
    print(prefB)
    print(prefN)
    print(drop)

    print("------------")
    print("Weryfikacja parowań")

    pairs = set()
    for index, item in enumerate(tmpPairs):
        print("Sprawdzam pare:", item)

        op = getPlayerByPN(group, item[1])

        if(item[0] in op['opponents']):
            print("Grali już ze sobą")

            found = False

            for i in range (index+1, len(tmpPairs)-1):
                newOp = getPlayerByPN(group, tmpPairs[i][1])

                if(item[0] not in newOp['opponents']):
                    print("Znaleziono przeciwnika. Zamieniamy")
                    mypair = (item[0], tmpPairs[i][1])
                    oppair = (tmpPairs[i][0], item[1])
                    tmpPairs[index] = mypair
                    tmpPairs[i] = oppair


            #zamieniamy przeciwnikow
            #jak nie ma zadnego to sprawdzamy czy koniecnznie musi miec ten kolor
            #jak nie musi to zamieniamy kolor i lecimy od nowa




    print("----------")
    print("Ostateczne pary")
    print(tmpPairs)




lista = [
    [
     {'name': 'Giorgia', 'rating': 2555, 'pairing_no': 1, 'score': 1, 'color_hist': (-1,), 'opponents': (7,)},
     {'name': 'Bruno', 'rating': 2500, 'pairing_no': 2, 'score': 1, 'color_hist': (1,), 'opponents': (8,)},
     {'name': 'Alice', 'rating': 2400, 'pairing_no': 3, 'score': 1, 'color_hist': (-1,), 'opponents': (9,)},
     {'name': 'Eloise', 'rating': 2350, 'pairing_no': 4, 'score': 1, 'color_hist': (1,), 'opponents': (10,)},
     {'name': 'Qba', 'rating': 1800, 'pairing_no': 5, 'score': 1, 'color_hist': (0,), 'opponents': (0,)}
    ],

    [
    {'name': 'Carla', 'rating': 2600, 'pairing_no': 1, 'score': 0, 'color_hist': (1,), 'opponents': (6,)},
        {'name': 'Pablo', 'rating': 2000, 'pairing_no': 6, 'score': 0, 'color_hist': (-1,), 'opponents': (1,)},
        {'name': 'Blazej', 'rating': 1950, 'pairing_no': 7, 'score': 0, 'color_hist': (1,), 'opponents': (2,)},
        {'name': 'Ktos', 'rating': 1900, 'pairing_no': 8, 'score': 0, 'color_hist': (-1,), 'opponents': (3,)},
        {'name': 'Ziom', 'rating': 1855, 'pairing_no': 9, 'score': 0, 'color_hist': (1,), 'opponents': (4,)}]
]



runda = 2

for i in range(len(lista)):
    for j in range(len(lista[i])):
        if(len(lista[i][j]['opponents'])==runda):
            del lista[i][j]
            break


groupsNo = len(lista)
center = math.ceil((groupsNo/2))

pairGroup(0)






#1. dzielimy na pol i zaokraglamy do gory OK
#2. sprawdzamy 1 grupe OK
#3. jezeli liczba w grupie <2 zrzucamy wszystkich w dol jezeli > polowa, w gore<polowa OK
#4. parujemy, jezeli nieparzysta, zrzucamy ostatniego, ktory w dol jezeli > polowa, w gore<polowa
#5. jezeli ktos nie moze miec pary rzucamy  w dol jezeli > polowa, w gore<polowa

