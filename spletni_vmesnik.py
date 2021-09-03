import bottle
import model


@bottle.route('/')
def osnovna_stran():
    return bottle.template("osnovna_stran.html", mesec= model.poskus.datum.ime_meseca(), leto = model.poskus.datum.leto, tabela = model.poskus.koledar.tabela_datumov, vklopljen = model.poskus.koledar.vklopljen)

@bottle.get('/naslednji_mesec/')
def naslednji_mesec():
    model.poskus.koledar.vklopljen = 0
    model.poskus.koledar.dodaj_mesece(1)
    bottle.redirect("/")

@bottle.get('/prejsnji_mesec/')
def prejsnji_mesec():
    model.poskus.koledar.vklopljen = 0
    model.poskus.koledar.dodaj_mesece(-1)
    bottle.redirect("/")

@bottle.get('/vklopi<i>/')
def vklopi(i):
    model.poskus.koledar.preklopi(int(i))
    bottle.redirect("/")

@bottle.post('/dodaj_dogodek/')
def dodaj_dogodek():
    ime = bottle.request.forms.getunicode('ime_dogodka')
    opis = bottle.request.forms.getunicode('opis_dogodka')
    datumod = bottle.request.forms.getunicode('datumod')
    datumdo = bottle.request.forms.getunicode('datumdo')
    model.poskus.koledar.dodaj_dogodek(ime, model.poskus.koledar.oblikuj_datum(datumod),model.poskus.koledar.oblikuj_datum(datumdo), opis)
    bottle.redirect("/")

@bottle.get('/izbrisi_dogodek<i>/')
def izbrisi_dogodek(i):
    model.poskus.koledar.izbrisi_dogodek(i)
    bottle.redirect("/")

bottle.run()