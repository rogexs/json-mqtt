import time
import json
from supabase import create_client, Client
import paho.mqtt.client as mqtt
from flask import Flask, jsonify, render_template
from flask_cors import CORS

# URL y clave API anónima de Supabase
supabase_url = "https://qiuemjqtqiyyxumrkdga.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFpdWVtanF0cWl5eXh1bXJrZGdhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjczODgyMDMsImV4cCI6MjA0Mjk2NDIwM30.9R7O3A_sVy01z6OgjseBxxks5J5CdVlYnyffAiEV3So"

# Crear cliente de Supabase
supabase: Client = create_client(supabase_url, supabase_key)

# Crear la aplicación Flask
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Habilita CORS para todas las rutas

# Ruta para la página de inicio, renderizando el archivo index.html
@app.route('/')
def index():
    return render_template('index.html')  # Servir el archivo index.html desde templates/

@app.route('/registros')
def registros():
    return render_template('registros.html')


# Ruta para obtener los datos de la tabla 'lecturas'
@app.route('/lecturas', methods=['GET'])
def get_lecturas():
    try:
        # Obtenemos todas las lecturas en una sola consulta
        response = supabase.table("lecturas").select("*").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Función para manejar la conexión a MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado a MQTT con código de resultado:", rc)
    client.subscribe("test/topic")

# Función para manejar los mensajes recibidos
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        data_mapped = {
            "flujo": data["flujo"],
            "frecuencia1": data["frecuencia"]["valor1"],
            "frecuencia2": data["frecuencia"]["valor2"],
            "lote1": data["lote"]["valor1"],
            "lote2": data["lote"]["valor2"],
            "repeticion1": data["repeticiones"]["valor1"],
            "repeticion2": data["repeticiones"]["valor2"],
            "porcentaje": data["porcentaje"],
            "densidad": data["densidad"],
            "a_y_sed": data["a_y_sed"],
            "grabs_a": data["grabs_a"],
            "peso_a": data["peso_a"],
            "volumen_a": data["volumen_a"],
            "grabs_b": data["grabs_b"],
            "peso_b": data["peso_b"],
            "volumen_b": data["volumen"]
        }

        # Insertar los datos en Supabase
        supabase.table("lecturas").insert(data_mapped).execute()
        print("Datos insertados en Supabase:", data_mapped)
    except Exception as e:
        print("Error al insertar datos en Supabase:", e)

# Configuración del cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.tls_set(ca_certs="/home/roge/Documents/isrgrootx1.pem")
mqtt_client.username_pw_set("SuperRoot-99", "SuperRoot-99")
mqtt_client.connect("fee7a60180ef4e41a8186ff373e7ff32.s1.eu.hivemq.cloud", 8883)

# Iniciar el cliente MQTT en segundo plano
mqtt_client.loop_start()

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
