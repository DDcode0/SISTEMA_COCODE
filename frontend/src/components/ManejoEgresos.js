import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Egresos = () => {
    const [egresos, setEgresos] = useState([]);
    const [fondosDisponibles, setFondosDisponibles] = useState(0); // Estado para fondos disponibles
    const [nuevoEgreso, setNuevoEgreso] = useState({
        Fecha: '',
        Monto: '',
        Descripcion: ''
    });
    const [mensaje, setMensaje] = useState('');

    // Obtener la lista de egresos y los fondos disponibles desde el backend
    useEffect(() => {
        cargarEgresos();
        cargarFondosDisponibles();
    }, []);

    const cargarEgresos = () => {
        api.get('/egresos')
            .then(response => setEgresos(response.data))
            .catch(() => setMensaje('Error al cargar los egresos.'));
    };

    const cargarFondosDisponibles = () => {
        api.get('/fondos/disponibles')
            .then(response => {
                const fondos = response.data.fondos_disponibles;
                setFondosDisponibles(fondos); // Verifica que fondos sea un número
            })
            .catch(() => setMensaje('Error al calcular los fondos disponibles.'));
    };
    

    // Manejar el envío del formulario
    const manejarEnvio = (e) => {       
        e.preventDefault();
        if (!nuevoEgreso.Fecha || !nuevoEgreso.Monto || !nuevoEgreso.Descripcion) {
            setMensaje('Por favor completa todos los campos obligatorios.');
            return;
        }

        api.post('/egresos', nuevoEgreso)
            .then(() => {
                setMensaje('Egreso creado exitosamente.');
                setNuevoEgreso({ Fecha: '', Monto: '', Descripcion: '' });
                cargarEgresos(); // Actualizar la lista de egresos
                cargarFondosDisponibles(); // Actualizar los fondos disponibles
            })
            .catch((error) => {
                setMensaje(error.response?.data?.errores.join(', ') || 'Error al registrar el egreso.');
            });
    };

    // Manejar cambios en el formulario
    const manejarCambio = (e) => {
        const { name, value } = e.target;
        setNuevoEgreso({
            ...nuevoEgreso,
            [name]: name === 'Monto' ? parseFloat(value) || '' : value // Convertir Monto a número
        });
    };

    return (
        <div className="container mt-4">
            <h3>Gestión de Egresos</h3>
            {mensaje && (
                <div className={`alert ${mensaje.includes('exitosamente') ? 'alert-success' : 'alert-danger'}`} role="alert">
                    {mensaje}
                </div>
            )}
            <form onSubmit={manejarEnvio}>
                <div className="form-group">
                    <label htmlFor="Fecha">Fecha:</label>
                    <input
                        type="date"
                        id="Fecha"
                        name="Fecha"
                        className="form-control mb-3"
                        value={nuevoEgreso.Fecha}
                        onChange={manejarCambio}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="Monto">Monto:</label>
                    <input
                        type="number"
                        id="Monto"
                        name="Monto"
                        className="form-control mb-3"
                        value={nuevoEgreso.Monto}
                        onChange={manejarCambio}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="Descripcion">Descripción:</label>
                    <textarea
                        id="Descripcion"
                        name="Descripcion"
                        className="form-control mb-3"
                        value={nuevoEgreso.Descripcion}
                        onChange={manejarCambio}
                    />
                </div>
                <button type="submit" className="btn btn-primary">
                    Registrar Egreso
                </button>
            </form>

            {/* Mostrar fondos disponibles */}
            <div className="alert alert-info mt-4" role="alert">
                <strong>Fondos Disponibles:</strong> Q{fondosDisponibles.toFixed(2)}
            </div>

            <h4 className="mt-4">Lista de Egresos</h4>
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Fecha</th>
                        <th>Monto</th>
                        <th>Descripción</th>
                    </tr>
                </thead>
                <tbody>
                    {egresos.map((egreso) => (
                        <tr key={egreso.ID_Egreso}>
                            <td>{egreso.ID_Egreso}</td>
                            <td>{egreso.Fecha}</td>
                            <td>Q{parseFloat(egreso.Monto).toFixed(2)}</td>
                            <td>{egreso.Descripcion}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Egresos;