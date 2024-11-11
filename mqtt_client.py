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
    print(f"Conectado a MQTT con código de resultado: {rc}")
    if rc == 0:
        print("Conexión exitosa, suscribiendo al tema...")
        client.subscribe("test/topic")
    else:
        print(f"Error en conexión MQTT: {rc}")

def on_message(client, userdata, msg):
    global last_message_time
    print(f"Mensaje recibido en el tema {msg.topic}: {msg.payload.decode('utf-8')}")
    
    current_time = time.time()
    
    # Comprobar si han pasado 60 segundos desde el último mensaje
    if current_time - last_message_time >= 60:
        last_message_time = current_time
        try:
            # Procesar y mapear los datos
            data = json.loads(msg.payload.decode("utf-8"))
            data_mapped = {
                "flujo": data["flujo"],
                "frecuencia1": data.get("frecuencia", {}).get("valor1", None),
                "frecuencia2": data.get("frecuencia", {}).get("valor2", None),
                "lote1": data.get("lote", {}).get("valor1", None),
                "lote2": data.get("lote", {}).get("valor2", None),
                "repeticion1": data.get("repeticiones", {}).get("valor1", None),
                "repeticion2": data.get("repeticiones", {}).get("valor2", None),
                "porcentaje": data.get("porcentaje", None),
                "densidad": data.get("densidad", None),
                "a_y_sed": data.get("a_y_sed", None),
                "grabs_a": data.get("grabs_a", None),
                "peso_a": data.get("peso_a", None),
                "volumen_a": data.get("volumen_a", None),
                "grabs_b": data.get("grabs_b", None),
                "peso_b": data.get("peso_b", None),
                "volumen_b": data.get("volumen", None)
            }
            # Insertar en Supabase
            response = supabase.table("lecturas").insert(data_mapped).execute()

            # Verificar si hubo un error en la respuesta
            if response.error:
                print(f"Error al insertar datos en Supabase: {response.error}")
            else:
                print(f"Datos insertados exitosamente: {response.data}")
        except Exception as e:
            print(f"Error procesando el mensaje o insertando en Supabase: {e}")
    else:
        print("Mensaje ignorado, menos de 60 segundos desde el último mensaje.")

# Configuración del cliente MQTT
mqtt_client = mqtt.Client()

# Asignar las funciones de callback
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Establecer TLS con el certificado
mqtt_client.tls_set(ca_certs="certs/isrgrootx1.pem")

# Configurar credenciales y conexión
mqtt_client.username_pw_set("SuperRoot-99", "SuperRoot-99")
mqtt_client.connect("fee7a60180ef4e41a8186ff373e7ff32.s1.eu.hivemq.cloud", 8883)

# Iniciar el bucle del cliente MQTT
mqtt_client.loop_start()

# Mantener el proceso en ejecución para que el cliente MQTT siga funcionando
try:
    while True:
        time.sleep(1)  # Esperar mientras se reciben los mensajes
except KeyboardInterrupt:
    print("Cliente MQTT detenido.")
    mqtt_client.loop_stop()
