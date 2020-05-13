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
    def expected_colour(self):
        res = sum(self._colour_hist)
        return res

    @property
    def strong_of_preference(self):
        sum = abs(sum(self._colour_hist))
        return sum

    @property
    def expected_colour(self):
        colours = list(self._colour_hist)
        exp = colours[-1]
        if exp > 0:
            return -1
        if exp<0 :
            return 1
        if exp==0:
            return 0

    def can_play(self, ops):
        can = False
        for op in ops:
            if(self._pairing_no not in op.opponents):
                can = True
        return can

    def pair(self, opponent, mycolour):
        self._opponents += (opponent,)
        self._colour_hist += (mycolour,)

    def bye(self):
        self._opponents += (0,)
        self._colour_hist += (0,)
        self._score += 1