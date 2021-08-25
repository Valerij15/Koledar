import bottle
import model


@bottle.route('/')
def osnovna_stran():
    return bottle.template("osnovna_stran.html", stevilo_dni = model.poskus.stevilo_dni_v_mesecu(), zacetek_meseca = model.poskus.zacetek_meseca())

bottle.run(debugger= True)