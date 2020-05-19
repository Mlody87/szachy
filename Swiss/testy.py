from swiss import SwissEngine
from player import Player

input_players = (
        Player(name='Zawodnik1',
               rating=2500,
               opponents=(3,2),
               colour_hist=(-1,1),
               score=1.5,
               pairing_no=1),
        Player(name='Zawodnik2',
               rating=2500,
               opponents=(4,1),
               colour_hist = (1,-1),
               score =0.5,
               pairing_no = 2
               ),
        Player(name='Zawodnik3',
               rating=2500,
                opponents=(1,5),
               colour_hist = (1,-1),
               score =0.5,
               pairing_no = 3
               ),
        Player(name='Zawodnik4',
               rating=2500,
               opponents=(2,0),
               colour_hist = (-1,0),
               score =2,
               pairing_no = 4
               ),
        Player(name='Zawodnik5',
               rating=2500,
               opponents=(22, 6,),
               colour_hist=(0, 1),
               score=0,
               pairing_no=5
               ),
       Player(name='Zawodnik6',
               rating=2000,
               opponents=(21, 5,),
               colour_hist=(0, 1),
               score=0,
               pairing_no=6
               )

)
result_players = SwissEngine(3, input_players)

