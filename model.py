import datetime
from calendar import monthrange
from dateutil.relativedelta import relativedelta

class Koledar:

    def __init__(self, datum):
        self.datum = datum
        self.dogodki = []
        self.stevilo_dogodkov = 0
        self.dodaj_praznike()
        self.tabela_datumov = self.naredi_tabelo_datumov()
        self.vklopljen = 0

    def dodaj_mesece(self, n):
        prejsnje_leto = self.datum.leto
        self.datum.dodaj_mesece(n)
        if not (self.datum.leto == prejsnje_leto):
            self.dodaj_praznike()
        self.tabela_datumov = self.naredi_tabelo_datumov()

    def preklopi(self, i):
        self.vklopljen = i

    def dodaj_dogodek(self, ime, časod, časdo = 0, opis = '', tip = 'dogodek'):
        if(časdo == 0):
            časdo = časod
        while(not časod.je_enak(časdo)):
                self.dogodki.append(Dogodek(self.stevilo_dogodkov, ime, Datum(časod.dan, časod.mesec, časod.leto), 0, opis, tip))
                časod.dodaj_dneve(1)
        self.dogodki.append(Dogodek(self.stevilo_dogodkov, ime, Datum(časod.dan, časod.mesec, časod.leto), 0, opis, tip))
        self.stevilo_dogodkov += 1
        self.tabela_datumov = self.naredi_tabelo_datumov()

    def naredi_tabelo_datumov(self):
        tabela = []
        prvi_dan = Datum(1, self.datum.mesec, self.datum.leto)
        zacetek_meseca = prvi_dan.stevilo_dneva_v_tednu()
        konec_meseca = self.datum.stevilo_dni_v_mesecu() + zacetek_meseca - 1
        zacetek_koledarja = Datum(1, self.datum.mesec, self.datum.leto)
        zacetek_koledarja.dodaj_dneve(-(zacetek_meseca - 1))
        for i in range(1, 43):
            if i < zacetek_meseca or i > konec_meseca:
                tabela.append((Datum(zacetek_koledarja.dan, zacetek_koledarja.mesec, zacetek_koledarja.leto), "grey", self.naredi_tabelo_dogodkov(zacetek_koledarja)))
            else:
                tabela.append((Datum(zacetek_koledarja.dan, zacetek_koledarja.mesec, zacetek_koledarja.leto), "black", self.naredi_tabelo_dogodkov(zacetek_koledarja)))
            zacetek_koledarja.dodaj_dneve(1)
        return tabela
    
    def naredi_tabelo_dogodkov(self, dan):
        tab = []
        for dogodek in self.dogodki:
            if dogodek.datum.je_enak(dan):
                tab.append(dogodek)
        return tab

    def oblikuj_datum(self, neoblikovan):

        if(neoblikovan == ''):
            return self.tabela_datumov[self.vklopljen][0]

        else:
            neoblikovan = neoblikovan.replace(",", "")
            oblikovan = neoblikovan.split()
            tab = ['Jan', 'Feb', 'Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            mesec = tab.index(oblikovan[0]) + 1
            dan = int(oblikovan[1])
            leto = int(oblikovan[2])
            return Datum(dan, mesec, leto)
    
    def dodaj_praznike(self):
        prazniki = [("novo leto", 1, 1)]
        for praznik in prazniki:
            self.dodaj_dogodek(praznik[0], Datum(praznik[1], praznik[2], self.datum.leto), 0, '', "praznik")


class Datum:

    def __init__(self, dan, mesec, leto):
        self.datum = datetime.datetime(leto, mesec, dan)
        self.dan = dan
        self.mesec = mesec
        self.leto = leto
    
    def je_enak(self, drugi):
        return not(drugi.datum < self.datum) and not(drugi.datum > self.datum)
           
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
        self.datum = Datum(int(datetime.datetime.today().strftime("%d")), int(datetime.datetime.today().strftime("%m")), int(datetime.datetime.today().strftime("%Y")))
        self.koledar = Koledar(self.datum)

class Dogodek:

    def __init__(self, id, ime, datumod, datumdo = 0, opis = '', tip = 'dogodek'):
        self.id = id
        self.ime = ime
        self.tip = tip
        self.datum = datumod
        self.opis = opis
        if(datumdo == 0):
            self.datumdo = datumod
        else:
            self.datumdo = datumdo

poskus = Uporabnik("Valerij")




