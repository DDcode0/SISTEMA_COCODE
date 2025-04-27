import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Ingresos = () => {
    const [ingresos, setIngresos] = useState([]);
    const [totalIngresos, setTotalIngresos] = useState(0); // Estado para el total

    const [nuevoIngreso, setNuevoIngreso] = useState({
        Fecha: '',
        Monto: '',
        Fuente: '',
        Observaciones: ''
    });
    const [mensaje, setMensaje] = useState('');

    // Obtener la lista de ingresos desde el backend
    useEffect(() => {
        cargarIngresos();
        cargarTotalIngresos();

    }, []);

    const cargarIngresos = () => {
        api.get('/ingresos')
            .then(response => setIngresos(response.data))
            .catch(() => setMensaje('Error al cargar los ingresos.'));
    };

    const cargarTotalIngresos = () => {
        api.get('/ingresos/total')
            .then(response => setTotalIngresos(response.data.total_ingresos))
            .catch(() => setMensaje('Error al calcular el total de ingresos.'));
    };

    // Manejar el envío del formulario
    const manejarEnvio = (e) => {
        e.preventDefault();
        if (!nuevoIngreso.Fecha || !nuevoIngreso.Monto || !nuevoIngreso.Fuente) {
            setMensaje('Por favor completa todos los campos obligatorios.');
            return;
        }

        api.post('/ingresos', nuevoIngreso)
            .then(() => {
                setMensaje('Ingreso creado exitosamente.');
                setNuevoIngreso({ Fecha: '', Monto: '', Fuente: '', Observaciones: '' });
                cargarIngresos(); // Actualizar la lista de ingresos
                cargarTotalIngresos(); // Actualizar el total

            })
            .catch((error) => {
                setMensaje(error.response?.data?.errores.join(', ') || 'Error al registrar el ingreso.');
            });
    };

    // Manejar cambios en el formulario
    const manejarCambio = (e) => {
        const { name, value } = e.target;
        setNuevoIngreso({ ...nuevoIngreso, [name]: value });
    };

    return (
        <div className="container mt-4">
            <h3>Gestión de Ingresos</h3>
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
                        value={nuevoIngreso.Fecha}
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
                        value={nuevoIngreso.Monto}
                        onChange={manejarCambio}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="Fuente">Fuente:</label>
                    <input
                        type="text"
                        id="Fuente"
                        name="Fuente"
                        className="form-control mb-3"
                        value={nuevoIngreso.Fuente}
                        onChange={manejarCambio}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="Observaciones">Observaciones:</label>
                    <textarea
                        id="Observaciones"
                        name="Observaciones"
                        className="form-control mb-3"
                        value={nuevoIngreso.Observaciones}
                        onChange={manejarCambio}
                    />
                </div>
                <button type="submit" className="btn btn-primary">
                    Registrar Ingreso
                </button>
            </form>
            {/* Mostrar el total de ingresos */}
            <div className="alert alert-info mt-4" role="alert">
                <strong>Total de Ingresos:</strong> Q{totalIngresos.toFixed(2)}
            </div>

            <h4 className="mt-4">Lista de Ingresos</h4>
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Fecha</th>
                        <th>Monto</th>
                        <th>Fuente</th>
                        <th>Observaciones</th>
                    </tr>
                </thead>
                <tbody>
                    {ingresos.map((ingreso) => (
                        <tr key={ingreso.ID_Ingreso}>
                            <td>{ingreso.ID_Ingreso}</td>
                            <td>{ingreso.Fecha}</td>
                            <td>Q{ingreso.Monto}</td>
                            <td>{ingreso.Fuente}</td>
                            <td>{ingreso.Observaciones}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Ingresos;