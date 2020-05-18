from player import Player
import math
import copy

class ScoreBracket:
    def __init__(self, players):
        self.players = players
        self.pairs = []

    def firstPairing(self):
        center = math.ceil(len(self.players) / 2)
        s1 = self.players[:center]
        s2 = self.players[center:]

        for a, b in zip(s1, s2):
            pair = [a, b]
            self.pairs.append(pair)

        for x in (self.pairs):
            print(x)

    def playerIndex(self, p):
        for index, item in enumerate(self.pairs):
            if(item[0]==p or item[1]==p):
                return index

    def searchS2(self, index, p1):
        found = False
        players = self.getPlayersFrom(index, 1)
        for p2 in players:
            if p1.can_play([p2]):
                p2index = self.playerIndex(p2)
                tmp = self.pairs[index][1]
                self.pairs[index][1] = self.pairs[p2index][1]
                self.pairs[p2index][1] = tmp
                found = True

    def getPlayersFrom(self, index, s):
        other_players = []
        if(s==1):
            players_copy = copy.deepcopy(self.pairs)
            s1 = players_copy[:index]
            s2 = players_copy[index:]
            s1.reverse()
            for x in s2:
                other_players.append(x[1])
            for x in s1:
                other_players.append((x[1]))
            return other_players
        else:
            players_copy = copy.deepcopy(self.pairs)
            players_copy.reverse()
            for x in players_copy:
                other_players.append(x[0])
                return other_players

    def searchS1(self, index, p1):
        found = False
        players = self.getPlayersFrom(index, 0)
        player.remove(p1)
        for p2 in players:
            if p1.can_play([p2]):
                p2index = self.playerIndex(p2)
                tmp = self.pairs[index][1]
                self.pairs[index][1] = self.pairs[p2index][0]
                self.pairs[p2index][0] = tmp
                found = True

    def pairBracket(self):
        self.players.sort(key=lambda Player: Player.rating, reverse=True)
        self.firstPairing()
        bracketPaired = True
        for index, item in enumerate(self.pairs):
            if(item[0].can_play([item[1]])==False):
                result1 = self.searchS2(index,  item[0])
                if(result1==False):
                    result2 = self.searchS1(index, item[0])
                    if(result2==False):
                        bracketPaired = False
                        break

        if(bracketPaired):
            print("Znaleziono wszsystkie pary:")
            for x in (self.pairs):
                print(x)
        else:
            print("Nie znaleziono par w tym brackecie")