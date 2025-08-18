
from flask import Flask, render_template, abort
import json, os

app = Flask(__name__)

DATA_FILE = os.path.join('data', 'propiedades.json')

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def filtrar(tipo=None, estado=None):
    data = load_data()
    if tipo:
        data = [d for d in data if d.get('tipo') == tipo]
    if estado:
        data = [d for d in data if d.get('estado') == estado]
    return data

@app.route('/')
def home():
    data = load_data()
    destacados = [d for d in data if d.get('destacado')]
    destacados = destacados[:3]  # Solo 3 inmuebles destacados
    return render_template('index.html', destacados=destacados)

@app.route('/casas-nuevas')
def casas_nuevas():
    return render_template('listado.html', titulo='Casas nuevas', propiedades=filtrar('casa', 'nuevo'))

@app.route('/casas-usadas')
def casas_usadas():
    return render_template('listado.html', titulo='Casas usadas', propiedades=filtrar('casa', 'usado'))

@app.route('/apartamentos-nuevos')
def apartamentos_nuevos():
    return render_template('listado.html', titulo='Apartamentos nuevos', propiedades=filtrar('apartamento', 'nuevo'))

@app.route('/apartamentos-usados')
def apartamentos_usados():
    return render_template('listado.html', titulo='Apartamentos usados', propiedades=filtrar('apartamento', 'usado'))

@app.route('/propiedad/<int:pid>')
def detalle_propiedad(pid):
    p = next((x for x in load_data() if x.get('id') == pid), None)
    if not p:
        abort(404)
    return render_template('detalle.html', p=p)

@app.route('/reduccion-credito')
def reduccion_credito():
    return render_template('reduccion.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
