from player import Player
import math
import collections
import copy


class SwissEngine:
    def __init__(self, round, players):
        self._round = round
        self._players = list(players)
        self._center = None
        self._sortedGroups = None
        self._byePlayer = None
        self._checkPlayersAgain = False

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

        groupsNo = len(groups)
        self._center = math.ceil(groupsNo / 2) if not groupsNo % 2 else math.ceil((groupsNo / 2)) - 1

        g1 = groups[:self._center]
        g2 = groups[self._center:]
        finalGroups = list()

        while g1:
            p1 = g1.pop(0)
            finalGroups.append(p1)
        while g2:
            p2 = g2.pop()
            finalGroups.append(p2)

        return finalGroups

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

    def _preparePlayers(self, groupNo):
        group = self._sortedGroups[groupNo]
        dir = self._floatDirection(groupNo)

        group.sort(key=lambda Player: Player.score,
                           reverse=True)

        if(groupNo != self._center):
            if (len(group) % 2):
                drop = group.pop(-1)
                self._sortedGroups[groupNo+dir].append(drop)

            for p in group:
                opponents = copy.deepcopy(group)
                opponents.remove(p)
                if(not p.can_play(opponents)):
                    drop = group.pop(-1)
                    self._sortedGroups[groupNo + dir].append(drop)

            if(len(group)<2):
                self._sortedGroups[groupNo + dir] + group
                return
        else:
            if(len(group)<2):
                dir = self._flipDir(dir)
                self._sortedGroups[groupNo + dir] + group
                self._checkPlayersAgain = True
                return
            canPlay = True
            for p in group:
                if(not p.can_play(group)):
                    canPlay = False
            if(not canPlay):
                dir = self._flipDir(dir)
                self._sortedGroups[groupNo + dir] + group
                self._checkPlayersAgain = True

    def _pairingGroups(self):

        while True:
            for index, item in enumerate(self._sortedGroups):
                self._preparePlayers(index)
            if(self._checkPlayersAgain==False):
                break

        print(self._sortedGroups)

    def _checkBye(self):
        if(len(self._players) % 2):
            self._byePlayer = self._players.pop(-1)
            self._byePlayer.bye()



    def _pairRound(self):
        self._players.sort(key=lambda Player: Player.score,
                           reverse=True)
        self._checkBye()
        self._sortedGroups = self._createGroups()

        firstpairing = self._pairingGroups()




        #w forze bedziemy sprawdzac zawodnikow w kazdej grupie i przenosic