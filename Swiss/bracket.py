from player import Player
import math
import copy

class ScoreBracket:
    def __init__(self, players):
        self.players = players
        self.pairs = []
        self.s1 = []
        self.s2 = []

    def createPairs(self):
        center = math.ceil(len(self.players) / 2)
        self.s1 = self.players[:center]
        self.s2 = self.players[center:]
        for a,b in zip(self.s1,self.s2):
            pair = [a,b]
            self.pairs.append(pair)

    def checkAndExchange(self, index1, index2, p1, p2):
        if ((p1[0].can_play([p2[1]])) and (p1[1].can_play([p2[0]]))):
            t1 = p1[1]
            t2 = p2[1]
            self.pairs[index1][1] = t2
            self.pairs[index2][1] = t1
            return True
        else:
            if ((p1[0].can_play([p2[0]])) and (p1[1].can_play([p2[1]]))):
                t1 = p1[1]
                t2 = p2[0]
                self.pairs[index1][1] = t2
                self.pairs[index2][1] = t1
                return True
        return False

    def searchDown(self, index, p1):
        found = False
        for i in range(index+1, len(self.pairs)-1):
            result = self.checkAndExchange(index, i, p1, self.pairs[i])
            if(result):
                return True
        return found

    def searchUp(self, index, p1):
        found = False
        for i in range(index-1, 0, -1):
            result = self.checkAndExchange(index, i, p1, self.pairs[i])
            if (result):
                return True
        return found

    def searchOpponent(self, index, pair):
        result = self.searchDown(index, pair)
        if(result==False):
            result = self.searchUp(index, pair)
        return result

    def checkPairs(self):
        #for index, pair in enumerate(self.pairs):
         index=0
         while index<= len(self.pairs)-1:
                pair = self.pairs[index]
                if(pair[0].can_play([pair[1]])==False):
                    print("Nie moga grac: ", pair)
                    result = self.searchOpponent(index, pair)
                    print("Ale znalazlem pare")
                index+=1

    def pairBracket(self):
        self.players.sort(key=lambda Player: Player.rating, reverse=True)
        self.createPairs()
        print("Zawodnicy")
        for x in self.players:
            print(x)
        print("Pary")
        for x in self.pairs:
            print(x)
        self.checkPairs()
        print("Wynik:")
        for x in self.pairs:
            print(x)

