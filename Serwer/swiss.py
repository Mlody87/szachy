from enum import IntEnum
import collections

class Colour(IntEnum):
    black = -1
    none  =  0,
    white =  1


class swissPairing:
    def __init__(self, round, players, last_round=False):
        self.round = round
        self.players = players
        self.last_round = last_round
        self.pairing()



    def checkIsBye(self):
        if (self.isOdd(len(self.players))):
            self.isBye = 1
        else:
            self.isBye = 0

    def sort(self, by):
        self.players = sorted(self.players, key=lambda i: i[by], reverse=True)

    def setPairingNo(self):
        self.sort('rating')
        i=1
        for k in self.players:
            k['pairing_no'] = i
            k['score'] = 0
            k['color_hist'] = ()
            k['opponents'] = ()
            i+=1

    def isOdd(self, num):
        if (num % 2) == 0:
            return False
        else:
            return True

    def setBye(self):
        for player in reversed(self.players):
            if(0 not in player['opponents']):
                player['score'] += 1
                player['color_hist'] += (0,)
                player['opponents'] += (0,)
                break

    def getPlayerByPN(self, group, pn):
        for k in group:
            if (k['pairing_no'] == pn):
                return k

    def pair1round(self):
        if(self.isBye>0):
            self.setBye()

        half = len(self.players)//2
        for i in range(1, half+1):
            op1 = self.getPlayerByPN(self.players, i)
            op2 = self.getPlayerByPN(self.players, half+i)

            if(not self.isOdd(i)):
                op1['opponents']=(op2['pairing_no'],)
                op1['color_hist'] += (-1,)

                op2['opponents']=(op1['pairing_no'],)
                op2['color_hist'] += (1,)
            else:
                op1['opponents']=(op2['pairing_no'],)
                op1['color_hist'] += (1,)

                op2['opponents']=(op1['pairing_no'],)
                op2['color_hist'] += (-1,)


    def createGroups(self):
        result = collections.defaultdict(list)

        for d in self.players:
            result[d['score']].append(d)

        result_list = list(result.values())
        return result_list

    def removeByePlayer(self, groups):
        for i in range(len(groups)):
            for j in range(len(groups[i])):
                if (len(groups[i][j]['opponents']) == self.round):
                    del groups[i][j]
                    break
        return groups

    def canPlay(self, group, pn):
        result = False
        for x in group:
            if((pn not in group[x]['opponents']) and (pn != group[x]['pairing_no'])):
                result = True
        return result

    def dropPlayersWithoutOpponents(self, group, destGroup):
        drop = list()
        for index, item in enumerate(group):
            if (not self.CanPlay(group, group[x]['pairing_no'])):
                drop.append(index)
                destGroup.append(item)
        for i in drop:
            group.remove(i)



    def getDir(self, no, center):
        if (no > center):
            dir = -1
        if (no < center):
            dir = +1


    def pairRound(self):
        self.sort('score')
        if (self.isBye > 0):
            self.setBye()

        groups = self.createGroups()
        groups = self.removeByePlayer(groups)
        print(groups)

        groupsNo = len(lista)
        center = math.ceil((groupsNo / 2))
        #dodac podzial grup na czesci itp. testy.py

        #TU TRZEBA ZROBIC JAKAS PETLE DLA WSZYSTKICH GRUP

        #Sprawdzamy pierwsza grupe
        dir = self.getDir(0, center)
        drop = self.dropPlayersWithoutOpponents(groups[0], groups[dir])




        self.pairGroup(groups[0])

        #1. dodac do dropu zawodnikow ktorzy nie moga znalezc przeciwnika
        #2. dodac do dropu zawodnika jezeli nie jest parzysta liczba graczy
        # sprawdzamy ogolny oczekiwany wynik kolorow i przenosimy tego, ktory najmniej sie przyczynie do wyrwonania
        #Jeżeli liczba zawodników oczekujących na kolor biały jest równa liczbie zawodników oczekujących na kolor czarny,
        # to pływakami są:  najniżej  zaszeregowany  gracz  przy  ko-jarzeniu  w  dół  oraz  najwyżej  zaszeregowany  gracz  przy  kojarzeniu w górę
        #3. dzielimy graczy na 2 grupy uszeregowanych wedlugn umerow startowych
        #. 1 z [n/2+1], 2 z [n/2+2], 3 z [n/2+3] ... ... [n/2] z n
        #4.  Jednakże ża-den zawodnik nie może: (a)    otrzymać  tego  samego  koloru  w  trzech  kolejnych  ru-dach
        #Jeżeli  zawodnik  w  dwóch  poprzednich  rundach  otrzymałten sam kolor bierek, musi otrzymać w najbliższej rundzie kolor  odmienny.
        # Jeśli  obydwaj  zawodnicy  grali  tym  sa-mym kolorem w poprzednich dwóch rundach i nie można znaleźć  dla  nich  odpowiednich  przeciwników  w
        # grupie,  wówczas  jeden  lub  nawet  obaj  muszą  być  przeniesieni  do grupy sąsiedniej.
        #Przy  kojarzeniu  ostatniej  rundy,  zasada  3,  wymagająca,  aby  kojarzyć  ze  sobą  zawodników  z  tą  samą  liczbą  punktów  (o  ile  nie  spotkali  się  we
        # wcześniejszej  rundzie),
        # ma  moc  nadrzędnąw  stosunku  do  zróżnicowania  lub  wyrównania  kolorów  bierek,  nawet jeśli będzie konieczne przydzielenie
        # jednemu z zawodni-ków  tego  samego  koloru  po  raz  trzeci  z  rzędu  lub  w  wyniku  przydzielenia  koloru  będzie  grał  jednym  kolorem  o  trzy  partie  więcej od
        # przeciwnika


    def pairing(self):
        self.checkIsBye()

        if(self.round==1):
            self.setPairingNo()
            self.pair1round()
            print(self.players)
        else:
            self.pairRound()




runda1 = (
            {'name':'Bruno', 'rating':2500},
            {'name':'Alice', 'rating':2400},
            {'name':'Carla', 'rating':2600},
            {'name':'Eloise', 'rating':2350},
            {'name':'Giorgia', 'rating':2555},
            {'name':'Qba', 'rating':1800},
            {'name':'Pablo', 'rating':2000},
            {'name':'Qba', 'rating':1850},
            {'name':'Ziom', 'rating':1855},
            {'name':'Ktos', 'rating':1900},
            {'name':'Blazej', 'rating':1950}

)

swissPairing(1, runda1)

runda2 = ({'name': 'Carla', 'rating': 2600, 'pairing_no': 1, 'score': 0, 'color_hist': (1,), 'opponents': (6,)},
{'name': 'Giorgia', 'rating': 2555, 'pairing_no': 2, 'score': 1, 'color_hist': (-1,), 'opponents': (7,)},
{'name': 'Bruno', 'rating': 2500, 'pairing_no': 3, 'score': 1, 'color_hist': (1,), 'opponents': (8,)},
{'name': 'Alice', 'rating': 2400, 'pairing_no': 4, 'score': 1, 'color_hist': (-1,), 'opponents': (9,)},
{'name': 'Eloise', 'rating': 2350, 'pairing_no': 5, 'score': 1, 'color_hist': (1,), 'opponents': (10,)},
{'name': 'Pablo', 'rating': 2000, 'pairing_no': 6, 'score': 0, 'color_hist': (-1,), 'opponents': (1,)},
{'name': 'Blazej', 'rating': 1950, 'pairing_no': 7, 'score': 0, 'color_hist': (1,), 'opponents': (2,)},
{'name': 'Ktos', 'rating': 1900, 'pairing_no': 8, 'score': 0, 'color_hist': (-1,), 'opponents': (3,)},
{'name': 'Ziom', 'rating': 1855, 'pairing_no': 9, 'score': 0, 'color_hist': (1,), 'opponents': (4,)},
{'name': 'Qba', 'rating': 1850, 'pairing_no': 10, 'score': 0, 'color_hist': (-1,), 'opponents': (5,)},
{'name': 'Qba', 'rating': 1800, 'pairing_no': 11, 'score': 1, 'color_hist': (0,), 'opponents': (0,)})


swissPairing(2, runda2)