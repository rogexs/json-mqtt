const options = {
    protocol: 'wss',
    clientId: 'mqttjs_' + Math.random().toString(16).substr(2, 8),
    username: 'SuperRoot-99',
    password: 'SuperRoot-99',
};

const client = mqtt.connect('wss://fee7a60180ef4e41a8186ff373e7ff32.s1.eu.hivemq.cloud:8884/mqtt', options);

client.on('connect', () => {
    console.log('Conectado al broker');
    client.subscribe('test/topic', (err) => {
        if (!err) {
            console.log('Suscrito al tópico');
        } else {
            console.error('Error al suscribirse:', err);
        }
    });
});

client.on('message', (topic, message) => {
    const data = JSON.parse(message.toString());

    document.getElementById('flujo').textContent = data.flujo;
    document.getElementById('frecuencia1').textContent = data.frecuencia.valor1;
    document.getElementById('frecuencia2').textContent = data.frecuencia.valor2;
    document.getElementById('lote1').textContent = data.lote.valor1;
    document.getElementById('lote2').textContent = data.lote.valor2;
    document.getElementById('repeticion1').textContent = data.repeticiones.valor1;
    document.getElementById('repeticion2').textContent = data.repeticiones.valor2;
    document.getElementById('porcentaje').textContent = data.porcentaje;
    document.getElementById('densidad').textContent = data.densidad;
    document.getElementById('a_y_sed').textContent = data.a_y_sed;
    document.getElementById('grabs_a').textContent = data.grabs_a;
    document.getElementById('peso_a').textContent = data.peso_a;
    document.getElementById('volumen_a').textContent = data.volumen_a;
    document.getElementById('grabs_b').textContent = data.grabs_b;
    document.getElementById('peso_b').textContent = data.peso_b;
    document.getElementById('volumen_b').textContent = data.volumen;
});

client.on('error', (err) => {
    console.error('Error de conexión:', err);
});
