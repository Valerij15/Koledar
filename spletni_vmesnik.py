import bottle
import model


@bottle.route('/')
def osnovna_stran():
    return bottle.template("osnovna_stran.html", mesec= model.poskus.datum.ime_meseca(), leto = model.poskus.datum.leto, tabela = model.poskus.koledar.tabela_datumov, vklopljen = model.poskus.koledar.vklopljen)

@bottle.get('/naslednji_mesec/')
def naslednji_mesec():
    model.poskus.koledar.vklopljen = 1
    model.poskus.koledar.dodaj_mesece(1)
    bottle.redirect("/")

@bottle.get('/prejsnji_mesec/')
def prejsnji_mesec():
    model.poskus.koledar.vklopljen = 1
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
    model.poskus.koledar.dodaj_dogodek(ime, model.poskus.koledar.tabela_datumov[model.poskus.koledar.vklopljen][0], opis)
    bottle.redirect("/")

bottle.run()