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

@app.route('/lecturas', methods=['GET'])
def get_lecturas():
    try:
        # Validar parámetros offset y limit
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 20))

        if offset < 0 or limit <= 0:
            return jsonify({"error": "Parámetros inválidos"}), 400

        # Consulta a Supabase
        response = supabase.table("lecturas").select("*").order("id", asc=True).range(offset, offset + limit - 1).execute()

        if response.error:
            return jsonify({"error": response.error.message}), 500

        return jsonify(response.data), 200 if response.data else jsonify([]), 200
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500


# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
