from player import Player
import math
import collections
import copy


class SwissEngine:
    def __init__(self, round, players):
        self._round = round
        self._players = list(players)
        self._byePlayer = None
        self._checkPlayersAgain = False
        self._groupsNo = None
        self._g1 = []
        self._g2 = []
        self._g0 = []

        if(self._round==1):
            self._firstRound()
        else:
            self._pairRound()

    def __str__(self) -> str:
        return ','.join(el.__str__() for el in self._players)

    def __iter__(self):
        return iter(self._players)

    def _assignPairingNo(self):
        for i in range(len(self._players)):
            p = self._players[i]
            p.pairing_no = i + 1

    def _firstRound(self):
        self._players.sort(key=lambda Player: Player.rating,
                          reverse=True)
        self._assignPairingNo()

        k = math.floor(len(self._players) / 2)
        s1 = self._players[:k]
        s2 = self._players[k:]

        while s1:
            p1 = s1.pop(0)
            p2 = s2.pop(0)
            odd, even = (p1, p2) if p1.pairing_no % 2 else (p2, p1)
            odd.pair(even.pairing_no, 1)
            even.pair(odd.pairing_no, -1)

        if s2:
            s2[0].bye()

        return self._players

   #next rounds

    def _createGroups(self):
        result = collections.defaultdict(list)
        for p in self._players:
            result[p.score].append(p)

        groups = list(result.values())

        self._groupsNo = len(groups)


        top = True
        for i in range(0, (self._groupsNo)):
            if (len(groups) == 1):
                p = groups.pop(0)
                self._g0.append(p)
                break

            if (top):
                self._g1.append(groups.pop(0))
            else:
                self._g2.append(groups.pop(-1))

            if (top):
                top = False
            else:
                top = True


    def _preparePlayers(self, dir, groupNo):
        center=False
        if(dir>0):
            source = self._g1
        if(dir<0):
            source = self._g2
        if(dir==0):
            source = self._g0
            center=True

        print("Numer grupy: ", groupNo)

        group = source[groupNo]
        print("Grupa: ",group)


        if(len(list(group))==0):
            print("Grupa pusta. Pomijam")
            return

        group.sort(key=lambda Player: Player.score,
                           reverse=True)

        if(not center):
            print("Grupa nie srodkowa")

            if (len(group) % 2):
                print("Liczba nieparzysta")
                drop = group.pop(-1)
                print("Przenosze gracza: ",drop)
                if((len(source)-1)==groupNo):
                    print("Ostatnia grupa przed centrum. Przenosze do centrum")
                    self._g0[0].append(drop)
                    print("Grupa po przeniesieniu: ",group)
                    print("Centrum: ",self._g0)
                else:
                    print("Przenosze grupe wyzej")
                    source[groupNo+1].append(drop)
                    print("Grupa po przeniesieniu: ", group)
                    print("Centrum: ", source[groupNo+1])

            for p in group:
                print("Sprawdzam czy maja przeciwnikow")
                opponents = copy.deepcopy(group)
                opponents.remove(p)
                if(not p.can_play(opponents)):
                    print("Gracz nie ma przeciwnika: ",p)
                    drop = group.pop(-1)
                    if ((len(source) - 1) == groupNo):
                        print("Ostatnia grupa, przenosze do centrum")
                        self._g0[0].append(drop)
                        print("Grupa po przeniesieniu: ", group)
                        print("Centrum: ", self._g0)
                    else:
                        print("Przenosze wyzej")
                        source[groupNo+1].append(drop)
                        print("Grupa po przeniesieniu: ", group)
                        print("Centrum: ", source[groupNo+1])

            if (len(group) == 1):
                print("Grupa ma 1 gracza: ", group)
                if ((len(source) - 1) == groupNo):
                    self._g0[0] += group
                    print("Przenioslem do 0: ",self._g0)
                else:
                    source[groupNo+1] += group
                    print("Przenioslem wyzej: ",source[groupNo+1])
                return

        else:
            print("Grupa srodkowa")
            if(len(group)==1):
                print("Jeden gracz w srodkowej")
                if(self._groupsNo % 2 == 0):
                    dropTo = self._g1[-1]
                    print("Parzyste grupy, przenosze do top: ", dropTop)
                else:
                    dropTo = self._g2[-1]
                    print("Nieparzyste grupy, przenosze do bottom: ",dropTo)

                dropTo += group
                print("Po przeniesieniu: ",dropTo)
                self._checkPlayersAgain = True
                print("Ustawiam checkP i koniec")
                return

            canPlay = True
            print("Sprawdzam czy moga grac ze soba")
            for p in group:
                if(not p.can_play(group)):
                    print("Gracz nie ma przciwnikow: ",p)
                    canPlay = False
            if(not canPlay):
                if (self._groupsNo % 2 == 0):
                    dropTo = self._g1[-1]
                    print("Parzyste grupy, przenosze do top: ", dropTop)
                else:
                    dropTo = self._g2[-1]
                    print("Nieparzyste grupy, przenosze do bottom: ", dropTop)

                dropTo += group
                print("Po przeniesieniu: ", dropTo)
                self._checkPlayersAgain = True
                print("Ustawiam checkP")

    def _createGroupsAgaing(self):
        print("Again")
        groups = []
        groups += self._g1
        groups += self._g2
        groups += self._g0


        self._groupsNo = len(groups)

        groupsC = copy.deepcopy(groups)

        top = True
        for i in range(0, (len(groups))):
            if (len(groupsC) == 1):
                self._g0.append(groupsC.pop(0),)
                break

            if (top):
                self._g1.append(groupsC.pop(0),)
            else:
                self._g2.append(groupsC.pop(-1),)

            if (top):
                top = False
            else:
                top = True

        return True


    def _pairingGroups(self):

        while True:
            self._checkPlayersAgain = False
            #Pair top groups
            for index, item in enumerate(self._g1):
                self._preparePlayers(1,index)

            #Pair bottom groups
            for index, item in enumerate(self._g2):
                self._preparePlayers(-1,index)

            #Pair center group
            for index, item in enumerate(self._g0):
                self._preparePlayers(0,index)

            if(self._checkPlayersAgain):
                self._createGroupsAgaing()
            else:
                break
        print("----------------")
        print('ostatecznie')
        print('g1: ',self._g1)
        print('g2: ',self._g2)
        print('g0: ',self._g0)

    def _checkBye(self):
        if(len(self._players) % 2):
            self._byePlayer = self._players.pop(-1)
            self._byePlayer.bye()



    def _pairRound(self):
        self._players.sort(key=lambda Player: Player.score,
                           reverse=True)
        self._checkBye()
        self._createGroups()

        firstpairing = self._pairingGroups()




        #w forze bedziemy sprawdzac zawodnikow w kazdej grupie i przenosic