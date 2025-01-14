#python3 --version

#pip install virtualenv
##python -m venv apivenv
##apivenv\Scripts\activate

#pip intall Flask

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return "Mi Rest API"



#GET
@app.route("/usuario/<id>", methods=['GET'])
def obtener_usuario(id):
    usuario =  {
        "id": id,
        "nombre": "NombrePrueba",
        "apellido": "ApellidoPrueba"
    }

    #/usuario/11143?q=test

    datos = request.args.get('q')
    if datos:
        usuario["ParametroDinamicoPorURL"] = datos

    return jsonify(usuario), 200


#POST
@app.route("/usuario/<id>", methods=['POST'])
def crear_usuario():
    datos = request.get_json()
    datos['estado'] = 'creado'
    return jsonify(datos), 200


#PUT



if __name__ == '__main__':
    app.run(debug=True) 


