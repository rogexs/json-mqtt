# mqtt_client.py
import time
import json
from supabase import create_client
import paho.mqtt.client as mqtt

# URL y clave API de Supabase
supabase_url = "https://qiuemjqtqiyyxumrkdga.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFpdWVtanF0cWl5eXh1bXJrZGdhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjczODgyMDMsImV4cCI6MjA0Mjk2NDIwM30.9R7O3A_sVy01z6OgjseBxxks5J5CdVlYnyffAiEV3So"

# Crear cliente de Supabase
supabase = create_client(supabase_url, supabase_key)

# Variable para manejar el intervalo
last_message_time = 0

# Funciones MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado a MQTT:", rc)
    client.subscribe("test/topic")

def on_message(client, userdata, msg):
    global last_message_time
    current_time = time.time()
    
    if current_time - last_message_time >= 60:
        last_message_time = current_time
        try:
            data = json.loads(msg.payload.decode("utf-8"))
            data_mapped = {
                "flujo": data["flujo"],
                # Mapeo de datos...
            }
            supabase.table("lecturas").insert(data_mapped).execute()
            print("Datos insertados:", data_mapped)
        except Exception as e:
            print("Error en Supabase:", e)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.tls_set(ca_certs="certs/isrgrootx1.pem")
mqtt_client.username_pw_set("SuperRoot-99", "SuperRoot-99")
mqtt_client.connect("fee7a60180ef4e41a8186ff373e7ff32.s1.eu.hivemq.cloud", 8883)
mqtt_client.loop_start()
