import subprocess
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from supabase import create_client, Client

# URL y clave API anónima de Supabase
supabase_url = "https://qiuemjqtqiyyxumrkdga.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFpdWVtanF0cWl5eXh1bXJrZGdhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjczODgyMDMsImV4cCI6MjA0Mjk2NDIwM30.9R7O3A_sVy01z6OgjseBxxks5J5CdVlYnyffAiEV3So"

# Crear cliente de Supabase
supabase: Client = create_client(supabase_url, supabase_key)

# Crear la aplicación Flask
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Habilita CORS para todas las rutas

# Ejecutar mqtt_client.py como un proceso separado
subprocess.Popen(["python3", "mqtt_client.py"])

# Ruta para la página de inicio, renderizando el archivo index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registros')
def registros():
    return render_template('registros.html')

# Ruta para obtener los datos de la tabla 'lecturas' con paginación
@app.route('/lecturas', methods=['GET'])
def get_lecturas():
    try:
        limite = int(request.args.get('limite', 50))  # Límite predeterminado
        offset = int(request.args.get('offset', 0))  # Desplazamiento inicial

        # Consulta paginada a la tabla 'lecturas'
        response = supabase.table("lecturas").select("*").range(offset, offset + limite - 1).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
