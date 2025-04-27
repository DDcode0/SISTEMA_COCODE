import React, { useState } from 'react';
import api from '../services/api';

const BuscarPersonas = ({ setPersonasConDerechos }) => {
    const [nombre, setNombre] = useState('');
    const [dpi, setDpi] = useState('');
    const [derecho, setDerecho] = useState('');

    const buscarPersonas = () => {
        const params = new URLSearchParams();
        if (nombre) params.append('Nombre', nombre);
        if (dpi) params.append('DPI', dpi);
        if (derecho) params.append('Derecho', derecho);

        api.get(`/persona_derecho/detalle_combinado?${params.toString()}`)
            .then(response => setPersonasConDerechos(response.data))
            .catch(() => console.error('Error al buscar personas.'));
    };

    const handleKeyDown = (event) => {
        if (event.key === 'Tab') {
            event.preventDefault(); // Evitar el cambio de foco
            buscarPersonas(); // Ejecutar la búsqueda
        }
    };

    const limpiarFiltros = () => {
        setNombre('');
        setDpi('');
        setDerecho('');
        api.get('/persona_derecho/detalle_combinado') // Requerir todos los datos nuevamente
            .then(response => setPersonasConDerechos(response.data))
            .catch(() => console.error('Error al cargar todos los datos.'));
    };

    return (
        <div className="mb-4">
            <h5>Buscar Personas</h5>
            <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
                <input
                    type="text"
                    placeholder="Nombre"
                    value={nombre}
                    onChange={(e) => setNombre(e.target.value)}
                    onKeyDown={handleKeyDown}
                    className="form-control"
                />
                <input
                    type="text"
                    placeholder="DPI"
                    value={dpi}
                    onChange={(e) => setDpi(e.target.value)}
                    onKeyDown={handleKeyDown}
                    className="form-control"
                />
                <input
                    type="text"
                    placeholder="Derecho"
                    value={derecho}
                    onChange={(e) => setDerecho(e.target.value)}
                    onKeyDown={handleKeyDown}
                    className="form-control"
                />
                <button onClick={buscarPersonas} className="btn btn-primary">Buscar</button>
                <button onClick={limpiarFiltros} className="btn btn-secondary">Limpiar Filtros</button>
            </div>
        </div>
    );
};

export default BuscarPersonas;