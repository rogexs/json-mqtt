let offset = 0; // Controla el desplazamiento de la consulta
const limit = 20; // Cantidad de registros a cargar por solicitud
let isLoading = false; // Evita solicitudes concurrentes

// Función para obtener datos paginados y llenar la tabla
async function fetchLecturas() {
    if (isLoading) return; // Evita múltiples solicitudes al mismo tiempo
    isLoading = true;

    try {
        const response = await fetch(`/lecturas?offset=${offset}&limit=${limit}`);
        if (!response.ok) {
            throw new Error(`Error del servidor: ${response.status}`);
        }

        const data = await response.json();
        if (data.length > 0) {
            llenarTabla(data);
            offset += limit; // Incrementa el desplazamiento
        } else {
            mostrarMensaje("No hay más datos para cargar.");
        }
    } catch (error) {
        console.error('Error al obtener los datos:', error);
        mostrarMensaje("Error al conectar con el servidor.");
    } finally {
        isLoading = false;
    }
}

// Función para llenar la tabla con datos
function llenarTabla(datos) {
    const tableBody = document.getElementById('lecturas-table');
    datos.forEach(reading => {
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
}

// Función para mostrar mensajes
function mostrarMensaje(mensaje) {
    const errorDiv = document.getElementById('error-notification');
    errorDiv.textContent = mensaje;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// Detecta el scroll para cargar más datos
window.addEventListener('scroll', () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        fetchLecturas();
    }
});

// Carga inicial
document.addEventListener('DOMContentLoaded', fetchLecturas);
