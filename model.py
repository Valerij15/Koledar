import datetime
from calendar import monthrange

class Datum:
    def __init__(self):
        self.stevilo_dneva_v_tednu = int(self.danasnji_datum().strftime("%w"))
        self.dan = int(self.danasnji_datum().strftime("%d"))
        self.mesec = int(self.danasnji_datum().strftime("%m"))
        self.leto = int(self.danasnji_datum().strftime("%Y"))
        
    def danasnji_datum(self):
        return datetime.datetime.now()
        
    def stevilo_dni_v_mesecu(self):
        return monthrange(self.leto, self.mesec)[1]
        
    def zacetek_meseca(self):
        return 8 + (self.stevilo_dneva_v_tednu - (self.dan % 7))

class Uporabnik:

    def __init__(self, username):
        self.username = username
        self.dogodki = []

    def dodaj_dogodek(self, ime, datum, opis = ''):
        self.dogodki.append(Dogodek(ime, datum, opis))

    def izpisi_dogodke(self):
        for dogodek in self.dogodki:
            print(f' Ime dogodka: {dogodek.ime}\n Datum dogodka: {dogodek.datum}\n Opis dogodka: {dogodek.opis}')
            print('')

class Dogodek:

    def __init__(self, ime, datum, opis = ''):
        self.ime = ime
        self.datum = datum
        self.opis = opis

poskus = Datum()