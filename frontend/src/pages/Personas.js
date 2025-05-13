// src/pages/Personas.js

import React, { useEffect, useState } from 'react';
import api from '../services/api';

export default function Personas() {
  // Lista de personas
  const [personas, setPersonas] = useState([]);

  // Formulario controlado
  const [form, setForm] = useState({
    DPI: '',
    Nombre: '',
    Email: '',
    Telefono: '',
    Direccion: '',
    Estado: 'Activo',
    Rol: 'Sin rol'
  });

  // Estados de interfaz
  const [modoEditar, setModoEditar] = useState(false);
  const [idEditando, setIdEditando] = useState(null);
  const [mensaje, setMensaje] = useState('');
  const [filtro, setFiltro] = useState('');
  const [sortKey, setSortKey] = useState('Nombre');
  const [sortOrder, setSortOrder] = useState('asc');

  // Roles posibles
  const ROLES = [
    'Presidente',
    'Vicepresidente',
    'Secretario',
    'Tesorero',
    'Vocal I',
    'Vocal II',
    'Vocal III',
    'Sin rol'
  ];

  // Carga inicial
  useEffect(() => {
    cargarPersonas();
  }, []);

  async function cargarPersonas() {
    try {
      const { data } = await api.get('/personas');
      setPersonas(data);
    } catch {
      setMensaje('Error al cargar personas.');
    }
  }

  // Calcula roles disponibles
  function getRolesDisponibles() {
    const usados = personas
      .filter(p => p.Estado === 'Activo' && (!modoEditar || p.ID_Persona !== idEditando))
      .map(p => p.Rol)
      .filter(r => r && r !== 'Sin rol');

    let disponibles = ROLES.filter(r => r === 'Sin rol' || !usados.includes(r));
    if (modoEditar && form.Rol && !disponibles.includes(form.Rol)) {
      disponibles = [form.Rol, ...disponibles];
    }
    return disponibles;
  }

  // Manejo de inputs
  function manejarCambio(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  // Crear o actualizar persona
  async function manejarSubmit(e) {
    e.preventDefault();
    try {
      if (modoEditar) {
        await api.put(`/personas/${idEditando}`, form);
        setMensaje('Persona actualizada.');
      } else {
        await api.post('/personas', form);
        setMensaje('Persona creada.');
      }
      // Reset formulario
      setForm({
        DPI: '',
        Nombre: '',
        Email: '',
        Telefono: '',
        Direccion: '',
        Estado: 'Activo',
        Rol: 'Sin rol'
      });
      setModoEditar(false);
      setIdEditando(null);
      cargarPersonas();
    } catch (err) {
      const errs = err.response?.data?.errores;
      setMensaje(errs ? errs.join(', ') : 'Error al guardar.');
    }
  }

  // Iniciar edición
  function manejarEditar(p) {
    if (p.Estado === 'Inactivo') {
      setMensaje('¡Esta persona está inactiva y no se puede modificar!');
      return;
    }
    setForm({
      DPI: p.DPI,
      Nombre: p.Nombre,
      Email: p.Email || '',
      Telefono: p.Telefono || '',
      Direccion: p.Direccion || '',
      Estado: p.Estado,
      Rol: p.Rol || 'Sin rol'
    });
    setModoEditar(true);
    setIdEditando(p.ID_Persona);
    setMensaje('');
  }

  // Inactivar / eliminar persona
  async function manejarEliminar(id) {
    const confirmacion = window.confirm('¿Marcar esta persona como inactiva?');
    if (!confirmacion) return;
    try {
      await api.delete(`/personas/${id}`);
      setMensaje('Persona inactivada y rol liberado.');
      await cargarPersonas();

      // Si estábamos editando a esa persona, salimos de modo edición
      if (modoEditar && idEditando === id) {
        setModoEditar(false);
        setIdEditando(null);
      }

      // Limpiar formulario
      setForm({
        DPI: '',
        Nombre: '',
        Email: '',
        Telefono: '',
        Direccion: '',
        Estado: 'Activo',
        Rol: 'Sin rol'
      });
    } catch {
      setMensaje('Error al inactivar.');
    }
  }

  // Alternar orden de columnas
  function toggleSort(key) {
    if (sortKey === key) {
      setSortOrder(prev => (prev === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortKey(key);
      setSortOrder('asc');
    }
  }

  // Filtrar y ordenar datos
  const personasOrdenadas = personas
    .filter(p =>
      p.Nombre.toLowerCase().includes(filtro.toLowerCase()) ||
      p.DPI.includes(filtro)
    )
    .sort((a, b) => {
      const va = (a[sortKey] || '').toString().toLowerCase();
      const vb = (b[sortKey] || '').toString().toLowerCase();
      if (va < vb) return sortOrder === 'asc' ? -1 : 1;
      if (va > vb) return sortOrder === 'asc' ? 1 : -1;
      return 0;
    });

  return (
    <div className="container mt-4">
      <h2>Gestión de Personas</h2>

      {/* Formulario */}
      <form onSubmit={manejarSubmit} className="mb-4">
        <div className="row g-2">
          <div className="col-md-3">
            <label className="form-label">DPI</label>
            <input
              name="DPI"
              value={form.DPI}
              onChange={manejarCambio}
              className="form-control"
              minLength={13}
              maxLength={13}
              placeholder="13 dígitos"
              required
            />
          </div>
          <div className="col-md-3">
            <label className="form-label">Nombre</label>
            <input
              name="Nombre"
              value={form.Nombre}
              onChange={manejarCambio}
              className="form-control"
              placeholder="Nombre completo"
              required
            />
          </div>
          <div className="col-md-3">
            <label className="form-label">Correo</label>
            <input
              type="email"
              name="Email"
              value={form.Email}
              onChange={manejarCambio}
              className="form-control"
              placeholder="opcional"
            />
          </div>
          <div className="col-md-3">
            <label className="form-label">Teléfono</label>
            <input
              name="Telefono"
              value={form.Telefono}
              onChange={manejarCambio}
              className="form-control"
              placeholder="opcional"
            />
          </div>
          <div className="col-md-6">
            <label className="form-label">Dirección</label>
            <input
              name="Direccion"
              value={form.Direccion}
              onChange={manejarCambio}
              className="form-control"
              placeholder="opcional"
            />
          </div>
          <div className="col-md-3">
            <label className="form-label">Estado</label>
            <select
              name="Estado"
              value={form.Estado}
              onChange={manejarCambio}
              className="form-select"
              required
            >
              <option value="Activo">Activo</option>
              <option value="Inactivo">Inactivo</option>
            </select>
          </div>
          <div className="col-md-3">
            <label className="form-label">Rol</label>
            <select
              name="Rol"
              value={form.Rol}
              onChange={manejarCambio}
              className="form-select"
              required
            >
              {getRolesDisponibles().map(r => (
                <option key={r} value={r}>{r}</option>
              ))}
            </select>
          </div>
          <div className="col-md-12 text-end mt-2 d-flex justify-content-end gap-2">
            {modoEditar && (
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => {
                  setForm({
                    DPI: '',
                    Nombre: '',
                    Email: '',
                    Telefono: '',
                    Direccion: '',
                    Estado: 'Activo',
                    Rol: 'Sin rol'
                  });
                  setModoEditar(false);
                  setIdEditando(null);
                  setMensaje('');
                }}
              >
                Cancelar
              </button>
            )}
            <button type="submit" className="btn btn-primary">
              {modoEditar ? 'Actualizar Persona' : 'Agregar Persona'}
            </button>
          </div>
        </div>
      </form>

      {/* Mensaje */}
      {mensaje && <div className="alert alert-info">{mensaje}</div>}

      {/* Filtro */}
      <div className="mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Buscar por nombre o DPI..."
          value={filtro}
          onChange={e => setFiltro(e.target.value)}
        />
      </div>

      {/* Tabla ordenable */}
      <div className="table-responsive">
        <table className="table table-striped align-middle">
          <thead>
            <tr>
              <th style={{ cursor: 'pointer' }} onClick={() => toggleSort('Nombre')}>
                Nombre {sortKey==='Nombre' ? (sortOrder==='asc' ? '▲' : '▼') : ''}
              </th>
              <th>DPI</th>
              <th>Correo</th>
              <th>Teléfono</th>
              <th>Dirección</th>
              <th>Estado</th>
              <th style={{ cursor: 'pointer' }} onClick={() => toggleSort('Rol')}>
                Rol {sortKey==='Rol' ? (sortOrder==='asc' ? '▲' : '▼') : ''}
              </th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {personasOrdenadas.map(p => (
              <tr
                key={p.ID_Persona}
                className={p.Estado === 'Inactivo' ? 'table-secondary' : ''}
              >
                <td>{p.Nombre}</td>
                <td>{p.DPI}</td>
                <td>{p.Email || '—'}</td>
                <td>{p.Telefono || '—'}</td>
                <td>{p.Direccion || '—'}</td>
                <td>
                  <span className={`badge bg-${p.Estado==='Activo'?'success':'secondary'}`}>
                    {p.Estado}
                  </span>
                </td>
                <td>{p.Rol}</td>
                <td>
                  <button
                    className="btn btn-sm btn-warning me-2"
                    onClick={() => manejarEditar(p)}
                  >
                    Editar
                  </button>
                  <button
                    className={`btn btn-sm ${p.Estado==='Activo'?'btn-danger':'btn-secondary'}`}
                    onClick={() => manejarEliminar(p.ID_Persona)}
                  >
                    {p.Estado==='Activo'?'Inactivar':'Eliminar'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
