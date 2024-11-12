let limite = 50; // Número de registros a cargar
let offset = 0; // Desplazamiento inicial
const apiUrl = 'https://json-mqtt.onrender.com/lecturas'; // URL de la API

// Función para obtener datos de la API con paginación
async function fetchLecturas() {
    try {
        const response = await fetch(`${apiUrl}?limite=${limite}&offset=${offset}`);
        if (!response.ok) {
            throw new Error(`Error del servidor: ${response.status}`);
        }

        const data = await response.json();
        const tableBody = document.getElementById('lecturas-table');

        if (data.length) {
            data.forEach(reading => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${reading.id || '-'}</td>
                    <td>${reading.flujo || '-'}</td>
                    <td>${reading.frecuencia1 || '-'}</td>
                    <td>${reading.frecuencia2 || '-'}</td>
                    <td>${reading.lote1 || '-'}</td>
                    <td>${reading.lote2 || '-'}</td>
                    <td>${reading.repeticion1 || '-'}</td>
                    <td>${reading.repeticion2 || '-'}</td>
                    <td>${reading.porcentaje || '-'}</td>
                    <td>${reading.densidad || '-'}</td>
                    <td>${reading.a_y_sed || '-'}</td>
                    <td>${reading.grabs_a || '-'}</td>
                    <td>${reading.peso_a || '-'}</td>
                    <td>${reading.volumen_a || '-'}</td>
                    <td>${reading.grabs_b || '-'}</td>
                    <td>${reading.peso_b || '-'}</td>
                    <td>${reading.volumen_b || '-'}</td>
                `;
                tableBody.appendChild(row);
            });

            offset += limite; // Incrementar el desplazamiento
        } else {
            mostrarError("No hay más datos para cargar.");
            document.getElementById('cargar-mas').disabled = true; // Deshabilitar el botón
        }
    } catch (error) {
        console.error('Error al obtener los datos:', error);
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

// Evento para cargar más registros
document.getElementById('cargar-mas').addEventListener('click', fetchLecturas);

// Cargar datos iniciales al cargar la página
document.addEventListener('DOMContentLoaded', fetchLecturas);
