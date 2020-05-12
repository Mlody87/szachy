from player import Player
import math


class SwissEngine:
    def __init__(self, round, players):
        self._round = round
        self._players = list(players)

        if(self._round==1):
            self._firstRound()
        else:
            self._round()

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

        #print(self._players)
        return self._players

   #next rounds

    def createGroups(self):
        result = collections.defaultdict(list)
        for p in self._players:
            result[p.score].append(p)

        groups = list(result.values())
        groupsNo = len(groups)
        center = math.ceil(groupsNo / 2) if not groupsNo % 2 else math.ceil((groupsNo / 2)) - 1

        g1 = groups[:center]
        g2 = groups[center:]
        finalGroups = list()

        while g1:
            p1 = g1.pop(0)
            finalGroups.append(p1)
        while g2:
            p2 = g2.pop()
            finalGroups.append(p2)

        return finalGroups

    def _round(self):
        self._players.sort(key=lambda Player: Player.score,
                           reverse=True)

        groups = self.createGroups()


        #w forze bedziemy sprawdzac zawodnikow w kazdej grupie i przenosic