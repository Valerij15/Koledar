import datetime
from calendar import monthrange
from dateutil.relativedelta import relativedelta

class Koledar:

    def __init__(self, datum, dogodki):
        self.datum = datum
        self.dogodki = dogodki
        self.tabela_datumov = self.naredi_tabelo_datumov()
        self.vklopljen = (False, -1)

    def dodaj_mesece(self, n):
        self.datum.dodaj_mesece(n)
        self.tabela_datumov = self.naredi_tabelo_datumov()

    def vklopi(self, i):
        if self.vklopljen[1] == i or self.vklopljen[1] == -1:
            self.vklopljen = (not (self.vklopljen[0]), i)
        else:
            self.vklopljen = (True, i)

    def posodobi(self, dogodki):
        self.dogodki = dogodki
        self.tabela_datumov = self.naredi_tabelo_datumov()

    def naredi_tabelo_datumov(self):
        tabela = []
        prvi_teden = Datum(datetime.datetime(self.datum.leto, self.datum.mesec, 1))
        zacetek_meseca = prvi_teden.stevilo_dneva_v_tednu()
        konec_meseca = self.datum.stevilo_dni_v_mesecu() + zacetek_meseca - 1
        prejsnji_teden = Datum(datetime.datetime(prvi_teden.leto, prvi_teden.mesec, prvi_teden.dan))
        prejsnji_teden.dodaj_dneve(-(zacetek_meseca - 1))
        for i in range(1, 43):
            if i < zacetek_meseca or i > konec_meseca:
                tabela.append((prejsnji_teden.dan, prejsnji_teden.ime_meseca(), prejsnji_teden.leto,  0, self.naredi_tabelo_dogodkov(prejsnji_teden)))
            else:
                tabela.append((prejsnji_teden.dan, prejsnji_teden.ime_meseca(), prejsnji_teden.leto, 1, self.naredi_tabelo_dogodkov(prejsnji_teden)))
            prejsnji_teden.dodaj_dneve(1)
        return tabela
    
    def naredi_tabelo_dogodkov(self, dan):
        tab = []
        for dogodek in self.dogodki:
            if not(dogodek.datum.datum < dan.datum)  and not(dogodek.datum.datum > dan.datum):
                tab.append((dogodek.id, dogodek.ime))
        return tab


class Datum:

    def __init__(self, datum = datetime.datetime(2021,9,1), dogodki = []):
        self.datum = datum
        self.dogodki = dogodki
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
        self.stevilo_dogodkov = 0
        self.datum = Datum()
        self.dogodki = []
        self.koledar = Koledar(self.datum, self.dogodki)

    def dodaj_dogodek(self, ime, datum, opis = ''):
        self.dogodki.append(Dogodek(self.stevilo_dogodkov, ime, datum, opis))
        self.koledar.posodobi(self.dogodki)
        self.stevilo_dogodkov += 1

    def izpisi_dogodke(self):
        for dogodek in self.dogodki:
            print(f' Ime dogodka: {dogodek.ime}\n Datum dogodka: {dogodek.datum}\n Opis dogodka: {dogodek.opis}')
            print('')

class Dogodek:

    def __init__(self, id, ime, datum, opis = ''):
        self.id = id
        self.ime = ime
        self.datum = datum
        self.opis = opis

poskus = Uporabnik("Valerij")
poskus.dodaj_dogodek("hmm", Datum())
poskus.dodaj_dogodek("ree", Datum())
poskus.dodaj_dogodek("yo", Datum())
poskus.dodaj_dogodek("hfffsdfsm", Datum())



