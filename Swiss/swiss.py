from player import Player
import math
import collections
import copy
import random


class SwissEngine:
    def __init__(self, ro, pl):
        self.round = ro
        self.players = list(pl)
        self.byePlayer = None

        if(self.round==1):
            self.firstRound()
        else:
            self.pairRound()

    def printPlayer(self, p):
        print("Player(name='",p.name,"',")
        print("rating=",p.rating,",")
        print("pairing_no=",p.pairing_no,",")
        print("score=",p.score,",")
        print("opponents=",p.opponents,",")
        print("colour_hist=",p.colour_hist,",")
        print("),")


    def __str__(self) -> str:
        return ','.join(el.__str__() for el in self.players)

    def __iter__(self):
        return iter(self.players)

    def assignPairingNo(self):
        for i in range(len(self.players)):
            p = self.players[i]
            p.pairing_no = i + 1

    def firstRound(self):
        self.players.sort(key=lambda Player: Player.rating,
                          reverse=True)
        self.assignPairingNo()

        k = math.floor(len(self.players) / 2)
        s1 = self.players[:k]
        s2 = self.players[k:]

        while s1:
            p1 = s1.pop(0)
            p2 = s2.pop(0)
            odd, even = (p1, p2) if p1.pairing_no % 2 else (p2, p1)
            odd.pair(even.pairing_no, 1)
            even.pair(odd.pairing_no, -1)

        if s2:
            s2[0].bye()

        return self.players

    def pickBye(self):
            for i in range(len(self.players)-1, -1, -1):
                if(self.players[i].paused==False):
                    self.byePlayer = copy.deepcopy(self.players[i])
                    return i
                    break

    def preparePairs(self):
        self.players.sort(key=lambda Player: Player.score, reverse=True)
        other_players = copy.deepcopy(self.players)
        pairs = []

        rm = -1
        while True:
            p1 = other_players.pop(0)

            if (len(other_players) ==1):
                p2 = other_players.pop(0)
                pair = [p1, p2]
                pairs.append(pair)
                break
            elif(len(other_players) ==0):
                self.byePlayer = p1
                break

            found=False
            for index, p2 in (enumerate(other_players)):
                if (p1.can_play(p2)):
                    pair = [p1, p2]
                    pairs.append(pair)
                    rm = index
                    found=True
                    break
            if(found==False):
                p2 = other_players.pop(-1)
                pair = [p1, p2]
                pairs.append(pair)
            if (rm >= 0):
                del other_players[rm]
                rm = -1

        return pairs

    def findBye(self,p):
        pairs = p

        if (self.byePlayer.paused==False):
            self.byePlayer.bye()
            return pairs
        else:
            wasChecked = []
            index=0
            while True:

                if(self.byePlayer.paused):
                    if(index>len(pairs)):
                        print("NIE ZNALEZIONO OSTATECZNIE BYE")
                        break
                    for i in range(0, len(pairs)):
                        if(pairs[i][0].can_play(self.byePlayer) and (pairs[i][1].pairing_no not in wasChecked)):
                            t1 = copy.deepcopy(pairs[i][1])
                            t2 = copy.deepcopy(self.byePlayer)
                            pairs[i][1] = t2
                            self.byePlayer = t1
                            wasChecked.append(self.byePlayer.pairing_no,)
                            break
                        if (pairs[i][1].can_play(self.byePlayer) and (pairs[i][0].pairing_no not in wasChecked)):
                            t1 = copy.deepcopy(pairs[i][0])
                            t2 = copy.deepcopy(self.byePlayer)
                            pairs[i][0] = t2
                            self.byePlayer = t1
                            wasChecked.append(self.byePlayer.pairing_no,)
                            break
                else:
                    self.byePlayer.bye()
                    return pairs
                    break
                index += 1

    def checkPairs(self, pa):
        pairs = pa

        pairs.reverse()

        for index, pair in enumerate(pairs):
            if(pair[0].can_play(pair[1]) == False):
                found=False
                for i in range(index+1, len(pairs)):
                    p = pairs[i]
                    if(pair[0].can_play(p[1]) and pair[1].can_play(p[0])):
                        #Moga grac w poziomie
                        t1 = copy.deepcopy(pair[1])
                        t2 = copy.deepcopy(p[1])
                        pairs[index][1] = t2
                        pairs[i][1] = t1
                        #pair[1] = t2
                        #p[1] = t1
                        found = True
                        break
                    else:
                        if (pair[0].can_play(p[0]) and pair[1].can_play(p[1])):
                            #Mogą grać w pionie
                            t1 = copy.deepcopy(p[0])
                            t2 = copy.deepcopy(pair[1])
                            pairs[index][1] = t1
                            pairs[i][0] = t2
                            #pair[1] = t1
                            #p[0] = t2
                            found = True
                            break
                if(found==False):
                    if(self.byePlayer != None):
                        if(pair[0].can_play(self.byePlayer)):
                            #Pierwszy moze grac z pauza
                            t1 = copy.deepcopy(pair[1])
                            t2 = copy.deepcopy(self.byePlayer)
                            pairs[index][1] = t2
                            self.byePlayer = t1
                            found = True
                        elif(pair[1].can_play(self.byePlayer)):
                            #Drugi moze grac z pauza
                            t1 = copy.deepcopy(pair[0])
                            t2 = copy.deepcopy(self.byePlayer)
                            pairs[index][0] = t2
                            self.byePlayer = t1
                            found = True

                    if(found==False):
                        print("Wśród par: ",pairs)
                        print("NIE ZNALEZIONO ODPOWIEDNIEGO PRZECIWNIKA DLA PARY:",pair)
                        break



        if(self.byePlayer != None):
            pairs = self.findBye(pairs)

        pairs.reverse()

        return pairs

    def reverseColour(self, c):
        if c > 0:
            return -1
        elif c < 0:
            return 1

    def assignColours(self, p):
        pairs = p
        result = []
        for index, pair in enumerate(pairs):
            p1 = pair[0]
            p2 = pair[1]
            #DO REFAKTORA W PIERWSZEJ KOLEJNOSCI
            if p1.strong_of_preference > p2.strong_of_preference:
                pref = p1.expected_colour
                p1.pair(p2.pairing_no, pref)
                c = self.reverseColour(pref)
                p2.pair(p1.pairing_no, c)
                p = [p1, p2]
                result.append(p)
            elif p1.strong_of_preference < p2.strong_of_preference:
                pref = p2.expected_colour
                p2.pair(p1.pairing_no, pref)
                c = self.reverseColour(pref)
                p1.pair(p2.pairing_no, c)
                p = [p2, p1]
                result.append(p)
            elif p1.score > p2.score:
                pref = p1.expected_colour
                p1.pair(p2.pairing_no, pref)
                c = self.reverseColour(pref)
                p2.pair(p1.pairing_no, c)
                p = [p1, p2]
                result.append(p)
            elif p1.score < p2.score:
                pref = p2.expected_colour
                p2.pair(p1.pairing_no, pref)
                c = self.reverseColour(pref)
                p1.pair(p2.pairing_no, c)
                p = [p2, p1]
                result.append(p)
            elif p1.pairing_no > p2.pairing_no:
                pref = p1.expected_colour
                p1.pair(p2.pairing_no, pref)
                c = self.reverseColour(pref)
                p2.pair(p1.pairing_no, c)
                p = [p1, p2]
                result.append(p)
            else:
                pref = p2.expected_colour
                p2.pair(p1.pairing_no, pref)
                c = self.reverseColour(pref)
                p1.pair(p2.pairing_no, c)
                p = [p2, p1]
                result.append(p)

        return result

    def pairRound(self):
        pairs = self.preparePairs()
        pairs = self.checkPairs(pairs)
        pairs = self.assignColours(pairs)

        players = []
        if(self.byePlayer != None):
            players.append(self.byePlayer)
        for x in pairs:
            players.append(x[0])
            players.append(x[1])

        self.players.clear()
        self.players = players

        self.players.sort(key=lambda Player: Player.score, reverse=True)

        return self.players