import datetime
from calendar import monthrange
from re import U
from dateutil.relativedelta import relativedelta
import sqlite3
import os.path

#kreiranje podatkovne baze
if(os.path.isfile('database.db')):  
    base = sqlite3.connect('database.db')
else:
    base = sqlite3.connect('database.db')
    b = base.cursor()
    b.execute('CREATE TABLE uporabniki (uporabnisko_ime text, geslo text)') #če baza še ne obstaja jo naredimo
    b.execute(
        'CREATE TABLE dogodki (id integer, ime text, datumod text, datumdo text, opis, ime_uporabnika text)')
    base.commit()
    b.close()


class Koledar:    #razred, ki opravlja s dogodki ter dnevi na koledarju.

    def __init__(self, datum, ime_uporabnika):
        self.datum = datum      #datum, ki pomaga pri tem kateri mesec si uporabnik ogleduje
        self.ime_uporabnika = ime_uporabnika
        self.dogodki = []       #tabela uporabnikovih dogodkov
        self.stevilo_dogodkov = 0   #število dogodkov, ki jih je uporabnik do zdaj naredil
        self.preberi_dogodke()       #napolnimo tabelo s dogodki
        self.prazniki = [("novo leto", 1, 1, "ZDRAVO, SREČNO IN VESELO NOVO LETO!"), ("novo leto", 1, 2, "ZDRAVO, SREČNO IN VESELO NOVO LETO!"), ("Prešernov dan", 8, 2, "Obletnica smrti največjega slovenskega pesnika Franceta Prešerna"), ("dan upora proti okupatorju", 27, 4, "Obeležuje pomembni dogodek iz leta 1941, ko so se 26. aprila v Rožni dolini, v hiši književnika Josipa Vidmarja, zbrali Aleš Bebler, Boris Ziherl, Boris Kidrič, France Šturm, Ferdo Kozak, Josip Rus in Tone Fajfar in določili smernice za organiziran oborožen odpor proti okupatorju."),
                         ("praznik dela", 1, 5, "Mednarodni praznik delavstva, ki ga 1. maja vsako leto praznujejo v večini držav sveta."), ("dan Primoža Trubarja", 8, 6, "Praznik je namenjen obeležitvi osrednje osebnosti slovenskega protestantizma v 16. stoletju in hkrati najpomembnejše osebnosti v razvijanju temeljev za oblikovanje slovenskega naroda Primoža Trubarja"), ("dan državnosti",25, 6, " Obeležuje spomin na 25. junij 1991, ko je Slovenija formalno postala neodvisna."), ("združitev prekmurskih Slovencev z matičnim narodom", 17, 8, "Dan, ko je Prekmurje po določilih Pariške mirovne konference pripadlo Kraljevini Srbov, Hrvatov in Slovencev, s tem pa so bili prekmurski Slovenci po stoletjih madžarske oblasti znova združeni z matičnim narodom."),
                         ("vrnitev Primorske k matični domovini", 15, 9, "Praznik obeležuje 15. september 1947, ko je bila uveljavljena pariška mirovna pogodba z Italijo, ki je takratni Jugoslaviji in s tem tudi Sloveniji dodelila velik del Primorske."), ("dan slovenskega športa", 23, 9, " Datum je izbran kot obletnica 23. septembra 2000, ko je ob zmagi veslačev Iztoka Čopa in Luke Špika ter strelca Rajmonda Debevca na poletnih olimpijskih igrah v Sydneyju prvič zaigrala slovenska himna Zdravljica."), ("dan suverenosti", 25, 10, "Dan, ko je po osamosvojitveni vojni zadnji vojak Jugoslovanske ljudske armade zapustil slovensko ozemlje."), ("dan spomina na mrtve", 1, 11, "Na dan spomina na mrtve se ljudje množično odpravljajo na pokopališča na grobove bližnjih ter tam prižigajo sveče, prinašajo šopke rož, vence in ikebane ter se."),
                         ("dan Rudolfa Maistra", 23, 11, "Na ta dan je Rudolf Maister leta 1918 s svojo vojsko razorožil nemško varnostno stražo in jo razpustil."), ("dan samostojnosti in enotnosti", 26, 12, "Ta dan obeležuje razglasitev izidov plebiscita o samostojnosti 26. decembra 1990."), ("Marijino vnebovzetje", 15, 8, " Na ta dan se kristjani spominjajo, da je bila Devica Marija z dušo in telesom vzeta v nebesa. "), ("dan reformacije", 31, 10, "Dan reformacije je protestantski krščanski verski praznik, ki se praznuje v spomin na začetek reformacije."), ("božič", 25, 12, "Božič je tradicionalni krščanski praznik, ki ga v katoliških in protestantskih državah praznujejo 25. decembra kot spomin na rojstvo Jezusa Kristusa.")]
        self.tabela_datumov = self.naredi_tabelo_datumov()  #tabela datumov za trenutno izbrano mesec in leto
        self.vklopljen = 0      #spremenljivka ki pove kateri datum je uporabnik izbral

    def dodaj_mesece(self, n):     #metoda, ki prestavi koledar v naslednji mesec
        self.datum.dodaj_mesece(n)
        self.tabela_datumov = self.naredi_tabelo_datumov()

    def preklopi(self, i):
        self.vklopljen = i

    def preberi_dogodke(self):   #metoda ki prebere dogodke iz podatkovne baze ter jih spravi v tabelo dogodkov
        b = base.cursor()
        b.execute('SELECT * FROM dogodki where ime_uporabnika =?',
                  (self.ime_uporabnika,))
        tab = b.fetchall()
        b.close()
        for dogodek in tab:
            self.stevilo_dogodkov += 1
            self.dogodki.append(Dogodek(dogodek[0], dogodek[1], Datum.spremeni_v_datum(
                dogodek[2]), Datum.spremeni_v_datum(dogodek[3]), dogodek[4]))

    def dodaj_dogodek(self, ime, časod, časdo=0, opis=''):  #metoda ki doda dogodek v podatkovno bazo ter tabelo dogodkov
        b = base.cursor()
        if(časdo == 0 or časod.je_vecji_od(časdo)): 
            časdo = časod
        b.execute('INSERT INTO dogodki (id, ime, datumod, datumdo, opis, ime_uporabnika) VALUES (?, ?, ?, ?, ?, ?)',
                  (self.stevilo_dogodkov, ime, časod.oblika_za_bazo(), časdo.oblika_za_bazo(), opis, self.ime_uporabnika))
        base.commit()
        b.close()
        self.dogodki.append(
            Dogodek(self.stevilo_dogodkov, ime, časod, časdo, opis))
        self.stevilo_dogodkov += 1
        self.tabela_datumov = self.naredi_tabelo_datumov()

    def izbrisi_dogodek(self, id): #metoda ki odstrani dogodek iz podatkovne baze ter tabele dogodkov
        b = base.cursor()
        b.execute('DELETE FROM dogodki where ime_uporabnika =? AND id =?',
                  (self.ime_uporabnika, id))
        base.commit()
        b.close()
        n = 0
        id = int(id)
        for dogodek in self.dogodki:
            if(dogodek.id == id):
                self.dogodki.pop(n)
            n += 1
        self.tabela_datumov = self.naredi_tabelo_datumov()

    def naredi_tabelo_datumov(self):  #metoda, ki naredi tabelo s dnevi, dogodki ter zanimivostmi glede na izbran mesec ter leto na koledarju
        tabela = []
        prvi_dan = Datum(1, self.datum.mesec, self.datum.leto)
        zacetek_meseca = prvi_dan.stevilo_dneva_v_tednu()
        konec_meseca = self.datum.stevilo_dni_v_mesecu() + zacetek_meseca - 1
        zacetek_koledarja = Datum(1, self.datum.mesec, self.datum.leto)
        zacetek_koledarja.dodaj_dneve(-(zacetek_meseca - 1))
        for i in range(1, 43):
            if i < zacetek_meseca or i > konec_meseca:
                tabela.append((Datum(zacetek_koledarja.dan, zacetek_koledarja.mesec, zacetek_koledarja.leto), "grey",
                              self.naredi_tabelo_dogodkov(zacetek_koledarja), self.naredi_tabelo_zanimivosti(zacetek_koledarja)))
            else:
                tabela.append((Datum(zacetek_koledarja.dan, zacetek_koledarja.mesec, zacetek_koledarja.leto), "black",
                              self.naredi_tabelo_dogodkov(zacetek_koledarja), self.naredi_tabelo_zanimivosti(zacetek_koledarja)))
            zacetek_koledarja.dodaj_dneve(1)
        return tabela

    def naredi_tabelo_dogodkov(self, dan): #metoda, ki naredi tabelo dogodkov za določen dan na koledarju
        tab = []
        for dogodek in self.dogodki:
            datumod = Datum(dogodek.datum.dan,
                            dogodek.datum.mesec, dogodek.datum.leto)
            while(not datumod.je_enak(dogodek.datumdo)):
                if datumod.je_enak(dan):
                    tab.append(dogodek)
                datumod.dodaj_dneve(1)
            if datumod.je_enak(dan):
                tab.append(dogodek)
        return tab

    def oblikuj_datum(self, neoblikovan): #metoda ki dobi datum dogodka ki ga je uporabnik izbral ter ga spremeni v razred Datum

        if(neoblikovan == ''):
            return self.tabela_datumov[self.vklopljen][0]

        else:
            try:
                neoblikovan = neoblikovan.replace(",", "")
                oblikovan = neoblikovan.split()
                tab = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                mesec = tab.index(oblikovan[0]) + 1
                dan = int(oblikovan[1])
                leto = int(oblikovan[2])
                return Datum(dan, mesec, leto)
            
            except:
                raise Exception("Napačna oblika datumov!") 



    def naredi_tabelo_zanimivosti(self, dan): #naredi tabelo zanimivosti na določen dan
        tab = []
        id = 0
        zdaj = Datum(int(datetime.datetime.now().strftime("%d")), int(
            datetime.datetime.now().strftime("%m")), int(datetime.datetime.now().strftime("%Y")))
        if dan.je_enak(zdaj):
            tab.append((id, "Današnji dan", zdaj, "hmm"))
            id += 1
        for praznik in self.prazniki:
            if(dan.dan == praznik[1] and dan.mesec == praznik[2]):
                tab.append((id, praznik[0], Datum(
                    praznik[1], praznik[2], dan.leto), praznik[3]))
                id += 1
        return tab

    def naredi_urejeno_tabelo(self): #naredi tabelo dogodkov urejeno po vrsti od najmanj oddaljenega do najbolj oddaljenega ter izloči dogodke, ki so se že zgodili.
        tab = []
        danes = Datum()
        n = 0
        for dogodek in self.dogodki:
            if(dogodek.datum.je_vecji_od(danes)):
                if len(tab) == 0:
                    tab.append((dogodek.ime, dogodek.datum, dogodek.datumdo,
                               dogodek.opis, dogodek.datum.časdo(), dogodek.id))
                else:
                    while(n < len(tab)):
                        if tab[n][1].je_vecji_od(dogodek.datum):
                            tab.insert(n, (dogodek.ime, dogodek.datum, dogodek.datumdo,
                                       dogodek.opis, dogodek.datum.časdo(), dogodek.id))
                            n = len(tab)
                        n += 1
                    if(n == len(tab)):
                        tab.append((dogodek.ime, dogodek.datum, dogodek.datumdo,
                                   dogodek.opis, dogodek.datum.časdo(), dogodek.id))
            elif(dogodek.datum.je_enak(danes)):
                tab.insert(0, (dogodek.ime, dogodek.datum,
                           dogodek.datumdo, dogodek.opis, "danes", dogodek.id))
        return tab


class Datum: #razred, ki pomaga pri delanju s datumi

    def __init__(self, dan=int(datetime.datetime.today().strftime("%d")), mesec=int(datetime.datetime.today().strftime("%m")), leto=int(datetime.datetime.today().strftime("%Y"))):
        self.datum = datetime.datetime(leto, mesec, dan)   #objekt razreda datetime
        self.dan = dan
        self.mesec = mesec
        self.leto = leto

    def je_enak(self, drugi): #metoda, ki primerja dva datuma in vrne če sta enaka
        return not(drugi.datum < self.datum) and not(drugi.datum > self.datum)

    def stevilo_dni_v_mesecu(self):  #metoda, ki vrne število dni v mesecu za določen datum
        return monthrange(self.leto, self.mesec)[1]

    def stevilo_dneva_v_tednu(self): #metoda, ki vrne kateri dan v tednu je določen datum
        n = int(self.datum.strftime("%w"))
        if n == 0:
            n = 7
        return n

    def ime_meseca(self):  #metoda, ki vrne ime meseca za določen datum
        meseci = ["Januar", "Februar", "Marec", "April", "Maj", "Junij",
                  "Julij", "Avgust", "September", "Oktober", "November", "December"]
        return meseci[self.mesec - 1]

    def dodaj_mesece(self, n):  #metoda ki datumu doda n mesecov.
        self.datum = self.datum + relativedelta(months=n)
        self.posodobi_spremenljivke()

    def dodaj_dneve(self, n): #metoda ki datumu doda n tednov.
        self.datum = self.datum + relativedelta(days=n)
        self.posodobi_spremenljivke()

    def je_vecji_od(self, drugi):  #metoda ki preveri ali je naš datum večji od datuma v argumentu
        return (self.datum > drugi.datum)

    def posodobi_spremenljivke(self):  #metoda, ki posodbi spremenljivke
        self.dan = int(self.datum.strftime("%d"))
        self.mesec = int(self.datum.strftime("%m"))
        self.leto = int(self.datum.strftime("%Y"))

    def oblika_za_bazo(self):   #metoda, ki spravi datum v obliko za podatkovno bazo
        return str(self.dan) + "/" + str(self.mesec) + "/" + str(self.leto)

    def časdo(self):            #metoda, ki pove koliko časa je od današnjega dneva do določenega datuma
        danes = datetime.datetime.today()
        razlika = self.datum - danes
        return razlika.days + 1

    @staticmethod
    def spremeni_v_datum(datum):    #metoda ki niz iz baze spremeni v datum
        tab = datum.split("/")
        return Datum(int(tab[0]), int(tab[1]), int(tab[2]))


class Uporabnik:   #razred uporabnika

    def __init__(self, uporabnisko_ime, geslo):
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo
        self.datum = Datum()
        self.koledar = Koledar(self.datum, self.uporabnisko_ime)

    def preveri_geslo(self, vtipkano_geslo):  #metoda, ki preveri ali sta vtipkano geslo ter geslo uporabnika enaki
        return self.geslo == Uporabnik.zasifriraj_geslo(vtipkano_geslo)

    @staticmethod
    def zasifriraj_geslo(geslo):  #metoda ki zašifira geslo
        sifra = ""
        for i in geslo:
            char = ord(i[0])
            char += 1
            char = chr(char)
            sifra += char
        return sifra

    @staticmethod
    def registracija(uporabnisko_ime, geslo):  #metoda ki doda novega uporabnika če ta še ne obstaja
        b = base.cursor()
        b.execute('SELECT * FROM uporabniki WHERE uporabnisko_ime =?',
                  (uporabnisko_ime,))
        if(len(b.fetchall()) == 0):
            geslo = Uporabnik.zasifriraj_geslo(geslo)
            b.execute('INSERT INTO uporabniki (uporabnisko_ime, geslo) VALUES (?, ?)',
                      (uporabnisko_ime, geslo))
            base.commit()
            b.close()
            return Uporabnik(uporabnisko_ime, geslo)
        else:
            b.close()
            raise ValueError("Uporabniško ime že obstaja!")

    @staticmethod
    def prijava(uporabnisko_ime, geslo):   #metoda ki vpiše vporabnika če ima ta pravilno geslo
        uporabnik = Uporabnik.vrniUporabnika(uporabnisko_ime)
        if uporabnik:
            if not uporabnik.preveri_geslo(geslo):
                raise ValueError("Geslo je napačno!")
            else:
                return Uporabnik(uporabnisko_ime, geslo)
        else:
            raise ValueError("Uporabniško ime ne obstaja!")

    @staticmethod
    def vrniUporabnika(uporabnisko_ime):  #metoda, ki vrne uporabnika iz podatkovne baze če ta obstaja
        b = base.cursor()
        b.execute('SELECT * FROM uporabniki WHERE uporabnisko_ime =?',
                  (uporabnisko_ime,))
        tab = b.fetchall()
        b.close()
        if(len(tab) == 0):
            raise ValueError("Uporabnik ne obstaja!")
        else:
            return Uporabnik(tab[0][0], tab[0][1])


class Dogodek: #razred za lažje upravljanje s dogodki

    def __init__(self, id, ime, datumod, datumdo=0, opis=''):
        self.id = id
        self.ime = ime
        self.datum = datumod
        self.opis = opis
        if(datumdo == 0):
            self.datumdo = datumod
        else:
            self.datumdo = datumdo
