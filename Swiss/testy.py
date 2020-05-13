from swiss import SwissEngine
from player import Player
import math

input_players = (
        Player(name='Alice',
               score=1,
               pairing_no=1,
               opponents=(2,),
               colour_hist=(1,),
               rating=2300),
        Player(name='Pablo',
                score=0,
pairing_no=2,
               opponents=(1,),
               colour_hist=(-1,),
               rating=2200),
        Player(name='Qba',
               rating=2100,
pairing_no=3,
                score=1,
               opponents=(4,),
               colour_hist=(1,)),
        Player(name='Tester',
               rating=2000,
pairing_no=4,
                score=0,
               opponents=(3,),
               colour_hist=(-1,)),
                Player(name='ktos',
               rating=1900,
pairing_no=5,
                score=1,
                opponents=(0,),
                colour_hist=(0,),
                       ),
Player(name='Draw1',
               rating=2155,
pairing_no=6,
                score=0.5,
                opponents=(7,),
                colour_hist=(1,),
                       ),
Player(name='Draw2',
               rating=2166,
pairing_no=7,
                score=0.5,
                opponents=(6,),
                colour_hist=(-1,),
                       )
)

engine = SwissEngine(2, input_players)



