import datetime
from calendar import monthrange
from re import U
from dateutil.relativedelta import relativedelta
import sqlite3
import os.path


if(os.path.isfile('database.db')):
    base = sqlite3.connect('database.db')
else:
    base = sqlite3.connect('database.db')
    b = base.cursor()
    b.execute('CREATE TABLE uporabniki (uporabnisko_ime text, geslo text)')
    b.execute('CREATE TABLE dogodki (id integer, ime text, datumod text, datumdo text, opis, ime_uporabnika text)')
    base.commit()
    b.close()

class Koledar:

    def __init__(self, datum, ime_uporabnika):
        self.datum = datum
        self.ime_uporabnika = ime_uporabnika
        self.dogodki = []
        self.stevilo_dogodkov = 0
        self.preberi_dogodke()
        self.prazniki = [("novo leto", 1, 1, "opis"), ("novo leto", 1, 2, "opis"), ("Prešernov dan", 8, 2, "opis"), ("dan upora proti okupatorju", 27, 4, "opis"), ("praznik dela", 1, 5, "opis"),
        ("dan Primoža Trubarja", 8, 6, "opis"), ("dan državnosti", 25, 6, "opis"), ("združitev prekmurskih Slovencev z matičnim narodom", 17, 8, "opis"), ("vrnitev Primorske k matični domovini", 15, 9, "opis"), ("dan slovenskega športa", 23, 9, "opis"),
        ("dan suverenosti", 25, 10, "opis"), ("dan spomina na mrtve", 1, 11, "opis"), ("dan Rudolfa Maistra", 23, 11, "opis"), ("dan samostojnosti in enotnosti", 26, 12, "opis"), ("Marijino vnebovzetje", 15, 8, "opis"), ("dan reformacije", 31, 10, "opis"),("božič", 25, 12, "opis")]
        self.tabela_datumov = self.naredi_tabelo_datumov()
        self.vklopljen = 0

    def dodaj_mesece(self, n):
        self.datum.dodaj_mesece(n)
        self.tabela_datumov = self.naredi_tabelo_datumov()

    def preklopi(self, i):
        self.vklopljen = i

    def preberi_dogodke(self):
        b = base.cursor()
        b.execute('SELECT * FROM dogodki where ime_uporabnika =?', (self.ime_uporabnika,))
        tab = b.fetchall()
        b.close()
        for dogodek in tab:
            self.stevilo_dogodkov += 1
            self.dogodki.append(Dogodek(dogodek[0], dogodek[1], Datum.spremeni_v_datum(dogodek[2]), Datum.spremeni_v_datum(dogodek[3]), dogodek[4]))

    def dodaj_dogodek(self, ime, časod, časdo = 0, opis = ''):
        b = base.cursor()
        if(časdo == 0 or časod.je_vecji_od(časdo)):
            časdo = časod
        b.execute('INSERT INTO dogodki (id, ime, datumod, datumdo, opis, ime_uporabnika) VALUES (?, ?, ?, ?, ?, ?)', (self.stevilo_dogodkov, ime, časod.oblika_za_bazo(), časdo.oblika_za_bazo(), opis, self.ime_uporabnika))
        base.commit()
        b.close()
        self.dogodki.append(Dogodek(self.stevilo_dogodkov, ime, časod, časdo, opis))
        self.stevilo_dogodkov += 1
        self.tabela_datumov = self.naredi_tabelo_datumov()
    
    def izbrisi_dogodek(self, id):
        b = base.cursor()
        b.execute('DELETE FROM dogodki where ime_uporabnika =? AND id =?', (self.ime_uporabnika, id))
        base.commit()
        b.close()
        n = 0
        id = int(id)
        for dogodek in self.dogodki:
            if(dogodek.id == id):
                self.dogodki.pop(n)
            n += 1
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
                tabela.append((Datum(zacetek_koledarja.dan, zacetek_koledarja.mesec, zacetek_koledarja.leto), "grey", self.naredi_tabelo_dogodkov(zacetek_koledarja), self.naredi_tabelo_zanimivosti(zacetek_koledarja)))
            else:
                tabela.append((Datum(zacetek_koledarja.dan, zacetek_koledarja.mesec, zacetek_koledarja.leto), "black", self.naredi_tabelo_dogodkov(zacetek_koledarja), self.naredi_tabelo_zanimivosti(zacetek_koledarja)))
            zacetek_koledarja.dodaj_dneve(1)
        return tabela
    
    def naredi_tabelo_dogodkov(self, dan):
        tab = []
        for dogodek in self.dogodki:
            datumod = Datum(dogodek.datum.dan, dogodek.datum.mesec, dogodek.datum.leto )
            while( not datumod.je_enak(dogodek.datumdo)):
                if datumod.je_enak(dan):
                    tab.append(dogodek)
                datumod.dodaj_dneve(1)
            if datumod.je_enak(dan):
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
    
    def naredi_tabelo_zanimivosti(self, dan):
        tab = []
        id = 0
        zdaj = Datum(int(datetime.datetime.now().strftime("%d")), int(datetime.datetime.now().strftime("%m")), int(datetime.datetime.now().strftime("%Y")))
        if dan.je_enak(zdaj):
            tab.append((id, "Današnji dan", zdaj, "hmm"))
            id += 1
        for praznik in self.prazniki:
            if(dan.dan == praznik[1] and dan.mesec == praznik[2]):
                tab.append((id, praznik[0], Datum(praznik[1], praznik[2], dan.leto), praznik[3]))
                id += 1
        return tab
    
    def naredi_urejeno_tabelo(self):
        tab = []
        danes = Datum()
        n = 0
        for dogodek in self.dogodki:
            if(dogodek.datum.je_vecji_od(danes)):
                if len(tab) == 0:
                    tab.append((dogodek.ime, dogodek.datum, dogodek.datumdo, dogodek.opis, dogodek.datum.časdo(), dogodek.id))
                else:
                    while(n < len(tab)):
                        if tab[n][1].je_vecji_od(dogodek.datum):
                            tab.insert(n, (dogodek.ime, dogodek.datum, dogodek.datumdo, dogodek.opis, dogodek.datum.časdo(), dogodek.id))
                            n = len(tab)
                        n += 1
                    if(n == len(tab)):
                        tab.append((dogodek.ime, dogodek.datum, dogodek.datumdo, dogodek.opis, dogodek.datum.časdo(), dogodek.id))
            elif(dogodek.datum.je_enak(danes)):
                tab.insert(0, (dogodek.ime, dogodek.datum, dogodek.datumdo, dogodek.opis, "danes", dogodek.id))
        return tab



class Datum:

    def __init__(self, dan = int(datetime.datetime.today().strftime("%d")), mesec = int(datetime.datetime.today().strftime("%m")), leto = int(datetime.datetime.today().strftime("%Y"))):
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
    
    def je_vecji_od(self, drugi):
        return (self.datum > drugi.datum)
    
    def posodobi_spremenljivke(self):
        self.dan = int(self.datum.strftime("%d"))
        self.mesec = int(self.datum.strftime("%m"))
        self.leto = int(self.datum.strftime("%Y"))

    def  oblika_za_bazo(self):
        return str(self.dan) +"/" + str(self.mesec) + "/"  + str(self.leto)

    def časdo(self):
        danes = datetime.datetime.today()
        razlika = self.datum - danes
        return razlika.days + 1

    @staticmethod
    def spremeni_v_datum(datum):
        tab = datum.split("/")
        return Datum(int(tab[0]), int(tab[1]), int(tab[2]))
    

class Uporabnik:

    def __init__(self, uporabnisko_ime, geslo):
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo
        self.datum = Datum()
        self.koledar = Koledar(self.datum, self.uporabnisko_ime)

    def preveri_geslo(self, vtipkano_geslo):
        return self.geslo == Uporabnik.zasifriraj_geslo(vtipkano_geslo)

    @staticmethod
    def zasifriraj_geslo(geslo):
        sifra = ""
        for i in geslo:
            char = ord(i[0])
            char += 1
            char = chr(char)
            sifra += char
        return sifra

    @staticmethod
    def registracija(uporabnisko_ime, geslo):
        b = base.cursor()
        b.execute('SELECT * FROM uporabniki WHERE uporabnisko_ime =?', (uporabnisko_ime,) )
        if(len(b.fetchall()) == 0):
            geslo = Uporabnik.zasifriraj_geslo(geslo)
            b.execute('INSERT INTO uporabniki (uporabnisko_ime, geslo) VALUES (?, ?)', (uporabnisko_ime, geslo))
            base.commit()
            b.close()
            return Uporabnik(uporabnisko_ime, geslo)
        else:
            b.close()
            raise ValueError("Uporabniško ime že obstaja!")

    @staticmethod
    def prijava(uporabnisko_ime, geslo):
        uporabnik = Uporabnik.vrniUporabnika(uporabnisko_ime)
        if uporabnik:
            if  not uporabnik.preveri_geslo(geslo):
                raise ValueError("Geslo je napačno!")
            else:
                return Uporabnik(uporabnisko_ime, geslo)
        else:
            raise ValueError("Uporabniško ime ne obstaja!")
    
    @staticmethod
    def vrniUporabnika(uporabnisko_ime):
        b = base.cursor()
        b.execute('SELECT * FROM uporabniki WHERE uporabnisko_ime =?', (uporabnisko_ime,) )
        tab = b.fetchall()
        b.close()
        if(len(tab) == 0):
            raise ValueError("Uporabnik ne obstaja!")
        else:
            return Uporabnik(tab[0][0], tab[0][1])

        

class Dogodek:

    def __init__(self, id, ime, datumod, datumdo = 0, opis = ''):
        self.id = id
        self.ime = ime
        self.datum = datumod
        self.opis = opis
        if(datumdo == 0):
            self.datumdo = datumod
        else:
            self.datumdo = datumdo





