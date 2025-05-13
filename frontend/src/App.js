// frontend/src/App.js
import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Personas from './pages/Personas';
import Derechos from './pages/Derechos';
import Cuotas from './pages/Cuotas';
import AsignarDerecho from './pages/Asignar_derecho';
import Pagos from './pages/Pagos';
import Ingresos from './pages/Ingresos';
import Egresos from './pages/Egresos';

export default function App() {
  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">Sistema COCODE</Link>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#mainNav"
            aria-controls="mainNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
            >
            <span className="navbar-toggler-icon"></span>
            </button>
          <div className="collapse navbar-collapse" id="mainNav">
            <ul className="navbar-nav me-auto">
              <li className="nav-item"><Link className="nav-link" to="/">Dashboard</Link></li>
              <li className="nav-item"><Link className="nav-link" to="/Personas">Personas</Link></li>
              <li className="nav-item"><Link className="nav-link" to="/Derechos">Derechos</Link></li>
              <li className="nav-item"><Link className="nav-link" to="/Cuotas">Cuotas</Link></li>
              <li className="nav-item"><Link className="nav-link" to="/Asignar_derecho">Asignar_derechos</Link></li>
              <li className="nav-item"><Link className="nav-link" to="/Pagos">Pagos</Link></li>
              <li className="nav-item"><Link className="nav-link" to="/Ingresos">Ingresos</Link></li>
              <li className="nav-item"><Link className="nav-link" to="/Egresos">Egresos</Link></li>
            </ul>
          </div>
        </div>
      </nav>

      <div className="container mt-4">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/Personas" element={<Personas />} />
          <Route path="/Derechos" element={<Derechos />} />
          <Route path="/Cuotas" element={<Cuotas />} />
          <Route path="/Asignar_derecho" element={<AsignarDerecho />} />
          <Route path="/Pagos" element={<Pagos />} />
          <Route path="/Ingresos" element={<Ingresos />} />
          <Route path="/Egresos" element={<Egresos />} />
        </Routes>
      </div>
    </>
  );
}
