class Player:
    def __init__(self, name, rating, pairing_no=None, score=0, opponents=(), colour_hist=()):
        self._name         = name
        self._rating       = rating
        self._pairing_no   = pairing_no
        self._score        = score
        self._opponents    = opponents
        self._colour_hist  = colour_hist

    def __repr__(self):
        return ('sn:{0}, r:{1}, pn:{2}, s:{3}, op:{4}, ch:{5}'
            .format(self._name, self._rating, self._pairing_no,
                    self._score,  self._opponents, self._colour_hist))

    def __str__(self) -> str:
        return ('sn:{0}, r:{1}, pn:{2}, s:{3}, op:{4}, ch:{5}'
            .format(self._name, self._rating, self._pairing_no,
                    self._score,  self._opponents, self._colour_hist))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return (self._name == other.name
                and self._rating == other.rating
                and self._pairing_no == other.pairing_no
                and self._score == other.score
                and self._opponents == other.opponents
                and self._colour_hist == other.colour_hist
                if isinstance(other, Player) else NotImplemented)

    @property
    def name(self):
        return self._name

    @property
    def rating(self):
        return self._rating

    @property
    def title(self):
        return self._title

    @property
    def pairing_no(self):
        return self._pairing_no

    @pairing_no.setter
    def pairing_no(self, n):
        self._pairing_no = n

    @property
    def score(self):
        return self._score

    @property
    def colour_hist(self):
        return self._colour_hist

    @property
    def opponents(self):
        return self._opponents

    @property
    def strong_of_preference(self):
        suma = abs(sum(self._colour_hist))
        return suma

    @property
    def expected_colour(self):
        col = 1
        expected = list(self._colour_hist)[-1]

        if expected > 0:
            col = -1
        elif expected < 0:
            col = 1
        else:
            lastcol = 1
            for c in reversed(self._colour_hist):
                if c != 0:
                    lastcol = c
                    break
            if lastcol > 0:
                col = -1
            elif lastcol < 0:
                col = 1

        return col


    @property
    def paused(self):
        if(0 in self._opponents):
            return True
        else:
            return False

    def can_play(self, opponent):
        can = True
        if(opponent.pairing_no in self._opponents):
            can = False
        return can

    def pair(self, opponent, mycolour):
        self._opponents += (opponent,)
        self._colour_hist += (mycolour,)

    def bye(self):
        self._opponents += (0,)
        self._colour_hist += (0,)
        self._score += 1