from swissdutch.dutch import DutchPairingEngine
from swissdutch.constants import FideTitle, Colour, FloatStatus
from swissdutch.player import Player
import copy


engine  = DutchPairingEngine()
input_players = (
            Player(name='Bruno',
                   rating=2500),
            Player(name='Alice',
                   rating=2500),
            Player(name='Carla',
                   rating=2400),
            Player(name='Eloise',
                   rating=2350),
            Player(name='Giorgia',
                   rating=2250)
)
round1 = engine.pair_round(1, input_players)
print(round1)
round2 = engine.pair_round(2, round1)
print(round2)

try:
       round3 = engine.pair_round(3, round2)
except:
       print("Nie da sie kolejnej rundy")

print(round3)

round3 = engine.pair_round(4, round3)
print(round3)