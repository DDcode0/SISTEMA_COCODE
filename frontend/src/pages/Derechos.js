// src/pages/Derechos.js

import React, { useEffect, useState } from 'react';
import api from '../services/api';
import FormVincularCuota from '../components/FormVincularCuota';

export default function Derechos() {
  // Lista de derechos
  const [derechos, setDerechos] = useState([]);

  // Formulario controlado
  const [nombre, setNombre] = useState('');
  const [modoEditar, setModoEditar] = useState(false);
  const [idEditando, setIdEditando] = useState(null);

  // Mensajes
  const [mensaje, setMensaje] = useState('');

  // Filtro y orden
  const [filtro, setFiltro] = useState('');
  const [sortOrder, setSortOrder] = useState('asc');

  // Carga inicial y recargas tras vincular cuota
  useEffect(() => {
    cargarDerechos();
  }, []);

  async function cargarDerechos() {
    try {
      const { data } = await api.get('/derechos');
      setDerechos(data);
    } catch {
      setMensaje('Error al cargar derechos.');
    }
  }

  // Crear o actualizar derecho
  async function manejarSubmit(e) {
    e.preventDefault();
    if (!nombre.trim()) {
      setMensaje('El nombre no puede estar vacío.');
      return;
    }
    try {
      if (modoEditar) {
        await api.put(`/derechos/${idEditando}`, { Nombre: nombre });
        setMensaje('Derecho actualizado.');
      } else {
        await api.post('/derechos', { Nombre: nombre });
        setMensaje('Derecho creado.');
      }
      resetForm();
      cargarDerechos();
    } catch (err) {
      const errs = err.response?.data?.errores;
      setMensaje(errs?.join(', ') || 'Error al guardar.');
    }
  }

  function resetForm() {
    setNombre('');
    setModoEditar(false);
    setIdEditando(null);
    setMensaje('');
  }

  // Iniciar edición
  function manejarEditar(d) {
    setNombre(d.Nombre);
    setModoEditar(true);
    setIdEditando(d.ID_Derecho);
    setMensaje('');
  }

  // Inactivar derecho
  async function manejarEliminar(id) {
    if (!window.confirm('¿Inactivar este derecho?')) return;
    try {
      // suponiendo que el backend marca el derecho como inactivo en lugar de borrarlo
      await api.delete(`/derechos/${id}`);
      setMensaje('Derecho inactivado.');
      cargarDerechos();
    } catch {
      setMensaje('Error al inactivar.');
    }
  }

  // Alterna orden alfabético
  function toggleSort() {
    setSortOrder(prev => (prev === 'asc' ? 'desc' : 'asc'));
  }

  // Filtrar + ordenar
  const lista = derechos
    .filter(d => d.Nombre.toLowerCase().includes(filtro.toLowerCase()))
    .sort((a, b) => {
      const va = a.Nombre.toLowerCase();
      const vb = b.Nombre.toLowerCase();
      if (va < vb) return sortOrder === 'asc' ? -1 : 1;
      if (va > vb) return sortOrder === 'asc' ? 1 : -1;
      return 0;
    });

  return (
    <div className="container mt-4">
      <h2>Gestión de Derechos</h2>

      {/* Formulario de creación/edición */}
      <form onSubmit={manejarSubmit} className="mb-4">
        <div className="input-group">
          <input
            type="text"
            className="form-control"
            placeholder="Nombre del derecho"
            value={nombre}
            onChange={e => setNombre(e.target.value)}
            required
          />
          <button className="btn btn-primary" type="submit">
            {modoEditar ? 'Actualizar' : 'Crear'}
          </button>
          {modoEditar && (
            <button
              type="button"
              className="btn btn-secondary"
              onClick={resetForm}
            >
              Cancelar
            </button>
          )}
        </div>
      </form>

      {/* Mensaje de estado */}
      {mensaje && <div className="alert alert-info">{mensaje}</div>}

      {/* Filtro */}
      <div className="mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Buscar derecho..."
          value={filtro}
          onChange={e => setFiltro(e.target.value)}
        />
      </div>

      {/* Formulario de vincular cuotas */}
      <FormVincularCuota onSuccess={cargarDerechos} />

      {/* Tabla de derechos */}
      <table className="table table-striped">
        <thead>
          <tr>
            <th style={{ cursor: 'pointer' }} onClick={toggleSort}>
              Nombre {sortOrder === 'asc' ? '▲' : '▼'}
            </th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {lista.map(d => (
            <tr key={d.ID_Derecho}>
              <td>{d.Nombre}</td>
              <td>
                <button
                  className="btn btn-sm btn-warning me-2"
                  onClick={() => manejarEditar(d)}
                >
                  Editar
                </button>
                <button
                  className="btn btn-sm btn-danger"
                  onClick={() => manejarEliminar(d.ID_Derecho)}
                >
                  Inactivar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
