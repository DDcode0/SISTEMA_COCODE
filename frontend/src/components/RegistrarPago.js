import React, { useState, useEffect } from 'react';
import api from '../services/api';

const RegistrarPago = () => {
    const [personas, setPersonas] = useState([]);
    const [cuotas, setCuotas] = useState([]);
    const [personaSeleccionada, setPersonaSeleccionada] = useState('');
    const [cuotaSeleccionada, setCuotaSeleccionada] = useState('');
    const [monto, setMonto] = useState('');
    const [fechaPago, setFechaPago] = useState('');
    const [montoRestante, setMontoRestante] = useState(0);
    const [estadoCuota, setEstadoCuota] = useState('');
    const [mensaje, setMensaje] = useState('');

    // Obtener datos iniciales desde el backend
    useEffect(() => {
        api.get('/personas').then(response => setPersonas(response.data));
        api.get('/cuotas').then(response => setCuotas(response.data));
    }, []);

    // Calcular el monto restante y el estado de la cuota al seleccionar una cuota
    useEffect(() => {
        if (cuotaSeleccionada && personaSeleccionada) {
            api.get(`/pagos/cuota/${cuotaSeleccionada}?ID_Persona=${personaSeleccionada}`).then(response => {
                const cuota = response.data;
                setMontoRestante(cuota.MontoRestante);
                setEstadoCuota(cuota.Estado);
            }).catch(() => {
                setMontoRestante(0);
                setEstadoCuota('Pendiente');
            });
        }
    }, [cuotaSeleccionada, personaSeleccionada]);

    const registrarPago = () => {
        if (!personaSeleccionada || !cuotaSeleccionada || !monto || !fechaPago) {
            setMensaje('Por favor, completa todos los campos.');
            return;
        }

        api.post('/pagos', {
            ID_Persona: personaSeleccionada,
            ID_Cuota: cuotaSeleccionada,
            Monto_Pagado: parseFloat(monto),
            Fecha_Pago: fechaPago
        }).then(() => {
            setMensaje('Pago registrado exitosamente.');
            api.get(`/pagos/cuota/${cuotaSeleccionada}?ID_Persona=${personaSeleccionada}`).then(response => {
                const cuota = response.data;
                setMontoRestante(cuota.MontoRestante);
                setEstadoCuota(cuota.Estado);
            });
            setMonto('');
            setFechaPago('');
        }).catch(error => {
            const errores = error.response?.data?.errores || ['Error al registrar el pago.'];
            setMensaje(errores.join(', '));
        });
    };

    return (
        <div className="container mt-4">
            <h3>Registrar Pago</h3>
            <div className="form-group">
                <label htmlFor="persona">Seleccionar Persona:</label>
                <select
                    id="persona"
                    className="form-control mb-3"
                    value={personaSeleccionada}
                    onChange={(e) => setPersonaSeleccionada(e.target.value)}
                >
                    <option value="">-- Seleccione una persona --</option>
                    {personas.map(persona => (
                        <option key={persona.ID_Persona} value={persona.ID_Persona}>
                            {persona.Nombre} (DPI: {persona.DPI})
                        </option>
                    ))}
                </select>
            </div>
            <div className="form-group">
                <label htmlFor="cuota">Seleccionar Cuota:</label>
                <select
                    id="cuota"
                    className="form-control mb-3"
                    value={cuotaSeleccionada}
                    onChange={(e) => setCuotaSeleccionada(e.target.value)}
                >
                    <option value="">-- Seleccione una cuota --</option>
                    {cuotas.map(cuota => (
                        <option key={cuota.ID_Cuota} value={cuota.ID_Cuota}>
                            {cuota.Descripcion} - Q{cuota.Monto}
                        </option>
                    ))}
                </select>
            </div>
            <div className="form-group">
                <p className="text-info">Monto restante: Q{montoRestante}</p>
                <p className="text-info">Estado de la cuota: {estadoCuota}</p>
            </div>
            <div className="form-group">
                <label htmlFor="monto">Monto a Pagar:</label>
                <input
                    type="number"
                    id="monto"
                    className="form-control mb-3"
                    value={monto}
                    onChange={(e) => setMonto(e.target.value)}
                />
            </div>
            <div className="form-group">
                <label htmlFor="fechaPago">Fecha de Pago:</label>
                <input
                    type="date"
                    id="fechaPago"
                    className="form-control mb-3"
                    value={fechaPago}
                    onChange={(e) => setFechaPago(e.target.value)}
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
            <button className="btn btn-primary" onClick={registrarPago}>
                Registrar Pago
            </button>
        </div>
    );
};

export default RegistrarPago;