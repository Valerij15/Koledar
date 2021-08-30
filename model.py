import datetime
from calendar import monthrange
from dateutil.relativedelta import relativedelta

class Datum:

    def __init__(self):
        self.datum = self.danasnji_datum()
        self.stevilo_dneva_v_tednu = int(self.datum.strftime("%w"))
        self.dan = int(self.datum.strftime("%d"))
        self.mesec = int(self.datum.strftime("%m"))
        self.leto = int(self.datum.strftime("%Y"))
        self.tabela_datumov = self.naredi_tabelo()
        
    def danasnji_datum(self):
        return datetime.datetime.now()
        
    def stevilo_dni_v_mesecu(self):
        return monthrange(self.leto, self.mesec)[1]
    
    def ime_meseca(self):
        meseci = ["Januar", "Februar", "Marec", "April", "Maj", "Junij", "Julij", "Avgust", "September", "Oktober", "November", "December"]
        return meseci[self.mesec - 1]
        
    def zacetek_meseca(self):
        return 8 + (self.stevilo_dneva_v_tednu - (self.dan % 7))

    def dodaj_mesece(self, n):
        self.datum = self.datum + relativedelta(months=n)
        self.posodobi_spremenljivke()
    
    def posodobi_spremenljivke(self):
        self.stevilo_dneva_v_tednu = int(self.datum.strftime("%w"))
        self.dan = int(self.datum.strftime("%d"))
        self.mesec = int(self.datum.strftime("%m"))
        self.leto = int(self.datum.strftime("%Y"))
        self.tabela_datumov = self.naredi_tabelo()
    
    def naredi_tabelo(self):
        tabela = []
        prvi_teden = datetime.date(self.leto, self.mesec, 1)
        zacetek_meseca = int(prvi_teden.strftime("%w"))
        if zacetek_meseca == 0:
            zacetek_meseca = 7
        konec_meseca = self.stevilo_dni_v_mesecu() + zacetek_meseca - 1
        prejsnji_teden = prvi_teden + relativedelta(days = -(zacetek_meseca - 1))
        naslednji_teden = datetime.date(self.leto, self.mesec, self.stevilo_dni_v_mesecu()) + relativedelta(days = 1)
        for i in range(1, 43):
            if i < zacetek_meseca:
                tabela.append((int(prejsnji_teden.strftime("%d")), 0))
                prejsnji_teden += relativedelta(days = 1)
            elif i > konec_meseca:
                tabela.append((int(naslednji_teden.strftime("%d")), 0))
                naslednji_teden += relativedelta(days = 1)
            else:
                tabela.append((i- zacetek_meseca + 1, 1))
        return tabela


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