import React, { useState, useEffect } from 'react';
import api from '../services/api';

const ModuloAsignarDerechos = () => {
    const [personas, setPersonas] = useState([]);
    const [derechos, setDerechos] = useState([]);
    const [personaSeleccionada, setPersonaSeleccionada] = useState('');
    const [derechoSeleccionado, setDerechoSeleccionado] = useState('');
    const [fechaInicio, setFechaInicio] = useState(''); // Campo para fecha de inicio
    const [fechaFin, setFechaFin] = useState(''); // Campo para fecha de fin
    const [mensaje, setMensaje] = useState(''); // Mensajes de feedback

    // Obtener las personas desde el backend
    const fetchPersonas = async () => {
        try {
            const response = await api.get('/personas');
            setPersonas(response.data);
        } catch (error) {
            console.error('Error al cargar personas:', error);
            setMensaje('Hubo un problema al cargar la lista de personas.');
        }
    };

    // Obtener los derechos desde el backend
    const fetchDerechos = async () => {
        try {
            const response = await api.get('/derechos');
            setDerechos(response.data);
        } catch (error) {
            console.error('Error al cargar derechos:', error);
            setMensaje('Hubo un problema al cargar la lista de derechos.');
        }
    };

    // Asignar derecho a la persona seleccionada
    const asignarDerecho = async () => {
        if (!personaSeleccionada || !derechoSeleccionado || !fechaInicio) {
            setMensaje('Por favor, completa todos los campos obligatorios.');
            return;
        }

        try {
            await api.post('/persona_derecho', {
                ID_Persona: personaSeleccionada,
                ID_Derecho: derechoSeleccionado,
                Fecha_Inicio: fechaInicio,
                Fecha_Fin: fechaFin || null, // Opcional
            });

            setMensaje('¡Derecho asignado exitosamente!');
            setPersonaSeleccionada('');
            setDerechoSeleccionado('');
            setFechaInicio('');
            setFechaFin('');
        } catch (error) {
            console.error('Error al asignar derecho:', error);
            if (error.response && error.response.data.errores) {
                setMensaje(error.response.data.errores.join(', ')); // Mostrar errores del backend
            } else {
                setMensaje('Hubo un problema al asignar el derecho. Por favor, verifica los datos.');
            }
        }
    };

    useEffect(() => {
        fetchPersonas();
        fetchDerechos();
    }, []);

    return (
        <div className="container mt-4">
            <h3 className="mb-4">Módulo de Asignación de Derechos</h3>
            <div className="form-group">
                <label htmlFor="persona">Seleccionar Persona:</label>
                <select
                    id="persona"
                    className="form-control mb-3"
                    value={personaSeleccionada}
                    onChange={(e) => setPersonaSeleccionada(e.target.value)}
                >
                    <option value="">-- Selecciona una persona --</option>
                    {personas.map((persona) => (
                        <option key={persona.ID_Persona} value={persona.ID_Persona}>
                            {persona.Nombre} (DPI: {persona.DPI})
                        </option>
                    ))}
                </select>
            </div>
            <div className="form-group">
                <label htmlFor="derecho">Seleccionar Derecho:</label>
                <select
                    id="derecho"
                    className="form-control mb-3"
                    value={derechoSeleccionado}
                    onChange={(e) => setDerechoSeleccionado(e.target.value)}
                >
                    <option value="">-- Selecciona un derecho --</option>
                    {derechos.map((derecho) => (
                        <option key={derecho.ID_Derecho} value={derecho.ID_Derecho}>
                            {derecho.Nombre}
                        </option>
                    ))}
                </select>
            </div>

            {/* Campos para las fechas */}
            <div className="form-group">
                <label htmlFor="fechaInicio">Fecha de Inicio:</label>
                <input
                    type="date"
                    id="fechaInicio"
                    className="form-control mb-3"
                    value={fechaInicio}
                    onChange={(e) => setFechaInicio(e.target.value)}
                />
            </div>
            <div className="form-group">
                <label htmlFor="fechaFin">Fecha de Fin:</label>
                <input
                    type="date"
                    id="fechaFin"
                    className="form-control mb-3"
                    value={fechaFin}
                    onChange={(e) => setFechaFin(e.target.value)}
                />
            </div>

            {mensaje && (
                <div
                    className={`alert ${mensaje.includes('exitosamente') ? 'alert-success' : 'alert-danger'}`}
                    role="alert"
                >
                    {mensaje}
                </div>
            )}
            <button className="btn btn-primary" onClick={asignarDerecho}>
                Asignar Derecho
            </button>
        </div>
    );
};

export default ModuloAsignarDerechos;