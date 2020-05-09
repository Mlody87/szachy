import asyncio
import time
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
from connection import UserConnection
import threading
import conf
from gameslobbycontroler import GamesLobbyControler
from gamecontroler import GameControler
from tournamentslobbycontroler import TournamentsLobbyControler
from tournamentControler import tournamentControler


def MainServer():

    time.sleep(5)
    turniej = tournamentControler(1)
    turniej.start()
    #while True:
    #    time.sleep(100)


def make_app():
    return tornado.web.Application([
        (r"/connection/(.*)", UserConnection)
    ]
    )

def main():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    conf.gamesLobbyControler = GamesLobbyControler()
    conf.gamesLobbyControler.start()

    conf.tournamentsLobbyControler = TournamentsLobbyControler()
    conf.tournamentsLobbyControler.start()

    conf.games['1'] = GameControler(1,60)
    conf.games['1'].start()

    server = threading.Thread(target=MainServer)
    server.start()

    app = make_app()
    app.listen(8888)
    print("Server started")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()