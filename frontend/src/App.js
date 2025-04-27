

import './styles.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Personas from './pages/Personas';
import Derechos from './pages/Derechos';
import Cuotas from './pages/Cuotas';
import Asignar_derecho from './pages/Asignar_derecho';
import RegistrarPago from './components/RegistrarPago';
import Ingresos from './components/ManejoIngresos';
import Egresos from './components/ManejoEgresos';

const App = () => {
    return (
        <Router>
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
                <div className="container">
                    <Link className="navbar-brand" to="/">Sistema Cocode</Link>
                    <div className="collapse navbar-collapse">
                        <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                            <li className="nav-item">
                                <Link className="nav-link" to="/">Dashboard</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/personas">Personas</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/derechos">Derechos</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/cuotas">Cuotas</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/asignar-derechos">Asignar Derechos</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/registrar_pago">Realizar Pagos</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/registrar_ingresos">Ingresos</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/registrar_egresos">Egresos</Link>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
            <div className="container mt-4">
                <Routes>
                    # 
                    # Define las rutas de tu aplicación aquí
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/personas" element={<Personas />} />
                    <Route path="/derechos" element={<Derechos />} />
                    <Route path="/cuotas" element={<Cuotas />} />
                    <Route path="/asignar-derechos" element={<Asignar_derecho />} />
                    <Route path="/registrar_pago" element={<RegistrarPago />} />
                    <Route path="/registrar_ingresos" element={<Ingresos />} />
                    <Route path="/registrar_egresos" element={<Egresos />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;