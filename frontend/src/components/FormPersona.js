import React, { useState, useEffect } from 'react';
import api from '../services/api';

const FormPersona = () => {
    const [formData, setFormData] = useState({
        DPI: '',
        Nombre: '',
        Correo: '',
        Estado: 'Activo',
        Telefono: '',
        Direccion: '',
        Rol: 'Sin rol',
    });

    const [errores, setErrores] = useState([]); // Estado para manejar errores
    const [mensajeExito, setMensajeExito] = useState(''); // Estado para mostrar el mensaje de éxito

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Limpiar mensajes previos
        setErrores([]);
        setMensajeExito('');

        try {
            const response = await api.post('/personas', formData);
            setMensajeExito(response.data.mensaje); // Capturar el mensaje de éxito
        } catch (error) {
            if (error.response && error.response.data.errores) {
                setErrores(error.response.data.errores); // Capturar errores del backend
            } else {
                alert('Error inesperado al registrar la persona.');
            }
        }
    };

    // Hook para cerrar el mensaje automáticamente después de 5 segundos
    useEffect(() => {
        if (mensajeExito) {
            const timer = setTimeout(() => setMensajeExito(''), 5000); // Oculta el mensaje después de 5 segundos
            return () => clearTimeout(timer); // Limpia el temporizador al desmontar
        }
    }, [mensajeExito]);

    return (
        <form onSubmit={handleSubmit} className="mb-4">
            <h2>Registrar Persona</h2>
            <div className="mb-3">
                <label htmlFor="DPI" className="form-label">DPI:</label>
                <input
                    type="text"
                    id="DPI"
                    name="DPI"
                    value={formData.DPI}
                    onChange={handleChange}
                    className="form-control"
                    required
                />
            </div>
            <div className="mb-3">
                <label htmlFor="Nombre" className="form-label">Nombre:</label>
                <input
                    type="text"
                    id="Nombre"
                    name="Nombre"
                    value={formData.Nombre}
                    onChange={handleChange}
                    className="form-control"
                    required
                />
            </div>
            <div className="mb-3">
                <label htmlFor="Correo" className="form-label">Correo:</label>
                <input
                    type="email"
                    id="Correo"
                    name="Correo"
                    value={formData.Correo}
                    onChange={handleChange}
                    className="form-control"
                />
            </div>
            <div className="mb-3">
                <label htmlFor="Estado" className="form-label">Estado:</label>
                <select
                    id="Estado"
                    name="Estado"
                    value={formData.Estado}
                    onChange={handleChange}
                    className="form-control"
                >
                    <option value="Activo">Activo</option>
                    <option value="Inactivo">Inactivo</option>
                </select>
            </div>
            <div className="mb-3">
                <label htmlFor="Telefono" className="form-label">Teléfono:</label>
                <input
                    type="text"
                    id="Telefono"
                    name="Telefono"
                    value={formData.Telefono}
                    onChange={handleChange}
                    className="form-control"
                />
            </div>
            <div className="mb-3">
                <label htmlFor="Direccion" className="form-label">Dirección:</label>
                <input
                    type="text"
                    id="Direccion"
                    name="Direccion"
                    value={formData.Direccion}
                    onChange={handleChange}
                    className="form-control"
                />
            </div>
            <div className="mb-3">
                <label htmlFor="Rol" className="form-label">Rol:</label>
                <select
                    id="Rol"
                    name="Rol"
                    value={formData.Rol}
                    onChange={handleChange}
                    className="form-control"
                >
                    <option value="Presidente">Presidente</option>
                    <option value="Vicepresidente">Vicepresidente</option>
                    <option value="Secretario">Secretario</option>
                    <option value="Tesorero">Tesorero</option>
                    <option value="Vocal I">Vocal I</option>
                    <option value="Vocal II">Vocal II</option>
                    <option value="Vocal III">Vocal III</option>
                    <option value="Sin rol">Sin rol</option>
                </select>
            </div>
            <button type="submit" className="btn btn-primary">Registrar</button>
            
            {/* Mostrar mensaje de éxito */}
            {mensajeExito && (
                <div className="custom-success-message">
                    <i className="success-icon">&#10003;</i> {mensajeExito}
                </div>
            )}

            {/* Mostrar errores debajo del formulario */}
            {errores.length > 0 && (
                <div className="alert alert-danger mt-3">
                    <ul>
                        {errores.map((error, index) => (
                            <li key={index}>{error}</li>
                        ))}
                    </ul>
                </div>
            )}
        </form>
    );
};

export default FormPersona;