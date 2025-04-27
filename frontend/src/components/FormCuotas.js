import React, { useState } from 'react';
import api from '../services/api';

const FormCuotas = ({ onSuccess }) => {
    const [descripcion, setDescripcion] = useState('');
    const [monto, setMonto] = useState('');
    const [fechaLimite, setFechaLimite] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const cuotaData = {
            Descripcion: descripcion,
            Monto: parseFloat(monto),
            Fecha_Limite: fechaLimite,
        };
        console.log('Datos enviados al servidor:', cuotaData); // Registro para verificar los datos
        try {
            await api.post('/cuotas', cuotaData);
            onSuccess();
            setDescripcion('');
            setMonto('');
            setFechaLimite('');
            alert('Cuota creada exitosamente');
        } catch (error) {
            console.error('Error al crear la cuota:', error);
            if (error.response && error.response.data.errores) {
                alert(`Errores: ${error.response.data.errores.join(', ')}`);
            } else {
                alert('Hubo un problema al conectar con el servidor.');
            }
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="mb-3">
                <label htmlFor="descripcion" className="form-label">Descripción:</label>
                <input
                    type="text"
                    id="descripcion"
                    value={descripcion}
                    onChange={(e) => setDescripcion(e.target.value)}
                    className="form-control"
                    required
                />
            </div>
            <div className="mb-3">
                <label htmlFor="monto" className="form-label">Monto:</label>
                <input
                    type="number"
                    id="monto"
                    value={monto}
                    onChange={(e) => setMonto(e.target.value)}
                    className="form-control"
                    required
                />
            </div>
            <div className="mb-3">
                <label htmlFor="fechaLimite" className="form-label">Fecha Límite:</label>
                <input
                    type="date"
                    id="fechaLimite"
                    value={fechaLimite}
                    onChange={(e) => setFechaLimite(e.target.value)}
                    className="form-control"
                    required
                />
            </div>
            <button type="submit" className="btn btn-primary">Crear Cuota</button>
        </form>
    );
};

export default FormCuotas;