import bottle
import model

PRIJAVA = "prijavljen"
SKRIVNOST = "adkdjnsnkfsdjd"
aktivni_uporabniki = []

@bottle.route('/')
def osnovna_stran():
    uporabnik = preveri_prijavo()
    return bottle.template("osnovna_stran.html", mesec = uporabnik.datum.ime_meseca(), leto = uporabnik.datum.leto, tabela = uporabnik.koledar.tabela_datumov, vklopljen = uporabnik.koledar.vklopljen, uporabnik = uporabnik.uporabnisko_ime, stran = "osnovna_stran")

@bottle.get('/dogodki/')
def na_dogodke():
    uporabnik = preveri_prijavo()
    return bottle.template('dogodki.html', tab = uporabnik.koledar.naredi_urejeno_tabelo(), uporabnik = uporabnik.uporabnisko_ime, stran = "dogodki")

@bottle.get('/naslednji_mesec/')
def naslednji_mesec():
    uporabnik = preveri_prijavo()
    uporabnik.koledar.vklopljen = 0
    uporabnik.koledar.dodaj_mesece(1)
    bottle.redirect("/")

@bottle.get('/prejsnji_mesec/')
def prejsnji_mesec():
    uporabnik = preveri_prijavo()
    uporabnik.koledar.vklopljen = 0
    uporabnik.koledar.dodaj_mesece(-1)
    bottle.redirect("/")

@bottle.get('/vklopi<i>/')
def vklopi(i):
    uporabnik = preveri_prijavo()
    uporabnik.koledar.preklopi(int(i))
    bottle.redirect("/")

@bottle.post('/dodaj_dogodek/')
def dodaj_dogodek():
    uporabnik = preveri_prijavo()
    ime = bottle.request.forms.getunicode('ime_dogodka')
    opis = bottle.request.forms.getunicode('opis_dogodka')
    datumod = uporabnik.koledar.oblikuj_datum(bottle.request.forms.getunicode('datumod'))
    datumdo = uporabnik.koledar.oblikuj_datum(bottle.request.forms.getunicode('datumdo'))
    uporabnik.koledar.dodaj_dogodek(ime, datumod, datumdo, opis)
    bottle.redirect("/")

@bottle.post('/dogodki_dodaj_dogodek/')
def dodaj_dogodek():
    uporabnik = preveri_prijavo()
    ime = bottle.request.forms.getunicode('ime_dogodka')
    opis = bottle.request.forms.getunicode('opis_dogodka')
    datumod = uporabnik.koledar.oblikuj_datum(bottle.request.forms.getunicode('datumod'))
    datumdo = uporabnik.koledar.oblikuj_datum(bottle.request.forms.getunicode('datumdo'))
    uporabnik.koledar.dodaj_dogodek(ime, datumod, datumdo, opis)
    bottle.redirect("/dogodki/")

@bottle.post('/izbrisi_dogodek<i>/')
def izbrisi_dogodek(i):
    uporabnik = preveri_prijavo()
    uporabnik.koledar.izbrisi_dogodek(i)
    bottle.redirect("/")

@bottle.post('/dogodki_izbrisi_dogodek<i>/')
def izbrisi_dogodek(i):
    uporabnik = preveri_prijavo()
    uporabnik.koledar.izbrisi_dogodek(i)
    bottle.redirect("/dogodki/")

@bottle.get('/prijava/')
def prijava_get():
    return bottle.template("prijava.html", napaka = None, uporabnik = None)

@bottle.post('/prijava/')
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime')
    geslo = bottle.request.forms.getunicode('geslo')
    if not uporabnisko_ime:
        return bottle.template("registracija.html", napaka="Vnesi uporabniško ime!", uporabnik = None, stran = "prijava")
    try:
        model.Uporabnik.prijava(uporabnisko_ime, geslo)
        bottle.response.set_cookie(PRIJAVA, uporabnisko_ime, path="/", secret=SKRIVNOST)
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template("prijava.html", napaka=e.args[0], uporabnik = None)


@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija.html", napaka = None, uporabnik = None)

@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("registracija.html", napaka="Vnesi uporabniško ime!", uporabnik = None, stran = "registracija")
    try:
        model.Uporabnik.registracija(uporabnisko_ime, geslo)
        bottle.response.set_cookie(PRIJAVA, uporabnisko_ime, path="/", secret=SKRIVNOST)
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template("registracija.html", napaka = e.args[0], uporabnik = None)

def preveri_prijavo():
    uporabnisko_ime = bottle.request.get_cookie(PRIJAVA,  secret = SKRIVNOST)
    if uporabnisko_ime:
        for uporabnik in aktivni_uporabniki:
            if uporabnik.uporabnisko_ime == uporabnisko_ime:
                return uporabnik
        try:
            uporabnik = model.Uporabnik.vrniUporabnika(uporabnisko_ime)
            aktivni_uporabniki.append(uporabnik)
            return uporabnik
        except ValueError as e:
            bottle.redirect("/prijava/")
    else:
        bottle.redirect("/prijava/")

@bottle.post("/odjava/")
def odjava():
    uporabnisko_ime = bottle.request.get_cookie(PRIJAVA,  secret = SKRIVNOST)
    n = 0
    for uporabnik in aktivni_uporabniki:
        if uporabnik.uporabnisko_ime == uporabnisko_ime:
            aktivni_uporabniki.pop(n)
        n += 1
    bottle.response.delete_cookie(PRIJAVA, path="/")
    bottle.redirect("/")   

bottle.run()