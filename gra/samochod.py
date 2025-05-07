import pygame

class Obraz(pygame.sprite.Sprite):
    def __init__(self,sciezka):
        super().__init__()
        self.obraz = pygame.image.load(sciezka)

class Samochod():
    def __init__(self, nazwa,wybrany, lista_obrazow, przyspieszenie ,bak,nitro):
        self.wybrany = wybrany
        self.nazwa = nazwa
        self.obrazek = lista_obrazow[0]
        self.przyspieszenie = przyspieszenie
        self.bak = bak
        self.nitro = nitro
        self.lista_obrazow = lista_obrazow
        self.tekstura_samochodu = self.lista_obrazow[0]

class Audi(Samochod):
    def __init__(self):
        super().__init__("audi",1,['auto1.png','auto1 lewo.png','auto1drift.png','auto1drift lewo.png','auto1nitro.png','auto1nitro lewo.png','autokaput.png'], 2.5, 50,80)


class Mercedes(Samochod):
    def __init__(self):
        super().__init__("mercedes",2,['auto2.png','auto2 lewo.png','auto2drift.png','auto2drift lewo.png','auto2nitro.png','auto2nitro lewo.png','autokaput.png'],2.7,40,85)

class Bmw(Samochod):
    def __init__(self):
        super().__init__("bmw",3,['auto3.png','auto3 lewo.png','auto3drift.png','auto3drift lewo.png','auto3nitro.png','auto3nitro lewo.png','autokaput.png'],2.3,70,60)

class Porshe(Samochod):
    def __init__(self):
        super().__init__("porshe",4,['auto4.png','auto4 lewo.png','auto4drift.png','auto4drift lewo.png','auto4nitro.png','auto4nitro lewo.png','autokaput.png'],3,45,85)


dostepne_samochody = [Audi(), Bmw(), Mercedes(), Porshe()]
samochod_gracza = Audi()

def wybierz_nastepny(samochod_gracza):
    numer_samchodu_gracza = samochod_gracza.wybrany
    nastepny_samochod_numer = numer_samchodu_gracza + 1
    if nastepny_samochod_numer > len(dostepne_samochody):
        nastepny_samochod_numer = 1
    print("wybor nastepnego")
    for samochod in dostepne_samochody:
        if samochod.wybrany == nastepny_samochod_numer:
            return samochod