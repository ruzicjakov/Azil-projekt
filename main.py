from flask import Flask,jsonify,request,make_response,render_template, Blueprint, redirect, url_for
from pony import orm
import datetime

app = Flask(__name__)

baza = orm.Database()
baza.bind(provider='sqlite', filename='baza.sqlite', create_db=True)

class Pas(baza.Entity):
    id_pas=orm.PrimaryKey(int, auto=True)
    pasmina=orm.Required(str)
    dob=orm.Required(str)
    spol=orm.Required(str)
    ime=orm.Required(str)
    boja=orm.Required(str)
    datum_dolaska = orm.Required(datetime.date)
    zdravstveno_stanje=orm.Optional(str)
    tezina=orm.Required(float)

baza.generate_mapping(create_tables=True)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/dodavanje', methods=["POST", "GET"])
def dodavanje():
    if request.method == "POST":
        try:
            with orm.db_session:
                novi = Pas(
                    pasmina=request.form['pasmina'],
                    dob=request.form['dob'],
                    spol=request.form['spol'],
                    ime=request.form['ime'],
                    boja=request.form['boja'],
                    datum_dolaska=datetime.datetime.strptime(request.form['datum_dolaska'], '%Y-%m-%d'),
                    zdravstveno_stanje=request.form['zdravstveno_stanje'],
                    tezina=float(request.form['tezina'])
                )
                orm.commit()
            return redirect(url_for('home'))
        except Exception as e:
            response = {"message": "Greška prilikom dodavanja psa: " + str(e)}
            return make_response(jsonify(response), 404)
    else:
        return render_template("dodaj_psa.html")

@app.route('/dostupni', methods=["GET"])
def dostupni():
    with orm.db_session:
        psi = Pas.select()
        lista_pasa = []
        for pas in psi:
            pas_dict = {
                'id_pas': pas.id_pas,
                'pasmina': pas.pasmina,
                'dob': pas.dob,
                'spol': pas.spol,
                'ime': pas.ime,
                'boja': pas.boja,
                'datum_dolaska': pas.datum_dolaska.strftime('%Y-%m-%d'),
                'zdravstveno_stanje': pas.zdravstveno_stanje,
                'tezina': pas.tezina
            }
            lista_pasa.append(pas_dict)
    return render_template('dostupni_psi.html', psi=lista_pasa)

@app.route('/izmjena/<int:id_pas>', methods=["POST", "GET"])
@orm.db_session
def izmjena(id_pas):
    pas_update = Pas.get(id_pas=id_pas)
    if not pas_update:
        return "Pas nije pronađen", 404

    if request.method == "POST":
        try:
            pas_update.pasmina = request.form['pasmina']
            pas_update.dob = request.form['dob']
            pas_update.spol = request.form['spol']
            pas_update.ime = request.form['ime']
            pas_update.boja = request.form['boja']
            pas_update.datum_dolaska = datetime.datetime.strptime(request.form['datum_dolaska'], '%Y-%m-%d').date()
            pas_update.zdravstveno_stanje = request.form['zdravstveno_stanje']
            pas_update.tezina = float(request.form['tezina'])
            orm.commit()
            return redirect(url_for('dostupni'))
        except orm.TransactionIntegrityError:
            return "Izmjena nije moguća"
    return render_template('izmjena.html', pas_update=pas_update)


@app.route('/brisanje/<int:id_pas>', methods=["POST"])
@orm.db_session
def brisanje(id_pas):
    pas = Pas.get(id_pas=id_pas)
    if pas:
        pas.delete()
        orm.commit()
        return redirect(url_for('dostupni'))
    else:
        response = {"message": "Pas s navedenim ID-em nije pronađen."}
        return jsonify(response), 404




if __name__=="__main__":
    app.run(debug=True,port=8080)