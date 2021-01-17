import json
import os.path


class Spiel():
    def __init__(self, players):
        self.players = players
        self.trumps = [9, 10, 11, 12]

    def round(self):
        player = self.player()
        multiplikator = evalinput("Was wurde gespielt?")
        points = self.trump() * (multiplikator + self.extras()) * self.winloss()
        print("{} hat {} punkte gemacht".format(player, points))
        self.updatepoints(player, points)
        printpoints(self.players)
        self.round()

    def trump(self):
        trump = evalinput("Was war Trumpf (Wert des gespielten Trumpfs)?")
        if trump in self.trumps:
            return trump
        else:
            print("ERROR: Dumm oder was?")

    def winloss(self):
        winloss = evalinput("Verloren(0),Gewonnen(1) oder Siegmultiplikator eingeben")
        if winloss == 0:
            return -2
        else:
            return winloss

    def updatepoints(self, player, points):
        with open("savefile.json", "w") as savefile:
            self.players[player] += points
            json.dump(self.players, savefile)

    def extras(self):
        extras = evalinput("Extras wie Schneider, Hand, usw.")
        if extras < 0:
            self.extras()
        else:
            return extras

    def player(self):
        player = input("Wer hat gespielt? Punkte um Punktestand anzueigen. 0 um Spiel zu beenden.").upper()
        if player in self.players:
            return player
        elif player == "0":
            quit()
        elif player.upper() == "PUNKTE":
            printpoints(self.players)
            self.player()
        else:
            self.player()


def evalinput(inputtxt):
    check = input(inputtxt)
    if check.isdigit():
        return int(check)

    else:
        evalinput(inputtxt)


def printpoints(players):
    for player in players:
        print(player, players[player])
    print("\n")


def newgame(f):
    with open(f, "w") as savefile:
        players = {input("Spieler1").upper(): 0,
                   input("Spieler2").upper(): 0,
                   input("Spieler3").upper(): 0, }
        json.dump(players, savefile)
    return players


def main():
    # known bug: wenn man keine spielernamen eingibt und das programm beendet
    # macht es ein leeres savefile welches beim laden crahsed. hatte kein bock mehr das zu fixen
    print("SKATNADO")
    print("DAS Skatpunkteaufschreibeprogramm")
    f = "savefile.json"
    if os.path.isfile(f):
        print("Spielstand laden?")
        resume = input("Y/N?").upper()
        if resume == "Y":
            with open(f, "r") as savefile:
                players = json.load(savefile)
            printpoints(players)
        elif resume == "N":
            players = newgame(f)
        else:
            main()
    else:
        print("LOS GEEEEHTS!!")
        players = newgame(f)
    Spiel(players).round()


main()
