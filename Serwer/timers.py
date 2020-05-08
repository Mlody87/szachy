import threading
import time


class SecondCounter(threading.Thread):
    def __init__(self, gametime, callback=None):
        threading.Thread.__init__(self)
        self.callback = callback
        self.move = False

        self.dozwolonyczas = gametime
        self.ilelaczniemysli = 0
        self.ilemysli = 0
        self.zaczynamyslec = 0

        self.didit = False

    def run(self):
        while True:
            time.sleep(0.01)

            if(self.move):
                self.ilemysli = time.time() - self.zaczynamyslec

                if((self.ilelaczniemysli+self.ilemysli) > self.dozwolonyczas):
                    print("Koniec")
                    self.dostringa = "{:.2f}".format(self.ilemysli)
                    print(self.dostringa)
                    self.dostringa = "{:.2f}".format(self.ilelaczniemysli+self.ilemysli)
                    print(self.dostringa)
                    self.finish()
                    break

    def timeleft(self, t):
        self.wynik = self.dozwolonyczas - t
        return self.wynik


    def startthinking(self):
        self.zaczynamyslec = time.time()
        self.move = True

    def stopthinking(self):
        self.move = False
        self.ilemyslal = time.time() - self.zaczynamyslec
        self.ilelaczniemysli += self.ilemyslal
        self.ilezostalo = self.timeleft(self.ilelaczniemysli)
        self.dostringa = "{:.2f}".format(self.ilezostalo)
        return self.dostringa

    def peek(self):
        if(self.move):
            self.ilemyslal = time.time() - self.zaczynamyslec
            self.tmp = self.ilemyslal + self.ilelaczniemysli
            self.ilezostalo = self.timeleft(self.tmp)
        else:
            self.ilezostalo = self.timeleft(self.ilelaczniemysli)

        self.dostringa = "{:.2f}".format(self.ilezostalo)
        return self.dostringa

    def addLag(self, lag):
        self.ilelaczniemysli -= lag

    def finish(self):
        self.move = False
        self.callback()