from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from supabase import create_client, Client

# Configuración de Supabase
supabase_url = "https://qiuemjqtqiyyxumrkdga.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFpdWVtanF0cWl5eXh1bXJrZGdhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjczODgyMDMsImV4cCI6MjA0Mjk2NDIwM30.9R7O3A_sVy01z6OgjseBxxks5J5CdVlYnyffAiEV3So"

supabase: Client = create_client(supabase_url, supabase_key)

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

@app.route('/lecturas', methods=['GET'])
def get_lecturas():
    try:
        # Validar y obtener parámetros offset y limit
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 20))

        if offset < 0 or limit <= 0:
            return jsonify({"error": "Parámetros inválidos"}), 400

        # Consulta a Supabase con rango y orden explícito
        response = supabase.table("lecturas").select("*").order("id", asc=True).range(offset, offset + limit - 1).execute()

        if response.error:
            return jsonify({"error": response.error.message}), 500

        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ejecutar la app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
