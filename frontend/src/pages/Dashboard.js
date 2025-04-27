import React, { useState, useEffect } from 'react';
import api from '../services/api';
import BuscarPersonas from '../components/busquedaPersona'; // Componente para buscar personas
import { generarPDF } from '../utils/pdfGenerator';

const Dashboard = () => {
    const [activeTab, setActiveTab] = useState('resumenPersonas'); // Controla el tab activo
    const [personasConDerechos, setPersonasConDerechos] = useState([]);
    const [cuotas, setCuotas] = useState([]);
    const [ingresos, setIngresos] = useState(0);
    const [egresos, setEgresos] = useState(0);
    const [saldo, setSaldo] = useState(0);
    const [isLoading, setIsLoading] = useState(false); // Indicador de carga

    // Efecto para cargar datos según el tab activo
    useEffect(() => {
        setIsLoading(true);
        if (activeTab === 'resumenPersonas') {
            cargarPersonasConDerechos();
            cargarCuotas();
        } else if (activeTab === 'resumenFinanciero') {
            cargarInformeFinanciero();
        }
    }, [activeTab]);

    const cargarPersonasConDerechos = () => {
        api.get('/persona_derecho/detalle_combinado')
            .then(response => setPersonasConDerechos(response.data))
            .catch(() => console.error('Error al cargar personas con derechos y sin derechos.'));
    };

    const cargarCuotas = () => {
        api.get('/cuotas/con-pagos')
            .then(response => {
                console.log('Cuotas con pagos:', response.data); // Verificar datos
                setCuotas(response.data);
            })
            .catch(() => console.error('Error al cargar cuotas con pagos.'))
            .finally(() => setIsLoading(false)); // Siempre cambiar isLoading a false
    };

    const cargarCuotasMejoradas = () => {
        api.get('/cuotas/estado/mejorado')
            .then(response => setCuotas(response.data))
            .catch(() => console.error('Error al cargar cuotas mejoradas.'));
    };

    const cargarInformeFinanciero = () => {
        Promise.all([
            api.get('/ingresos/total'),
            api.get('/egresos/total'),
            api.get('/fondos/disponibles')
        ])
        .then(([resIngresos, resEgresos, resFondos]) => {
            setIngresos(resIngresos.data.total_ingresos || 0);
            setEgresos(resEgresos.data.total_egresos || 0);
            setSaldo(resFondos.data.fondos_disponibles || 0);
        })
        .catch(() => console.error('Error al cargar el informe financiero.'))
        .finally(() => setIsLoading(false));
    };

    return (
        <div className="container mt-4">
            <h3>Dashboard</h3>
            <div className="btn-group mb-4">
                <button
                    className={`btn btn-${activeTab === 'resumenPersonas' ? 'primary' : 'secondary'}`}
                    onClick={() => setActiveTab('resumenPersonas')}
                >
                    Resumen de Personas y Cuotas
                </button>
                <button
                    className={`btn btn-${activeTab === 'resumenFinanciero' ? 'primary' : 'secondary'}`}
                    onClick={() => setActiveTab('resumenFinanciero')}
                >
                    Estado Financiero
                </button>
            </div>

            {isLoading && <p>Cargando datos...</p>}

            {activeTab === 'resumenPersonas' && !isLoading && (





                <div>
                    <BuscarPersonas setPersonasConDerechos={setPersonasConDerechos} />
                    <h4>Personas con y sin Derechos</h4>
                    <table className="table table-striped">
                        <thead>
                            <tr>
                                <th>Nombre</th>
                                <th>DPI</th>
                                <th>Derecho</th>
                                <th>Fecha de Inicio</th>
                                <th>Fecha de Vencimiento</th>
                                <th>Email</th>
                                <th>Teléfono</th>
                                <th>Rol</th>
                            </tr>
                        </thead>
                        <tbody>
                            {personasConDerechos.map((persona, index) => (
                                <tr key={index} className={persona.Descripcion_Derecho === 'Sin derechos' ? 'table-danger' : ''}>
                                    <td>{persona.Nombre}</td>
                                    <td>{persona.DPI}</td>
                                    <td>{persona.Descripcion_Derecho}</td>
                                    <td>{persona.Fecha_Inicio}</td>
                                    <td>{persona.Fecha_Fin}</td>
                                    <td>{persona.Email}</td>
                                    <td>{persona.Telefono}</td>
                                    <td>{persona.Rol}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>

                    {/* Tabla de Cuotas Mejoradas */}
                    
                    <h4>Cuotas con Pagos</h4>
                    <table className="table table-striped">
                        <thead>
                            <tr>
                                <th>ID Cuota</th>
                                <th>Descripción</th>
                                <th>Monto Total</th>
                                <th>Pagos Realizados</th>
                                <th>Monto Pendiente</th>
                                <th>Estado</th>
                                <th>Fecha Límite</th>
                                <th>Participantes</th>
                            </tr>
                        </thead>
                        <tbody>
                            {cuotas.map((cuota, index) => (
                                <tr key={index} className={cuota.Estado === 'Completado' ? 'table-success' : 'table-warning'}>
                                    <td>{cuota.ID_Cuota}</td>
                                    <td>{cuota.Descripcion}</td>
                                    <td>Q{Number(cuota.Monto).toFixed(2)}</td>
                                    <td>Q{Number(cuota.PagosRealizados).toFixed(2)}</td>
                                    <td>Q{Number(cuota.MontoPendiente).toFixed(2)}</td>
                                    <td>{cuota.Estado}</td>
                                    <td>{cuota.Fecha_Limite}</td>
                                    <td>{cuota.Participantes}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>

                    <button
                        className="btn btn-primary mt-4"
                        onClick={() => generarPDF(personasConDerechos, cuotas, { ingresos, egresos, saldo })}
                    >
                        Generar PDF
                    </button>
                </div>

                
            )}

            {activeTab === 'resumenFinanciero' && !isLoading && (
                <div>
                    <h4>Estado Financiero</h4>
                    <ul className="list-group">
                        <li className="list-group-item">
                            <strong>Total de Ingresos:</strong> Q{ingresos.toFixed(2)}
                        </li>
                        <li className="list-group-item">
                            <strong>Total de Egresos:</strong> Q{egresos.toFixed(2)}
                        </li>
                        <li className="list-group-item">
                            <strong>Saldo Total:</strong> Q{saldo.toFixed(2)}
                        </li>
                    </ul>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
