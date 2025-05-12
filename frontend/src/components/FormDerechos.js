// frontend/src/components/FormDerechos.js

import React, { useState } from 'react';
import api from '../services/api';
import AlertList from './AlertList';

export default function FormDerechos({ onSuccess }) {
  // Estado del input
  const [nombre, setNombre] = useState('');

  // Estados para mensajes
  const [errores, setErrores] = useState([]);
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrores([]);
    setSuccess('');

    try {
      const res = await api.post('/derechos', { Nombre: nombre });
      setSuccess(res.data.mensaje || 'Derecho creado exitosamente');
      setNombre('');
      if (onSuccess) onSuccess();
    } catch (err) {
      setErrores(err.response?.data?.errores || ['Error inesperado al crear el derecho.']);
    }
  };

  return (
    <>
      {/* Mensajes */}
      <AlertList errores={errores} success={success} />

      <form onSubmit={handleSubmit} className="mb-4">
        <h2>Crear Derecho</h2>

        <div className="mb-3">
          <label htmlFor="nombre" className="form-label">Nombre del Derecho:</label>
          <input
            type="text"
            id="nombre"
            className="form-control"
            value={nombre}
            onChange={e => setNombre(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="btn btn-primary">Crear Derecho</button>
      </form>
    </>
  );
}
