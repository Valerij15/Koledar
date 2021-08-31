import datetime
from calendar import monthrange
from dateutil.relativedelta import relativedelta

class Koledar:

    def __init__(self, datum, dogodki):
        self.datum = datum
        self.dogodki = dogodki
        self.tabela_datumov = self.naredi_tabelo_datumov()
        self.vklopljen = (False, 0)

    def dodaj_mesece(self, n):
        self.datum.dodaj_mesece(n)
        self.tabela_datumov = self.naredi_tabelo_datumov()

    def vklopi(self, i):
        if self.vklopljen[1] == i:
            self.vklopljen = (not (self.vklopljen[0]), i)
        else:
            self.vklopljen = (self.vklopljen[0], i)

    def naredi_tabelo_datumov(self):
        tabela = []
        prvi_teden = Datum(datetime.date(self.datum.leto, self.datum.mesec, 1))
        zacetek_meseca = prvi_teden.stevilo_dneva_v_tednu()
        konec_meseca = self.datum.stevilo_dni_v_mesecu() + zacetek_meseca - 1
        prejsnji_teden = Datum(datetime.date(prvi_teden.leto, prvi_teden.mesec, prvi_teden.dan))
        prejsnji_teden.dodaj_dneve(-(zacetek_meseca - 1))
        naslednji_teden = Datum(datetime.date(self.datum.leto, self.datum.mesec, self.datum.stevilo_dni_v_mesecu()))
        naslednji_teden.dodaj_dneve(1)
        for i in range(1, 43):
            if i < zacetek_meseca:
                tabela.append((prejsnji_teden.dan, prejsnji_teden.ime_meseca(), prejsnji_teden.leto,  0))
                prejsnji_teden.dodaj_dneve(1)
            elif i > konec_meseca:
                tabela.append((naslednji_teden.dan, naslednji_teden.ime_meseca(), naslednji_teden.leto, 0))
                naslednji_teden.dodaj_dneve(1)
            else:
                tabela.append((i- zacetek_meseca + 1, self.datum.ime_meseca(), self.datum.leto, 1))
        return tabela


class Datum:

    def __init__(self, datum = datetime.datetime.now()):
        self.datum = datum
        self.dan = int(self.datum.strftime("%d"))
        self.mesec = int(self.datum.strftime("%m"))
        self.leto = int(self.datum.strftime("%Y"))
        
    def danasnji_datum(self):
        return datetime.datetime.now()
        
    def stevilo_dni_v_mesecu(self):
        return monthrange(self.leto, self.mesec)[1]
    
    def stevilo_dneva_v_tednu(self):
        n = int(self.datum.strftime("%w"))
        if n == 0:
            n = 7
        return n

    def ime_meseca(self):
        meseci = ["Januar", "Februar", "Marec", "April", "Maj", "Junij", "Julij", "Avgust", "September", "Oktober", "November", "December"]
        return meseci[self.mesec - 1]
        
    def dodaj_mesece(self, n):
        self.datum = self.datum + relativedelta(months=n)
        self.posodobi_spremenljivke()

    def dodaj_dneve(self, n):
        self.datum = self.datum + relativedelta(days=n)
        self.posodobi_spremenljivke()
    
    def posodobi_spremenljivke(self):
        self.dan = int(self.datum.strftime("%d"))
        self.mesec = int(self.datum.strftime("%m"))
        self.leto = int(self.datum.strftime("%Y"))
    


class Uporabnik:

    def __init__(self, username):
        self.username = username
        self.datum = Datum()
        self.dogodki = []
        self.koledar = Koledar(self.datum, self.dogodki)

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

poskus = Uporabnik("Valerij")