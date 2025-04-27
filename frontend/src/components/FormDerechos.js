import React, { useState } from 'react';
import api from '../services/api'; // Usamos Axios para conectar con el backend

const FormDerechos = ({ onSuccess }) => {
    const [nombre, setNombre] = useState('');
   
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post('/derechos', { Nombre: nombre });
            onSuccess(); // Recargar la tabla de derechos en la página principal
            setNombre('');
            alert('Derecho creado exitosamente');
        } catch (error) {
            if (error.response && error.response.data.errores) {
                alert(`Error: ${error.response.data.errores.join(', ')}`);
            } else {
                alert('Hubo un problema al conectar con el servidor.');
            }
            console.error('Error al crear el derecho:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="mb-3">
                <label htmlFor="nombre" className="form-label">Nombre del Derecho:</label>
                <input
                    type="text"
                    id="nombre"
                    value={nombre}
                    onChange={(e) => setNombre(e.target.value)}
                    className="form-control"
                    required
                />
            </div>
            <button type="submit" className="btn btn-primary">Crear Derecho</button>
        </form>
    );
};

export default FormDerechos;