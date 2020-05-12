from swiss import SwissEngine
from player import Player

class T:
    def __init__(self, name):
        self._name         = name
    def __hash__(self):
        return 1234
    def __eq__(self, other):
        return (self._name == other.name
                if isinstance(other, T) else NotImplemented)
    def __repr__(self):
        return (str(self._name))
    @property
    def name(self):
        return self._name

t1 = T(2)
t2 = T(1)
t3 = T(5)

my_set = [ t1,t2,t3 ]

my_set.sort(key=lambda T: T.name,
                           reverse=True)

print(my_set)

p1=1
p2=2
odd, even = (p1, p2)

print(even)

input_players = (
        Player(name='Alice',
               rating=2500),
        Player(name='Pablo',
               rating=2600),
        Player(name='Qba',
               rating=2700),
        Player(name='Tester',
               rating=2550)
)

engine = SwissEngine(1, input_players)
print(engine)