// frontend/src/components/RegistrarPago.js

import React, { useState, useEffect } from 'react';
import api from '../services/api';
import AlertList from './AlertList';

export default function RegistrarPago() {
  const [personas, setPersonas] = useState([]);
  const [cuotas, setCuotas] = useState([]);

  const [ID_Persona, setID_Persona] = useState('');
  const [ID_Cuota, setID_Cuota] = useState('');
  const [Monto_Pagado, setMonto_Pagado] = useState('');
  const [Fecha_Pago, setFecha_Pago] = useState('');

  const [montoRestante, setMontoRestante] = useState(0);
  const [estadoCuota, setEstadoCuota] = useState('');

  const [errores, setErrores] = useState([]);
  const [success, setSuccess] = useState('');

  // 1) Cargo personas y cuotas al arrancar
  useEffect(() => {
    api.get('/personas').then(res => setPersonas(res.data));
    api.get('/cuotas').then(res => {
      // Aseguro que Monto es número
      setCuotas(res.data.map(c => ({ ...c, Monto: Number(c.Monto) })));
    });
  }, []);

  // 2) Sólo cuando tenga cuotas, persona y cuota seleccionadas
  useEffect(() => {
    if (!ID_Persona || !ID_Cuota || cuotas.length === 0) {
      // no hago nada hasta que todo esté listo
      return;
    }

    // Intento la consulta al backend
    api.get(`/pagos/cuota/${ID_Cuota}?ID_Persona=${ID_Persona}`)
      .then(res => {
        setMontoRestante(res.data.MontoRestante);
        setEstadoCuota(res.data.Estado);
      })
      .catch(err => {
        // Si 404 o falla, tomo el monto completo de la cuota
        const cuotaObj = cuotas.find(c => c.ID_Cuota === Number(ID_Cuota));
        if (cuotaObj) {
          setMontoRestante(cuotaObj.Monto);
          setEstadoCuota('Pendiente');
        } else {
          // seguridad
          setMontoRestante(0);
          setEstadoCuota('');
        }
      });
  }, [ID_Persona, ID_Cuota, cuotas]);

  const handleSubmit = async () => {
    setErrores([]);
    setSuccess('');

    // validación cliente
    if (!ID_Persona || !ID_Cuota || !Monto_Pagado || !Fecha_Pago) {
      setErrores(['Todos los campos son obligatorios.']);
      return;
    }

    try {
      // Registro del pago
      const res = await api.post('/pagos', {
        ID_Persona,
        ID_Cuota,
        Monto_Pagado: parseFloat(Monto_Pagado),
        Fecha_Pago
      });
      setSuccess(res.data.mensaje || 'Pago registrado exitosamente');
      setMonto_Pagado('');
      setFecha_Pago('');

      // Refresco el estado y monto restante
      const rpt = await api.get(`/pagos/cuota/${ID_Cuota}?ID_Persona=${ID_Persona}`);
      setMontoRestante(rpt.data.MontoRestante);
      setEstadoCuota(rpt.data.Estado);

    } catch (err) {
      setErrores(err.response?.data?.errores || ['Error al registrar el pago.']);
    }
  };

  return (
    <>
      <AlertList errores={errores} success={success} />

      <div className="container mt-4">
        <h3>Registrar Pago</h3>

        <div className="mb-3">
          <label>Persona:</label>
          <select
            className="form-control"
            value={ID_Persona}
            onChange={e => setID_Persona(e.target.value)}
          >
            <option value="">-- Selecciona persona --</option>
            {personas.map(p =>
              <option key={p.ID_Persona} value={p.ID_Persona}>
                {p.Nombre} (DPI: {p.DPI})
              </option>
            )}
          </select>
        </div>

        <div className="mb-3">
          <label>Cuota:</label>
          <select
            className="form-control"
            value={ID_Cuota}
            onChange={e => setID_Cuota(e.target.value)}
          >
            <option value="">-- Selecciona cuota --</option>
            {cuotas.map(c =>
              <option key={c.ID_Cuota} value={c.ID_Cuota}>
                {c.Descripcion} – Q{c.Monto.toFixed(2)}
              </option>
            )}
          </select>
        </div>

        {estadoCuota && (
          <div className="mb-3">
            <p><strong>Monto restante:</strong> Q{montoRestante.toFixed(2)}</p>
            <p><strong>Estado:</strong> {estadoCuota}</p>
          </div>
        )}

        <div className="mb-3">
          <label>Monto a Pagar:</label>
          <input
            type="number"
            className="form-control"
            value={Monto_Pagado}
            onChange={e => setMonto_Pagado(e.target.value)}
          />
        </div>

        <div className="mb-3">
          <label>Fecha de Pago:</label>
          <input
            type="date"
            className="form-control"
            value={Fecha_Pago}
            onChange={e => setFecha_Pago(e.target.value)}
          />
        </div>

        <button className="btn btn-primary" onClick={handleSubmit}>
          Registrar Pago
        </button>
      </div>
    </>
  );
}
