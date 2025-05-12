// frontend/src/components/FormCuotas.js

import React, { useState } from 'react';
import api from '../services/api';
import AlertList from './AlertList';

export default function FormCuotas({ onSuccess }) {
  // Estado del formulario
  const [descripcion, setDescripcion] = useState('');
  const [monto, setMonto] = useState('');
  const [fechaLimite, setFechaLimite] = useState('');

  // Estados para mensajes
  const [errores, setErrores] = useState([]);
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrores([]);
    setSuccess('');

    // Construimos el payload según la API
    const payload = {
      Descripcion: descripcion,
      Monto: parseFloat(monto),
      Fecha_Limite: fechaLimite,
    };

    try {
      const res = await api.post('/cuotas', payload);
      setSuccess(res.data.mensaje || 'Cuota creada exitosamente');
      setDescripcion('');
      setMonto('');
      setFechaLimite('');
      // Si el padre pasa un onSuccess, lo ejecutamos para recargar lista
      if (onSuccess) onSuccess();
    } catch (err) {
      setErrores(err.response?.data?.errores || ['Error inesperado al crear la cuota.']);
    }
  };

  return (
    <>
      {/* Mensajes de error / éxito */}
      <AlertList errores={errores} success={success} />

      <form onSubmit={handleSubmit}>
        <h2>Crear Cuota</h2>

        <div className="mb-3">
          <label htmlFor="descripcion" className="form-label">Descripción:</label>
          <input
            type="text"
            id="descripcion"
            className="form-control"
            value={descripcion}
            onChange={e => setDescripcion(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label htmlFor="monto" className="form-label">Monto:</label>
          <input
            type="number"
            id="monto"
            className="form-control"
            value={monto}
            onChange={e => setMonto(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label htmlFor="fechaLimite" className="form-label">Fecha Límite:</label>
          <input
            type="date"
            id="fechaLimite"
            className="form-control"
            value={fechaLimite}
            onChange={e => setFechaLimite(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="btn btn-primary">Crear Cuota</button>
      </form>
    </>
  );
}
