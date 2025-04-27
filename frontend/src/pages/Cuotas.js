import React from 'react';
import FormCuotas from '../components/FormCuotas';
import TablaCuotas from '../components/TablaCuotas';

const Cuotas = () => {
    return (
        <div className="container">
            <h1>Gestión de Cuotas</h1>
            <div className="mb-4">
                <FormCuotas onSuccess={() => window.location.reload()} /> {/* Recarga la tabla */}
            </div>
            <TablaCuotas />
        </div>
    );
};

export default Cuotas;