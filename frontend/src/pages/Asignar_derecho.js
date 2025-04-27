import React from 'react';

import ModuloAsignarDerechos from '../components/ModuloAsignarDerechos';


const Asignar_derecho = () => {
    return (
        <div className="container">
            <h1>Asiganar derechos</h1>
            <div className="mb-4">
                <ModuloAsignarDerechos onSuccess={() => window.location.reload()} /> {/* Recarga la tabla */}
            </div>
          
        </div>
    );
};

export default Asignar_derecho;