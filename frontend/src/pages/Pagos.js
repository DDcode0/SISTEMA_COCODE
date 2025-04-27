import React from 'react';

import RegistrarPago from '../components/RegistrarPago';

const RegistrarPago = () => {
    return (
        <div className="container">
            <h1>Realizar Pagos</h1>
            <div className="mb-4">
                <RegistrarPago onSuccess={() => window.location.reload()} /> {/* Recarga al crear */}
            </div>
          
        </div>
    );
};

export default RegistrarPago ;