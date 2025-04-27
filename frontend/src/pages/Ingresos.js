import React from 'react';

import RegistrarPago from '../components/ManejoIngresos';

const RegistrarPago = () => {
    return (
        <div className="container">
            <h1>Ingresos</h1>
            <div className="mb-4">
                <ManejoIngresos onSuccess={() => window.location.reload()} /> {/* Recarga al crear */}
            </div>
          
        </div>
    );
};

export default RegistrarPago ;