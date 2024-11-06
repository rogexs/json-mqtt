// lecturas.js

// Función para obtener los datos de la API y llenar la tabla
async function fetchLecturas() {
    try {
        const response = await fetch('http://localhost:5000/lecturas');
        if (!response.ok) {
            throw new Error(`Error del servidor: ${response.status}`);
        }

        const data = await response.json();
        const tableBody = document.getElementById('lecturas-table');
        tableBody.innerHTML = ''; // Limpia el contenido existente

        if (data.length) {
            data.forEach(reading => {
                const row = document.createElement('tr');

                // Especificar el orden de los datos en la fila
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
        } else {
            mostrarError("No se encontraron datos en la base de datos.");
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

// Llama a fetchLecturas al cargar la página y actualiza la tabla cada 10 segundos
document.addEventListener('DOMContentLoaded', fetchLecturas);
setInterval(fetchLecturas, 10000);
