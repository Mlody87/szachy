from player import Player
import math
import collections
import copy
from toolz.itertoolz import interleave
#zainstalowac na serwerze toolz


class SwissEngine:
    def __init__(self, round, players):
        self._round = round
        self._players = list(players)
        self._byePlayer = None
        self._reverseGroups = False
        self._reverseList = []
        self._groupsNo = None
        self._groups = None
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

    def _movePlayer(self, group, source, groupNo, drop):
        if ((len(source) - 1) == groupNo):
            self._g0[0].append(drop)
        else:
            source[groupNo + 1].append(drop)

    def _prepareGroup(self, dir, groupNo):
        if (dir > 0):
            source = self._g1
        if (dir < 0):
            source = self._g2

        group = source[groupNo]

        if(len(group) == 0):
            return

        group.sort(key=lambda Player: Player.score, reverse=True)

        if (len(group) % 2):
            drop = group.pop(-1)
            self._movePlayer(group, source, groupNo, drop)
            if (len(list(group)) == 0):
                return

        for index, item in enumerate(group):
            opponents = copy.deepcopy(group)
            opponents.remove(item)
            if (item.can_play(opponents) == False):
                drop = group.pop(index)
                self._movePlayer(group, source, groupNo, drop)

        if (len(group) == 1):
            self._movePlayer(group, source, groupNo, drop)
            del group

    def _prepareCenter(self):
        source = self._g0
        group = source[0]

        if (len(group) == 1):
            self._reverseGroups = True
            return

        canPlay = True
        for index, item in enumerate(group):
            opponents = copy.deepcopy(group)
            opponents.remove(item)
            if (item.can_play(opponents) == False):
                canPlay = False
                break
        if (canPlay == False):
            self._reverseGroups = True

    def _prepareReversedList(self):
        self._reverseList = []
        self._reverseList.append(self._g0[0])

        self._g1.reverse()

        while self._g2:
            p2 = self._g2.pop(0)
            self._reverseList.append(p2)
        while self._g1:
            p1 = self._g1.pop(0)
            self._reverseList.append(p1)

        dl = []
        for index, item in enumerate(self._reverseList):
            if len(self._reverseList[index]) == 0:
                dl.append(index)

        dl.reverse()
        for x in dl:
            del self._reverseList[x]

    def _checkGroupsAgain(self):
        for index, item in enumerate(self._reverseList):
            group = item

            for i, it in enumerate(group):
                opponents = copy.deepcopy(group)
                opponents.remove(it)
                if (it.can_play(opponents) == False):
                    if(index==(len(self._reverseList)-1)):
                        print("Ostatnia grupa i nie da sie sparowac graczy. Kojarzenie niemozliwe")
                        return
                    else:
                        self._reverseList[index+1] += group
                        self._reverseList[index].clear()
        dl = []
        for index, item in enumerate(self._reverseList):
            if len(self._reverseList[index]) == 0:
                dl.append(index)

        dl.reverse()
        for x in dl:
            del self._reverseList[x]

    def _finalCreateGroups(self):
        if(self._reverseGroups):
            return self._reverseList
        else:
            result = []
            for index, item in enumerate(self._g1):
                if(len(item)>0):
                    result.append(item)
            for index, item in enumerate(self._g0):
                if(len(item)>0):
                    result.append(item)
            for index, item in enumerate(self._g2):
                if(len(item)>0):
                    result.append(item)
            return result

    def _prepareGroups(self):

        for index, item in enumerate(self._g1):
            self._prepareGroup(1,index)

        for index, item in enumerate(self._g2):
            self._prepareGroup(-1,index)

        self._prepareCenter()

        print("g1:",self._g1)
        print("g0:",self._g0)
        print("g2:",self._g2)
        print(self._reverseGroups)

        if(self._reverseGroups):
            self._prepareReversedList()
            self._checkGroupsAgain()

        self._groups = self._finalCreateGroups()

        print("Final groups:")
        for index, item in enumerate(self._groups):
            print(index, " :",item)


    def _checkBye(self):
        if(len(self._players) % 2):
            self._byePlayer = self._players.pop(-1)
            self._byePlayer.bye()


    def _pairRound(self):
        self._players.sort(key=lambda Player: Player.score,
                           reverse=True)
        self._checkBye()
        self._createGroups()

        firstpairing = self._prepareGroups()