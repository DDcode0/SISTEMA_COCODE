import React, { useState, useEffect } from 'react';
import api from '../services/api';

const FormVincularCuota = ({ onSuccess }) => {
  const [derechos, setDerechos] = useState([]);
  const [cuotas, setCuotas]     = useState([]);
  const [idDerecho, setIdDerecho] = useState('');
  const [idCuota, setIdCuota]     = useState('');
  const [mensaje, setMensaje]     = useState('');

  useEffect(() => {
    // Cargar listas para los select
    api.get('/derechos').then(r => setDerechos(r.data));
    api.get('/cuotas').then(r => setCuotas(r.data));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje('');
    try {
      await api.post(`/derechos/${idDerecho}/vincular-cuota`, { ID_Cuota: idCuota });
      setMensaje('¡Vinculación exitosa!');
      onSuccess && onSuccess();
    } catch (err) {
      const errs = err.response?.data?.errores || ['Error de servidor'];
      setMensaje(errs.join(', '));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <h5>Vincular Cuota a Derecho</h5>

      <div className="mb-3">
        <label>Derecho:</label>
        <select
          className="form-control"
          value={idDerecho}
          onChange={e => setIdDerecho(e.target.value)}
          required
        >
          <option value="">-- Selecciona un derecho --</option>
          {derechos.map(d => (
            <option key={d.ID_Derecho} value={d.ID_Derecho}>
              {d.Nombre}
            </option>
          ))}
        </select>
      </div>

      <div className="mb-3">
        <label>Cuota:</label>
        <select
          className="form-control"
          value={idCuota}
          onChange={e => setIdCuota(e.target.value)}
          required
        >
          <option value="">-- Selecciona una cuota --</option>
          {cuotas.map(c => (
            <option key={c.ID_Cuota} value={c.ID_Cuota}>
              {c.Descripcion} (Q{c.Monto})
            </option>
          ))}
        </select>
      </div>

      {mensaje && (
        <div className={`alert ${mensaje.includes('exitosa') ? 'alert-success' : 'alert-danger'}`}>
          {mensaje}
        </div>
      )}

      <button type="submit" className="btn btn-primary">Vincular</button>
    </form>
  );
};

export default FormVincularCuota;
