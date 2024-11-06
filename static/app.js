// app.js

// Función para obtener los datos más recientes de la API
async function obtenerDatos() {
    try {
        const response = await fetch('https://json-mqtt.onrender.com/lecturas');
        if (!response.ok) {
            throw new Error(`Error del servidor: ${response.status}`);
        }
        const data = await response.json();

        if (data.length > 0) {
            // Muestra el último dato y actualiza directamente los valores en la página
            const lecturasRecientes = data[data.length - 1];

            const elementos = {
                flujo: 'flujo',
                frecuencia1: 'frecuencia1',
                frecuencia2: 'frecuencia2',
                lote1: 'lote1',
                lote2: 'lote2',
                repeticion1: 'repeticion1',
                repeticion2: 'repeticion2',
                porcentaje: 'porcentaje',
                densidad: 'densidad',
                a_y_sed: 'a_y_sed',
                grabs_a: 'grabs_a',
                peso_a: 'peso_a',
                volumen_a: 'volumen_a',
                grabs_b: 'grabs_b',
                peso_b: 'peso_b',
                volumen_b: 'volumen_b'
            };

            for (const [key, id] of Object.entries(elementos)) {
                document.getElementById(id).textContent = lecturasRecientes[key] || '-';
            }
        } else {
            mostrarError("No hay datos recientes disponibles.");
        }
    } catch (error) {
        console.error("Error al obtener los datos:", error);
        mostrarError("Error al conectar con el servidor.");
    }
}

// Función para mostrar errores en la interfaz
function mostrarError(mensaje) {
    const errorDiv = document.getElementById('error-notification');
    errorDiv.textContent = mensaje;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000); // Desaparece en 5 segundos
}

// Modificación en fetchLecturas para manejar errores
async function fetchLecturas() {
    try {
        const response = await fetch('http://localhost:5000/lecturas');
        if (!response.ok) {
            throw new Error(`Error del servidor: ${response.status}`);
        }
        const data = await response.json();
        // Actualiza la tabla solo si hay datos
        if (data.length) {
            llenarTabla(data);
        } else {
            mostrarError("No se encontraron datos en la base de datos.");
        }
    } catch (error) {
        console.error('Error al obtener los datos:', error);
        mostrarError("Error al conectar con el servidor.");
    }
}

// Llama a la función cada 5 segundos para actualizar los datos en tiempo real
setInterval(obtenerDatos, 5000); 
document.addEventListener('DOMContentLoaded', obtenerDatos);
