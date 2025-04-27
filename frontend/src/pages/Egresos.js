import React from 'react';

import RegistrarPago from '../components/ManejoEgresos';

const RegistrarPago = () => {
    return (
        <div className="container">
            <h1>Ingresos</h1>
            <div className="mb-4">
                <ManejoEgresos onSuccess={() => window.location.reload()} /> {/* Recarga al crear */}
                
            </div>
          
        </div>
    );
};

export default RegistrarPago ;