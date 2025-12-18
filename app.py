from flask import Flask, request, jsonify
app = Flask(__name__)

torneos = []
servicios = []

@app.route("/registrar-torneo", methods=["POST"])
def registrar_torneo():
    data = request.json
    torneos.append(data)
    return jsonify({"message": "Registro de torneo recibido correctamente!"})

@app.route("/registrar-servicio", methods=["POST"])
def registrar_servicio():
    data = request.json
    servicios.append(data)
    return jsonify({"message": "Solicitud de servicio recibida correctamente!"})

@app.route("/registros-torneos")
def registros_torneos():
    return jsonify(torneos)

@app.route("/registros-servicios")
def registros_servicios():
    return jsonify(servicios)

if __name__ == "__main__":
    app.run(debug=True)