import bottle
import model


@bottle.route('/')
def osnovna_stran():
    return bottle.template("osnovna_stran.html", stevilo_dni = model.poskus.stevilo_dni_v_mesecu(), zacetek_meseca = model.poskus.zacetek_meseca())

@bottle.get('/naslednji_mesec/')
def naslednji_mesec():
    model.poskus.dodaj_mesece(1)
    bottle.redirect("/")

@bottle.get('/prejsnji_mesec/')
def prejsnji_mesec():
    model.poskus.dodaj_mesece(-1)
    bottle.redirect("/")

bottle.run(debugger= True)