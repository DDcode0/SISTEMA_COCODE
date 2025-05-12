// frontend/src/components/FormPersona.js

import React, { useState, useEffect } from 'react';
import api from '../services/api';
import AlertList from './AlertList';

export default function FormPersona() {
  // Estado del formulario
  const [formData, setFormData] = useState({
    DPI: '',
    Nombre: '',
    Email: '',
    Telefono: '',
    Direccion: '',
    Rol: 'Sin rol',
    Estado: 'Activo',
  });

  // Estados para mensajes de error y éxito
  const [errores, setErrores] = useState([]);
  const [success, setSuccess] = useState('');

  // Captura cambios en los inputs
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Envía los datos al backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrores([]);
    setSuccess('');

    try {
      const response = await api.post('/personas', {
        DPI: formData.DPI,
        Nombre: formData.Nombre,
        Email: formData.Email,
        Telefono: formData.Telefono,
        Direccion: formData.Direccion,
        Rol: formData.Rol,
        Estado: formData.Estado,
      });
      setSuccess(response.data.mensaje);
      // Opcional: limpiar formulario tras éxito
      setFormData({
        DPI: '',
        Nombre: '',
        Email: '',
        Telefono: '',
        Direccion: '',
        Rol: 'Sin rol',
        Estado: 'Activo',
      });
    } catch (error) {
      setErrores(error.response?.data?.errores || ['Error inesperado al registrar la persona.']);
    }
  };

  // Limpia el mensaje de éxito después de 5 segundos
  useEffect(() => {
    if (success) {
      const timer = setTimeout(() => setSuccess(''), 5000);
      return () => clearTimeout(timer);
    }
  }, [success]);

  return (
    <>
      {/* Mensajes de error / éxito */}
      <AlertList errores={errores} success={success} />

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
          <label htmlFor="Email" className="form-label">Correo electrónico:</label>
          <input
            type="email"
            id="Email"
            name="Email"
            value={formData.Email}
            onChange={handleChange}
            className="form-control"
          />
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
            <option value="Sin rol">Sin rol</option>
            <option value="Presidente">Presidente</option>
            <option value="Vicepresidente">Vicepresidente</option>
            <option value="Secretario">Secretario</option>
            <option value="Tesorero">Tesorero</option>
            <option value="Vocal I">Vocal I</option>
            <option value="Vocal II">Vocal II</option>
            <option value="Vocal III">Vocal III</option>
          </select>
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

        <button type="submit" className="btn btn-primary">Registrar</button>
      </form>
    </>
  );
}


