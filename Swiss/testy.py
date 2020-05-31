from swiss import SwissEngine
from player import Player
import random

input_players = (
Player(name='  Zawodnik1  ',
rating= 2200 ,
pairing_no= 1 ,
score= 2 ,
opponents= (3, 2) ,
colour_hist= (1, -1) ,
),
Player(name='  Zawodnik2  ',
rating= 2200 ,
pairing_no= 2 ,
score= 0.5 ,
opponents= (4, 1) ,
colour_hist= (-1, 1) ,
),
Player(name='  Zawodnik4  ',
rating= 2200 ,
pairing_no= 4 ,
score= 1.0 ,
opponents= (2, 3) ,
colour_hist= (1, -1) ,
),
Player(name='  Zawodnik3  ',
rating= 2200 ,
pairing_no= 3 ,
score= 0.5 ,
opponents= (1, 4) ,
colour_hist= (-1, 1) ,
),



)

result_players = SwissEngine(3, input_players)
wynik2 = round(math.log2(g))+round(math.log2(m))

