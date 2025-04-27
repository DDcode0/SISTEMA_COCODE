

import React, { useState } from 'react';
import FormPersona from '../components/FormPersona';
import TablaPersonas from '../components/TablaPersonas';

const Personas = () => {
    const [mostrar, setMostrar] = useState('formulario'); // Estado para alternar entre vistas

    return (
        <div className="container">
            <h1 className="text-center mb-4">Gestión de Personas</h1>
            
            {/* Botones para alternar entre formulario y tabla */}
            <div className="mb-3 text-center">
                <button
                    className={`btn ${mostrar === 'formulario' ? 'btn-primary' : 'btn-outline-primary'} mx-2`}
                    onClick={() => setMostrar('formulario')}
                >
                    Mostrar Formulario
                </button>
                <button
                    className={`btn ${mostrar === 'tabla' ? 'btn-primary' : 'btn-outline-primary'} mx-2`}
                    onClick={() => setMostrar('tabla')}
                >
                    Mostrar Tabla
                </button>
            </div>

            {/* Alternar entre vistas */}
            {mostrar === 'formulario' && <FormPersona />}
            {mostrar === 'tabla' && <TablaPersonas />}
        </div>
    );
};

export default Personas;