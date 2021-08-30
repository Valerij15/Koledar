import bottle
import model


@bottle.route('/')
def osnovna_stran():
    return bottle.template("osnovna_stran.html", mesec= model.poskus.ime_meseca(), leto = model.poskus.leto, tabela = model.poskus.tabela_datumov)

@bottle.get('/naslednji_mesec/')
def naslednji_mesec():
    model.poskus.dodaj_mesece(1)
    bottle.redirect("/")

@bottle.get('/prejsnji_mesec/')
def prejsnji_mesec():
    model.poskus.dodaj_mesece(-1)
    bottle.redirect("/")

bottle.run(debugger= True)