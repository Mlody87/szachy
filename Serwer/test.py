from enum import IntEnum

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
                player['color_hist']=(0,)
                player['opponents']=(0,)
                break

    def getPlayerByPN(self, pn):
        for k in self.players:
            if(k['pairing_no'] == pn):
                return k

    def pair1round(self):
        if(self.isBye>0):
            self.setBye()

        half = len(self.players)//2
        for i in range(1, half+1):
            op1 = self.getPlayerByPN(i)
            op2 = self.getPlayerByPN(half+i)

            if(not self.isOdd(i)):
                op1['opponents']=(op2['pairing_no'],)
                op1['color_hist']=(-1,)

                op2['opponents']=(op1['pairing_no'],)
                op2['color_hist']=(1,)
            else:
                op1['opponents']=(op2['pairing_no'],)
                op1['color_hist']=(1,)

                op2['opponents']=(op1['pairing_no'],)
                op2['color_hist']=(-1,)


    def pairRound(self):
        self.sort('score')
        if (self.isBye > 0):
            self.setBye()

        

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
            {'name':'Giorgia', 'rating':2555}
)

swissPairing(1, runda1)

runda2 = (
     {'name': 'Carla', 'rating': 2600, 'pairing_no': 1, 'score': 1, 'color_hist': (1,), 'opponents': (3,)},
     {'name': 'Giorgia', 'rating': 2555, 'pairing_no': 2, 'score': 1, 'color_hist': (-1,), 'opponents': (4,)},
     {'name': 'Bruno', 'rating': 2500, 'pairing_no': 3, 'score': 0, 'color_hist': (-1,), 'opponents': (1,)},
     {'name': 'Alice', 'rating': 2400, 'pairing_no': 4, 'score': 0, 'color_hist': (1,), 'opponents': (2,)},
     {'name': 'Eloise', 'rating': 2350, 'pairing_no': 5, 'score': 1, 'color_hist': (0,), 'opponents': (0,)}
)

swissPairing(2, runda2)