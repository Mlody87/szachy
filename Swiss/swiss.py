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
        self._g1 = list()
        self._g2 = list()
        self._g0 = list()

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
                self._g0.append(groups.pop(0))
                break

            if (top):
                self._g1.append(groups.pop(0))
            else:
                self._g2.append(groups.pop(-1))

            if (top):
                top = False
            else:
                top = True


    def _floatDirection(self, i):
        if i> self._center:
            return -1
        if i< self._center:
            return 1
        return 0

    def _flipDir(self, dir):
        if dir>0:
            return -1
        if dir<0:
            return 1

    def _preparePlayers(self, dir, groupNo):
        center=False
        if(dir>0):
            source = self._g1
        if(dir<0):
            source = self._g2
        if(dir==0):
            source = self._g0
            center=True

        group = source[groupNo]

        if(len(list(group))==0):
            return

        group.sort(key=lambda Player: Player.score,
                           reverse=True)

        if(not center):

            if (len(group) % 2):
                drop = group.pop(-1)
                if((len(source)-1)==groupNo):
                    self._g0.append(drop)
                else:
                    source[groupNo+1].append(drop)

            for p in group:
                opponents = copy.deepcopy(group)
                opponents.remove(p)
                if(not p.can_play(opponents)):
                    drop = group.pop(-1)
                    if ((len(source) - 1) == groupNo):
                        self._g0.append(drop)
                    else:
                        source[groupNo + 1].append(drop)

            if (len(group) == 1):
                if ((len(source) - 1) == groupNo):
                    self._g0 += group
                else:
                    source[groupNo + 1] += group
                return

        else:
            if(len(group)==1):
                if(self._groupsNo % 2 == 0):
                    dropTo = self._g1[-1]
                else:
                    dropTo = self._g2[-1]

                dropTo += group
                self._checkPlayersAgain = True
                return

            canPlay = True
            for p in group:
                if(not p.can_play(group)):
                    canPlay = False
            if(not canPlay):
                if (self._groupsNo % 2 == 0):
                    dropTo = self._g1[-1]
                else:
                    dropTo = self._g2[-1]

                dropTo += group
                self._checkPlayersAgain = True

    def _createGroupsAgaing(self):
        groups = list()
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